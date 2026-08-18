/**
 * ==============================================================================
 * David 精力維持計畫 v1.0 - Google Sheets 雲端同步後端腳本 (Google Apps Script)
 * ==============================================================================
 * 
 * 【3 步驟快速安裝指引】：
 * 1. 開啟 Google 雲端硬碟 (Google Drive)，建立一個全新的 Google 試算表（例如命名為「David_精力維持追蹤表」）。
 * 2. 點擊頂部選單「擴充功能」->「Apps Script」。
 * 3. 清除編輯器內所有預設代碼，將本檔案代碼「全部複製並貼上」，點擊右上角「儲存 (磁碟圖示)」。
 * 4. 點擊右上角藍色「部署」按鈕 -> 選擇「新增部署作業」：
 *    - 種類選擇：網頁應用程式 (Web App)
 *    - 說明：精力追蹤 API
 *    - 誰可以存取 (Who has access)：選擇「所有人 (Anyone)」
 * 5. 點擊「部署」，完成授權後複製產生的「網頁應用程式網址 (Web App URL)」，貼回追蹤儀表板的「雲端同步設定」中即可！
 */

const SHEET_NAME_DAILY = '每日打卡紀錄';
const SHEET_NAME_WEEKLY = '每週測量數據';

/**
 * 處理 GET 請求：讀取試算表中的所有歷史資料並以 JSON 格式回傳
 */
function doGet(e) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    initSheetsIfNotExist(ss);
    
    const dailySheet = ss.getSheetByName(SHEET_NAME_DAILY);
    const weeklySheet = ss.getSheetByName(SHEET_NAME_WEEKLY);
    
    const dailyData = getSheetRows(dailySheet);
    const weeklyData = getSheetRows(weeklySheet);
    
    return createJsonResponse({
      status: 'success',
      message: '資料讀取成功',
      data: {
        daily: dailyData,
        weekly: weeklyData
      }
    });
  } catch (err) {
    return createJsonResponse({
      status: 'error',
      message: err.toString()
    });
  }
}

/**
 * 處理 POST 請求：寫入或更新每日打卡與每週數據
 */
function doPost(e) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    initSheetsIfNotExist(ss);
    
    let payload = {};
    if (e.postData && e.postData.contents) {
      payload = JSON.parse(e.postData.contents);
    } else if (e.parameter) {
      payload = e.parameter;
    }
    
    const action = payload.action || (payload.type === 'weekly' ? 'save_weekly' : 'save_daily');
    const timestamp = Utilities.formatDate(new Date(), "Asia/Taipei", "yyyy-MM-dd HH:mm:ss");
    
    if (action === 'save_daily' || payload.type === 'daily') {
      const dailySheet = ss.getSheetByName(SHEET_NAME_DAILY);
      const data = payload.data || payload;
      
      const date = data.date || Utilities.formatDate(new Date(), "Asia/Taipei", "yyyy-MM-dd");
      const weight = data.weight !== undefined && data.weight !== '' ? Number(data.weight) : '';
      const sleepTime = data.sleepTime || '';
      const steps = data.steps !== undefined && data.steps !== '' ? Number(data.steps) : '';
      const energy = data.energy !== undefined && data.energy !== '' ? Number(data.energy) : '';
      const dayType = data.dayType || '平日 (1800kcal)';
      
      const habitBreakfast = data.habitBreakfast ? '✓' : '-';
      const habitLunchOrder = data.habitLunchOrder ? '✓' : '-';
      const habitCaffeineCutoff = data.habitCaffeineCutoff ? '✓' : '-';
      const habitSocialRules = data.habitSocialRules ? '✓' : '-';
      const habitWorkout = data.habitWorkout ? '✓' : '-';
      const notes = data.notes || '';
      
      // 檢查是否已有當日紀錄（若有則更新，若無則新增）
      const existingRowIndex = findRowIndexByDate(dailySheet, date);
      const rowValues = [
        date, weight, sleepTime, steps, energy, dayType,
        habitBreakfast, habitLunchOrder, habitCaffeineCutoff, habitSocialRules, habitWorkout,
        notes, timestamp
      ];
      
      if (existingRowIndex > 0) {
        dailySheet.getRange(existingRowIndex, 1, 1, rowValues.length).setValues([rowValues]);
      } else {
        dailySheet.appendRow(rowValues);
      }
      
      return createJsonResponse({
        status: 'success',
        message: '每日紀錄已成功同步至 Google Sheet！',
        date: date
      });
    }
    
    if (action === 'save_weekly' || payload.type === 'weekly') {
      const weeklySheet = ss.getSheetByName(SHEET_NAME_WEEKLY);
      const data = payload.data || payload;
      
      const weekName = data.weekName || 'W1';
      const date = data.date || Utilities.formatDate(new Date(), "Asia/Taipei", "yyyy-MM-dd");
      const avgWeight = data.avgWeight !== undefined && data.avgWeight !== '' ? Number(data.avgWeight) : '';
      const bodyFat = data.bodyFat !== undefined && data.bodyFat !== '' ? Number(data.bodyFat) : '';
      const leanMass = data.leanMass !== undefined && data.leanMass !== '' ? Number(data.leanMass) : '';
      const waist = data.waist !== undefined && data.waist !== '' ? Number(data.waist) : '';
      const avgSteps = data.avgSteps !== undefined && data.avgSteps !== '' ? Number(data.avgSteps) : '';
      const avgSleep = data.avgSleep || '';
      const avgEnergy = data.avgEnergy !== undefined && data.avgEnergy !== '' ? Number(data.avgEnergy) : '';
      const statusAssessment = (leanMass && leanMass >= 60.5) ? '合格保肌 (≥60.5kg)' : (leanMass ? '需警惕 (<60.5kg)' : '待評估');
      const notes = data.notes || '';
      
      const existingRowIndex = findRowIndexByWeek(weeklySheet, weekName);
      const rowValues = [
        weekName, date, avgWeight, bodyFat, leanMass, waist, avgSteps, avgSleep, avgEnergy, statusAssessment, notes, timestamp
      ];
      
      if (existingRowIndex > 0) {
        weeklySheet.getRange(existingRowIndex, 1, 1, rowValues.length).setValues([rowValues]);
      } else {
        weeklySheet.appendRow(rowValues);
      }
      
      return createJsonResponse({
        status: 'success',
        message: '每週測量數據已成功同步至 Google Sheet！',
        week: weekName
      });
    }
    
    // 批次同步
    if (action === 'batch_sync') {
      const dailySheet = ss.getSheetByName(SHEET_NAME_DAILY);
      const weeklySheet = ss.getSheetByName(SHEET_NAME_WEEKLY);
      
      if (payload.dailyLogs && Array.isArray(payload.dailyLogs)) {
        payload.dailyLogs.forEach(d => {
          const rowIndex = findRowIndexByDate(dailySheet, d.date);
          const rowVals = [
            d.date, d.weight, d.sleepTime, d.steps, d.energy, d.dayType,
            d.habitBreakfast ? '✓' : '-', d.habitLunchOrder ? '✓' : '-', d.habitCaffeineCutoff ? '✓' : '-',
            d.habitSocialRules ? '✓' : '-', d.habitWorkout ? '✓' : '-', d.notes, timestamp
          ];
          if (rowIndex > 0) {
            dailySheet.getRange(rowIndex, 1, 1, rowVals.length).setValues([rowVals]);
          } else {
            dailySheet.appendRow(rowVals);
          }
        });
      }
      
      if (payload.weeklyLogs && Array.isArray(payload.weeklyLogs)) {
        payload.weeklyLogs.forEach(w => {
          const rowIndex = findRowIndexByWeek(weeklySheet, w.weekName);
          const statusAssessment = (w.leanMass && w.leanMass >= 60.5) ? '合格保肌 (≥60.5kg)' : (w.leanMass ? '需警惕 (<60.5kg)' : '待評估');
          const rowVals = [
            w.weekName, w.date, w.avgWeight, w.bodyFat, w.leanMass, w.waist, w.avgSteps, w.avgSleep, w.avgEnergy, statusAssessment, w.notes, timestamp
          ];
          if (rowIndex > 0) {
            weeklySheet.getRange(rowIndex, 1, 1, rowVals.length).setValues([rowVals]);
          } else {
            weeklySheet.appendRow(rowVals);
          }
        });
      }
      
      return createJsonResponse({
        status: 'success',
        message: '全部本地歷史紀錄已批次同步至 Google Sheet！'
      });
    }
    
    return createJsonResponse({
      status: 'error',
      message: '未知的 Action 類型'
    });
    
  } catch (err) {
    return createJsonResponse({
      status: 'error',
      message: err.toString()
    });
  }
}

/**
 * 輔助函數：初始化試算表與表頭
 */
function initSheetsIfNotExist(ss) {
  // 1. 每日打卡工作表
  let dailySheet = ss.getSheetByName(SHEET_NAME_DAILY);
  if (!dailySheet) {
    dailySheet = ss.insertSheet(SHEET_NAME_DAILY, 0);
    const headers = [
      '日期', '晨起體重(kg)', '昨晚入睡時間', '今日步數', '今日精力(1-10)', '日子型態',
      '早餐40g蛋白', '午餐順序/減碳', '15:00咖啡因斷點', '應酬3硬規則', '阻力訓練完成',
      '備註', '最後同步時間'
    ];
    dailySheet.getRange(1, 1, 1, headers.length).setValues([headers]);
    dailySheet.getRange(1, 1, 1, headers.length)
      .setBackground('#0f766e')
      .setFontColor('#ffffff')
      .setFontWeight('bold')
      .setHorizontalAlignment('center');
    dailySheet.setFrozenRows(1);
  }
  
  // 2. 每週測量工作表
  let weeklySheet = ss.getSheetByName(SHEET_NAME_WEEKLY);
  if (!weeklySheet) {
    weeklySheet = ss.insertSheet(SHEET_NAME_WEEKLY, 1);
    const headers = [
      '週次', '量測日期', '7日均體重(kg)', '體脂率(%)', '瘦體重(kg)', '腰圍(cm)',
      '平均步數', '平均入睡', '平均精力', '保肌狀態評估', '備註', '最後同步時間'
    ];
    weeklySheet.getRange(1, 1, 1, headers.length).setValues([headers]);
    weeklySheet.getRange(1, 1, 1, headers.length)
      .setBackground('#1e3a8a')
      .setFontColor('#ffffff')
      .setFontWeight('bold')
      .setHorizontalAlignment('center');
    weeklySheet.setFrozenRows(1);
  }
}

/**
 * 依日期查詢已有列數
 */
function findRowIndexByDate(sheet, dateStr) {
  const data = sheet.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    const rowDate = data[i][0];
    let formattedDate = rowDate;
    if (rowDate instanceof Date) {
      formattedDate = Utilities.formatDate(rowDate, "Asia/Taipei", "yyyy-MM-dd");
    }
    if (String(formattedDate).substring(0, 10) === String(dateStr).substring(0, 10)) {
      return i + 1;
    }
  }
  return -1;
}

/**
 * 依週次查詢已有列數
 */
function findRowIndexByWeek(sheet, weekStr) {
  const data = sheet.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    if (String(data[i][0]).trim() === String(weekStr).trim()) {
      return i + 1;
    }
  }
  return -1;
}

/**
 * 取得工作表全部數據為物件陣列
 */
function getSheetRows(sheet) {
  if (!sheet) return [];
  const data = sheet.getDataRange().getValues();
  if (data.length <= 1) return [];
  
  const headers = data[0];
  const rows = [];
  
  for (let i = 1; i < data.length; i++) {
    const rowObj = {};
    for (let j = 0; j < headers.length; j++) {
      let val = data[i][j];
      if (val instanceof Date) {
        val = Utilities.formatDate(val, "Asia/Taipei", "yyyy-MM-dd HH:mm:ss");
        if (headers[j] === '日期' || headers[j] === '量測日期') {
          val = val.substring(0, 10);
        }
      }
      rowObj[headers[j]] = val;
    }
    rows.push(rowObj);
  }
  return rows;
}

/**
 * 封裝 JSON 回應與 CORS 設定
 */
function createJsonResponse(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
