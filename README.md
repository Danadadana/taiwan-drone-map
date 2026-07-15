# 全台無人機產業地圖 Taiwan Drone Industry Map

互動網站：台灣無人機產業 315 家公司分布地圖、產業鏈全景、官方政策時間軸。
發佈於 Claude Artifact：https://claude.ai/code/artifact/d82d258f-e966-4b6a-a5ae-6375a42f950c

## 檔案結構

- `site_template.html` — 網站模板（含 CSS/JS，資料槽 `/*__DATA__*/` `/*__GEO__*/` `/*__LOGOS__*/` `/*__POLICY__*/`）
- `build_site.py` — 組裝腳本：讀取下列資料檔，產出 `drone_map.html`
- `companies_merged.json` — 公司資料庫（315 家）
- `policy_timeline.json` — 重要政策時間軸資料（每週更新的目標檔）
- `geocode_cache.json` — 地址→座標快取
- `logo_pack.json` — 公司 logo base64 圖包
- `tw_county_simplified.geojson` — 台灣縣市底圖
- `excluded_review.json` — 曾剔除公司與原因記錄
- `drone_map.html` — 組裝產出（發佈用）

## 建置

```
python3 build_site.py   # 在 repo 根目錄執行，產出 drone_map.html
```

## policy_timeline.json 綱要

```json
{
  "updated": "YYYY-MM-DD",
  "industry": [ {"d":"YYYY-MM-DD","org":"部會名","t":"標題","s":"摘要(第三人稱,保留數字,≤2句)","u":"官方原始連結"} ],
  "defense":  [ 同上 ]
}
```

事件按日期由舊到新排列（前端會反轉為最新在上）。`d` 可為 `"進行中"`（置於陣列最後，會以銅色標記）。

## 時間軸收錄規則

- 兩軸：`defense`＝國防軍購（特別條例、特別預算、立法進度、軍購政策）；`industry`＝產業嘉惠措施（統籌型計畫、補助、資安檢測、認證、拓銷、高層宣示）。
- **僅收官方一手來源**：president.gov.tw、ey.gov.tw、ly.gov.tw / ppg.ly.gov.tw、mnd.gov.tw / mna.mnd.gov.tw、moea.gov.tw、moda.gov.tw、ait.org.tw。**不收任何媒體報導**。
- 每筆必附原始文件 URL；日期以官方文件為準；摘要第三人稱、保留關鍵數字、不加評論。
- 去重：以 URL 與事件標題比對既有條目。
