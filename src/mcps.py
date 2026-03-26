# Copyright (C) 2026 xhdlphzr
# This file is part of EasyMate.
# EasyMate is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
# EasyMate is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with EasyMate.  If not, see <https://www.gnu.org/licenses/>.

"""
MCP 服务器发现与工具转换模块
扫描局域网内的 MCP 服务器，获取工具列表，转换为 OpenAI 兼容的 tool 格式
支持手动添加公网服务器
"""

import socket
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any
import ipaddress

class MCPScanner:
    """MCP 服务器扫描器，返回工具列表（每个工具附带来源服务器 URL）"""

    def __init__(self, config_path: str = "./config.json", timeout: float = 1.0, port_range: range = None, max_workers: int = 30):
        """
        初始化扫描器，加载配置文件中的黑名单和手动服务器列表

        :param config_path: 配置文件路径
        :param timeout: 每个 HTTP 请求的超时时间（秒）
        :param port_range: 要扫描的端口范围，默认只扫描 8000 端口
        :param max_workers: 并发线程数
        """
        self.blacklist = self._load_blacklist(config_path)
        self.manual_servers = self._load_manual_servers(config_path)
        self.timeout = timeout
        # 默认只扫描 8000 端口，绝大多数 MCP 服务器使用此端口
        self.port_range = port_range if port_range is not None else range(8000, 8001)
        self.max_workers = max_workers

    def _load_blacklist(self, config_path: str) -> List[str]:
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config.get("mcps", [])
        except Exception as e:
            print(f"加载配置文件失败: {e}，黑名单为空")
            return []

    def _load_manual_servers(self, config_path: str) -> List[str]:
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config.get("mcp_servers", [])
        except Exception as e:
            print(f"加载配置文件失败: {e}，手动服务器列表为空")
            return []

    def _get_local_network_prefixes(self) -> List[str]:
        """获取本机所有私有 IPv4 地址的网络前缀（如 192.168.1.）"""
        prefixes = set()
        try:
            hostname = socket.gethostname()
            addrs = socket.gethostbyname_ex(hostname)[2]
            for ip in addrs:
                if ip.startswith('127.'):
                    continue
                try:
                    ip_obj = ipaddress.ip_address(ip)
                    if ip_obj.is_private:
                        parts = ip.split('.')
                        if len(parts) == 4:
                            prefix = '.'.join(parts[:3]) + '.'
                            prefixes.add(prefix)
                except:
                    pass
        except Exception as e:
            print(f"获取网络前缀失败: {e}")

        if not prefixes:
            prefixes = {'192.168.', '10.', '172.16.', '172.17.', '172.18.', '172.19.',
                        '172.20.', '172.21.', '172.22.', '172.23.', '172.24.', '172.25.',
                        '172.26.', '172.27.', '172.28.', '172.29.', '172.30.', '172.31.'}
        return list(prefixes)

    def _check_mcp_server(self, url: str) -> List[Dict[str, Any]]:
        """检查一个 URL 是否为 MCP 服务器，返回工具列表（OpenAI 格式）"""
        try:
            payload = {
                "jsonrpc": "2.0",
                "method": "tools/list",
                "id": 1
            }
            resp = requests.post(url, json=payload, timeout=self.timeout)
            if resp.status_code != 200:
                return []
            data = resp.json()
            if "result" not in data or not isinstance(data["result"], list):
                return []
            tools = data["result"]
            openai_tools = []
            for tool in tools:
                if "name" not in tool:
                    continue
                openai_tool = {
                    "type": "function",
                    "function": {
                        "name": tool["name"],
                        "description": tool.get("description", ""),
                        "parameters": tool.get("inputSchema", {"type": "object", "properties": {}})
                    }
                }
                openai_tools.append(openai_tool)
            return openai_tools
        except Exception:
            return []

    def scan(self) -> List[Dict[str, Any]]:
        """
        扫描所有可用的 MCP 服务器，返回工具列表，每个工具附带其来源服务器 URL。
        返回格式: [{"url": "http://...", "tool": openai_tool_dict}, ...]
        根据工具名去重（先发现的保留）。
        """
        discovered = []
        seen_names = set()
        urls_to_check = []

        # 手动指定的服务器
        for url in self.manual_servers:
            if url not in self.blacklist:
                urls_to_check.append(url)

        # 局域网自动发现（只扫描 8000 端口，遍历整个 /24 子网）
        prefixes = self._get_local_network_prefixes()
        for prefix in prefixes:
            for i in range(1, 255):
                ip = f"{prefix}{i}"
                for port in self.port_range:
                    url = f"http://{ip}:{port}"
                    if url in self.blacklist:
                        continue
                    urls_to_check.append(url)

        # 并发扫描
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self._check_mcp_server, url): url for url in urls_to_check}
            for future in as_completed(futures):
                url = futures[future]
                tools = future.result()
                for tool in tools:
                    name = tool["function"]["name"]
                    if name not in seen_names:
                        seen_names.add(name)
                        discovered.append({"url": url, "tool": tool})
        return discovered