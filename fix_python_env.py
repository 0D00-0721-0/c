#!/usr/bin/env python3
import sys
import subprocess
import os

def check_python_versions():
    """检查系统上的Python版本"""
    print("="*50)
    print("检查Python版本:")
    versions = {}
    
    # 检查常见Python路径
    paths = [
        "/usr/bin/python",          # macOS系统默认
        "/usr/bin/python3",         # 系统Python3
        "/usr/local/bin/python3",   # Homebrew安装
        "/opt/homebrew/bin/python3" # M1 Homebrew路径
    ]
    
    for path in paths:
        if os.path.exists(path):
            try:
                result = subprocess.run(
                    [path, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=3
                )
                version = result.stdout.strip() or result.stderr.strip()
                versions[path] = version
                print(f"{path}: {version}")
            except:
                versions[path] = "无法获取版本"
    
    return versions

def check_requests_installation(python_path):
    """检查指定Python路径是否安装了requests"""
    print("\n" + "="*50)
    print(f"检查 {python_path} 的requests安装:")
    try:
        result = subprocess.run(
            [python_path, "-c", "import requests; print(requests.__version__)"],
            capture_output=True,
            text=True,
            timeout=3
        )
        if result.returncode == 0:
            print(f"✅ 已安装requests (版本: {result.stdout.strip()})")
            return True
        else:
            print(f"❌ 未安装requests: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"检查失败: {e}")
        return False

def install_requests(python_path):
    """为指定Python路径安装requests"""
    print("\n" + "="*50)
    print(f"为 {python_path} 安装requests...")
    try:
        subprocess.run(
            [python_path, "-m", "pip", "install", "requests"],
            check=True
        )
        print("✅ 安装成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 安装失败: {e}")
        print("请尝试手动安装:")
        print(f"  {python_path} -m pip install requests")
        return False
    except Exception as e:
        print(f"❌ 意外错误: {e}")
        return False

def create_runner_script():
    """创建B站爬虫运行脚本"""
    script_content = """#!/usr/bin/env python3
import sys
import os
import subprocess

def main():
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 查找bilibili_comment_crawler.py
    crawler_path = os.path.join(script_dir, "bilibili_comment_crawler.py")
    
    if not os.path.exists(crawler_path):
        print(f"错误: 未找到爬虫脚本 {crawler_path}")
        return
    
    # 使用当前环境的Python解释器运行
    python_exec = sys.executable
    print(f"使用Python解释器: {python_exec}")
    
    try:
        subprocess.run([python_exec, crawler_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"运行爬虫失败: {e}")
    except Exception as e:
        print(f"意外错误: {e}")

if __name__ == "__main__":
    main()
"""
    
    with open("run_crawler.py", "w") as f:
        f.write(script_content)
    
    # 设置执行权限
    os.chmod("run_crawler.py", 0o755)
    print("\n已创建运行脚本: run_crawler.py")
    print("使用以下命令运行爬虫:")
    print("  ./run_crawler.py")

def main():
    print("="*50)
    print("Python环境诊断与修复工具")
    print("="*50)
    
    # 1. 检查Python版本
    versions = check_python_versions()
    
    # 2. 检查当前使用的Python
    current_python = sys.executable
    print(f"\n当前脚本使用的Python: {current_python}")
    
    # 3. 检查requests安装
    if not check_requests_installation(current_python):
        print("\n尝试修复...")
        if install_requests(current_python):
            # 重新检查
            check_requests_installation(current_python)
    
    # 4. 创建运行脚本
    create_runner_script()
    
    print("\n" + "="*50)
    print("修复完成！请使用以下步骤:")
    print("1. 确保爬虫脚本命名为 'bilibili_comment_crawler.py'")
    print("2. 运行命令: ./run_crawler.py")

if __name__ == "__main__":
    main()
