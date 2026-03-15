import subprocess

def execute(command):
    dangerous = ["rm", "del", "rmdir", "rd", "erase", "shred", "unlink"]
    first = command.strip().split()[0].lower()
    if first in dangerous:
        return ("错误：禁止直接执行删除命令。如需删除文件，请使用移动操作 "
                "（如：mv 文件 ~/.Trash/ 或 move 文件 C:\\待删除\\）")

    try:
        # 不使用 text=True，而是手动解码，指定编码和错误处理
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            timeout=30
        )
        # 尝试用 utf-8 解码，失败时用 replace 替换无法解码的字符
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