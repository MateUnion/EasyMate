import os
import time
import json
import threading
from datetime import datetime
from agent import EasyMate

def multi_line_input(prompt):
    print(prompt, end='')
    lines = []
    while True:
        line = input()
        if line == "c":
            break
        lines.append(line)
    return '\n'.join(lines)

def run_tasks():
    if not os.path.exists("./config.json"):
        print("配置文件 './config.json' 不存在，请从 config.example.json 复制一份并修改。")
        return
    
    try:
        with open("./config.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"配置文件 './config.json' 格式错误：{e}")
        return
    
    required = ["api_key", "base_url", "model"]
    missing = [field for field in required if field not in config]
    if missing:
        print(f"配置文件中缺少必需字段：{', '.join(missing)}")
        return
    
    try:
        with open("memory.txt", "r", encoding="utf-8") as f:
            pre_memory = f.read()
    except FileNotFoundError:
        pre_memory = ""

    if config.get("settings"):
        Agent = EasyMate(
            key=config["api_key"],
            url=config["base_url"],
            model=config["model"],
            settings=f"{config['settings']}\n\n{pre_memory}"
        )
    else:
        Agent = EasyMate(
            key=config["api_key"],
            url=config["base_url"],
            model=config["model"]
        )

    while True:
        if not os.path.exists("./tasks.json"):
            time.sleep(10)
            continue

        try:
            with open("./tasks.json", 'r', encoding='utf-8') as f:
                tasks = json.load(f)
        except json.JSONDecodeError as e:
            print(f"配置文件 './tasks.json' 格式错误：{e}")
            time.sleep(10)
            continue
        
        for i in tasks.values():
            now = datetime.now().strftime("%H:%M")
            if now == i[1]:
                print(f"AI完成任务{i[0]}：{Agent.input(i[0])}")

        time.sleep(60)

def main():
    if not os.path.exists("./config.json"):
        print("配置文件 './config.json' 不存在，请从 config.example.json 复制一份并修改。")
        return
    
    try:
        with open("./config.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"配置文件 './config.json' 格式错误：{e}")
        return
    
    required = ["api_key", "base_url", "model"]
    missing = [field for field in required if field not in config]
    if missing:
        print(f"配置文件中缺少必需字段：{', '.join(missing)}")
        return
    
    try:
        with open("memory.txt", "r", encoding="utf-8") as f:
            pre_memory = f.read()
    except FileNotFoundError:
        pre_memory = ""

    if config.get("settings"):
        Agent = EasyMate(
            key=config["api_key"],
            url=config["base_url"],
            model=config["model"],
            settings=f"{config['settings']}\n\n{pre_memory}"
        )
    else:
        Agent = EasyMate(
            key=config["api_key"],
            url=config["base_url"],
            model=config["model"]
        )

    print("欢迎使用EasyMate助手，输入c结束当前输入，输入 q 单独一行可退出聊天。")

    t = threading.Thread(target=run_tasks, daemon=True)
    t.start()

    while True:
        print("用户：")
        msg = multi_line_input("")
        if msg.strip().lower() == "q":
            with open("memory.txt", "w", encoding="utf-8") as f:
                f.write(Agent.summarize_msg(len(Agent.msgs())))
            break
        if msg.strip() == "":
            continue
        print(f"AI：{Agent.input(msg)}")
        Agent.memory()

if __name__ == "__main__":
    main()