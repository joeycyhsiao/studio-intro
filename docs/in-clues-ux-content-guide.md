# In-Clues UX 網站內容調整指南

> 目的：讓 **in-clues-ux.com（工作室站）** 與 **joeyhsiao.com（個人顧問 deck）** 分工清楚、避免 SEO 內容重複互打，並把 in-clues 經營成「內容與知識庫的 SEO 主場」。
> 版本：2026-07-12

---

## 0. 一句話定位

| 網站 | 角色 | 主要訪客 | 核心任務 |
|---|---|---|---|
| **joeyhsiao.com** | 個人顧問 sales deck | 想找「蕭喬尹本人」談合作的窗口 | 建立信任 → 預約 30 分鐘諮詢 |
| **in-clues-ux.com** | 工作室品牌 + 知識庫 | 搜尋 UX／AI 創新主題、想看方法與資源的人 | 累積內容權重、展示專業、蒐集名單 |

**原則：** 同一件事只在「主場」深寫，另一站用**摘要 + 連結**帶過。誰是主場，看下表。

| 內容主題 | 主場（深寫） | 另一站（摘要＋連結） |
|---|---|---|
| 個人故事 / 顧問定位 | joeyhsiao.com | in-clues 只放一段「創辦人」簡介 |
| 服務內容 / 合作方式 | in-clues（工作室名義接案） | joeyhsiao deck 已有六種合作方式，維持；但用語錯開 |
| 文章 / 研究報告 | **in-clues（SEO 主場）** | joeyhsiao deck 用精選卡片＋「更多 →」連回 in-clues |
| 公開資源 / 下載庫 | in-clues | joeyhsiao 不放，需要時才連 |

---

## 1. 需要處理的重疊清單

以下是兩站目前**內容打架**的地方，逐一處理：

1. **服務內容** — 兩邊都在講「我提供什麼服務」，文案接近。
2. **創辦人／個人故事** — deck 有完整「專業經歷」，in-clues 首頁也有一段自我介紹。
3. **文章** — 目前文章在 vocus / Substack，canonical 指向 Substack；in-clues 的 `/post-archive/` 反而不是 SEO 受益方。
4. **CTA 出口** — 兩站都有「聯繫我」，要確保訪客不會在兩站間繞圈。

---

## 2. 逐區修改指引（in-clues-ux.com）

### 2-1. 首頁 Hero
- **保留**：工作室品牌名、一句 slogan、主視覺。
- **加一顆按鈕**：「想直接找 Joey 談合作 →」連到 `joeyhsiao.com`。
  讓「找工作室」與「找個人顧問」兩種意圖在入口就分流。

### 2-2. 服務內容區
- **定位**：這裡是**服務的主場**（工作室名義承接）。可以寫得比 deck 更完整（流程、交付物、適合對象、預算級距）。
- **與 deck 錯開用語**：deck 用的是「六種合作方式（A 承接／B 陪跑）」的**顧問視角**；in-clues 這邊用**服務型錄視角**（專案類型、產出、時程），不要整段複製 deck 文案。
- **結尾 CTA**：導向 in-clues 自己的聯繫區或表單，不要直接把人踢去 deck（避免出口混亂）。

### 2-3. 創辦人／關於
- **只留一段**（3–5 行）：姓名、頭銜、一句代表性成就、一句理念。
- 結尾放「完整經歷與合作方式 → joeyhsiao.com」。
- **不要**在 in-clues 重寫整份「專業經歷」——那是 deck 的主場，重複會稀釋兩邊。

### 2-4. 最新文章 / 部落格（`/post-archive/`）★ 最重要
**現況：in-clues 已經有完整文章內文，只是 canonical 指向 Substack。**
＝ 內容資產已經在自己手上，Google 卻被告知「正本在 Substack」，所有排名權重都送給別人。這是純設定問題，改 canonical 即可，**不需要搬文**。

目標：**讓 in-clues 成為每篇文章的 canonical 正本**。

做法（依平台）：
- **in-clues（WordPress + Yoast 假設）**：進每篇文章 → Yoast SEO → Advanced → **Canonical URL** 欄位**清空**（清空＝自我 canonical），或明確填該篇自己的 in-clues 網址。
  - 若 canonical 不是逐篇設的，而是主題／外掛統一輸出的：檢查佈景的 `header.php` 或 SEO 外掛設定，找到寫死指向 Substack 的地方拿掉。
  - 改完用「檢視原始碼」搜 `rel="canonical"`，確認指向的是 in-clues 自己的網址。
- **Substack**：每篇 → Settings → **Canonical URL** 填對應的 in-clues 網址（方向反過來）。
- **vocus**：若支援 canonical 就指 in-clues；不支援就把該篇當**純導流**，文首註明「本文首發於 in-clues-ux.com」並附連結。
- **往後流程**：**先發 in-clues → 再轉載** Substack / vocus，且轉載時設 canonical 回 in-clues。

改完後：到 Google Search Console 對幾篇文章做「網址檢查 → 要求建立索引」，加速 Google 重新認定正本。預期 2–6 週看到 in-clues 開始取代 Substack 出現在搜尋結果。

### 2-5. 公開資源 / 下載庫
- 維持在 in-clues，作為**名單蒐集**（下載換 email）與專業展示。
- 每個資源頁補：一段說明、適用情境、1 張預覽圖 → 有助於長尾搜尋。
- deck 不放這區；未來 deck 若需要，用單一連結帶過。

### 2-6. 聯繫我們
- in-clues 收「工作室 / 專案」洽詢；deck 收「個人 30 分鐘諮詢」。
- 兩邊的 email 可共用 `contact@in-clues-ux.com`，但**表單前的文案**要講清楚各自受理什麼，避免訪客不知道該從哪進。

---

## 3. 兩站交叉連結策略

- **joeyhsiao.com → in-clues**：deck 的「媒體曝光」已加「更多研究文章與報告 → in-clues」（已上線）。維持這一條主要導流。
- **in-clues → joeyhsiao.com**：在 Hero 與「關於」各放一個「找 Joey 本人談 →」出口。
- **連結數量克制**：每站對另一站的主動連結 2–3 個即可，過多會讓訪客分心、也稀釋權重集中效果。

---

## 4. SEO 檢核（做完後逐項確認）

- [ ] in-clues 每篇文章 canonical = 自我網址（原始碼搜 `rel="canonical"` 確認）
- [ ] Substack 每篇 canonical = 對應 in-clues 網址
- [ ] vocus 各篇：能設 canonical 就設，否則文首註明首發並連回
- [ ] Search Console 對主要文章「要求建立索引」
- [ ] 服務內容：deck 與 in-clues 文案不逐段重複（用語視角錯開）
- [ ] 創辦人故事只在 deck 深寫，in-clues 摘要＋連結
- [ ] 兩站各自的 CTA 出口清楚、不繞圈
- [ ] （可選）in-clues 提交 sitemap 到 Google Search Console，觀察索引狀況

---

## 5. 建議執行順序

1. **先做 canonical**（2-4 + 第 4 節）——文章內文已在 in-clues，這純粹是設定問題：**效益最大、工最少、完全不動版面**。先做這個。
2. **Search Console 要求重新索引**（跟著上一步做完）。
3. **服務內容錯開用語**（2-2）。
4. **創辦人區收斂成摘要 + 連結**（2-3）。
5. **加兩站交叉連結出口**（第 3 節）。
6. **公開資源補說明與預覽**（2-5），行有餘力再做。
7. **回頭把 deck 的兩張文章卡改連 in-clues**（見附錄）。

---

## 附：deck 側可搭配的一步（待你提供網址）
deck「媒體曝光」的兩張專欄卡目前連到 Substack。等文章在 in-clues 有正本網址後，把卡片改連 in-clues，連 deck 的文章連結也一起幫自家網域累積權重。對應檔案：
- `content/collections/articles/01-agent-ai.md`
- `content/collections/articles/02-genz.md`
