param(
    [string]$WheelPath = "dist/anti7ocr-0.1.0-py3-none-any.whl"
)

$ErrorActionPreference = "Stop"

if (-not (Test-Path $WheelPath)) {
    Write-Error "Wheel not found: $WheelPath"
}

if (-not (Test-Path ".venv-deploy")) {
    python -m venv .venv-deploy
}

& .\.venv-deploy\Scripts\python.exe -m pip install --force-reinstall $WheelPath
& .\.venv-deploy\Scripts\anti7ocr.exe preset list

if (-not (Test-Path "outputs")) {
    New-Item -Type Directory outputs | Out-Null
}

Set-Content -Encoding utf8 outputs\deploy-input.txt "line1`nsecond line"

& .\.venv-deploy\Scripts\anti7ocr.exe generate `
  --text "deployment smoke" `
  --output outputs\deploy-smoke.png `
  --sensitive-check `
  --sensitive-keyword smoke `
  --sensitive-backend "static:smoke"

& .\.venv-deploy\Scripts\anti7ocr.exe batch `
  --input-file outputs\deploy-input.txt `
  --output-dir outputs\deploy-batch `
  --sensitive-check `
  --sensitive-keyword blocked `
  --sensitive-backend "static:none"

& .\.venv-deploy\Scripts\anti7ocr.exe eval `
  --manifest outputs\deploy-batch\manifest.jsonl `
  --backend "static:mocked_ocr" `
  --report reports\deploy-eval.json

Write-Host "Deploy smoke completed."
