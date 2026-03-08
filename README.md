# anti7ocr

`anti7ocr` 是一個以正體中文場景為優先的「下一代 Anti-OCR 文字圖片生成套件」。

專案目標是：
- 讓人類閱讀體驗盡量維持自然。
- 同時顯著提高 OCR 辨識難度。
- 保留原始 `antiOCR` 核心能力，並提供更可重現、可評估、可擴充的架構。

## 文件中心（正體中文）

- 文件入口：[docs/README.zh-TW.md](docs/README.zh-TW.md)
- 快速開始：[docs/quickstart.zh-TW.md](docs/quickstart.zh-TW.md)
- 預設參數指南：[docs/preset-guide.zh-TW.md](docs/preset-guide.zh-TW.md)
- 測試與部署：[docs/testing-and-deploy.zh-TW.md](docs/testing-and-deploy.zh-TW.md)
- 後續強化方向：[docs/roadmap.zh-TW.md](docs/roadmap.zh-TW.md)

## Features

### 1) 與 antiOCR 功能相容的核心能力
- 文字轉圖片
- 字元隨機字體大小
- 中文字隨機倒轉/旋轉
- 部分字元轉拼音
- 干擾背景
- 自行指定字體

### 2) 模組化 Pipeline
- `layout -> render -> fragment -> perturb -> export -> evaluate`
- 每個 stage 可獨立配置與測試。

### 3) 進階擾動
- 筆畫層級：
  - `stroke fragmentation`
  - 封閉結構字（如 `口日目田國`）局部破壞
- 像素層級：
  - `edge jitter`
  - `edge brightness noise`
  - `local contrast noise`
  - `adversarial watermark`
- 渲染層級：
  - supersample rendering 後 downsample
- 排版微擾：
  - `micro kerning jitter`
  - `baseline jitter`
  - `character scale jitter`

### 4) 可重現性與配置
- YAML config
- 內建 preset（`tw_readable` / `tw_balanced` / `tw_aggressive` / `tw_hardened`）
- seed 控制可重現
- 覆寫優先序：`CLI > YAML > preset > default`

### 5) OCR 評估
- backend abstraction
- 內建 backend：
  - `tesseract`
  - `cnocr`
  - `static:<text>`（測試/CI 用）
  - `noop`
- 支援 CER 計算與每 backend 報告輸出

### 6) 敏感詞檢查（可開關）
- 預設關閉：`sensitive_check.enable = false`
- 可設定關鍵詞、OCR backend、比對模式
- 支援兩種行為：
  - `warn`：偵測到只標記，不重生
  - `retry`：偵測到則重生，直到 `max_attempts`

## 安裝與隔離開發

### 開發環境（不污染全域）

```powershell
python -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -e .[dev]
```

可選 OCR 依賴：

```powershell
& .\.venv\Scripts\python.exe -m pip install -e .[eval]
```

## Python API 快速開始

```python
from anti7ocr import AntiOcr, generate, generate_batch, evaluate

# 單張生成
single = generate(
    "拒絕圖片文字被 OCR，讓文字自由傳播。",
    preset="tw_readable",
    seed=20260308,
    output_options={"path": "outputs/single.png", "format": "PNG"},
)

# 批次生成
batch = generate_batch(
    "input.txt",  # 每行一筆文字
    output_dir="outputs/batch",
    preset="tw_aggressive",
    base_seed=1000,
    seed_strategy="incremental",
)

# antiOCR 相容介面
compat = AntiOcr()
img = compat(
    "這是 antiOCR 相容 API。",
    font_fp="C:/Windows/Fonts/msjh.ttc",
    char_reverse_ratio=0.2,
    seed=7,
)

# OCR 評估
images = [item.output_path for item in batch.items if item.output_path]
labels = [item.text for item in batch.items]
report = evaluate(images, labels, backends=["tesseract"])
print(report.avg_cer)
```

## CLI 指令

### 1) Preset

```powershell
& .\.venv\Scripts\anti7ocr.exe preset list
& .\.venv\Scripts\anti7ocr.exe preset show tw_readable
```

### 2) 單張生成

```powershell
& .\.venv\Scripts\anti7ocr.exe generate `
  --text "這是一段測試文字" `
  --preset tw_readable `
  --seed 7 `
  --output outputs/demo.png `
  --format PNG
```

### 3) 批次生成

```powershell
& .\.venv\Scripts\anti7ocr.exe batch `
  --input-file input.txt `
  --preset tw_aggressive `
  --base-seed 100 `
  --seed-strategy incremental `
  --output-dir outputs/batch `
  --format PNG
```

### 4) 評估

```powershell
& .\.venv\Scripts\anti7ocr.exe eval `
  --manifest outputs/batch/manifest.jsonl `
  --backend tesseract `
  --report reports/eval.json
```

### 5) 字體覆蓋檢查

```powershell
& .\.venv\Scripts\anti7ocr.exe font-check `
  --text "口日目田國測試ABC123" `
  --font-path "C:/Windows/Fonts/msjh.ttc"
```

### 6) 敏感詞檢查（可開關）

```powershell
& .\.venv\Scripts\anti7ocr.exe generate `
  --text "測試文本" `
  --output outputs/sensitive.png `
  --sensitive-check `
  --sensitive-keyword "機密詞" `
  --sensitive-backend "tesseract" `
  --sensitive-mode retry `
  --sensitive-max-attempts 3
```

關閉敏感詞檢查：

```powershell
& .\.venv\Scripts\anti7ocr.exe generate `
  --text "測試文本" `
  --output outputs/no_sensitive.png `
  --no-sensitive-check
```

## 配置範例（重點欄位）

`configs/tw_readable.yaml`、`configs/tw_balanced.yaml`、`configs/tw_aggressive.yaml`、`configs/tw_hardened.yaml` 已提供完整範本。

敏感詞檢查區塊：

```yaml
sensitive_check:
  enable: false
  backend: tesseract
  keywords: []
  case_sensitive: true
  mode: warn      # warn | retry
  max_attempts: 1
```

## 測試

```powershell
& .\.venv\Scripts\python.exe -m pytest -q
```

測試涵蓋：
- unit tests（stage 契約、config precedence、seed 重現）
- compatibility tests（`AntiOcr` 相容層）
- perturbation tests（stroke / pixel / watermark）
- integration workflow（generate -> batch -> eval）
- sensitive-check tests（off / warn / retry）
- CLI tests

## 本機部署（deployment smoke）

建議使用獨立部署環境檢驗 wheel 安裝：

```powershell
& .\.venv\Scripts\python.exe -m pip install build
& .\.venv\Scripts\python.exe -m build

python -m venv .venv-deploy
& .\.venv-deploy\Scripts\python.exe -m pip install dist/anti7ocr-0.1.0-py3-none-any.whl
& .\.venv-deploy\Scripts\anti7ocr.exe preset list
```

也可直接執行一鍵 smoke：

```powershell
& .\scripts\deploy_smoke.ps1
```

## Acknowledgements

本專案在設計與功能方向上大量參考並受益於以下專案與社群，特別感謝：

1. [breezedeus/antiOCR](https://github.com/breezedeus/antiOCR)  
   本專案的核心理念、基本 anti-OCR 方向與相容能力主要承襲自 antiOCR。  
   尤其感謝其開源分享「人可讀但機器難辨」這條清楚而實用的路線。
2. [breezedeus/CnOCR](https://github.com/breezedeus/cnocr)  
   提供中文 OCR 生態的重要基礎，並啟發本專案的 evaluator 抽象設計。
3. [Pillow (PIL Fork)](https://github.com/python-pillow/Pillow)  
   文字渲染與影像處理基礎。
4. [pypinyin](https://github.com/mozillazg/python-pinyin)  
   中文轉拼音能力。
5. [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)  
   作為本專案本地 OCR backend 支援之一。
6. 所有開源維護者與使用者社群  
   你們的回饋、issue、討論與實測資料，都是本專案持續改進的關鍵。

## License

MIT
