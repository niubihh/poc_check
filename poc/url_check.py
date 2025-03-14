# _*_ coding : utf-8 _*_
# @Time : 2025-03-11 13:08
# Author : 长安风生
# File : 9979
# Project : pythonProject
# 确保先安装了这个库
import os
import sys
# 获取当前脚本绝对路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(SCRIPT_DIR, "../check/url_add_check.txt")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "../result/url_add.txt")
#检测前描述
def print_logo():
    logo = """
             .__                                           _____                           .__                           
  ____ |  |__ _____    ____    _________    ____   _/ ____\____   ____    ____  _____|  |__   ____   ____    ____  
_/ ___\|  |  \\__  \  /    \  / ___\__  \  /    \  \   __\/ __ \ /    \  / ___\/  ___/  |  \_/ __ \ /    \  / ___\ 
\  \___|   Y  \/ __ \|   |  \/ /_/  > __ \|   |  \  |  | \  ___/|   |  \/ /_/  >___ \|   Y  \  ___/|   |  \/ /_/  >
 \___  >___|  (____  /___|  /\___  (____  /___|  /  |__|  \___  >___|  /\___  /____  >___|  /\___  >___|  /\___  / 
     \/     \/     \/     \//_____/     \/     \/             \/     \//_____/     \/     \/     \/     \//_____/
    """
    print(logo)

def print_usage():
    print("使用说明：")
    print("    1.在check文件下创建url_add_check.txt把要检测的url放入url_add_check.txt")
    print("    2.输入路径并执行")
    print("结果说明：")
    print("    添加完成的url会保存到url_add.txt")
    print()

def start_message():
    print("本程序仅供学习使用，如若非法他用，与本文作者无关，需自行负责！")
    print("程序功能：自动检测url前是否有https://没有就添加   By:长安风生")
    print("-" * 88)  # 打印分割线

def format_urls(file_path):
    updated_urls = []
    url_count = 0

    # 打开文件并逐行读取
    with open(file_path, 'r') as file:
        for line in file:
            url = line.strip()  # 去除行尾的换行符和空格
            if not (url.startswith('http://') or url.startswith('https://')):
                # 如果URL不是以http://或https://开头，则添加http://
                url = 'http://' + url
            updated_urls.append(url)
            url_count += 1  # 统计URL数量
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as  file:
        for url in updated_urls:
            file.write(url + '\n')

    return updated_urls, url_count
if __name__ == "__main__":
    print_logo()
    print_usage()
    start_message()
    # 询问是否想要执行检测
    print("您希望现在执行脚本吗？(yes/no):")
    execute_check = input().strip().lower()
    if execute_check not in ["yes", "y"]:
        print("执行已取消!")
        sys.exit(0)
    # 处理文件中的URLs并统计数量
    formatted_urls, total_urls = format_urls(file_path)

    # 输出格式化后的URLs和URL总数
    for url in formatted_urls:
        print(url)
    print(f"Total URLs: {total_urls}")
    print("url添加完成")

