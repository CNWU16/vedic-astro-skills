# Vedic Skills 四端同步脚本
# 源头: antigravity/skills/ → 同步到 claude-code + codex + gemini运行时 + git push

param(
    [string]$CommitMsg = "sync: update skills"
)

$repo = "d:\0417jhora\vedic-astrology-skills"
$src = "$repo\antigravity\skills"
$cc = "$repo\claude-code\skills"
$codex = "$repo\codex\skills"
$gemini = "C:\Users\14361\.gemini\config\skills"

# 要同步的skill列表
$skills = @("vedic-reader", "vedic-calculator", "vedic-core", "vedic-career", "vedic-love", "vedic-rectifier")

Write-Host "=== Vedic Skills 四端同步 ===" -ForegroundColor Cyan

# 1. 同步到 claude-code
Write-Host "`n[1/4] 同步到 claude-code..." -ForegroundColor Yellow
foreach ($skill in $skills) {
    if (Test-Path "$src\$skill") {
        if (Test-Path "$cc\$skill") { Remove-Item "$cc\$skill" -Recurse -Force }
        Copy-Item "$src\$skill" "$cc\$skill" -Recurse -Force
        Write-Host "  ✓ $skill" -ForegroundColor Green
    }
}

# 2. 同步到 codex
Write-Host "`n[2/4] 同步到 codex..." -ForegroundColor Yellow
foreach ($skill in $skills) {
    if (Test-Path "$src\$skill") {
        if (Test-Path "$codex\$skill") { Remove-Item "$codex\$skill" -Recurse -Force }
        Copy-Item "$src\$skill" "$codex\$skill" -Recurse -Force
        # codex 需要 agents/openai.yaml，保留已有的
        $agentFile = "$codex\$skill\agents\openai.yaml"
        if (-not (Test-Path $agentFile)) {
            New-Item (Split-Path $agentFile) -ItemType Directory -Force | Out-Null
            Set-Content $agentFile "model: o3" -Encoding utf8
        }
        Write-Host "  ✓ $skill" -ForegroundColor Green
    }
}

# 3. 同步到 Gemini 运行时（跳过 venv）
Write-Host "`n[3/4] 同步到 Gemini 运行时..." -ForegroundColor Yellow
foreach ($skill in $skills) {
    if (Test-Path "$src\$skill") {
        # 保留 venv 目录（不删不覆盖）
        Get-ChildItem "$src\$skill" -Recurse -File | Where-Object {
            $_.FullName -notmatch '\\venv\\' -and $_.FullName -notmatch '\\__pycache__\\'
        } | ForEach-Object {
            $rel = $_.FullName.Substring("$src\$skill".Length)
            $target = "$gemini\$skill$rel"
            $targetDir = Split-Path $target
            if (-not (Test-Path $targetDir)) { New-Item $targetDir -ItemType Directory -Force | Out-Null }
            Copy-Item $_.FullName $target -Force
        }
        Write-Host "  ✓ $skill" -ForegroundColor Green
    }
}

# 4. Git commit + push
Write-Host "`n[4/4] Git commit + push..." -ForegroundColor Yellow
Set-Location $repo
git add -A
git commit -m $CommitMsg
git push

Write-Host "`n=== 同步完成 ===" -ForegroundColor Cyan
