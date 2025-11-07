# Gemini CLI Windows Auto-Installer (繁體中文)

這是一個一鍵安裝腳本，旨在幫助使用者在 Windows 環境下，自動化安裝與設定完整的 Google Gemini CLI 工作環境。

本腳本透過一系列的自動化檢查、安裝與設定，讓使用者無需手動處理繁瑣的環境依賴，即可快速開始使用 Gemini CLI。

## ✨ 功能特性

- **全自動化**：腳本會自動處理所有必要的軟體安裝與設定。
- **智慧判斷**：
  - 自動檢查並安裝 [Chocolatey](https://chocolatey.org/) 套件管理器。
  - 如果未安裝 Python，則自動安裝。
  - 自動檢查並安裝/更新 [NVM for Windows](https://github.com/coreybutler/nvm-windows)。
  - 自動安裝最新的 Node.js LTS (長期支援) 版本。
  - 自動安裝或更新 `@google/gemini-cli`。
- **友善介面**：安裝過程以繁體中文顯示，並提供清晰的進度與安撫訊息。
- **乾淨輸出**：優化了終端機的輸出，將進度條彙整在同一行，避免資訊洗版。

## 📋 環境需求

- Windows 10 或更高版本。
- 系統管理員權限 (腳本會自動提示要求權限)。
- 可用的網際網路連線。

## 🚀 如何使用

1.  前往本專案的 GitHub 頁面： [https://github.com/Chiakai-Chang/Gemini-CLI-Windows-Auto-Installer](https://github.com/Chiakai-Chang/Gemini-CLI-Windows-Auto-Installer)
2.  點擊頁面中綠色的 `<> Code` 按鈕，然後選擇 `Download ZIP`。
3.  下載完成後，將 ZIP 檔案解壓縮到您喜歡的位置。
4.  進入解壓縮後的資料夾 (您會看到 `install.bat` 和 `install.py` 檔案)。
5.  在 `install.bat` 檔案上按一下滑鼠右鍵，選擇「**以系統管理員身分執行**」。
6.  之後，腳本將會自動執行，您只需要根據視窗中的提示稍作等待即可。

### 安裝後續步驟

當腳本執行完畢並顯示「🎉 全部安裝成功！」訊息後：

1.  **關閉** 當前的安裝視窗。
2.  **【非常重要】** 打開一個**新的**命令提示字元 (CMD) 或 PowerShell 視窗。
3.  在新視窗中，輸入以下指令來登入您的 Google 帳號：
    ```sh
    gemini auth login
    ```
4.  您的瀏覽器將會自動開啟，請依照畫面指示完成登入授權。
5.  完成後，您就可以開始享受 Gemini CLI 的強大功能了！

## 📄 授權

本專案採用 [MIT License](LICENSE) 授權。
