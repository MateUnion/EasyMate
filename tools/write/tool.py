from pathlib import Path

def execute(path: str, content: str, mode="overwrite") -> str:
    try:
        p = Path(path).expanduser().resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        flag = 'a' if mode == 'append' else 'w'
        with open(p, flag, encoding='utf-8') as f:
            f.write(content)
        return f"成功{'追加' if mode=='append' else '写入'}文件：{p}"
    except Exception as e:
        return f"写入失败：{e}"