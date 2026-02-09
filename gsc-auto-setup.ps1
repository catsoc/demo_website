# Google Search Console 自動化提交工具
# 用途：自動生成 GSC 設定指令和驗證檔案

param(
    [string]$Domain = "catsoc.github.io/demo_website",
    [string]$SiteUrl = "https://catsoc.github.io/demo_website/"
)

Write-Host "🎯 Google Search Console 自動設定工具" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

Write-Host "`n📋 網站資訊:" -ForegroundColor Yellow
Write-Host "   網域: $Domain"
Write-Host "   網址: $SiteUrl"

Write-Host "`n🔧 自動生成設定檔案..." -ForegroundColor Yellow

# 1. 生成 HTML 驗證檔案
$verificationCode = "google" + (Get-Date -Format "yyyyMMddHHmmss")
$htmlVerification = @"
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Google Search Console Verification</title>
    <meta name="google-site-verification" content="$verificationCode" />
</head>
<body>
    <h1>Google Search Console 驗證頁面</h1>
    <p>此頁面用於 Google Search Console 驗證</p>
    <p>生成時間: $(Get-Date)</p>
</body>
</html>
"@

$verificationFile = "google-verification.html"
$htmlVerification | Out-File -FilePath $verificationFile -Encoding UTF8
Write-Host "✅ 已生成驗證檔案: $verificationFile"

# 2. 生成設定腳本
$setupScript = @"
# Google Search Console 設定步驟
# 執行日期: $(Get-Date)

Write-Host '🚀 Google Search Console 自動設定' -ForegroundColor Green
Write-Host '======================================'

# 第一步：開啟 Google Search Console
Write-Host '1. 開啟 Google Search Console...' -ForegroundColor Yellow
Start-Process 'https://search.google.com/search-console/'

# 等待用戶操作
Read-Host '按 Enter 繼續到下一步 (請先在網頁中點選"新增資源")'

# 第二步：提供驗證資訊
Write-Host '^n2. 驗證資料:' -ForegroundColor Yellow
Write-Host '   網站網址: $SiteUrl' -ForegroundColor Cyan
Write-Host '   驗證檔案: $verificationFile' -ForegroundColor Cyan
Write-Host '   Sitemap: ${SiteUrl}sitemap.xml' -ForegroundColor Cyan

# 第三步：顯示後續步驟
Write-Host '^n3. 設定完成後的步驟:' -ForegroundColor Yellow
Write-Host '   ✅ 提交 Sitemap: ${SiteUrl}sitemap.xml'
Write-Host '   ✅ 請求索引首頁: $SiteUrl'
Write-Host '   ✅ 設定搜尋分析'

Write-Host '^n✅ 設定助手完成！' -ForegroundColor Green
"@

$scriptFile = "gsc-setup.ps1"
$setupScript | Out-File -FilePath $scriptFile -Encoding UTF8
Write-Host "✅ 已生成設定腳本: $scriptFile"

# 3. 生成快速連結檔案
$quickLinks = @"
# Google Search Console 快速連結
# 生成時間: $(Get-Date)

## 主要連結
- [Google Search Console 主頁](https://search.google.com/search-console/)
- [新增資源](https://search.google.com/search-console/welcome)
- [網域驗證說明](https://support.google.com/webmasters/answer/9008080)

## 你的網站資訊
- **網站網址**: $SiteUrl
- **Sitemap 位置**: ${SiteUrl}sitemap.xml
- **Robots.txt**: ${SiteUrl}robots.txt

## 設定檢查清單
- [ ] 在 GSC 中新增資源
- [ ] 完成網域驗證
- [ ] 提交 Sitemap
- [ ] 請求索引首頁
- [ ] 設定搜尋效能監控

## 驗證方法選項
1. **HTML 檔案** (推薦)：上傳驗證檔案到網站根目錄
2. **HTML 標籤**：在 <head> 中添加 meta 標籤
3. **DNS 記錄**：在 DNS 設定中添加 TXT 記錄
4. **Google Analytics**：如果已安裝 GA
5. **Google Tag Manager**：如果已安裝 GTM

## 完成驗證後
1. 提交 Sitemap: ${SiteUrl}sitemap.xml
2. 手動請求索引重要頁面
3. 監控搜尋效能和覆蓋率
4. 設定效能警示

---
**注意**：驗證檔案已自動生成，請上傳到網站根目錄後再進行驗證。
"@

$linksFile = "gsc-quicklinks.md"
$quickLinks | Out-File -FilePath $linksFile -Encoding UTF8
Write-Host "✅ 已生成快速連結: $linksFile"

Write-Host "`n🎯 下一步行動:" -ForegroundColor Cyan
Write-Host "1. 上傳 $verificationFile 到你的網站根目錄"
Write-Host "2. 執行 .\$scriptFile 開始設定流程"
Write-Host "3. 參考 $linksFile 查看詳細步驟"

Write-Host "`n⚡ 快速啟動設定:" -ForegroundColor Green
Write-Host "   .\$scriptFile"

Write-Host "`n✅ 自動化設定工具完成！" -ForegroundColor Green
