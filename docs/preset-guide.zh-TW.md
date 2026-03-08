# 預設參數建議（Preset Guide）

`anti7ocr` 目前提供四種繁中導向 preset：

1. `tw_readable`：可讀性優先
2. `tw_balanced`：平衡型（建議預設）
3. `tw_aggressive`：攻擊強度較高
4. `tw_hardened`：高強度模式（建議先做人工可讀性驗證）

## 選型建議

### tw_readable
- 適用：一般公告圖、教學圖、需要保留高閱讀舒適度
- 特性：擾動較溫和，OCR 抵抗中等

### tw_balanced
- 適用：大多數正式上線場景
- 特性：可讀性與 OCR 抵抗平衡

### tw_aggressive
- 適用：對 OCR 抵抗要求較高，允許些微可讀性下降
- 特性：fragment + pixel 擾動強度提高

### tw_hardened
- 適用：高風險文本、需強防 OCR 場景
- 特性：更高微擾與 watermark 強度
- 注意：建議先做人工抽樣可讀性測試

## 建議流程

1. 先從 `tw_balanced` 起跑。
2. 用 `eval` 比較 CER（至少 2 個 backend）。
3. 若 CER 不夠高，再逐步上調到 `tw_aggressive` 或 `tw_hardened`。
4. 每次調整後抽樣做人眼可讀性驗證。

## 常見客製參數

- 可讀性不佳時：
  - 降低 `fragment.stroke_fragmentation_prob`
  - 降低 `perturb.edge_jitter_strength`
  - 降低 `perturb.watermark_opacity`
- OCR 還是太容易辨識時：
  - 提高 `fragment.closed_structure_break_prob`
  - 提高 `perturb.local_contrast_noise`
  - 將 `sensitive_check.mode` 設為 `retry`
