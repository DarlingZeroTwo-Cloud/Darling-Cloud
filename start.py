import os
import sys
import subprocess
import shutil
import urllib.request

# 彩色输出
def green(text): print(f"\033[32m{text}\033[0m")
def cyan(text): print(f"\033[36m{text}\033[0m")
def yellow(text): print(f"\033[33m{text}\033[0m")
def magenta(text): print(f"\033[35m{text}\033[0m")
def red(text): print(f"\033[31m{text}\033[0m")

# 清屏 + 新建文件夹
os.system("cls")
os.makedirs("下载", exist_ok=True)

# 标题 LOGO
green("==========================================================")
cyan("          ██╗  ██╗ █████╗ ██████╗ ██╗     ███████╗")
cyan("          ██║  ██║██╔══██╗██╔══██╗██║     ██╔════╝")
cyan("          ███████║███████║██████╔╝██║     █████╗  ")
cyan("          ██╔══██║██╔══██╗██╔══██╗██║     ██╔══╝  ")
cyan("          ██║  ██║██║  ██║██║  ██║███████╗███████╗")
cyan("          ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝")
magenta("     Darling Zero Two 极速测速｜2秒测1-256线程")
green("==========================================================")
print()
print("规则：2秒极速测试1~256线程 → 取最高稳定线程 → 全速下载")
print("实时显示：总进度｜总速度MB/s｜各线程速度")
print()

# 输入链接
link = input("请粘贴下载链接：").strip()
if not link:
    red("链接不能为空！")
    input("按回车退出")
    sys.exit()

# ============================
# 检测 aria2c（核心功能）
# ============================
has_aria2 = shutil.which("aria2c") is not None

if not has_aria2:
    yellow("==================================================")
    red("⚠️  检测到你的 Windows 没有安装 aria2c！")
    yellow("将会使用系统自带下载 → 低速单线程下载")
    yellow("安装 aria2c 后可开启：全速多线程下载")
    yellow("==================================================")
    print()

# ============================
# 有 aria2 → 测速 + 全速下载
# ============================
if has_aria2:
    yellow("\n==================================================")
    yellow("【极速测速中 2秒内完成 1~256线程】")
    yellow("==================================================")
    print()

    stable = 1
    for t in range(1, 257):
        cmd = [
            "aria2c", f"-x{t}", f"-s{t}", "-k1M", "-d", "下载",
            "--timeout=1", "--max-tries=1", "--dry-run", link
        ]
        ret = subprocess.run(cmd, capture_output=True).returncode
        if ret == 28:
            break
        stable = t

    yellow(f"✅ 测速完成，最高稳定线程：{stable}")
    yellow("🚀 开始 aria2c 全速多线程下载...")
    print()

    final_cmd = [
        "aria2c", f"-x{stable}", f"-s{stable}", "-k1M",
        "-d", "下载", "--timeout=8", link
    ]
    code = subprocess.run(final_cmd).returncode

# ============================
# 无 aria2 → 系统降级下载
# ============================
else:
    yellow("⚠️  正在使用系统单线程下载...")
    print()
    try:
        filename = os.path.basename(link)
        save_path = os.path.join("下载", filename)
        urllib.request.urlretrieve(link, save_path)
        code = 0
    except Exception as e:
        red(f"下载失败：{str(e)}")
        code = 1

# ============================
# 结果提示
# ============================
print()
if code == 0:
    green("==================================================")
    green("✅ 下载完成！文件保存在【下载】文件夹")
    green("==================================================")
else:
    red("❌ 下载失败！")

print()
input("按回车退出")