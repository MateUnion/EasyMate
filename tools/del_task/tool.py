import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
TASKS_FILE = PROJECT_ROOT / "tasks.json"

def execute(id: int) -> str:
    if not TASKS_FILE.exists():
        return f"任务文件不存在，无法删除ID {id}。"

    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            tasks = json.load(f)
    except Exception as e:
        return f"读取任务文件失败: {e}"

    if not isinstance(tasks, dict):
        return "任务文件格式错误。"

    str_id = str(id)
    if str_id not in tasks:
        return f"未找到ID为 {id} 的任务。"

    del tasks[str_id]

    if not tasks:
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f, indent=2, ensure_ascii=False)
        return f"已删除ID {id} 的任务，现在无剩余任务。"

    sorted_items = sorted(tasks.items(), key=lambda x: int(x[0]))

    new_tasks = {}
    new_id = 1
    for _, value in sorted_items:
        new_tasks[str(new_id)] = value
        new_id += 1

    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(new_tasks, f, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"写入任务文件失败: {e}"

    return f"已删除ID {id} 的任务，并重新对齐任务ID（原ID大于{id}的任务ID均已减1）。"