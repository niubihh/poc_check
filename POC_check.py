# _*_ coding : utf-8 _*_
# @Time : 2025-03-14 15:18
# Author : 长安风生
# File : tuxin
# Project : pythonProject
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
import subprocess
import threading
import sys
import os
import re
import locale
import ast
import chardet
from datetime import datetime


class POCExecutor:
    def __init__(self, root):
        self.root = root
        root.title("长安风生 - POC&脚本V0.0")
        self.ansi_map = {
            "30": "black", "31": "red", "32": "green", "33": "yellow",
            "34": "blue", "35": "magenta", "36": "cyan", "37": "white",
            "90": "bright_black", "91": "bright_red", "92": "bright_green",
            "93": "bright_yellow", "94": "bright_blue", "95": "bright_magenta",
            "96": "bright_cyan", "97": "bright_white"
        }
        self.encoding = locale.getpreferredencoding()
        self.process = None
        self.is_running = False

        # 初始化界面
        self.setup_ui()
        self.setup_style()
        self.setup_tags()
        self.setup_shortcuts()

        # 显示初始信息
        self.show_help()
        self.scan_pocs()

    def setup_ui(self):
        """初始化用户界面"""
        main_frame = ttk.PanedWindow(self.root, orient=tk.VERTICAL)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 脚本选择区域
        script_frame = ttk.Frame(main_frame)
        main_frame.add(script_frame)

        ttk.Label(script_frame, text="POC&脚本路径:").pack(side=tk.LEFT)
        self.script_entry = ttk.Entry(script_frame, width=50)
        self.script_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        btn_frame = ttk.Frame(script_frame)
        btn_frame.pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="浏览", command=self.browse_script).pack(side=tk.LEFT)
        ttk.Button(btn_frame, text="扫描POC&脚本", command=self.scan_pocs).pack(side=tk.LEFT, padx=5)

        # 控制按钮
        ctrl_frame = ttk.Frame(main_frame)
        main_frame.add(ctrl_frame)

        self.run_btn = ttk.Button(ctrl_frame, text="执行POC&脚本", command=self.toggle_execution)
        self.run_btn.pack(side=tk.LEFT, padx=2)
        self.stop_btn = ttk.Button(ctrl_frame, text="停止", state=tk.DISABLED, command=self.stop_script)
        self.stop_btn.pack(side=tk.LEFT)

        # 输出区域
        output_frame = ttk.Frame(main_frame)
        main_frame.add(output_frame, weight=1)

        self.output = scrolledtext.ScrolledText(
            output_frame,
            wrap=tk.WORD,
            width=130,
            height=25,
            bg="#1E1E1E",
            insertbackground="white",
            foreground="white"
        )
        self.output.pack(fill=tk.BOTH, expand=True)

        # 输入区域
        input_frame = ttk.Frame(main_frame)
        main_frame.add(input_frame)

        ttk.Label(input_frame, text="输入:").pack(side=tk.LEFT)
        self.input_entry = ttk.Entry(input_frame)
        self.input_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        self.input_entry.bind("<Return>", self.send_input)
        self.send_btn = ttk.Button(input_frame, text="发送", command=self.send_input, state=tk.DISABLED)
        self.send_btn.pack(side=tk.LEFT)

        # 状态栏
        self.status = ttk.Label(self.root, text=" 就绪", relief=tk.SUNKEN)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_style(self):
        """配置界面样式"""
        style = ttk.Style()
        style.theme_use("alt")
        style.configure(".",
                        background="#2D2D2D",
                        foreground="white",
                        fieldbackground="#404040"
                        )
        style.map("TButton",
                  background=[("active", "#4D4D4D")],
                  foreground=[("active", "white")]
                  )

    def setup_tags(self):
        """配置文本标签"""
        colors = {
            "black": "#000000", "red": "#FF0000", "green": "#00FF00",
            "yellow": "#FFFF00", "blue": "#0000FF", "magenta": "#FF00FF",
            "cyan": "#00FFFF", "white": "#FFFFFF", "bright_black": "#808080",
            "bright_red": "#FF5555", "bright_green": "#55FF55",
            "bright_yellow": "#FFFF55", "bright_blue": "#5555FF",
            "bright_magenta": "#FF55FF", "bright_cyan": "#55FFFF",
            "bright_white": "#FFFFFF", "help": "#00B4FF", "header": "#FFA500",
            "command": "#55FF55", "warning": "#FF5555", "success": "#00FF00",
            "timestamp": "#888888"
        }
        for name, color in colors.items():
            self.output.tag_config(name, foreground=color)
        self.output.tag_config("bold", font=('TkDefaultFont', 9, 'bold'))
        self.output.tag_config("underline", underline=1)

    def setup_shortcuts(self):
        """绑定快捷键"""
        self.root.bind("<F1>", lambda e: self.show_help())
        self.root.bind("<Control-o>", lambda e: self.browse_script())
        self.root.bind("<Control-r>", lambda e: self.toggle_execution())
        self.root.bind("<Control-q>", lambda e: self.root.destroy())

    def show_help(self):
        """显示帮助信息"""
        help_text = """
╔════════════════════════ 使用帮助 ══════════════════════════╗
[使用说明]
  1. 点击【浏览】选择Python脚本或点击【扫描POC】自动检测POC&脚本路径
  2. 点击【执行POC&脚本】运行程序
  3. 在输入框与脚本交互

[POC&脚本]
  1. Cleo文件传输软件任意文件读取漏洞(CVE-2024-50623）
  2. 自动检测url并添加“https://”脚本

[注意事项]
  • 支持ANSI 16色显示
  • 自动处理GBK/UTF-8编码
  • 执行前进行四重安全检测

[特别注意]
  本程序仅供学习使用，如若非法他用，与本文作者无关，需自行负责！
  By:长安风生
╚═══════════════════════════════════════════════════════╝
"""
        self.output.config(state=tk.NORMAL)
        self.output.delete(1.0, tk.END)
        for line in help_text.split('\n'):
            if '╔═' in line or '╚═' in line:
                self.output.insert(tk.END, line + '\n', 'header')
            elif line.startswith('['):
                self.output.insert(tk.END, line + '\n', 'command')
            elif line.startswith('  •'):
                self.output.insert(tk.END, line + '\n', 'warning')
            elif '示例脚本' in line:
                self.output.insert(tk.END, line + '\n', 'success')
            else:
                self.output.insert(tk.END, line + '\n', 'help')
        self.output.config(state=tk.DISABLED)

    def scan_pocs(self):
        """扫描POC目录"""
        self.append_output("\n" + "=" * 40 + "\n", "timestamp")
        self.append_output(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 扫描POC目录\n", "timestamp")

        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            poc_dir = os.path.join(base_dir, "poc")
            os.makedirs(poc_dir, exist_ok=True)

            scripts = []
            for root, _, files in os.walk(poc_dir):
                for file in files:
                    if file.endswith(".py"):
                        scripts.append(os.path.join(root, file))

            if not scripts:
                self.append_output("未找到任何POC脚本\n", "bright_red")
                return

            self.append_output("发现以下POC脚本：\n", "bright_green")
            for idx, script in enumerate(scripts, 1):
                self.append_output(f"{idx}. {script}\n", "bright_cyan")
        except Exception as e:
            self.append_output(f"扫描失败：{str(e)}\n", "bright_red")

    def browse_script(self):
        """浏览脚本文件"""
        path = filedialog.askopenfilename(
            initialdir=os.path.join(os.path.dirname(__file__), "poc"),
            filetypes=[("Python脚本", "*.py")]
        )
        if path:
            self.script_entry.delete(0, tk.END)
            self.script_entry.insert(0, path)

    def toggle_execution(self):
        """切换执行状态"""
        if self.is_running:
            self.stop_script()
        else:
            self.start_script()

    def start_script(self):
        """启动脚本执行"""
        script_path = self.script_entry.get()
        if not script_path:
            messagebox.showwarning("警告", "请先选择脚本文件！")
            return

        try:
            # 预执行检查
            checks = [
                ("文件存在性", lambda: os.path.exists(script_path)),
                ("文件类型", lambda: script_path.lower().endswith('.py')),
                ("语法检查", lambda: ast.parse(open(script_path, 'rb').read().decode('utf-8', 'ignore'))),
                ("依赖检查", self.check_dependencies)
            ]

            self.append_output("\n[执行前检测]\n", "header")
            for idx, (name, check) in enumerate(checks, 1):
                self.append_output(f"检测{idx}/4 {name}...", "bright_yellow")
                try:
                    if check():
                        self.append_output(" ✓ 通过\n", "bright_green")
                    else:
                        self.append_output(" ✗ 失败\n", "bright_red")
                        return
                except Exception as e:
                    self.append_output(f" ✗ 错误：{str(e)}\n", "bright_red")
                    return

            # 启动进程
            self.process = subprocess.Popen(
                [sys.executable, "-u", script_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=0
            )
            self.is_running = True
            self.run_btn.config(text="停止脚本")
            self.stop_btn.config(state=tk.NORMAL)
            self.send_btn.config(state=tk.NORMAL)
            self.update_status("运行中...")
            self.clear_output()

            # 启动监控线程
            threading.Thread(target=self.monitor_stdout, daemon=True).start()
            threading.Thread(target=self.monitor_stderr, daemon=True).start()

        except Exception as e:
            self.append_output(f"启动失败: {str(e)}\n", "bright_red")
            self.cleanup()

    def check_dependencies(self):
        """检查依赖库"""
        try:
            with open(self.script_entry.get(), 'rb') as f:
                content = self.smart_decode(f.read())
                if "import requests" in content:
                    import requests
                if "import numpy" in content:
                    import numpy
            return True
        except ImportError as e:
            raise Exception(f"缺少依赖库：{e.name}")

    def smart_decode(self, byte_data):
        """智能解码"""
        try:
            detected = chardet.detect(byte_data)
            return byte_data.decode(detected['encoding'] if detected['confidence'] > 0.7 else 'utf-8', errors='replace')
        except:
            return byte_data.decode('utf-8', errors='replace')

    def monitor_stdout(self):
        """监控标准输出"""
        while self.is_running and self.process:
            byte_data = self.process.stdout.readline()
            if not byte_data and self.process.poll() is not None:
                break
            if byte_data:
                try:
                    text = self.smart_decode(byte_data)
                    segments = self.parse_ansi(text, 'white')
                    self.append_segments(segments)
                except Exception as e:
                    self.append_output(f"输出解析错误: {str(e)}\n", "bright_red")

    def monitor_stderr(self):
        """监控错误输出"""
        while self.is_running and self.process:
            byte_data = self.process.stderr.readline()
            if not byte_data and self.process.poll() is not None:
                break
            if byte_data:
                try:
                    text = self.smart_decode(byte_data)
                    segments = self.parse_ansi(text, 'bright_red')
                    self.append_segments(segments)
                except Exception as e:
                    self.append_output(f"错误输出解析错误: {str(e)}\n", "bright_red")

    def parse_ansi(self, text, default_tag):
        """解析ANSI转义序列"""
        ansi_escape = re.compile(r'\033\[([\d;]*)m')
        segments = []
        last_idx = 0
        current_tags = [default_tag]

        for match in ansi_escape.finditer(text):
            start, end = match.span()
            if start > last_idx:
                segments.append((current_tags.copy(), text[last_idx:start]))

            codes = match.group(1).split(';')
            current_tags = [default_tag]

            for code in codes:
                if code == '0':
                    current_tags = [default_tag]
                elif code == '1':
                    current_tags.append('bold')
                elif code == '4':
                    current_tags.append('underline')
                elif code in self.ansi_map:
                    current_tags.append(self.ansi_map[code])

            last_idx = end

        if last_idx < len(text):
            segments.append((current_tags.copy(), text[last_idx:]))

        return segments

    def append_segments(self, segments):
        """添加分段文本"""
        self.root.after(0, self._safe_append_segments, segments)

    def _safe_append_segments(self, segments):
        """线程安全添加文本"""
        self.output.config(state=tk.NORMAL)
        for tags, text in segments:
            seen = set()
            unique_tags = [tag for tag in tags if not (tag in seen or seen.add(tag))]
            self.output.insert(tk.END, text, tuple(unique_tags))
        self.output.see(tk.END)
        self.output.config(state=tk.DISABLED)

    def append_output(self, text, tag="white"):
        """添加输出"""
        self.root.after(0, self._safe_append, text, tag)

    def _safe_append(self, text, tag):
        """线程安全添加"""
        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, text, tag)
        self.output.see(tk.END)
        self.output.config(state=tk.DISABLED)

    def clear_output(self):
        """清空输出"""
        self.output.config(state=tk.NORMAL)
        self.output.delete(1.0, tk.END)
        self.output.config(state=tk.DISABLED)

    def stop_script(self):
        """停止脚本"""
        if self.process and self.process.poll() is None:
            try:
                self.process.terminate()
                self.process.wait(timeout=2)
            except Exception as e:
                self.append_output(f"终止异常: {str(e)}\n", "bright_yellow")
        self.cleanup()
        self.append_output("[进程已停止]\n", "header")
        self.update_status("已停止")

    def send_input(self, event=None):
        """发送输入"""
        if not self.is_running or not self.process:
            return

        text = self.input_entry.get()
        if text:
            try:
                self.process.stdin.write(text.encode() + b'\n')
                self.process.stdin.flush()
                self.append_output(f">>> {text}\n", "bright_cyan")
                self.input_entry.delete(0, tk.END)
            except Exception as e:
                self.append_output(f"输入失败: {str(e)}\n", "bright_red")

    def cleanup(self):
        """清理资源"""
        self.is_running = False
        self.run_btn.config(text="执行脚本")
        self.stop_btn.config(state=tk.DISABLED)
        self.send_btn.config(state=tk.DISABLED)
        if self.process:
            try:
                self.process.stdin.close()
                self.process.terminate()
            except:
                pass
        self.process = None

    def update_status(self, message):
        """更新状态栏"""
        self.status.config(text=f" 状态: {message}")


if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(800, 600)
    app = POCExecutor(root)
    root.mainloop()