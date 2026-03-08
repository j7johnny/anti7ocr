# 測試與部署指南

本文件涵蓋「開發環境測試」與「部署環境 smoke 測試」。

## 1. 開發環境測試

```powershell
& .\.venv\Scripts\python.exe -m pytest -q
```

目前測試類型：
- API 測試
- CLI 測試
- 相容層測試
- 擾動測試（stroke / pixel）
- 敏感詞檢查測試（off / warn / retry）
- 整合流程測試（generate -> batch -> eval）

## 2. 部署前建包

```powershell
& .\.venv\Scripts\python.exe -m pip install build
& .\.venv\Scripts\python.exe -m build
```

輸出：
- `dist/anti7ocr-<version>.tar.gz`
- `dist/anti7ocr-<version>-py3-none-any.whl`

## 3. 部署環境 smoke 測試

```powershell
python -m venv .venv-deploy
& .\.venv-deploy\Scripts\python.exe -m pip install --force-reinstall dist/anti7ocr-0.1.0-py3-none-any.whl

& .\.venv-deploy\Scripts\anti7ocr.exe preset list
& .\.venv-deploy\Scripts\anti7ocr.exe generate --text "deploy smoke" --output outputs/deploy-smoke.png
& .\.venv-deploy\Scripts\anti7ocr.exe batch --input-file input.txt --output-dir outputs/deploy-batch
& .\.venv-deploy\Scripts\anti7ocr.exe eval --manifest outputs/deploy-batch/manifest.jsonl --backend "static:mocked_ocr" --report reports/deploy-eval.json
```

或使用腳本：

```powershell
& .\scripts\deploy_smoke.ps1
```

## 4. 上線前最低驗收清單

1. `pytest` 全綠。
2. `.venv-deploy` wheel 安裝成功。
3. CLI `generate/batch/eval` 可在 `.venv-deploy` 成功執行。
4. 至少跑一次真實 OCR backend（例如 tesseract）CER 比較。
5. 人工抽樣檢查圖片可讀性。
