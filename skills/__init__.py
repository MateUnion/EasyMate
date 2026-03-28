# Copyright (C) 2026 xhdlphzr
# This file is part of FranxAI.
# FranxAI is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
# FranxAI is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with FranxAI.  If not, see <https://www.gnu.org/licenses/>.

"""
Skills 模块初始化
自动加载 skills 目录下的所有 Markdown 文件，并合并为一个字符串。
"""

from pathlib import Path

# 获取 skills 目录的绝对路径
SKILLS_DIR = Path(__file__).parent

# 存储所有读取到的 Markdown 内容
_readmes = []

# 遍历所有 .md 文件
for filepath in sorted(SKILLS_DIR.glob("*.md")):
    try:
        content = filepath.read_text(encoding='utf-8').strip()
        if content:
            _readmes.append(content)
    except Exception as e:
        # 读取失败时打印警告（模仿 tools 模块的风格）
        print(f"⚠️ 技能文件 {filepath.name} 读取失败：{e}")

# 合并所有 Markdown 内容，用两个换行符分隔
skills_readme = "\n\n".join(_readmes)
print("已加载技能文件:", [p.name for p in sorted(SKILLS_DIR.glob("*.md"))])

# 对外导出
__all__ = ['skills_readme']