import os, sys, threading, webbrowser, subprocess, urllib.request, time, tkinter as tk
from tkinter import messagebox

APP_NAME = "多手机工作台"
VERSION = "1.0.0"
BRIDGE_URL = "https://raw.githubusercontent.com/572126160-art/multi-phone-workbench/main/bridge.py"
WORKBENCH_URL = "http://127.0.0.1:8888"

def app_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

BASE = app_dir()
BRIDGE = os.path.join(BASE, "bridge.py")
proc = None

def download_bridge(status):
    try:
        status.set("正在检查最新版...")
        req = urllib.request.Request(BRIDGE_URL, headers={"User-Agent":"MultiPhoneWorkbench"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = r.read()
        with open(BRIDGE, "wb") as f:
            f.write(data)
        status.set("最新版已准备")
        return True
    except Exception as e:
        if os.path.exists(BRIDGE):
            status.set("网络异常，使用本地版本")
            return True
        messagebox.showerror(APP_NAME, f"无法下载 bridge.py\n\n{e}")
        status.set("启动失败")
        return False

def find_python():
    candidates = [
        ["py", "-3"],
        ["python"],
        ["python3"],
    ]
    for c in candidates:
        try:
            subprocess.run(c + ["--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
            return c
        except Exception:
            pass
    return None

def start_service(status, start_btn, open_btn):
    global proc
    start_btn.config(state="disabled")
    if not download_bridge(status):
        start_btn.config(state="normal")
        return
    py = find_python()
    if not py:
        messagebox.showerror(APP_NAME, "没有检测到 Python 3。\n\n请先安装 Python 3，并勾选 Add Python to PATH。")
        status.set("未检测到 Python")
        start_btn.config(state="normal")
        return
    try:
        status.set("正在启动本地服务...")
        creation = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        proc = subprocess.Popen(py + [BRIDGE], cwd=BASE, creationflags=creation)
        time.sleep(1.2)
        status.set("服务运行中")
        open_btn.config(state="normal")
        webbrowser.open(WORKBENCH_URL)
    except Exception as e:
        messagebox.showerror(APP_NAME, f"启动失败\n\n{e}")
        status.set("启动失败")
        start_btn.config(state="normal")

def check_update(status):
    def run():
        ok = download_bridge(status)
        if ok:
            messagebox.showinfo(APP_NAME, "已检查并更新到最新桥接版本。")
    threading.Thread(target=run, daemon=True).start()

def on_close(root):
    global proc
    try:
        if proc and proc.poll() is None:
            proc.terminate()
    except Exception:
        pass
    root.destroy()

root = tk.Tk()
root.title(f"{APP_NAME} V{VERSION}")
root.geometry("460x330")
root.resizable(False, False)

status = tk.StringVar(value="未启动")

title = tk.Label(root, text="📱 多手机工作台", font=("Microsoft YaHei UI", 20, "bold"))
title.pack(pady=(28,6))
tk.Label(root, text=f"版本 V{VERSION}", fg="#777").pack()
tk.Label(root, text="").pack(pady=4)

box = tk.Frame(root, bd=1, relief="solid", padx=18, pady=14)
box.pack(fill="x", padx=34)
tk.Label(box, text="状态", fg="#777").pack(anchor="w")
tk.Label(box, textvariable=status, font=("Microsoft YaHei UI", 13, "bold")).pack(anchor="w", pady=(2,8))
tk.Label(box, text=WORKBENCH_URL, fg="#555").pack(anchor="w")

buttons = tk.Frame(root)
buttons.pack(pady=20)

start_btn = tk.Button(buttons, text="启动工作台", width=14, height=2, command=lambda: threading.Thread(target=start_service,args=(status,start_btn,open_btn),daemon=True).start())
start_btn.grid(row=0,column=0,padx=6)

open_btn = tk.Button(buttons, text="打开工作台", width=14, height=2, state="disabled", command=lambda:webbrowser.open(WORKBENCH_URL))
open_btn.grid(row=0,column=1,padx=6)

tk.Button(root, text="检查更新", width=18, command=lambda:check_update(status)).pack()

tk.Label(root, text="以后网页功能更新后，重新打开或点检查更新即可。", fg="#888").pack(pady=(12,0))

root.protocol("WM_DELETE_WINDOW", lambda:on_close(root))
root.mainloop()
