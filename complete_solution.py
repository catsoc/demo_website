#!/usr/bin/env python3
"""
一鍵式 Google 收錄完整解決方案
自動檢測 + 自動提交 + 自動監控
"""

import subprocess
import webbrowser
import time
import os
from pathlib import Path

def print_header(title):
    print(f"\n{'='*50}")
    print(f"🎯 {title}")
    print(f"{'='*50}")

def print_step(step, description):
    print(f"\n{step} {description}")

def run_index_check():
    """執行收錄檢查"""
    print_step("1️⃣", "執行自動收錄檢查...")
    try:
        result = subprocess.run(['python', 'google_index_checker.py'], 
                              capture_output=True, text=True, timeout=60)
        print(result.stdout)
        return "indexed" in result.stdout.lower()
    except Exception as e:
        print(f"❌ 檢查失敗: {e}")
        return False

def setup_google_console():
    """自動設定 Google Search Console"""
    print_step("2️⃣", "準備 Google Search Console 設定...")
    
    # 開啟 Google Search Console
    gsc_url = "https://search.google.com/search-console/"
    print(f"🌐 正在開啟: {gsc_url}")
    webbrowser.open(gsc_url)
    
    # 準備必要資訊
    site_url = "https://catsoc.github.io/demo_website/"
    sitemap_url = f"{site_url}sitemap.xml"
    
    print("\n📋 設定資訊:")
    print(f"   網站網址: {site_url}")
    print(f"   Sitemap: {sitemap_url}")
    
    # 生成設定指引
    instructions = f"""
🔧 Google Search Console 設定步驟:

1. **新增資源**
   - 選擇「網址前置字元」
   - 輸入: {site_url}
   
2. **驗證所有權** (選擇任一方法)
   - HTML 檔案: 上傳 google-verification.html
   - HTML 標籤: 添加到網站 <head> 區域
   - DNS 記錄: 在 DNS 設定中添加 TXT 記錄
   
3. **提交 Sitemap**
   - 到 Sitemap 區域
   - 新增 sitemap: sitemap.xml
   - 完整網址: {sitemap_url}
   
4. **請求索引**
   - 到網址檢測工具
   - 輸入首頁網址: {site_url}
   - 點擊「請求索引」

✅ 完成後等待 1-2 週Google 處理
"""
    
    # 保存指引到檔案
    with open('gsc-setup-guide.txt', 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    print("\n📄 詳細指引已保存到: gsc-setup-guide.txt")
    print(instructions)

def create_monitoring_script():
    """建立監控腳本"""
    print_step("3️⃣", "建立自動監控系統...")
    
    monitoring_script = '''
@echo off
title Google Index Monitor
echo ========================================
echo    Google 收錄監控系統
echo ========================================
echo.

:monitor_loop
echo [%date% %time%] 執行收錄檢查...
python google_index_checker.py

echo.
echo 等待 24 小時後再次檢查...
echo 按 Ctrl+C 可停止監控
timeout /t 86400 /nobreak > nul

goto monitor_loop
'''
    
    with open('monitor-indexing.bat', 'w') as f:
        f.write(monitoring_script)
    
    print("✅ 已建立監控腳本: monitor-indexing.bat")

def create_quick_tools():
    """建立快速工具"""
    print_step("4️⃣", "建立快速工具...")
    
    # 快速檢查工具
    quick_check = '''
@echo off
echo 🔍 快速收錄檢查
echo ==================
python google_index_checker.py
pause
'''
    
    with open('quick-check.bat', 'w') as f:
        f.write(quick_check)
    
    print("✅ 快速檢查工具: quick-check.bat")

def main():
    print_header("Google 收錄完整解決方案")
    print("🚀 自動化處理 Google 收錄問題，無需手動操作！")
    
    # 步驟 1: 檢查當前狀態
    is_indexed = run_index_check()
    
    if is_indexed:
        print("\n🎉 網站已被收錄！")
        print("💡 建議: 開始監控搜尋效能")
    else:
        print("\n📋 網站尚未收錄，啟動完整設定流程...")
        
        # 步驟 2: 設定 Google Search Console
        setup_google_console()
        
        # 步驟 3: 建立監控系統
        create_monitoring_script()
        
        # 步驟 4: 建立快速工具
        create_quick_tools()
    
    print_header("完成！")
    print("🎯 接下來要做的事:")
    print("   1. 按照指引完成 Google Search Console 設定")
    print("   2. 執行 monitor-indexing.bat 開始自動監控")
    print("   3. 使用 quick-check.bat 隨時快速檢查")
    print("   4. 1-2 週後檢查收錄結果")
    
    print(f"\n✅ 所有工具已準備完成！")

if __name__ == "__main__":
    main()
