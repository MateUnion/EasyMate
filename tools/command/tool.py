import subprocess

def execute(command):
    dangerous = ["rm", "del", "rmdir", "rd", "erase", "shred", "unlink"]
    first = command.strip().split()[0].lower()
    if first in dangerous:
        return ("错误：禁止直接执行删除命令。如需删除文件，请使用移动操作 "
                "（如：mv 文件 ~/.Trash/ 或 move 文件 C:\\待删除\\）")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout + result.stderr
        return output.strip() or "命令执行成功（无输出）"
    except subprocess.TimeoutExpired:
        return "错误：命令执行超时"
    except Exception as e:
        return f"执行失败：{e}"