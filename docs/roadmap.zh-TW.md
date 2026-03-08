# 後續版本強化方向（Roadmap）

以下是建議優先順序。

## A. 功能面

1. 更多字體與字形支援
- OTF/TTF/TTC 覆蓋分析工具強化
- 異體字與字形替代策略

2. 更進階的版面生成
- 多欄與區塊模板
- 標題/內文/註解分層排版

3. 更強的擾動策略
- 自動調參（可讀性與 CER 平衡）
- 字形局部變形與筆畫重組擾動

4. OCR 評估能力擴充
- 更多 backend adapter
- 批次報表視覺化（HTML/CSV）

## B. 工程面

1. CI/CD
- PR 自動測試
- wheel build + smoke pipeline

2. 穩定性與可觀測性
- 統一 logging 結構
- 產出 metadata schema 版本化

3. 相容性
- 支援更多 Python 版本矩陣測試
- Windows/Linux/macOS 字體行為差異測試

## C. 產品面

1. 文件深化
- 圖文教學與常見故障排除（Troubleshooting）
- 用戶情境教學：社群貼文、公告圖、批次資料產圖

2. 社群治理
- Contribution Guide
- Issue template / PR template
- Benchmark dataset 與 baseline 指標
