import json
import importlib.util
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).parent

tools_metadata = []
tool_functions = {}
readmes = []

for item in TOOLS_DIR.iterdir():
    if not item.is_dir() or item.name.startswith('__'):
        continue

    tool_name = item.name
    config_path = item / 'config.json'
    tool_path = item / 'tool.py'
    readme_path = item / 'README.md'

    if not (config_path.exists() and tool_path.exists() and readme_path.exists):
        print(f"⚠️ 工具 {tool_name} 缺少必要文件，跳过")
        continue

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except Exception as e:
        print(f"⚠️ 工具 {tool_name} 的 config.json 解析失败：{e}，跳过")
        continue

    if not isinstance(config, dict) or 'type' not in config or 'function' not in config:
        print(f"⚠️ 工具 {tool_name} 的 config.json 格式不正确（缺少 type 或 function），跳过")
        continue

    func_info = config['function']
    if 'name' not in func_info:
        print(f"⚠️ 工具 {tool_name} 的 config.json 中 function 缺少 name 字段，跳过")
        continue

    name = func_info['name']

    try:
        spec = importlib.util.spec_from_file_location(f"tools.{tool_name}", tool_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[f"tools.{tool_name}"] = module
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"⚠️ 工具 {tool_name} 的 tool.py 导入失败：{e}，跳过")
        continue

    if not hasattr(module, 'execute'):
        print(f"⚠️ 工具 {tool_name} 的 tool.py 未定义 execute 函数，跳过")
        continue

    tools_metadata.append(config)

    tool_functions[name] = module.execute

    if readme_path.exists():
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read().strip()
                if readme_content:
                    readmes.append(readme_content)
        except Exception as e:
            print(f"⚠️ 工具 {tool_name} 的 README.md 读取失败：{e}")

readmes_combined = "\n\n".join(readmes)

__all__ = ['tools_metadata', 'tool_functions', 'readmes_combined']