# David 精力維持計畫 v1.0 | 數據追蹤儀表板 (Vitality Plan Dashboard)

> **計畫期間**：2026-08-18 ～ 2026-09-14（4 週定版）  
> **核心目標**：減重 1.4~1.8 kg，體脂降至 27.4~27.7%，**瘦體重守住 ≥ 60.5 kg (最高紅線)**。  
> **線上儀表板**：[https://davidyeh51.github.io/david-vitality-plan/](https://davidyeh51.github.io/david-vitality-plan/)

---

## 🌟 核心特色與功能模組

1. **每日 30 秒晨起打卡**：
   - 晨起體重 (只看 7 日平均，忽略單日水分波動)
   - 昨晚入睡時間 (收斂至 23:00 ± 30 分)
   - 今日步數 (寄生走路增量 +3,000 步)
   - 精力評分 (1~10 分，減重期精力不應下降)
   - 核心微習慣勾選 (早餐 40g 蛋白質、午餐順序菜肉先吃、15:00 咖啡因斷點、應酬 3 大硬規則)

2. **趨勢圖表與身體組成**：
   - 體重趨勢線與 7 日滑動均線
   - 瘦體重 vs 脂肪重 長條堆疊圖 (自動警示瘦體重 < 60.5kg)
   - 步數與精力雙軸趨勢相關圖

3. **每週日固定量測匯總**：
   - 晨起排尿後空腹量測
   - 4 週漸進疊加節奏追蹤

4. **居家阻力訓練課表與計時器**：
   - 週二、週四 20:30–21:00 (5 動作 × 3 輪)
   - 內建 60 秒動作間休息計時器與提示音

5. **Google Sheets 雙向雲端同步**：
   - 支援離線 LocalStorage 快取 + Google Apps Script Web App 雲端即時同步
   - 跨手機、平板、電腦無縫追蹤

---

## 📊 Google Sheets 雲端同步 3 步驟快速設定

1. 在 Google 雲端硬碟建立一個全新的 **Google 試算表**（例如命名為 `David_精力維持追蹤表`）。
2. 點擊頂部選單 **「擴充功能」->「Apps Script」**。
3. 清除編輯器內所有預設代碼，將專案中的 [`GoogleAppsScript.js`](GoogleAppsScript.js) 全部複製並貼上，點擊「儲存」。
4. 點擊右上角 **「部署」->「新增部署作業」**：
   - 種類：**網頁應用程式 (Web App)**
   - 說明：精力追蹤 API
   - 誰可以存取：**所有人 (Anyone)**
5. 點擊「部署」並授權，複製產生的「網頁應用程式網址 (Web App URL)」，貼回網頁右上角「Google Sheets 設定」中儲存即可！

---

## 🛠️ 技術架構

- 前端：HTML5, Tailwind CSS, Chart.js, Phosphor Icons, Canvas-Confetti, Vanilla JavaScript
- 後端儲存：Google Apps Script (GAS) Web App + Google Sheets 雲端試算表
- 本地存儲：Browser LocalStorage API
- 部署：GitHub Pages
