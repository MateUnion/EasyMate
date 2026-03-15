from datetime import datetime

def execute() -> str:
    now = datetime.now()

    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday = weekdays[now.weekday()]

    return now.strftime(f"%Y-%m-%d {weekday} %H:%M:%S")