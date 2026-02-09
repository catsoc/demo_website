#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google 收錄自動檢查器 - 完全自動化版本
作者：橘貓 AI 分身
功能：自動檢查網站是否被 Google 收錄，無需用戶手動操作
"""

import requests
import time
import json
import re
from urllib.parse import quote
from datetime import datetime

class GoogleIndexChecker:
    def __init__(self, website_url="https://catsoc.github.io/demo_website/"):
        self.website_url = website_url
        self.domain = website_url.replace("https://", "").replace("http://", "").rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        
    def check_website_status(self):
        """檢查網站基本狀態"""
        print("🔍 檢查網站狀態...")
        try:
            response = self.session.get(self.website_url, timeout=10)
            if response.status_code == 200:
                print(f"✅ 網站正常訪問 (狀態碼: {response.status_code})")
                
                # 提取標題
                title_match = re.search(r'<title>(.*?)</title>', response.text, re.IGNORECASE)
                if title_match:
                    print(f"📄 頁面標題: {title_match.group(1)}")
                return True
            else:
                print(f"⚠️ 網站狀態異常: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 網站無法訪問: {e}")
            return False
    
    def check_seo_files(self):
        """檢查 SEO 相關檔案"""
        print("\n🔧 檢查 SEO 檔案...")
        
        # 檢查 sitemap
        try:
            sitemap_url = f"{self.website_url}/sitemap.xml"
            response = self.session.get(sitemap_url, timeout=5)
            if response.status_code == 200:
                print("✅ Sitemap.xml 可訪問")
            else:
                print("❌ Sitemap.xml 無法訪問")
        except:
            print("❌ Sitemap.xml 無法訪問")
        
        # 檢查 robots.txt
        try:
            robots_url = f"{self.website_url}/robots.txt"
            response = self.session.get(robots_url, timeout=5)
            if response.status_code == 200:
                print("✅ Robots.txt 可訪問")
            else:
                print("❌ Robots.txt 無法訪問")
        except:
            print("❌ Robots.txt 無法訪問")
    
    def check_google_index(self):
        """檢查 Google 收錄狀態"""
        print("\n🔍 檢查 Google 收錄狀態...")
        
        search_query = f"site:{self.domain}"
        google_url = f"https://www.google.com/search?q={quote(search_query)}&num=10"
        
        print(f"搜尋查詢: {search_query}")
        
        try:
            # 添加隨機延遲避免被封
            time.sleep(2)
            
            response = self.session.get(google_url, timeout=15)
            
            if response.status_code != 200:
                print(f"⚠️ Google 查詢回應異常: {response.status_code}")
                return None
            
            content = response.text.lower()
            
            # 檢查是否找到結果
            if any(pattern in content for pattern in [
                self.domain.lower(),
                "demo_website",
                self.website_url.lower()
            ]):
                print("🎉 已被 Google 收錄！")
                print("✨ 在搜尋結果中找到你的網站")
                return True
            
            elif any(pattern in content for pattern in [
                "找不到",
                "沒有找到", 
                "no results found",
                "did not match any documents",
                "your search did not match"
            ]):
                print("❌ 尚未被 Google 收錄")
                return False
            
            else:
                print("🤔 收錄狀態不明確")
                return None
                
        except requests.RequestException as e:
            print(f"⚠️ Google 查詢失敗: {e}")
            return None
    
    def check_alternative_engines(self):
        """檢查其他搜尋引擎"""
        print("\n🔄 檢查其他搜尋引擎...")
        
        engines = {
            "Bing": f"https://www.bing.com/search?q=site%3A{self.domain}",
            "DuckDuckGo": f"https://duckduckgo.com/?q=site%3A{self.domain}"
        }
        
        for engine, url in engines.items():
            try:
                response = self.session.get(url, timeout=10)
                if self.domain in response.text.lower():
                    print(f"✅ 在 {engine} 找到結果")
                else:
                    print(f"❌ 在 {engine} 未找到結果")
            except:
                print(f"⚠️ 無法查詢 {engine}")
    
    def generate_action_plan(self, is_indexed):
        """生成行動計劃"""
        print(f"\n📋 行動建議:")
        
        if is_indexed:
            print("🎯 恭喜！網站已被收錄，SEO 設定成功")
            print("💡 可以考慮:")
            print("   • 監控搜尋排名變化")
            print("   • 優化關鍵字策略")  
            print("   • 增加更多優質內容")
        
        elif is_indexed == False:
            print("🔧 網站尚未收錄，建議立即行動:")
            print("   1. 【高優先級】前往 Google Search Console")
            print("      https://search.google.com/search-console/")
            print("   2. 【高優先級】驗證網站所有權")
            print("   3. 【高優先級】提交 Sitemap:")
            print(f"      {self.website_url}/sitemap.xml")
            print("   4. 【中優先級】手動請求索引首頁")
            print("   5. 【中優先級】在社群媒體分享網站連結")
            print("   6. 【低優先級】等待 1-2 週後再次檢查")
        
        else:
            print("🤔 收錄狀態不明確，可能原因:")
            print("   • 網站剛上線，Google 正在處理中")
            print("   • 需要更多外部連結幫助發現")
            print("   • 網路環境限制了檢測準確性")
            print("   • 建議一週後重新執行檢測")
    
    def save_report(self, results):
        """保存檢測報告"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report = {
            "timestamp": timestamp,
            "website": self.website_url,
            "domain": self.domain,
            "results": results
        }
        
        report_file = "google_index_report.json"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print(f"\n📄 檢測報告已保存到: {report_file}")
        except Exception as e:
            print(f"⚠️ 無法保存報告: {e}")
    
    def run_full_check(self):
        """執行完整檢查"""
        print("🚀 Google 收錄自動檢測開始")
        print("=" * 50)
        
        results = {}
        
        # 1. 基本網站狀態
        results['website_accessible'] = self.check_website_status()
        if not results['website_accessible']:
            print("\n❌ 網站無法訪問，停止後續檢查")
            return
        
        # 2. SEO 檔案檢查
        self.check_seo_files()
        
        # 3. Google 收錄檢查
        results['google_indexed'] = self.check_google_index()
        
        # 4. 其他搜尋引擎檢查
        self.check_alternative_engines()
        
        # 5. 生成建議
        self.generate_action_plan(results['google_indexed'])
        
        # 6. 保存報告
        self.save_report(results)
        
        print("\n✅ 自動檢測完成！")
        return results

def main():
    checker = GoogleIndexChecker()
    checker.run_full_check()

if __name__ == "__main__":
    main()
