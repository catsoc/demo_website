# Google 收錄檢查工具
# 自動化檢查，不需要用戶手動操作

Write-Host "🔍 自動檢查 Google 收錄狀態" -ForegroundColor Cyan
Write-Host "==============================" -ForegroundColor Cyan

$site = "catsoc.github.io/demo_website/"
Write-Host "檢查網站: $site" -ForegroundColor Yellow

# 1. 基本連線測試
try {
    $testUrl = "https://$site"
    $basicTest = Invoke-WebRequest -Uri $testUrl -UseBasicParsing -TimeoutSec 10
    Write-Host "✅ 網站可正常訪問 (狀態: $($basicTest.StatusCode))" -ForegroundColor Green
    
    # 檢查標題
    if ($basicTest.Content -match '<title>(.*?)</title>') {
        Write-Host "📄 頁面標題: $($Matches[1])" -ForegroundColor Cyan
    }
} catch {
    Write-Host "❌ 網站訪問失敗: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# 2. Google 收錄檢查 - 方法1: 直接查詢
Write-Host "`n🔍 檢查 Google 收錄..." -ForegroundColor Yellow

$searchUrl = "https://www.google.com/search?q=site%3A$site"
$headers = @{
    'User-Agent' = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    'Accept' = 'text/html,application/xhtml+xml'
    'Accept-Language' = 'zh-TW,zh;q=0.9'
}

try {
    $searchResult = Invoke-WebRequest -Uri $searchUrl -Headers $headers -UseBasicParsing -TimeoutSec 20
    $html = $searchResult.Content
    
    # 分析結果
    if ($html -match $site.Replace("/", "\/") -or $html -match "demo_website") {
        Write-Host "🎉 已被 Google 收錄！" -ForegroundColor Green
        Write-Host "找到網站相關結果" -ForegroundColor Green
        $isIndexed = $true
    } elseif ($html -match "找不到" -or $html -match "沒有找到" -or $html -match "No results") {
        Write-Host "❌ 尚未被 Google 收錄" -ForegroundColor Red
        $isIndexed = $false
    } else {
        Write-Host "🤔 收錄狀態不明確" -ForegroundColor Yellow
        Write-Host "可能原因: Google 正在處理或需要更多時間" -ForegroundColor Yellow
        $isIndexed = $null
    }
} catch {
    Write-Host "⚠️ Google 查詢失敗: $($_.Exception.Message)" -ForegroundColor Yellow
    $isIndexed = $null
}

# 3. 替代檢查方法
Write-Host "`n🔄 嘗試替代檢查方法..." -ForegroundColor Yellow

# 檢查 sitemap 和 robots
$sitemapUrl = "https://$site/sitemap.xml"
$robotsUrl = "https://$site/robots.txt"

try {
    $sitemapTest = Invoke-WebRequest -Uri $sitemapUrl -UseBasicParsing -TimeoutSec 5
    Write-Host "✅ Sitemap 可訪問" -ForegroundColor Green
} catch {
    Write-Host "❌ Sitemap 無法訪問" -ForegroundColor Red
}

try {
    $robotsTest = Invoke-WebRequest -Uri $robotsUrl -UseBasicParsing -TimeoutSec 5
    Write-Host "✅ Robots.txt 可訪問" -ForegroundColor Green
} catch {
    Write-Host "❌ Robots.txt 無法訪問" -ForegroundColor Red
}

# 4. 結論和建議
Write-Host "`n📋 檢查結論:" -ForegroundColor Cyan
if ($isIndexed -eq $true) {
    Write-Host "🎯 網站已被 Google 收錄，SEO 設定成功！" -ForegroundColor Green
} elseif ($isIndexed -eq $false) {
    Write-Host "🔧 網站尚未被收錄，建議採取以下行動:" -ForegroundColor Yellow
    Write-Host "   1. 前往 Google Search Console 提交網站" -ForegroundColor White
    Write-Host "   2. 提交 sitemap.xml: $sitemapUrl" -ForegroundColor White
    Write-Host "   3. 手動請求索引首頁" -ForegroundColor White
    Write-Host "   4. 在社群媒體分享網站連結增加曝光" -ForegroundColor White
    Write-Host "   5. 等待 1-2 週讓 Google 爬蟲處理" -ForegroundColor White
} else {
    Write-Host "❓ 無法確定收錄狀態，可能的原因:" -ForegroundColor Yellow
    Write-Host "   • 網站太新，Google 還在處理中" -ForegroundColor White
    Write-Host "   • 網路環境限制了檢查" -ForegroundColor White
    Write-Host "   • 需要更多外部連結幫助發現" -ForegroundColor White
}

Write-Host "`n✅ 自動檢查完成！" -ForegroundColor Green
