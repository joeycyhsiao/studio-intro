# 引鹿創新 studio deck — Python 靜態產生器

內容驅動的單頁 deck。所有文字與圖片都放在 `content/`，由 Jinja2 模板組出 `dist/index.html`。

## 快速開始

```bash
pip install -r requirements.txt        # Jinja2 / PyYAML / Markdown
pip install -r requirements-dev.txt    # 選用：--watch / --serve 需要

python build.py                        # 產出 dist/
python build.py --serve                # 產出並在 http://localhost:8899 預覽
python build.py --serve --watch        # 邊改邊看（存檔自動重建）
```

部署：`python build.py` 後把 `dist/` 整個上傳到任何靜態空間即可（`dist/` 已被 git 忽略）。

## 內容在哪裡改

| 想改什麼 | 改這裡 |
|---|---|
| 品牌色／導覽標籤／section 順序／CTA/meta | `content/site.yaml` |
| 各段文字（hero、CLUES、合作方式、關於…） | `content/sections/*.yaml` |
| 現場側錄照片 | 把圖丟進 `content/collections/gallery/`，說明寫在 `_captions.yaml`（可留空） |
| 公開受訪 | `content/collections/interviews/`（每則一個 `.md`，frontmatter 放 `kind/title/link`） |
| 深度文章 | `content/collections/articles/`（每則一個 `.md`，frontmatter 放 `title/tag/link`） |
| 客戶推薦語 | `content/collections/testimonials/`（每則一個 `.md`，frontmatter 放 `attribution/context`，本文＝引文） |
| 版面／樣式 | `templates/`（各段 partial）與 `static/styles.css` |
| 互動（scroll-spy／浮動 CTA／推薦輪播） | `static/main.js` |

新增清單項目＝在對應資料夾多放一個檔，重建即出現；不用碰程式碼。
