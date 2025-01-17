import os
from datetime import datetime
import win32evtlog

# 保存路径
OUTPUT_FILE = "system_logs_daily.txt"


def extract_system_logs():
    server = None  # 本地计算机
    log_type = "System"
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

    logs = []
    handle = win32evtlog.OpenEventLog(server, log_type)
    while True:
        events = win32evtlog.ReadEventLog(handle, flags, 0)
        if not events:
            break
        for event in events:
            if event.EventID == 30:  # 30: 开机
                logs.append(
                    {
                        "type": "开机",
                        "time": event.TimeGenerated,
                    }
                )
            elif event.EventID == 7002:  # 7002: 关机
                logs.append(
                    {
                        "type": "关机",
                        "time": event.TimeGenerated,
                    }
                )
    win32evtlog.CloseEventLog(handle)
    return logs


def save_logs_to_txt(logs):
    # 按日期分组最早开机和最晚关机时间
    daily_logs = {}
    for log in logs:
        date = log["time"].date()
        if date == datetime.now().date():  # 跳过当天的记录
            continue
        if date not in daily_logs:
            daily_logs[date] = {"first": None, "last": None}
        if log["type"] == "开机":
            if not daily_logs[date]["first"] or log["time"] < daily_logs[date]["first"]:
                daily_logs[date]["first"] = log["time"]
        if log["type"] == "关机":
            if not daily_logs[date]["last"] or log["time"] > daily_logs[date]["last"]:
                daily_logs[date]["last"] = log["time"]

    # 保存到文本文件
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for date, times in sorted(daily_logs.items()):
            first_time = (
                times["first"].strftime("%H:%M:%S") if times["first"] else "无记录"
            )
            last_time = (
                times["last"].strftime("%H:%M:%S") if times["last"] else "无记录"
            )
            f.write(f"{date}, {first_time}, {last_time}\n")
    print(f"日志已保存到 {OUTPUT_FILE}")


if __name__ == "__main__":
    logs = extract_system_logs()
    if not logs:
        print("未提取到任何日志，请检查系统日志或权限。")
    else:
        save_logs_to_txt(logs)
