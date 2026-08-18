/**
 * David 精力維持計畫 v1.0 - Web Dashboard Application Logic
 */

// --- 預設常數與基線 ---
const BASELINE = {
  date: '2026-08-18',
  age: 48,
  height: 180,
  weight: 86.0,
  bodyFat: 28.9,
  leanMass: 61.1, // 86 * (1 - 0.289) = 61.146 -> 61.1
  leanMassSafetyThreshold: 60.5,
  targetWeightMin: 84.2,
  targetWeightMax: 84.6,
  targetBodyFatMin: 27.4,
  targetBodyFatMax: 27.7,
  tdee: 2285,
  targetBedtime: '23:00'
};

const STORAGE_KEYS = {
  DAILY_LOGS: 'david_vitality_daily_logs_v1',
  WEEKLY_LOGS: 'david_vitality_weekly_logs_v1',
  GAS_URL: 'david_vitality_gas_url_v1',
  SETTINGS: 'david_vitality_settings_v1'
};

// --- 全域狀態 ---
let appState = {
  dailyLogs: [],
  weeklyLogs: [],
  gasUrl: '',
  charts: {
    weightChart: null,
    bodyCompChart: null,
    energyStepsChart: null
  },
  workoutTimer: null,
  timerSecondsRemaining: 60,
  timerRunning: false
};

// --- 初始化入口 ---
document.addEventListener('DOMContentLoaded', () => {
  initStorage();
  initUI();
  initEventListeners();
  renderAll();
});

// --- 存儲初始化與範例數據 ---
function initStorage() {
  const localGas = localStorage.getItem(STORAGE_KEYS.GAS_URL);
  if (localGas) {
    appState.gasUrl = localGas;
  }

  const localDaily = localStorage.getItem(STORAGE_KEYS.DAILY_LOGS);
  if (localDaily) {
    try {
      appState.dailyLogs = JSON.parse(localDaily);
    } catch (e) {
      console.error('Error parsing daily logs', e);
      appState.dailyLogs = [];
    }
  }

  const localWeekly = localStorage.getItem(STORAGE_KEYS.WEEKLY_LOGS);
  if (localWeekly) {
    try {
      appState.weeklyLogs = JSON.parse(localWeekly);
    } catch (e) {
      console.error('Error parsing weekly logs', e);
      appState.weeklyLogs = [];
    }
  }

  // 若無資料，放入基線第一筆
  if (appState.dailyLogs.length === 0) {
    appState.dailyLogs = [
      {
        date: '2026-08-18',
        weight: 86.0,
        sleepTime: '23:15',
        steps: 6200,
        energy: 8,
        dayType: '平日 (1800kcal)',
        habitBreakfast: true,
        habitLunchOrder: true,
        habitCaffeineCutoff: true,
        habitSocialRules: false,
        habitWorkout: true,
        notes: '計畫啟動第一天！早餐 40g 蛋白質達成（3顆蛋+無糖豆漿），晚餐後執行 W1 降階阻力訓練。'
      }
    ];
    saveLocalDaily();
  }

  if (appState.weeklyLogs.length === 0) {
    appState.weeklyLogs = [
      {
        weekName: '現況 (基線)',
        date: '2026-08-18',
        avgWeight: 86.0,
        bodyFat: 28.9,
        leanMass: 61.1,
        waist: 92.0,
        avgSteps: 6000,
        avgSleep: '23:00',
        avgEnergy: 7.5,
        statusAssessment: '基線確立 (瘦體重 61.1kg)',
        notes: '起始數據，守住 60.5kg 瘦體重為最高原則'
      }
    ];
    saveLocalWeekly();
  }
}

function saveLocalDaily() {
  localStorage.setItem(STORAGE_KEYS.DAILY_LOGS, JSON.stringify(appState.dailyLogs));
}

function saveLocalWeekly() {
  localStorage.setItem(STORAGE_KEYS.WEEKLY_LOGS, JSON.stringify(appState.weeklyLogs));
}

// --- UI 與互動初始化 ---
function initUI() {
  // 設定今日預設日期
  const todayStr = getTodayDateStr();
  const dateInput = document.getElementById('logDate');
  if (dateInput) {
    dateInput.value = todayStr;
  }
  const weeklyDateInput = document.getElementById('weeklyLogDate');
  if (weeklyDateInput) {
    weeklyDateInput.value = todayStr;
  }

  // 設定 GAS 網址輸入欄
  const gasInput = document.getElementById('gasApiUrl');
  if (gasInput && appState.gasUrl) {
    gasInput.value = appState.gasUrl;
    updateGasStatusBadge(true);
  } else {
    updateGasStatusBadge(false);
  }

  // 精力滑桿聯動
  const energySlider = document.getElementById('logEnergy');
  const energyDisplay = document.getElementById('energyDisplay');
  if (energySlider && energyDisplay) {
    energySlider.addEventListener('input', (e) => {
      energyDisplay.textContent = e.target.value;
      updateEnergyBadgeColor(e.target.value);
    });
  }

  // 載入當日已有的打卡資料（若有的話）
  loadDailyFormForDate(todayStr);
}

function updateEnergyBadgeColor(val) {
  const badge = document.getElementById('energyBadge');
  if (!badge) return;
  const num = Number(val);
  if (num >= 8) {
    badge.className = 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 dark:bg-emerald-950/80 dark:text-emerald-300';
    badge.textContent = `${num} 分 · 充沛良好`;
  } else if (num >= 6) {
    badge.className = 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-100 text-amber-800 dark:bg-amber-950/80 dark:text-amber-300';
    badge.textContent = `${num} 分 · 尚可維持`;
  } else {
    badge.className = 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-bold bg-rose-100 text-rose-800 dark:bg-rose-950/80 dark:text-rose-300';
    badge.textContent = `${num} 分 · 疲勞偏低 (注意熱量/睡眠)`;
  }
}

function getTodayDateStr() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}

// --- 事件監聽 ---
function initEventListeners() {
  // 日期選擇變更時，自動回填資料
  const logDateInput = document.getElementById('logDate');
  if (logDateInput) {
    logDateInput.addEventListener('change', (e) => {
      loadDailyFormForDate(e.target.value);
    });
  }

  // 每日打卡表單送出
  const dailyForm = document.getElementById('dailyCheckinForm');
  if (dailyForm) {
    dailyForm.addEventListener('submit', handleDailySubmit);
  }

  // 每週測量表單送出
  const weeklyForm = document.getElementById('weeklyMeasureForm');
  if (weeklyForm) {
    weeklyForm.addEventListener('submit', handleWeeklySubmit);
  }

  // 每週測量體重與體脂輸入時自動計算瘦體重
  const weeklyWeightInput = document.getElementById('weeklyAvgWeight');
  const weeklyBfInput = document.getElementById('weeklyBf');
  if (weeklyWeightInput && weeklyBfInput) {
    const calcLeanMass = () => {
      const w = parseFloat(weeklyWeightInput.value);
      const bf = parseFloat(weeklyBfInput.value);
      const display = document.getElementById('calculatedLeanMassDisplay');
      const hiddenInput = document.getElementById('weeklyLeanMass');
      if (!isNaN(w) && !isNaN(bf) && bf > 0 && bf < 100) {
        const lean = (w * (1 - bf / 100)).toFixed(1);
        if (display) {
          const isSafe = lean >= BASELINE.leanMassSafetyThreshold;
          display.innerHTML = `<span class="${isSafe ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400 font-bold'}">${lean} kg</span> ${isSafe ? '✅ 安全保肌' : '⚠️ 低於紅線 (60.5kg)'}`;
        }
        if (hiddenInput) hiddenInput.value = lean;
      } else {
        if (display) display.textContent = '-- kg';
      }
    };
    weeklyWeightInput.addEventListener('input', calcLeanMass);
    weeklyBfInput.addEventListener('input', calcLeanMass);
  }

  // 阻力訓練計時器按鈕
  const timerToggleBtn = document.getElementById('timerToggleBtn');
  const timerResetBtn = document.getElementById('timerResetBtn');
  if (timerToggleBtn) {
    timerToggleBtn.addEventListener('click', toggleWorkoutTimer);
  }
  if (timerResetBtn) {
    timerResetBtn.addEventListener('click', resetWorkoutTimer);
  }

  // Google Sheet 設定儲存
  const saveGasBtn = document.getElementById('saveGasUrlBtn');
  if (saveGasBtn) {
    saveGasBtn.addEventListener('click', saveGasSettings);
  }

  // Google Sheet 連線測試
  const testGasBtn = document.getElementById('testGasBtn');
  if (testGasBtn) {
    testGasBtn.addEventListener('click', testGasConnection);
  }

  // Google Sheet 雲端拉取
  const pullGasBtn = document.getElementById('pullGasBtn');
  if (pullGasBtn) {
    pullGasBtn.addEventListener('click', pullDataFromGas);
  }

  // Google Sheet 批次推送到雲端
  const pushGasBtn = document.getElementById('pushGasBtn');
  if (pushGasBtn) {
    pushGasBtn.addEventListener('click', pushAllDataToGas);
  }

  // 複製 GAS 代碼按鈕
  const copyGasCodeBtn = document.getElementById('copyGasCodeBtn');
  if (copyGasCodeBtn) {
    copyGasCodeBtn.addEventListener('click', copyGasScriptCode);
  }

  // 快速標籤跳轉
  document.querySelectorAll('[data-tab-target]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const targetId = btn.getAttribute('data-tab-target');
      switchTab(targetId);
    });
  });
}

// --- 切換分頁標籤 ---
function switchTab(tabId) {
  document.querySelectorAll('.tab-pane').forEach(pane => {
    pane.classList.add('hidden');
  });
  const activePane = document.getElementById(tabId);
  if (activePane) {
    activePane.classList.remove('hidden');
  }

  document.querySelectorAll('[data-tab-target]').forEach(btn => {
    if (btn.getAttribute('data-tab-target') === tabId) {
      btn.className = 'tab-btn active px-4 py-2 text-sm font-semibold rounded-lg bg-teal-600 text-white shadow-sm transition-all';
    } else {
      btn.className = 'tab-btn px-4 py-2 text-sm font-medium rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800 transition-all';
    }
  });

  // 若切換至數據分析，重新調整圖表寬度
  if (tabId === 'tab-analytics') {
    setTimeout(() => {
      renderCharts();
    }, 100);
  }
}

// --- 回填特定日期的表單 ---
function loadDailyFormForDate(dateStr) {
  const existing = appState.dailyLogs.find(l => l.date === dateStr);
  const weightInput = document.getElementById('logWeight');
  const sleepInput = document.getElementById('logSleepTime');
  const stepsInput = document.getElementById('logSteps');
  const energyInput = document.getElementById('logEnergy');
  const energyDisplay = document.getElementById('energyDisplay');
  const dayTypeSelect = document.getElementById('logDayType');
  const habitBreakfast = document.getElementById('habitBreakfast');
  const habitLunchOrder = document.getElementById('habitLunchOrder');
  const habitCaffeine = document.getElementById('habitCaffeine');
  const habitSocialRules = document.getElementById('habitSocialRules');
  const habitWorkout = document.getElementById('habitWorkout');
  const notesInput = document.getElementById('logNotes');

  if (existing) {
    if (weightInput) weightInput.value = existing.weight || '';
    if (sleepInput) sleepInput.value = existing.sleepTime || '';
    if (stepsInput) stepsInput.value = existing.steps || '';
    if (energyInput) {
      energyInput.value = existing.energy || 8;
      if (energyDisplay) energyDisplay.textContent = existing.energy || 8;
      updateEnergyBadgeColor(existing.energy || 8);
    }
    if (dayTypeSelect) dayTypeSelect.value = existing.dayType || '平日 (1800kcal)';
    if (habitBreakfast) habitBreakfast.checked = !!existing.habitBreakfast;
    if (habitLunchOrder) habitLunchOrder.checked = !!existing.habitLunchOrder;
    if (habitCaffeine) habitCaffeine.checked = !!existing.habitCaffeineCutoff;
    if (habitSocialRules) habitSocialRules.checked = !!existing.habitSocialRules;
    if (habitWorkout) habitWorkout.checked = !!existing.habitWorkout;
    if (notesInput) notesInput.value = existing.notes || '';
  } else {
    // 預設清空但保留合理預設
    if (weightInput) weightInput.value = '';
    if (sleepInput) sleepInput.value = '23:00';
    if (stepsInput) stepsInput.value = '';
    if (energyInput) {
      energyInput.value = 8;
      if (energyDisplay) energyDisplay.textContent = '8';
      updateEnergyBadgeColor(8);
    }
    if (dayTypeSelect) dayTypeSelect.value = '平日 (1800kcal)';
    if (habitBreakfast) habitBreakfast.checked = false;
    if (habitLunchOrder) habitLunchOrder.checked = false;
    if (habitCaffeine) habitCaffeine.checked = false;
    if (habitSocialRules) habitSocialRules.checked = false;
    if (habitWorkout) habitWorkout.checked = false;
    if (notesInput) notesInput.value = '';
  }
}

// --- 每日打卡送出處理 ---
async function handleDailySubmit(e) {
  e.preventDefault();
  const date = document.getElementById('logDate').value;
  const weight = parseFloat(document.getElementById('logWeight').value) || '';
  const sleepTime = document.getElementById('logSleepTime').value;
  const steps = parseInt(document.getElementById('logSteps').value, 10) || 0;
  const energy = parseInt(document.getElementById('logEnergy').value, 10) || 8;
  const dayType = document.getElementById('logDayType').value;
  const habitBreakfast = document.getElementById('habitBreakfast').checked;
  const habitLunchOrder = document.getElementById('habitLunchOrder').checked;
  const habitCaffeineCutoff = document.getElementById('habitCaffeine').checked;
  const habitSocialRules = document.getElementById('habitSocialRules').checked;
  const habitWorkout = document.getElementById('habitWorkout').checked;
  const notes = document.getElementById('logNotes').value;

  const logEntry = {
    date,
    weight,
    sleepTime,
    steps,
    energy,
    dayType,
    habitBreakfast,
    habitLunchOrder,
    habitCaffeineCutoff,
    habitSocialRules,
    habitWorkout,
    notes,
    updatedAt: new Date().toISOString()
  };

  // 儲存至本地
  const existingIdx = appState.dailyLogs.findIndex(l => l.date === date);
  if (existingIdx >= 0) {
    appState.dailyLogs[existingIdx] = logEntry;
  } else {
    appState.dailyLogs.push(logEntry);
  }

  // 依日期排序
  appState.dailyLogs.sort((a, b) => new Date(a.date) - new Date(b.date));
  saveLocalDaily();

  showToast('✅ 每日打卡已儲存至本地！', 'success');

  // 若有設定 GAS，非同步送出
  if (appState.gasUrl) {
    syncSingleDailyToGas(logEntry);
  }

  renderAll();

  // 若習慣打卡良好，跳出撒花慶祝
  if (habitBreakfast && habitLunchOrder) {
    triggerConfetti();
  }
}

// --- 每週測量送出處理 ---
async function handleWeeklySubmit(e) {
  e.preventDefault();
  const weekName = document.getElementById('weeklyWeekName').value;
  const date = document.getElementById('weeklyLogDate').value;
  const avgWeight = parseFloat(document.getElementById('weeklyAvgWeight').value) || '';
  const bodyFat = parseFloat(document.getElementById('weeklyBf').value) || '';
  let leanMass = parseFloat(document.getElementById('weeklyLeanMass').value);
  const waist = parseFloat(document.getElementById('weeklyWaist').value) || '';
  const avgSteps = parseInt(document.getElementById('weeklyAvgSteps').value, 10) || '';
  const avgSleep = document.getElementById('weeklyAvgSleep').value || '';
  const avgEnergy = parseFloat(document.getElementById('weeklyAvgEnergy').value) || '';
  const notes = document.getElementById('weeklyNotes').value || '';

  if (!leanMass && avgWeight && bodyFat) {
    leanMass = parseFloat((avgWeight * (1 - bodyFat / 100)).toFixed(1));
  }

  const statusAssessment = (leanMass && leanMass >= BASELINE.leanMassSafetyThreshold)
    ? '合格保肌 (≥60.5kg)'
    : (leanMass ? '需警惕 (<60.5kg)' : '待評估');

  const weeklyEntry = {
    weekName,
    date,
    avgWeight,
    bodyFat,
    leanMass,
    waist,
    avgSteps,
    avgSleep,
    avgEnergy,
    statusAssessment,
    notes,
    updatedAt: new Date().toISOString()
  };

  const existingIdx = appState.weeklyLogs.findIndex(w => w.weekName === weekName);
  if (existingIdx >= 0) {
    appState.weeklyLogs[existingIdx] = weeklyEntry;
  } else {
    appState.weeklyLogs.push(weeklyEntry);
  }

  saveLocalWeekly();
  closeModal('weeklyMeasureModal');
  showToast(`🎉 ${weekName} 數據已成功紀錄！`, 'success');

  if (appState.gasUrl) {
    syncSingleWeeklyToGas(weeklyEntry);
  }

  renderAll();
  triggerConfetti();
}

// --- 渲染全部儀表板視圖 ---
function renderAll() {
  renderHeaderMetrics();
  renderRecentLogsTable();
  renderWeeklySummaryTable();
  renderCharts();
}

// --- 頂部指標卡片渲染 ---
function renderHeaderMetrics() {
  const latestLog = appState.dailyLogs[appState.dailyLogs.length - 1] || {};
  const latestWeekly = appState.weeklyLogs[appState.weeklyLogs.length - 1] || {};

  // 1. 最新體重與 7 日均重
  const currentWeightEl = document.getElementById('metricCurrentWeight');
  const avg7DayWeightEl = document.getElementById('metric7DayAvgWeight');
  const weightProgressEl = document.getElementById('metricWeightProgress');

  const currentWeight = latestLog.weight || BASELINE.weight;
  const recent7 = appState.dailyLogs.slice(-7).filter(l => l.weight > 0);
  const avg7Weight = recent7.length > 0
    ? (recent7.reduce((sum, l) => sum + Number(l.weight), 0) / recent7.length).toFixed(1)
    : currentWeight;

  if (currentWeightEl) currentWeightEl.textContent = `${currentWeight} kg`;
  if (avg7DayWeightEl) avg7DayWeightEl.textContent = `7日均重: ${avg7Weight} kg`;
  if (weightProgressEl) {
    const diff = (currentWeight - BASELINE.weight).toFixed(1);
    const sign = diff > 0 ? `+${diff}` : `${diff}`;
    weightProgressEl.textContent = `距基線: ${sign} kg (目標 84.2kg)`;
  }

  // 2. 體脂率與瘦體重
  const currentBfEl = document.getElementById('metricBodyFat');
  const currentLeanEl = document.getElementById('metricLeanMass');
  const leanStatusEl = document.getElementById('metricLeanStatus');

  const bf = latestWeekly.bodyFat || BASELINE.bodyFat;
  const lean = latestWeekly.leanMass || BASELINE.leanMass;

  if (currentBfEl) currentBfEl.textContent = `${bf} %`;
  if (currentLeanEl) currentLeanEl.textContent = `瘦體重: ${lean} kg`;
  if (leanStatusEl) {
    if (lean >= BASELINE.leanMassSafetyThreshold) {
      leanStatusEl.className = 'text-xs font-semibold text-emerald-600 dark:text-emerald-400';
      leanStatusEl.innerHTML = `🛡️ 安全高於紅線 (≥${BASELINE.leanMassSafetyThreshold}kg)`;
    } else {
      leanStatusEl.className = 'text-xs font-bold text-rose-600 dark:text-rose-400';
      leanStatusEl.innerHTML = `⚠️ 低於安全紅線 (${BASELINE.leanMassSafetyThreshold}kg)！需增肌保固`;
    }
  }

  // 3. 今日步數與精力
  const currentStepsEl = document.getElementById('metricSteps');
  const currentEnergyEl = document.getElementById('metricEnergy');
  if (currentStepsEl) currentStepsEl.textContent = `${latestLog.steps || 0} 步`;
  if (currentEnergyEl) currentEnergyEl.textContent = `${latestLog.energy || 8} / 10 分`;
}

// --- 歷史打卡表格渲染 ---
function renderRecentLogsTable() {
  const tbody = document.getElementById('dailyLogsTableBody');
  if (!tbody) return;

  const logs = [...appState.dailyLogs].reverse().slice(0, 14); // 顯示最近 14 筆
  if (logs.length === 0) {
    tbody.innerHTML = `<tr><td colspan="8" class="text-center py-6 text-slate-400">目前尚無打卡紀錄</td></tr>`;
    return;
  }

  tbody.innerHTML = logs.map(l => {
    const habitsCount = [l.habitBreakfast, l.habitLunchOrder, l.habitCaffeineCutoff, l.habitSocialRules, l.habitWorkout].filter(Boolean).length;
    return `
      <tr class="border-b border-slate-100 dark:border-slate-800 hover:bg-slate-50/50 dark:hover:bg-slate-800/40 text-sm">
        <td class="py-3 px-3 font-semibold text-slate-900 dark:text-white">${l.date}</td>
        <td class="py-3 px-3 font-medium">${l.weight ? `${l.weight} kg` : '-'}</td>
        <td class="py-3 px-3">${l.sleepTime || '-'}</td>
        <td class="py-3 px-3">${l.steps ? l.steps.toLocaleString() : '-'}</td>
        <td class="py-3 px-3">
          <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold ${l.energy >= 8 ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950/80 dark:text-emerald-300' : l.energy >= 6 ? 'bg-amber-100 text-amber-800 dark:bg-amber-950/80 dark:text-amber-300' : 'bg-rose-100 text-rose-800 dark:bg-rose-950/80 dark:text-rose-300'}">
            ${l.energy || 8} 分
          </span>
        </td>
        <td class="py-3 px-3">
          <span class="text-xs px-2 py-0.5 rounded-full ${l.dayType && l.dayType.includes('應酬') ? 'bg-purple-100 text-purple-800 dark:bg-purple-950/80 dark:text-purple-300' : 'bg-blue-100 text-blue-800 dark:bg-blue-950/80 dark:text-blue-300'}">
            ${l.dayType || '平日'}
          </span>
        </td>
        <td class="py-3 px-3">
          <div class="flex items-center gap-1 text-xs">
            <span title="早餐 40g 蛋白質" class="${l.habitBreakfast ? 'text-emerald-600 font-bold' : 'text-slate-300'}">🍳</span>
            <span title="午餐順序/減碳" class="${l.habitLunchOrder ? 'text-emerald-600 font-bold' : 'text-slate-300'}">🥗</span>
            <span title="15:00 咖啡因斷點" class="${l.habitCaffeineCutoff ? 'text-emerald-600 font-bold' : 'text-slate-300'}">☕</span>
            <span title="應酬 3 硬規則" class="${l.habitSocialRules ? 'text-purple-600 font-bold' : 'text-slate-300'}">🍷</span>
            <span title="阻力訓練" class="${l.habitWorkout ? 'text-amber-600 font-bold' : 'text-slate-300'}">🏋️</span>
            <span class="ml-1 text-slate-500">(${habitsCount}/5)</span>
          </div>
        </td>
        <td class="py-3 px-3 text-slate-500 max-w-xs truncate" title="${l.notes || ''}">${l.notes || '-'}</td>
      </tr>
    `;
  }).join('');
}

// --- 每週量測匯總表格渲染 ---
function renderWeeklySummaryTable() {
  const tbody = document.getElementById('weeklySummaryTableBody');
  if (!tbody) return;

  const defaultRows = [
    { week: '現況 (基線)', targetW: '86.0', targetLean: '61.1', targetBf: '28.9%' },
    { week: 'W1', targetW: '建立基線', targetLean: '≥ 60.5', targetBf: '照常飲食校準' },
    { week: 'W2', targetW: '~85.5', targetLean: '≥ 60.5', targetBf: '雙預算啟動' },
    { week: 'W3', targetW: '~84.8', targetLean: '≥ 60.5', targetBf: '午餐減碳' },
    { week: 'W4 (目標)', targetW: '84.2~84.6', targetLean: '≥ 60.5', targetBf: '27.4~27.7%' }
  ];

  tbody.innerHTML = defaultRows.map(def => {
    const matched = appState.weeklyLogs.find(w => w.weekName.includes(def.week.split(' ')[0]));
    const isBaseline = def.week.includes('現況');
    const isSafe = matched ? (matched.leanMass >= BASELINE.leanMassSafetyThreshold) : true;

    return `
      <tr class="border-b border-slate-100 dark:border-slate-800 text-sm ${isBaseline ? 'bg-slate-50/70 dark:bg-slate-800/30' : ''}">
        <td class="py-3 px-4 font-bold text-slate-900 dark:text-white">${def.week}</td>
        <td class="py-3 px-4 font-semibold">${matched && matched.avgWeight ? `${matched.avgWeight} kg` : `<span class="text-slate-400">${def.targetW}</span>`}</td>
        <td class="py-3 px-4">${matched && matched.bodyFat ? `${matched.bodyFat} %` : `<span class="text-slate-400">${def.targetBf}</span>`}</td>
        <td class="py-3 px-4 font-bold ${isSafe ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}">
          ${matched && matched.leanMass ? `${matched.leanMass} kg ${isSafe ? '🛡️' : '⚠️'}` : `<span class="text-slate-400">${def.targetLean}</span>`}
        </td>
        <td class="py-3 px-4">${matched && matched.waist ? `${matched.waist} cm` : '<span class="text-slate-400">待測</span>'}</td>
        <td class="py-3 px-4">${matched && matched.avgSteps ? `${matched.avgSteps.toLocaleString()} 步` : '<span class="text-slate-400">-</span>'}</td>
        <td class="py-3 px-4">${matched && matched.avgSleep ? matched.avgSleep : '<span class="text-slate-400">-</span>'}</td>
        <td class="py-3 px-4">${matched && matched.avgEnergy ? `${matched.avgEnergy} 分` : '<span class="text-slate-400">-</span>'}</td>
      </tr>
    `;
  }).join('');
}

// --- Chart.js 圖表渲染 ---
function renderCharts() {
  if (typeof Chart === 'undefined') return;

  const dates = appState.dailyLogs.map(l => l.date.substring(5)); // 'MM-DD'
  const weights = appState.dailyLogs.map(l => l.weight || null);
  const steps = appState.dailyLogs.map(l => l.steps || null);
  const energies = appState.dailyLogs.map(l => l.energy || null);

  // 1. 體重與 7 日均重折線圖
  const ctxWeight = document.getElementById('weightTrendChart');
  if (ctxWeight) {
    if (appState.charts.weightChart) appState.charts.weightChart.destroy();

    // 計算 7 日滑動均線
    const movingAvg = [];
    for (let i = 0; i < appState.dailyLogs.length; i++) {
      const slice = appState.dailyLogs.slice(Math.max(0, i - 6), i + 1).filter(l => l.weight > 0);
      if (slice.length > 0) {
        const avg = slice.reduce((sum, l) => sum + Number(l.weight), 0) / slice.length;
        movingAvg.push(parseFloat(avg.toFixed(2)));
      } else {
        movingAvg.push(null);
      }
    }

    appState.charts.weightChart = new Chart(ctxWeight, {
      type: 'line',
      data: {
        labels: dates,
        datasets: [
          {
            label: '每日晨起體重 (kg)',
            data: weights,
            borderColor: '#0d9488',
            backgroundColor: 'rgba(13, 148, 136, 0.1)',
            borderWidth: 2,
            tension: 0.2,
            pointRadius: 4,
            pointBackgroundColor: '#0d9488'
          },
          {
            label: '7 日滑動平均線',
            data: movingAvg,
            borderColor: '#f59e0b',
            borderWidth: 3,
            borderDash: [5, 5],
            fill: false,
            tension: 0.3,
            pointRadius: 0
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top' },
          tooltip: {
            callbacks: {
              label: (ctx) => `${ctx.dataset.label}: ${ctx.parsed.y} kg`
            }
          }
        },
        scales: {
          y: {
            suggestedMin: 83.5,
            suggestedMax: 87.0
          }
        }
      }
    });
  }

  // 2. 瘦體重 vs 脂肪重 長條圖 (依每週測量)
  const ctxComp = document.getElementById('bodyCompChart');
  if (ctxComp) {
    if (appState.charts.bodyCompChart) appState.charts.bodyCompChart.destroy();

    const wLabels = appState.weeklyLogs.map(w => w.weekName);
    const leanData = appState.weeklyLogs.map(w => w.leanMass || 0);
    const fatData = appState.weeklyLogs.map(w => {
      if (w.avgWeight && w.leanMass) {
        return parseFloat((w.avgWeight - w.leanMass).toFixed(1));
      }
      return 0;
    });

    appState.charts.bodyCompChart = new Chart(ctxComp, {
      type: 'bar',
      data: {
        labels: wLabels,
        datasets: [
          {
            label: '瘦體重 (kg) - 需守住 ≥60.5kg',
            data: leanData,
            backgroundColor: '#0ea5e9'
          },
          {
            label: '脂肪重 (kg) - 減重目標來源',
            data: fatData,
            backgroundColor: '#f43f5e'
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top' }
        },
        scales: {
          x: { stacked: true },
          y: { stacked: true, suggestedMax: 90 }
        }
      }
    });
  }

  // 3. 步數與精力相關分析圖
  const ctxEnergy = document.getElementById('energyStepsChart');
  if (ctxEnergy) {
    if (appState.charts.energyStepsChart) appState.charts.energyStepsChart.destroy();

    appState.charts.energyStepsChart = new Chart(ctxEnergy, {
      type: 'line',
      data: {
        labels: dates,
        datasets: [
          {
            label: '精力評分 (1-10)',
            data: energies,
            borderColor: '#8b5cf6',
            backgroundColor: '#8b5cf6',
            yAxisID: 'y1',
            tension: 0.3,
            pointRadius: 4
          },
          {
            label: '步數 (步)',
            data: steps,
            borderColor: '#10b981',
            backgroundColor: 'rgba(16, 185, 129, 0.2)',
            type: 'bar',
            yAxisID: 'y',
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top' }
        },
        scales: {
          y: {
            type: 'linear',
            position: 'left',
            suggestedMax: 12000,
            title: { display: true, text: '步數' }
          },
          y1: {
            type: 'linear',
            position: 'right',
            min: 0,
            max: 10,
            grid: { drawOnChartArea: false },
            title: { display: true, text: '精力 (1-10)' }
          }
        }
      }
    });
  }
}

// --- 阻力訓練計時器邏輯 ---
function toggleWorkoutTimer() {
  const btn = document.getElementById('timerToggleBtn');
  if (appState.timerRunning) {
    clearInterval(appState.workoutTimer);
    appState.timerRunning = false;
    if (btn) btn.textContent = '▶ 開始 60 秒休息計時';
  } else {
    appState.timerRunning = true;
    if (btn) btn.textContent = '⏸ 暫停計時';
    appState.workoutTimer = setInterval(() => {
      appState.timerSecondsRemaining--;
      updateTimerDisplay();
      if (appState.timerSecondsRemaining <= 0) {
        clearInterval(appState.workoutTimer);
        appState.timerRunning = false;
        appState.timerSecondsRemaining = 60;
        if (btn) btn.textContent = '▶ 開始 60 秒休息計時';
        playBeep();
        showToast('🔔 60 秒休息結束，準備下一組！', 'info');
      }
    }, 1000);
  }
}

function resetWorkoutTimer() {
  clearInterval(appState.workoutTimer);
  appState.timerRunning = false;
  appState.timerSecondsRemaining = 60;
  updateTimerDisplay();
  const btn = document.getElementById('timerToggleBtn');
  if (btn) btn.textContent = '▶ 開始 60 秒休息計時';
}

function updateTimerDisplay() {
  const display = document.getElementById('timerDisplay');
  if (display) {
    const sec = appState.timerSecondsRemaining;
    display.textContent = `00:${sec < 10 ? '0' : ''}${sec}`;
  }
}

function playBeep() {
  try {
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = 'sine';
    osc.frequency.value = 800;
    gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.start();
    osc.stop(audioCtx.currentTime + 0.3);
  } catch (e) {
    console.log('AudioContext not supported or allowed', e);
  }
}

// --- Google Apps Script 雲端同步功能 ---
function saveGasSettings() {
  const input = document.getElementById('gasApiUrl');
  if (!input) return;
  const url = input.value.trim();
  appState.gasUrl = url;
  localStorage.setItem(STORAGE_KEYS.GAS_URL, url);
  updateGasStatusBadge(!!url);
  showToast('✅ Google Apps Script 網址已儲存！', 'success');
}

function updateGasStatusBadge(isConnected) {
  const badge = document.getElementById('gasStatusHeaderBadge');
  if (!badge) return;
  if (isConnected) {
    badge.className = 'inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800';
    badge.innerHTML = `<span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span> 雲端已連線`;
  } else {
    badge.className = 'inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400 border border-slate-200 dark:border-slate-700';
    badge.innerHTML = `<span class="w-2 h-2 rounded-full bg-slate-400"></span> 本地儲存模式`;
  }
}

async function testGasConnection() {
  if (!appState.gasUrl) {
    showToast('⚠️ 請先輸入 Google Apps Script Web App URL！', 'warning');
    return;
  }

  showToast('🔄 正在測試 Google Sheet 連線...', 'info');
  try {
    const res = await fetch(appState.gasUrl, { method: 'GET', mode: 'cors' });
    const json = await res.json();
    if (json.status === 'success') {
      showToast('🎉 連線成功！Google Sheet 運作正常', 'success');
      updateGasStatusBadge(true);
    } else {
      showToast(`⚠️ 連線回應：${json.message}`, 'warning');
    }
  } catch (err) {
    console.error('GAS connection error', err);
    showToast('❌ 連線失敗，請檢查 URL 是否正確部署且權限為「所有人」', 'danger');
  }
}

async function syncSingleDailyToGas(logEntry) {
  if (!appState.gasUrl) return;
  try {
    await fetch(appState.gasUrl, {
      method: 'POST',
      mode: 'no-cors', // Apps Script POST often requires no-cors on simple redirects
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type: 'daily', action: 'save_daily', data: logEntry })
    });
    console.log('Daily log synced to Google Sheet');
  } catch (err) {
    console.error('Failed to sync daily log to GAS', err);
  }
}

async function syncSingleWeeklyToGas(weeklyEntry) {
  if (!appState.gasUrl) return;
  try {
    await fetch(appState.gasUrl, {
      method: 'POST',
      mode: 'no-cors',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ type: 'weekly', action: 'save_weekly', data: weeklyEntry })
    });
    console.log('Weekly log synced to Google Sheet');
  } catch (err) {
    console.error('Failed to sync weekly log to GAS', err);
  }
}

async function pushAllDataToGas() {
  if (!appState.gasUrl) {
    showToast('⚠️ 請先輸入 Google Apps Script 網址！', 'warning');
    return;
  }

  showToast('⏳ 正在批次上傳全部資料至 Google Sheet...', 'info');
  try {
    await fetch(appState.gasUrl, {
      method: 'POST',
      mode: 'no-cors',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        action: 'batch_sync',
        dailyLogs: appState.dailyLogs,
        weeklyLogs: appState.weeklyLogs
      })
    });
    showToast('🎉 本地歷史紀錄已全數推送至 Google Sheet！', 'success');
  } catch (err) {
    console.error('Push error', err);
    showToast('❌ 上傳失敗，請檢查網路或腳本設定', 'danger');
  }
}

async function pullDataFromGas() {
  if (!appState.gasUrl) {
    showToast('⚠️ 請先輸入 Google Apps Script 網址！', 'warning');
    return;
  }

  showToast('⏳ 正在從 Google Sheet 載入最新數據...', 'info');
  try {
    const res = await fetch(appState.gasUrl, { method: 'GET', mode: 'cors' });
    const json = await res.json();
    if (json.status === 'success' && json.data) {
      if (json.data.daily && json.data.daily.length > 0) {
        // 轉換欄位格式
        appState.dailyLogs = json.data.daily.map(d => ({
          date: d['日期'] || '',
          weight: d['晨起體重(kg)'] ? Number(d['晨起體重(kg)']) : '',
          sleepTime: d['昨晚入睡時間'] || '',
          steps: d['今日步數'] ? Number(d['今日步數']) : '',
          energy: d['今日精力(1-10)'] ? Number(d['今日精力(1-10)']) : 8,
          dayType: d['日子型態'] || '平日 (1800kcal)',
          habitBreakfast: d['早餐40g蛋白'] === '✓',
          habitLunchOrder: d['午餐順序/減碳'] === '✓',
          habitCaffeineCutoff: d['15:00咖啡因斷點'] === '✓',
          habitSocialRules: d['應酬3硬規則'] === '✓',
          habitWorkout: d['阻力訓練完成'] === '✓',
          notes: d['備註'] || ''
        }));
        saveLocalDaily();
      }

      if (json.data.weekly && json.data.weekly.length > 0) {
        appState.weeklyLogs = json.data.weekly.map(w => ({
          weekName: w['週次'] || '',
          date: w['量測日期'] || '',
          avgWeight: w['7日均體重(kg)'] ? Number(w['7日均體重(kg)']) : '',
          bodyFat: w['體脂率(%)'] ? Number(w['體脂率(%)']) : '',
          leanMass: w['瘦體重(kg)'] ? Number(w['瘦體重(kg)']) : '',
          waist: w['腰圍(cm)'] ? Number(w['腰圍(cm)']) : '',
          avgSteps: w['平均步數'] ? Number(w['平均步數']) : '',
          avgSleep: w['平均入睡'] || '',
          avgEnergy: w['平均精力'] ? Number(w['平均精力']) : '',
          statusAssessment: w['保肌狀態評估'] || '',
          notes: w['備註'] || ''
        }));
        saveLocalWeekly();
      }

      renderAll();
      showToast('🎉 已成功從 Google Sheet 下載並同步資料！', 'success');
    } else {
      showToast('⚠️ Google Sheet 中尚未有足夠資料', 'warning');
    }
  } catch (err) {
    console.error('Pull error', err);
    showToast('❌ 下載失敗，請檢查 GAS 部署權限是否設為所有人', 'danger');
  }
}

// --- 複製 GAS 代碼 ---
function copyGasScriptCode() {
  const code = `/**
 * David 精力維持計畫 v1.0 - Google Apps Script 雲端同步後端
 */
const SHEET_NAME_DAILY = '每日打卡紀錄';
const SHEET_NAME_WEEKLY = '每週測量數據';

function doGet(e) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    initSheetsIfNotExist(ss);
    const dailySheet = ss.getSheetByName(SHEET_NAME_DAILY);
    const weeklySheet = ss.getSheetByName(SHEET_NAME_WEEKLY);
    return ContentService.createTextOutput(JSON.stringify({
      status: 'success',
      data: { daily: getSheetRows(dailySheet), weekly: getSheetRows(weeklySheet) }
    })).setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ status: 'error', message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doPost(e) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    initSheetsIfNotExist(ss);
    let p = e.postData && e.postData.contents ? JSON.parse(e.postData.contents) : (e.parameter || {});
    const action = p.action || (p.type === 'weekly' ? 'save_weekly' : 'save_daily');
    const ts = Utilities.formatDate(new Date(), "Asia/Taipei", "yyyy-MM-dd HH:mm:ss");

    if (action === 'save_daily' || p.type === 'daily') {
      const s = ss.getSheetByName(SHEET_NAME_DAILY);
      const d = p.data || p;
      const r = [d.date, d.weight, d.sleepTime, d.steps, d.energy, d.dayType, d.habitBreakfast ? '✓':'-', d.habitLunchOrder ? '✓':'-', d.habitCaffeineCutoff ? '✓':'-', d.habitSocialRules ? '✓':'-', d.habitWorkout ? '✓':'-', d.notes, ts];
      const idx = findRowIndex(s, d.date, 0);
      if (idx > 0) s.getRange(idx, 1, 1, r.length).setValues([r]); else s.appendRow(r);
      return ContentService.createTextOutput(JSON.stringify({ status: 'success' })).setMimeType(ContentService.MimeType.JSON);
    }
    if (action === 'save_weekly' || p.type === 'weekly') {
      const s = ss.getSheetByName(SHEET_NAME_WEEKLY);
      const d = p.data || p;
      const st = (d.leanMass && d.leanMass >= 60.5) ? '合格保肌 (≥60.5kg)' : '需警惕 (<60.5kg)';
      const r = [d.weekName, d.date, d.avgWeight, d.bodyFat, d.leanMass, d.waist, d.avgSteps, d.avgSleep, d.avgEnergy, st, d.notes, ts];
      const idx = findRowIndex(s, d.weekName, 0);
      if (idx > 0) s.getRange(idx, 1, 1, r.length).setValues([r]); else s.appendRow(r);
      return ContentService.createTextOutput(JSON.stringify({ status: 'success' })).setMimeType(ContentService.MimeType.JSON);
    }
    if (action === 'batch_sync') {
      const sd = ss.getSheetByName(SHEET_NAME_DAILY);
      const sw = ss.getSheetByName(SHEET_NAME_WEEKLY);
      (p.dailyLogs || []).forEach(d => {
        const r = [d.date, d.weight, d.sleepTime, d.steps, d.energy, d.dayType, d.habitBreakfast ? '✓':'-', d.habitLunchOrder ? '✓':'-', d.habitCaffeineCutoff ? '✓':'-', d.habitSocialRules ? '✓':'-', d.habitWorkout ? '✓':'-', d.notes, ts];
        const idx = findRowIndex(sd, d.date, 0);
        if (idx > 0) sd.getRange(idx, 1, 1, r.length).setValues([r]); else sd.appendRow(r);
      });
      (p.weeklyLogs || []).forEach(w => {
        const st = (w.leanMass && w.leanMass >= 60.5) ? '合格保肌 (≥60.5kg)' : '需警惕 (<60.5kg)';
        const r = [w.weekName, w.date, w.avgWeight, w.bodyFat, w.leanMass, w.waist, w.avgSteps, w.avgSleep, w.avgEnergy, st, w.notes, ts];
        const idx = findRowIndex(sw, w.weekName, 0);
        if (idx > 0) sw.getRange(idx, 1, 1, r.length).setValues([r]); else sw.appendRow(r);
      });
      return ContentService.createTextOutput(JSON.stringify({ status: 'success' })).setMimeType(ContentService.MimeType.JSON);
    }
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ status: 'error', message: err.toString() })).setMimeType(ContentService.MimeType.JSON);
  }
}

function initSheetsIfNotExist(ss) {
  if (!ss.getSheetByName(SHEET_NAME_DAILY)) {
    const s = ss.insertSheet(SHEET_NAME_DAILY, 0);
    s.getRange(1, 1, 1, 13).setValues([['日期', '晨起體重(kg)', '昨晚入睡時間', '今日步數', '今日精力(1-10)', '日子型態', '早餐40g蛋白', '午餐順序/減碳', '15:00咖啡因斷點', '應酬3硬規則', '阻力訓練完成', '備註', '最後同步時間']]);
    s.getRange(1, 1, 1, 13).setBackground('#0f766e').setFontColor('#ffffff').setFontWeight('bold');
    s.setFrozenRows(1);
  }
  if (!ss.getSheetByName(SHEET_NAME_WEEKLY)) {
    const s = ss.insertSheet(SHEET_NAME_WEEKLY, 1);
    s.getRange(1, 1, 1, 12).setValues([['週次', '量測日期', '7日均體重(kg)', '體脂率(%)', '瘦體重(kg)', '腰圍(cm)', '平均步數', '平均入睡', '平均精力', '保肌狀態評估', '備註', '最後同步時間']]);
    s.getRange(1, 1, 1, 12).setBackground('#1e3a8a').setFontColor('#ffffff').setFontWeight('bold');
    s.setFrozenRows(1);
  }
}

function findRowIndex(sheet, target, colIdx) {
  const d = sheet.getDataRange().getValues();
  for (let i = 1; i < d.length; i++) {
    let val = d[i][colIdx];
    if (val instanceof Date) val = Utilities.formatDate(val, "Asia/Taipei", "yyyy-MM-dd");
    if (String(val).substring(0, 10) === String(target).substring(0, 10)) return i + 1;
  }
  return -1;
}

function getSheetRows(sheet) {
  if (!sheet) return [];
  const d = sheet.getDataRange().getValues();
  if (d.length <= 1) return [];
  const h = d[0], res = [];
  for (let i = 1; i < d.length; i++) {
    const o = {};
    for (let j = 0; j < h.length; j++) {
      let v = d[i][j];
      if (v instanceof Date) v = Utilities.formatDate(v, "Asia/Taipei", "yyyy-MM-dd");
      o[h[j]] = v;
    }
    res.push(o);
  }
  return res;
}`;

  navigator.clipboard.writeText(code).then(() => {
    showToast('📋 Google Apps Script 代碼已複製到剪貼簿！', 'success');
  }).catch(() => {
    showToast('⚠️ 複製失敗，請手動開啟 GoogleAppsScript.js 複製', 'warning');
  });
}

// --- 備份與匯出 CSV ---
function exportCSV() {
  let csv = '日期,晨起體重(kg),昨晚入睡時間,今日步數,今日精力,日子型態,早餐40g蛋白,午餐順序減碳,15點咖啡因斷點,應酬3規則,阻力訓練,備註\n';
  appState.dailyLogs.forEach(l => {
    csv += `"${l.date}","${l.weight || ''}","${l.sleepTime || ''}","${l.steps || ''}","${l.energy || ''}","${l.dayType || ''}","${l.habitBreakfast ? 'Y' : 'N'}","${l.habitLunchOrder ? 'Y' : 'N'}","${l.habitCaffeineCutoff ? 'Y' : 'N'}","${l.habitSocialRules ? 'Y' : 'N'}","${l.habitWorkout ? 'Y' : 'N'}","${(l.notes || '').replace(/"/g, '""')}"\n`;
  });

  const blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', `David_精力維持打卡紀錄_${getTodayDateStr()}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  showToast('💾 CSV 紀錄檔已下載！', 'success');
}

// --- 通用 Modal 彈窗控制 ---
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('hidden');
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('hidden');
  }
}

// --- Toast 提示通知 ---
function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  const colors = {
    success: 'bg-emerald-600 text-white',
    warning: 'bg-amber-600 text-white',
    danger: 'bg-rose-600 text-white',
    info: 'bg-slate-800 text-white'
  };

  toast.className = `flex items-center gap-2 px-4 py-3 rounded-xl shadow-lg text-sm font-medium transition-all duration-300 transform translate-y-2 opacity-0 ${colors[type] || colors.info}`;
  toast.textContent = message;

  container.appendChild(toast);
  setTimeout(() => {
    toast.classList.remove('translate-y-2', 'opacity-0');
  }, 10);

  setTimeout(() => {
    toast.classList.add('opacity-0', 'translate-y-2');
    setTimeout(() => {
      toast.remove();
    }, 300);
  }, 3500);
}

// --- 簡易撒花效果 ---
function triggerConfetti() {
  if (typeof confetti === 'function') {
    confetti({
      particleCount: 50,
      spread: 60,
      origin: { y: 0.7 }
    });
  }
}
