import subprocess

def execute(command: str) -> str:
    cmd_lower = command.lower()
    
    dangerous_patterns = [
        "rm ", "del ", "rmdir ", "rd ", "erase ", "shred ", "unlink ",
        "remove-item", "ri ", "rmdir /s", "rd /s", "remove-item -recurse",
        "rm -r", "rm -f", "rm -rf",
        " && rmdir", " && del", " | rmdir", " | del"
    ]
    
    for pattern in dangerous_patterns:
        if pattern in cmd_lower:
            return ("❌ 错误：禁止执行删除类命令。EasyMate 的安全规则不允许直接删除文件或文件夹。"
                    "如果你需要清理文件，请告诉我用 'move' 操作，我会帮你把文件移动到 'C:\\待删除' 目录。")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, timeout=30)
        stdout = result.stdout.decode('utf-8', errors='replace')
        stderr = result.stderr.decode('utf-8', errors='replace')
        output = stdout + stderr
        if result.returncode != 0:
            output = f"命令返回非零退出码 {result.returncode}\n{output}"
        return output.strip() or "命令执行成功（无输出）"
    except subprocess.TimeoutExpired:
        return "错误：命令执行超时"
    except Exception as e:
        return f"执行失败：{e}"