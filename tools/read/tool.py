from pathlib import Path

def execute(path: str) -> str:
    try:
        p = Path(path).expanduser().resolve()
        if not p.exists():
            return f"错误：文件不存在 - {p}"
        if not p.is_file():
            return f"错误：路径不是文件 - {p}"
        with open(p, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except PermissionError:
        return f"错误：没有权限读取文件 - {path}"
    except Exception as e:
        return f"读取文件时发生错误：{str(e)}"