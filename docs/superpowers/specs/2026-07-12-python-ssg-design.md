# 設計：把 studio-intro deck 改寫成 Python 靜態產生器（內容驅動）

日期：2026-07-12
狀態：待審

## 目標

把目前由 Claude Design（x-dc runtime + `support.js`）驅動的單頁 deck，改寫成 **Python 靜態產生器（SSG）**：所有文字與圖片抽成 `content/` 底下的 YAML / Markdown / 圖片資料夾，由 Jinja2 模板組出 `dist/index.html`。

核心使用情境：**使用者把圖片或內容檔丟進資料夾 → 跑 `build.py` →（可選 `--watch`）→ 網站自動反映**，不需碰程式碼與模板。

**視覺完全沿用目前這版（commit `55025da`：CLUES 方法、「您」語氣、媒體曝光獨立段、預約 30 分鐘諮詢 CTA）。這是「同一個外觀改成資料驅動」，不是重新設計。**

## 決定（來自 brainstorming）

- 架構：**靜態產生器**（跑 build 產出純 HTML），不是常駐伺服器。
- 範圍：**全部內容資料化**（每段文字與圖片都從資料檔來）。
- 格式：**YAML（結構化欄位）＋ Markdown（長文）**。
- **Claude Design 退出產線**：之後視覺改動在模板＋CSS 進行；Claude Design 頂多當視覺草稿，其 x-dc 輸出不再併回。
- 開發模式：提供 `--watch`（存檔自動重建）與 `--serve`（本機預覽）。
- `dist/`：**git 忽略**，部署時再 build。

## 技術選型

- Python 3。
- 核心相依（`requirements.txt`）：`Jinja2`、`PyYAML`、`markdown`。
- 開發相依（`requirements-dev.txt`，可選）：`watchdog`（--watch）、`livereload`（--serve 自動刷新）。若不想裝，`--serve` 退化成 `http.server` + 手動重整。
- 無資料庫、無後台管理 UI、無框架。

## 資料夾結構

```
studio-intro/
  content/
    site.yaml                  # 品牌色/字型/meta/導覽/CTA/section 順序
    sections/
      hero.yaml
      situation.yaml           # 您面對的處境（痛點）
      method.yaml              # 我怎麼做（CLUES）
      services.yaml            # 合作方式（A/B 兩組卡）
      work.yaml                # 我做過的（數據 + 代表專案）
      about.yaml               # 關於蕭喬尹（自介 + 經歷/學歷/講座）
      media.yaml               # 媒體曝光（深度文章 + 公開受訪 子群設定）
      contact.yaml             # 聯絡
    collections/
      gallery/                 # 現場側錄：圖直接丟進來
        workshop-01.jpg
        _captions.yaml         # 檔名 → 說明（選填；沒寫也正常）
      interviews/              # 公開受訪：每則一個 .md（frontmatter）
      articles/                # 深度文章：每則一個 .md（frontmatter，連外）
      testimonials/            # 推薦語：每則一個 .md（frontmatter + 引文本文）
  templates/
    base.html                  # skeleton：head/style/vnav/依 layout 串 section/掛 main.js
    sections/                  # 每段一個 partial，對應目前視覺
      hero.html situation.html method.html services.html
      work.html media.html about.html contact.html
    partials/                  # 可重用：service_card.html gallery_item.html …
  static/
    styles.css                 # 從目前 inline style 抽出
    main.js                    # 取代 support.js 的極輕量 JS（見下）
  assets/                      # 品牌固定圖：logo、portrait、genz-*（沿用現有）
  build.py
  requirements.txt
  requirements-dev.txt
  .gitignore                   # 加入 dist/
  dist/                        # 產出（build 生成、git 忽略）
    index.html
    assets/…
```

## 內容模型（YAML / Markdown schema）

> 本節所有 YAML 範例值（含 `nav` 標籤、CTA 文案等）**僅為示意**；實際內容於遷移時**逐字取自 `55025da`**（包含「您」「有本」與目前的導覽標籤）。若要順便換掉導覽標籤（例如「您面對的處境」「我做過的」）可在 `site.yaml` 一併調整，但預設為原樣沿用。

### `content/site.yaml`
```yaml
meta:
  title: 引鹿創新體驗研究室 — 蕭喬尹
  description: …
  og_title: …
  og_description: …
brand:
  colors: {purple: "#5F5B8C", ink: "#33324A", gold: "#F9C04B",
           gold_dark: "#D98E00", bg_light: "#F6F6F9", lavender: "#EDEBF4"}
  fonts:  {serif: Noto Serif TC, sans: Noto Sans TC, hand: LXGW WenKai TC}
  logo:   {horizontal_purple: assets/logo-horizontal-purple.png,
           horizontal_white:  assets/logo-horizontal-white.png}
hero_theme: light            # light | purple（build 時決定 hero 配色）
cta: {primary: 預約 30 分鐘諮詢, contact_email: contact@in-clues-ux.com}
social: {linkedin: "https://…", substack: "https://…"}
nav:                          # 左側垂直導覽
  - {id: hero,      label: 首頁}
  - {id: situation, label: 您的處境}
  - {id: method,    label: 我的方法}
  - {id: services,  label: 合作方式}
  - {id: work,      label: 實績成果}
  - {id: voices,    label: 推薦}
  - {id: gallery,   label: 現場側錄}
  - {id: about,     label: 關於我}
  - {id: media,     label: 媒體曝光}
  - {id: contact,   label: 聯絡}
layout:                       # section 顯示順序（改這裡即可重排）
  [hero, situation, method, services, work, voices, gallery, about, media, contact]
```
（`nav` 標籤與 `layout` 順序都可自由改；`nav.id` 對應 section 的 anchor id。）

### `content/sections/*.yaml`（範例）
```yaml
# method.yaml（CLUES）
id: method
eyebrow: 我們使用的專業 CLUES 方法
title: 先看懂真實的人，再做有本的創新
steps:
  - {letter: C, en: CLARIFY,   name: 釐清脈絡, body: 先釐清問題發生的真實情境與限制…}
  - {letter: L, en: LISTEN,    name: 傾聽需求, body: …}
  - {letter: U, en: UNCOVER,   name: 挖掘洞察, body: …}
  - {letter: E, en: ESTABLISH, name: 建立方案, body: …}
  - {letter: S, en: SHIP,      name: 交付落地, body: …}
```
```yaml
# services.yaml（合作方式）
id: services
eyebrow: 我們可以怎麼開始？
title: 合作方式
groups:
  - {tag: "A ｜ 專案型", heading: 我承接客戶需求完成專案, cards: [ {number: "01", en: RESEARCH, name: 深入研究, positioning: …, gains: [...], audience: …, format: …}, … ]}
  - {tag: "B ｜ 賦能型", heading: 我帶領客戶培養創新實力, cards: [ … ]}
cta: {label: 來信詢問, href: "#contact"}
```
其餘 `hero / situation / work / about / contact` 各自對應目前該段的欄位（標題、副標、條列、數據、代表專案、經歷/學歷/講座清單…），一律照 `55025da` 的現有文字，逐字不改（包含「您」「有本」等）。

**`media.yaml`（媒體曝光）** 只放該段的標題/框架文字與兩個子群的小標；實際項目來自 collections：**深度文章 ← `collections/articles/`**、**公開受訪 ← `collections/interviews/`**。同理 **推薦語段（voices）← `collections/testimonials/`**、**現場側錄（gallery）← `collections/gallery/`**。

### Collections（丟檔就長出來）

- **gallery/**（現場側錄）：直接放 `*.jpg/*.png/*.webp`。`_captions.yaml` 以「檔名 → 說明」對應，選填。build 依檔名排序輸出；沒有說明的圖照常顯示。
- **interviews/**（公開受訪）、**articles/**（深度文章）、**testimonials/**（推薦語）：每則一個 Markdown 檔，YAML frontmatter 放結構化欄位、本文放引文/描述。
  ```markdown
  ---
  title: FAITH 框架演講
  source: Webconf 2025
  link: https://…        # 有連結才顯示「前往」
  date: 2025-11-01       # 排序用（新→舊）；缺則以檔名排序
  order: 10              # 可選，優先於 date
  ---
  （選填的補充描述）
  ```
  testimonials frontmatter：`author, org, role, context`；本文＝引文。
  articles frontmatter：`title, tag, link`。

**空集合處理**：某 collection 沒有任何項目時，該區塊仍渲染標題但清單為空（不報錯）。是否整段隱藏留待實作時以旗標控制，預設「照常渲染、清單為空」。

## 模板（Jinja2）

- `base.html`：輸出 `<!doctype>` 骨架、`<head>`（fonts/meta 來自 site.yaml）、內嵌 `static/styles.css`、左側 `vnav`（迴圈 `site.nav`）、依 `site.layout` 順序 `include` 對應 `sections/<id>.html`、末尾掛 `static/main.js`。
- `sections/*.html`：把目前該段的 HTML 結構搬進來，變數改讀對應 YAML。
- `partials/*.html`：service_card、gallery_item、interview_card、article_card、credential_group、testimonial 等重用元件。
- 顏色/字型從 `site.brand` 帶入（CSS 變數），hero 配色由 `hero_theme` 於 build 時決定，取代原本 x-dc 的 `heroBg/heroFg/heroIsPurple…` props。
- Markdown 欄位（如 about.bio、collection 本文）以 `markdown` 套件轉 HTML 後 `| safe` 輸出。

## 取代 support.js → `static/main.js`（純 JS，無框架）

目前 `support.js` 負責 x-dc 的 templating + 推薦輪播（DCLogic）。SSG 版：

- Templating / `sc-if` / `sc-for` → **Jinja2**（build 時完成，不需 runtime）。
- **推薦語輪播** → 重寫成純 JS：scroll-snap 橫向捲動 + 左右鍵 + 圓點；行為對齊目前效果，程式碼精簡。
- **垂直導覽 scroll-spy** → 用 `IntersectionObserver` 高亮目前 section。**順帶修掉**目前 x-dc 版「點遠處 section 不捲動」的問題（正式 build 後 anchor/scroll 皆正常）。
- 照片牆、CTA、平滑捲動等純 CSS 部分照舊。

## `build.py` 行為

- 讀 `content/`（site.yaml + sections/*.yaml + collections）→ 用 Jinja2 渲染 → 寫 `dist/index.html`。
- 複製 `assets/` 與各 collection 圖片到 `dist/assets/`（gallery 圖輸出到 `dist/assets/gallery/`）。
- Markdown 欄位以 `markdown` 轉換。
- `--watch`：以 watchdog 監看 `content/`、`templates/`、`static/`，變更即重建。
- `--serve [--port N]`：對 `dist/` 起本機伺服器；有裝 `livereload` 則自動刷新，否則純 `http.server`（手動重整）。
- 常見用法：`python build.py --serve --watch`（邊改邊看）。

## 邊界情況與錯誤處理

- 圖片缺說明 → 照常顯示、無 caption。
- collection 資料夾為空 → 該段標題仍在、清單為空、不報錯。
- 連結欄位缺（interview/article）→ 不顯示「前往」連結。
- 未知圖片副檔名 → 忽略並在 build log 提示。
- YAML/Markdown 解析錯 → build 中止並印出檔名與行號（明確錯誤，不產生半殘輸出）。

## 遷移步驟（實作時）

1. 從 `index.html`（`55025da`）逐段把**內容**抽進 `content/`（YAML/MD），文字逐字保留（含「您」「有本」）。
2. 把 HTML 結構＋CSS 移進 `templates/` 與 `static/styles.css`，變數改讀資料。
3. 把輪播與導覽 JS 改寫進 `static/main.js`。
4. 建 `build.py`、`requirements*.txt`、`.gitignore(dist/)`。
5. `python build.py` 後逐段比對 `dist/index.html` 與目前視覺一致。

## 驗證

- build 成功、無模板/解析錯誤。
- 瀏覽器開 `dist/index.html`，逐段截圖比對，視覺與 `55025da` 一致。
- 丟一張測試圖進 `gallery/` → 重建 → 出現於照片牆。
- 移除某圖的 caption → 仍正常顯示。
- 移動 `site.layout` 順序 → section 依序重排。

## 不在範圍

- 不做視覺重新設計（1:1 沿用現狀）。
- 不做資料庫、後台管理 UI、登入。
- 不做多頁（維持單頁 deck）。
- 不再整合 Claude Design 產線。
- 部署自動化（CI/GitHub Action）先不做，僅提供 `build.py` 產出 `dist/`；日後可加。

## 保留現有檔案

- 現行 `index.html`、`support.js` 在遷移期間**保留**（作為對照與可回退基準），待 SSG 版驗證一致後再決定是否移除或封存。
