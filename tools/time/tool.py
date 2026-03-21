"""
获取时间工具
返回当前的本地日期和时间
"""

from datetime import datetime

def execute() -> str:
    """
    获取当前日期和时间

    Returns:
        格式化的日期时间字符串，例如 "2024-01-15 星期三 15:30:45"
    """
    now = datetime.now()

    # 星期名称列表
    weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    # 获取星期几（0=星期一，6=星期日）
    weekday = weekdays[now.weekday()]

    # 返回格式化字符串
    return now.strftime(f"%Y-%m-%d {weekday} %H:%M:%S")
