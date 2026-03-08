# 快速開始（正體中文）

本教學示範從 0 到可用，包含單張生成、批次生成與 OCR 評估。

## 1. 建立隔離環境

```powershell
python -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -e .[dev]
```

如需 OCR backend（tesseract/cnocr）：

```powershell
& .\.venv\Scripts\python.exe -m pip install -e .[eval]
```

## 2. 第一張 Anti-OCR 圖片

```powershell
& .\.venv\Scripts\anti7ocr.exe generate `
  --text "這是一段正體中文測試文本" `
  --preset tw_readable `
  --seed 7 `
  --output outputs/hello.png `
  --format PNG
```

## 3. 批次生成

準備 `input.txt`（每行一筆）：

```txt
第一段文字
第二段文字
第三段文字
```

執行：

```powershell
& .\.venv\Scripts\anti7ocr.exe batch `
  --input-file input.txt `
  --preset tw_balanced `
  --base-seed 100 `
  --seed-strategy incremental `
  --output-dir outputs/batch `
  --format PNG
```

輸出：
- `outputs/batch/sample_0000.png ...`
- `outputs/batch/manifest.jsonl`

## 4. OCR 評估（CER）

```powershell
& .\.venv\Scripts\anti7ocr.exe eval `
  --manifest outputs/batch/manifest.jsonl `
  --backend tesseract `
  --report reports/eval.json
```

若本機尚未安裝 tesseract，可先用測試 backend：

```powershell
& .\.venv\Scripts\anti7ocr.exe eval `
  --manifest outputs/batch/manifest.jsonl `
  --backend "static:mocked_ocr" `
  --report reports/eval-static.json
```

## 5. 敏感詞檢查（可開關）

啟用檢查（warn 模式）：

```powershell
& .\.venv\Scripts\anti7ocr.exe generate `
  --text "測試文本" `
  --output outputs/sensitive-warn.png `
  --sensitive-check `
  --sensitive-keyword "機密詞" `
  --sensitive-backend "tesseract" `
  --sensitive-mode warn
```

啟用檢查（retry 模式）：

```powershell
& .\.venv\Scripts\anti7ocr.exe generate `
  --text "測試文本" `
  --output outputs/sensitive-retry.png `
  --sensitive-check `
  --sensitive-keyword "機密詞" `
  --sensitive-backend "tesseract" `
  --sensitive-mode retry `
  --sensitive-max-attempts 3
```

關閉檢查：

```powershell
& .\.venv\Scripts\anti7ocr.exe generate `
  --text "測試文本" `
  --output outputs/no-sensitive.png `
  --no-sensitive-check
```
