
import os
import subprocess
import sys


# ==============================================================================
# 風格設定 (用於彩色輸出)
# ==============================================================================
class Style:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'

def print_color(text, color=Style.RESET, bold=False):
    """以指定的顏色和樣式印出文字"""
    style = Style.BOLD if bold else ''
    print(f"{style}{color}{text}{Style.RESET}")

# ==============================================================================
# 核心功能
# ==============================================================================

def run_command(command, description, check=True):
    """執行一個 shell 命令並即時顯示其輸出，失敗時拋出例外"""
    print_color(f"\n>> {description}", Style.CYAN, bold=True)
    try:
        with subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding='utf-8',
            errors='replace'
        ) as process:
            progress_line_printed = False
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                
                stripped_line = line.strip()
                if stripped_line.startswith('Progress:'):
                    print(f"  {stripped_line}", end='\r')
                    progress_line_printed = True
                else:
                    if progress_line_printed:
                        print(' ' * 80, end='\r')
                        progress_line_printed = False
                    print(stripped_line)
            
            print()
            return_code = process.wait()

        if check and return_code != 0:
            raise subprocess.CalledProcessError(return_code, command)
        
        print_color(f"✓ {description.split('...')[0]} 成功完成。", Style.GREEN)
        return True
        
    except FileNotFoundError:
        print_color(f"✗ 錯誤：找不到命令，請確保相關程式已安裝並在 PATH 環境變數中。", Style.RED, bold=True)
        raise
    except subprocess.CalledProcessError as e:
        print_color(f"✗ 錯誤：'{description}' 執行失敗，返回碼 {e.returncode}。", Style.RED, bold=True)
        raise e
    except Exception as e:
        print_color(f"✗ 發生未知錯誤：{e}", Style.RED, bold=True)
        raise e
def command_exists(command):
    """檢查指定的命令是否存在於系統 PATH 中"""
    return subprocess.run(f"where {command}", shell=True, capture_output=True).returncode == 0

def refresh_environment():
    """嘗試刷新環境變數，以便腳本能找到剛安裝的命令"""
    print_color("\n>> 正在刷新環境變數...", Style.YELLOW)
    # Chocolatey 的環境變數刷新腳本
    choco_refresh_script = os.path.join(os.environ.get("ProgramData", "C:\\ProgramData"), "chocolatey\\helpers\\refreshenv.cmd")
    if os.path.exists(choco_refresh_script):
        run_command(f'"{choco_refresh_script}"', "刷新 Chocolatey 環境變數...")
    else:
        print_color("! 未找到 Chocolatey 環境刷新腳本，某些命令可能在下次開啟終端機前無法使用。", Style.YELLOW)


# ==============================================================================
# 主安裝流程
# ==============================================================================

def main():
    print_color("============================================================", Style.BOLD)
    print_color("    Gemini CLI 環境自動安裝程式 (Windows)", Style.BOLD)
    print_color("============================================================", Style.BOLD)
    print_color("本程式將會自動安裝以下軟體：")
    print_color("- Chocolatey (Windows 套件管理器)")
    print_color("- Python")
    print_color("- NVM for Windows (Node.js 版本管理器)")
    print_color("- Node.js (LTS 長期支援版)")
    print_color("- Google Gemini CLI")

    try:
        # --- 1. 安裝 Chocolatey ---
        if not command_exists("choco"):
            print_color("\n>> Chocolatey 未安裝，開始自動安裝...", Style.YELLOW, bold=True)
            print_color("這一步會花費一點時間下載並設定，請耐心等候...", Style.YELLOW)
            ps_command = "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
            run_command(f'powershell -Command "{ps_command}"', "安裝 Chocolatey 套件管理器...")
            refresh_environment()
        else:
            print_color("\n✓ Chocolatey 已安裝。", Style.GREEN)

        # --- 2. 檢查 Python ---
        if not command_exists("python"):
            print_color("正在準備安裝 Python，過程可能需要數分鐘...", Style.YELLOW)
            run_command("choco install python -y", "安裝 Python...")
        else:
            print_color("\n✓ Python 已安裝。", Style.GREEN)

        # --- 3. 安裝或更新 NVM for Windows ---
        if not command_exists("nvm"):
            run_command("choco install nvm -y", "安裝 NVM for Windows...")
            refresh_environment()
        else:
            print_color("\n✓ NVM for Windows 已安裝，檢查更新...", Style.GREEN)
            run_command("choco upgrade nvm -y", "更新 NVM for Windows...")

        # --- 4. 安裝 Node.js LTS 並使用它 ---
        print_color("\n>> 正在檢查 Node.js LTS 版本...", Style.CYAN, bold=True)
        nvm_root = os.environ.get("NVM_HOME", os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "nvm"))
        nvm_exe = f'"{os.path.join(nvm_root, "nvm.exe")}"'

        if not os.path.exists(nvm_exe.strip('"')):
            print_color(f"✗ 嚴重錯誤：在 {nvm_root} 找不到 nvm.exe。", Style.RED, bold=True)
            print_color("  請檢查 NVM for Windows 是否已成功安裝，或手動設定 NVM_HOME 環境變數。", Style.YELLOW)
            sys.exit(1)

        print_color("正在下載並安裝 Node.js，這是最耗時的步驟，可能需要5-10分鐘，請務必耐心等候...", Style.YELLOW)
        run_command(f"{nvm_exe} install lts", "檢查、安裝或更新 Node.js 至最新 LTS 版本...")
        run_command(f"{nvm_exe} use lts", "啟用 Node.js LTS 版本...")

        # --- 5. 安裝或更新 Gemini CLI ---
        print_color("\n>> 正在安裝或更新 Gemini CLI...", Style.CYAN, bold=True)
        try:
            if not command_exists("gemini"):
                print_color("正在從網路安裝 Gemini CLI，請稍候...", Style.YELLOW)
                run_command("npm install -g @google/gemini-cli", "透過 npm 安裝 Google Gemini CLI...")
            else:
                print_color("Google Gemini CLI 已安裝，檢查更新...", Style.GREEN)
                run_command("npm update -g @google/gemini-cli", "更新 Google Gemini CLI...")
        except subprocess.CalledProcessError:
            print_color("✗ Gemini CLI 安裝/更新失敗。", Style.RED, bold=True)
            print_color("  這通常是 npm 的問題。請嘗試在一個新的系統管理員終端機中執行以下指令來清理快取：", Style.YELLOW)
            print_color("  npm cache clean --force", Style.CYAN)
            print_color("  然後再重新執行本安裝腳本。", Style.YELLOW)
            sys.exit(1)

    except (subprocess.CalledProcessError, FileNotFoundError):
        # 捕獲由 run_command 拋出的任何其他錯誤
        print_color("\n安裝過程中發生嚴重錯誤，腳本已終止。", Style.RED, bold=True)
        print_color("請檢查上方的錯誤訊息以了解詳情。", Style.YELLOW)
        sys.exit(1)
    except Exception as e:
        print_color(f"\n發生未預期的嚴重錯誤: {e}", Style.RED, bold=True)
        sys.exit(1)


    # --- 最終說明 ---
    print_color("\n=======================================================================", Style.GREEN, bold=True)
    print_color("🎉 全部安裝成功！", Style.GREEN, bold=True)
    print_color("=======================================================================", Style.GREEN, bold=True)
    print_color("\n下一步：", Style.YELLOW, bold=True)
    print_color("1. 關閉此視窗。", Style.YELLOW)
    print_color("2. 【非常重要】請務必「開啟一個新的」命令提示字元(CMD)或 PowerShell 視窗。", Style.YELLOW)
    print_color("3. 在新視窗中，輸入以下指令來登入您的 Google 帳號：", Style.YELLOW)
    print_color("   gemini auth login", Style.CYAN)
    print_color("4. 您的瀏覽器將會開啟，請依照畫面指示完成登入。")
    print_color("5. 登入後，您就可以開始使用 gemini 指令了！", Style.YELLOW)


if __name__ == "__main__":
    # 確保在 Windows 上能顯示顏色
    os.system('')
    main()
