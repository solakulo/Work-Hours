import json
import os
from tkinter import Tk, Label, Entry, Button, StringVar, Frame, Toplevel
from tkinter.messagebox import showinfo

# 配置文件路径
CONFIG_FILE = "work_schedule_config.json"


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {
            "standard_start_time": "09:00",
            "standard_end_time": "18:00",
            "lunch_break": "12:00-13:00",
            "rest_periods": ["15:00-15:15"],
        }


def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


class WorkScheduleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("工作时间设置")
        self.config = load_config()

        # 初始化界面
        self.init_ui()

    def init_ui(self):
        frame = Frame(self.root)
        frame.pack(padx=10, pady=10)

        # 标准上班时间
        Label(frame, text="标准上班时间:").grid(row=0, column=0, sticky="w")
        self.start_time_var = StringVar(value=self.config["standard_start_time"])
        Entry(frame, textvariable=self.start_time_var).grid(row=0, column=1, pady=5)

        # 标准下班时间
        Label(frame, text="标准下班时间:").grid(row=1, column=0, sticky="w")
        self.end_time_var = StringVar(value=self.config["standard_end_time"])
        Entry(frame, textvariable=self.end_time_var).grid(row=1, column=1, pady=5)

        # 午休时间
        Label(frame, text="午休时间:").grid(row=2, column=0, sticky="w")
        self.lunch_break_var = StringVar(value=self.config["lunch_break"])
        Entry(frame, textvariable=self.lunch_break_var).grid(row=2, column=1, pady=5)

        # 公司规定休息时间段
        Label(frame, text="公司规定休息时间段 (用逗号分隔):").grid(
            row=3, column=0, sticky="w"
        )
        self.rest_periods_var = StringVar(value=",".join(self.config["rest_periods"]))
        Entry(frame, textvariable=self.rest_periods_var).grid(row=3, column=1, pady=5)

        # 保存按钮
        Button(frame, text="保存", command=self.save_config).grid(
            row=4, column=0, pady=10
        )

        # 关闭按钮
        Button(frame, text="关闭", command=self.root.quit).grid(
            row=4, column=1, pady=10
        )

    def save_config(self):
        self.config["standard_start_time"] = self.start_time_var.get()
        self.config["standard_end_time"] = self.end_time_var.get()
        self.config["lunch_break"] = self.lunch_break_var.get()
        self.config["rest_periods"] = [
            p.strip() for p in self.rest_periods_var.get().split(",") if p.strip()
        ]

        save_config(self.config)
        showinfo("提示", "配置已保存！")


if __name__ == "__main__":
    root = Tk()
    app = WorkScheduleApp(root)
    root.mainloop()
