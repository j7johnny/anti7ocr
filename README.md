# anti7ocr

`anti7ocr` is a next-generation Anti-OCR image generation toolkit focused on Traditional Chinese text.

## Highlights

- AntiOCR-compatible core behavior:
  - text-to-image generation
  - per-character randomized font size
  - randomized reverse rotation for Chinese glyphs
  - optional char-to-pinyin conversion
  - noisy background support
  - custom font file selection
- Stage-based modular pipeline:
  - `layout -> render -> fragment -> perturb -> export -> evaluate`
- Advanced perturbations:
  - stroke fragmentation
  - closed-structure partial break (for glyphs like `口日目田國`)
  - edge jitter / edge brightness noise
  - local contrast noise
  - adversarial watermark
  - supersample rendering + downsample
- Reproducible config:
  - YAML config
  - built-in presets
  - deterministic seed
  - precedence: `CLI overrides > YAML > preset > default`
- Full interfaces:
  - Python API (`generate`, `generate_batch`, `evaluate`)
  - compatibility API (`AntiOcr`, `AntiOcrCompat`)
  - CLI (`generate`, `batch`, `eval`, `preset`, `font-check`)

## Environment isolation

All commands below use project-local virtual environment (`.venv`):

```powershell
python -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -e .[dev]
```

Optional OCR backend dependencies:

```powershell
& .\.venv\Scripts\python.exe -m pip install -e .[eval]
```

## Python usage

```python
from anti7ocr import generate, generate_batch, AntiOcr

result = generate(
    "拒絕圖片文字被 OCR，讓文字自由傳播。",
    preset="tw_readable",
    seed=20260308,
    output_options={"path": "outputs/single.png", "format": "PNG"},
)

batch = generate_batch(
    "input.txt",  # one sample per line
    output_dir="outputs/batch",
    preset="tw_aggressive",
    base_seed=1000,
)

compat = AntiOcr()
img = compat(
    "這是 antiOCR 相容 API。",
    font_fp="C:/Windows/Fonts/msjh.ttc",
    char_reverse_ratio=0.2,
)
```

## CLI usage

```powershell
& .\.venv\Scripts\anti7ocr.exe preset list
& .\.venv\Scripts\anti7ocr.exe preset show tw_readable

& .\.venv\Scripts\anti7ocr.exe generate `
  --text "這是一段測試文字" `
  --preset tw_readable `
  --seed 7 `
  --output outputs/demo.png `
  --format PNG

& .\.venv\Scripts\anti7ocr.exe batch `
  --input-file input.txt `
  --preset tw_aggressive `
  --base-seed 100 `
  --seed-strategy incremental `
  --output-dir outputs/batch `
  --format PNG

& .\.venv\Scripts\anti7ocr.exe eval `
  --manifest outputs/batch/manifest.jsonl `
  --backend tesseract `
  --report reports/eval.json

& .\.venv\Scripts\anti7ocr.exe font-check `
  --text "口日目田國測試ABC123" `
  --font-path "C:/Windows/Fonts/msjh.ttc"
```

## Running tests

```powershell
& .\.venv\Scripts\python.exe -m pytest -q
```
