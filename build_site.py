# -*- coding: utf-8 -*-
"""
Generate index.html (Portal & Knowledge Base) and slides.html (Presentation Deck)
"""
import os
import json

base_dir = r"g:\我的雲端硬碟\0_AI Agent\Obsidian\DavidCloud\大衛人生\B3. 健康養生\B3.1 精力體態"

# HTML Template for index.html (Portal & Knowledge Base Hub)
index_html_content = '''<!DOCTYPE html>
<html lang="zh-TW" class="scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>大衛人生 · 精力管理知識門戶 | 得到大腦知識庫與高管行動系統</title>
  <meta name="description" content="專為1978年次（48歲）企業高階經理人量身打造的極限精力重塑系統，整合協和醫學博士張遇升《怎樣成為精力管理的高手》與得到大腦知識庫，具備即時關鍵字搜尋與互動簡報展示。">
  
  <!-- Google Fonts & Tailwind CSS CDN -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Noto+Sans+TC:wght@300;400;500;600;700;900&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  
  <!-- Phosphor Icons CDN -->
  <script src="https://unpkg.com/@phosphor-icons/web"></script>
  
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', '"Noto Sans TC"', 'sans-serif'],
          },
          colors: {
            brand: {
              50: '#ecfdf5',
              100: '#d1fae5',
              200: '#a7f3d0',
              300: '#6ee7b7',
              400: '#34d399',
              500: '#10b981',
              600: '#059669',
              700: '#047857',
              800: '#065f46',
              900: '#064e3b',
              950: '#022c22',
            },
            executive: {
              50: '#f8fafc',
              100: '#f1f5f9',
              200: '#e2e8f0',
              700: '#334155',
              800: '#1e293b',
              900: '#0f172a',
              950: '#090d16',
            },
            gold: {
              400: '#fbbf24',
              500: '#f59e0b',
              600: '#d97706',
            }
          }
        }
      }
    }
  </script>
  <style>
    /* Custom scrollbar and subtle glowing highlights */
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: #0f172a; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #10b981; }
    .glass-card {
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .glass-card:hover {
      border-color: rgba(16, 185, 129, 0.35);
    }
    .executive-gradient {
      background: linear-gradient(135deg, #090d16 0%, #0f172a 50%, #064e3b 100%);
    }
    .gold-border {
      border: 1px solid rgba(245, 158, 11, 0.3);
    }
    mark.highlight-match {
      background: rgba(245, 158, 11, 0.3);
      color: #fef08a;
      padding: 0 3px;
      border-radius: 2px;
    }
  </style>
</head>
<body class="bg-executive-950 text-slate-100 min-h-screen selection:bg-brand-500 selection:text-white">

  <!-- Top Navigation Header -->
  <header class="sticky top-0 z-50 glass-card border-b border-slate-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        
        <!-- Logo & Brand -->
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-600 to-emerald-400 flex items-center justify-center text-white shadow-lg shadow-brand-500/20">
            <i class="ph-bold ph-lightning text-xl"></i>
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="font-extrabold text-lg tracking-tight text-white">大衛人生</span>
              <span class="text-xs px-2 py-0.5 rounded-full bg-brand-500/10 text-brand-400 border border-brand-500/20 font-semibold">B3.1 精力體態</span>
            </div>
            <p class="text-xs text-slate-400">得到大腦知識門戶 · 1978高管決策系統</p>
          </div>
        </div>

        <!-- Desktop Nav Links -->
        <nav class="hidden md:flex items-center gap-1 text-sm font-medium text-slate-300">
          <a href="#overview" class="px-3 py-2 rounded-lg hover:text-white hover:bg-slate-800/60 transition">首頁總覽</a>
          <a href="#search-section" class="px-3 py-2 rounded-lg hover:text-white hover:bg-slate-800/60 transition">
            <i class="ph ph-magnifying-glass mr-1 text-brand-400"></i>知識庫檢索
          </a>
          <a href="slides.html" class="px-3 py-2 rounded-lg text-emerald-400 hover:text-emerald-300 hover:bg-brand-500/10 transition font-semibold">
            <i class="ph-bold ph-presentation mr-1"></i>互動簡報 (15頁)
          </a>
          <a href="#executive-part" class="px-3 py-2 rounded-lg text-gold-400 hover:text-gold-300 hover:bg-gold-500/10 transition font-semibold">
            <i class="ph-bold ph-crown mr-1"></i>1978 高管專章
          </a>
          <a href="#future-expansion" class="px-3 py-2 rounded-lg hover:text-white hover:bg-slate-800/60 transition">未來擴充庫</a>
          <a href="tracker.html" class="ml-2 px-3.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold flex items-center gap-1.5 border border-slate-700 transition shadow-sm">
            <i class="ph-bold ph-chart-line-up text-brand-400"></i>4週追蹤儀表板
          </a>
        </nav>

        <!-- Quick Action Button -->
        <div class="flex items-center gap-3">
          <a href="slides.html" class="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-brand-600 to-emerald-500 hover:from-brand-500 hover:to-emerald-400 text-white text-sm font-semibold shadow-lg shadow-brand-600/30 transition transform hover:-translate-y-0.5">
            <i class="ph-bold ph-presentation text-base"></i>
            <span>進入簡報模式</span>
          </a>
        </div>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section id="overview" class="relative pt-12 pb-20 overflow-hidden border-b border-slate-800/80">
    <div class="absolute inset-0 bg-[radial-gradient(circle_at_30%_30%,rgba(16,185,129,0.08),transparent_50%)] pointer-events-none"></div>
    <div class="absolute inset-0 bg-[radial-gradient(circle_at_75%_60%,rgba(245,158,11,0.05),transparent_50%)] pointer-events-none"></div>
    
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
        
        <!-- Hero Text -->
        <div class="lg:col-span-7">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800/90 border border-slate-700 text-slate-300 text-xs font-medium mb-5">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
            <span>得到大腦知識庫 · 張遇升 MD/MBA 醫學底層架構</span>
          </div>

          <h1 class="text-3xl sm:text-4xl lg:text-5xl font-black text-white tracking-tight leading-[1.2] mb-5">
            從精力枯竭到巔峰駕馭：<br>
            <span class="bg-gradient-to-r from-emerald-400 via-teal-300 to-amber-300 bg-clip-text text-transparent">
              企業高階經理人極限精力系統
            </span>
          </h1>

          <p class="text-base sm:text-lg text-slate-300 leading-relaxed mb-8 max-w-2xl">
            專為 <span class="text-gold-400 font-bold">1978 年次（48 歲）</span> 企業高階主管量身打造。時間是剛性的，精力卻如同肌肉般可持續訓練。將身體視為 F1 賽車底盤，重塑體能、情緒、注意力與意義感四層金字塔，守護高質量決策頻寬。
          </p>

          <!-- Action Buttons -->
          <div class="flex flex-wrap items-center gap-4 mb-10">
            <a href="slides.html" class="inline-flex items-center gap-2.5 px-6 py-3.5 rounded-xl bg-gradient-to-r from-brand-600 to-emerald-500 hover:from-brand-500 hover:to-emerald-400 text-white font-bold text-sm shadow-xl shadow-brand-500/25 transition transform hover:-translate-y-0.5">
              <i class="ph-bold ph-play text-lg"></i>
              <span>播放互動簡報 (全圖解 15 頁)</span>
            </a>
            <a href="#executive-part" class="inline-flex items-center gap-2 px-5 py-3.5 rounded-xl bg-slate-800/80 hover:bg-slate-700/80 text-gold-300 font-semibold text-sm border border-gold-500/30 transition">
              <i class="ph-bold ph-crown text-base text-gold-400"></i>
              <span>閱讀 48 歲專章思考架構</span>
            </a>
            <a href="#search-section" class="inline-flex items-center gap-2 px-4 py-3.5 rounded-xl bg-slate-900/60 hover:bg-slate-800 text-slate-300 text-sm font-medium border border-slate-700 transition">
              <i class="ph ph-magnifying-glass text-base"></i>
              <span>檢索 13 講知識庫</span>
            </a>
          </div>

          <!-- Feature Metric Badges -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-4 border-t border-slate-800">
            <div class="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
              <div class="text-2xl font-black text-emerald-400">4 層</div>
              <div class="text-xs text-slate-400 mt-0.5">精力金字塔模型</div>
            </div>
            <div class="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
              <div class="text-2xl font-black text-amber-400">13 講</div>
              <div class="text-xs text-slate-400 mt-0.5">得到完整精讀筆記</div>
            </div>
            <div class="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
              <div class="text-2xl font-black text-sky-400">15 頁</div>
              <div class="text-xs text-slate-400 mt-0.5">逐頁圖解顧問簡報</div>
            </div>
            <div class="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
              <div class="text-2xl font-black text-purple-400">100%</div>
              <div class="text-xs text-slate-400 mt-0.5">循證醫學可落地</div>
            </div>
          </div>
        </div>

        <!-- Hero Visual Showcase -->
        <div class="lg:col-span-5">
          <div class="relative group">
            <div class="absolute -inset-1 bg-gradient-to-r from-emerald-500 to-amber-500 rounded-3xl blur-xl opacity-25 group-hover:opacity-40 transition duration-1000"></div>
            <div class="relative rounded-2xl overflow-hidden border border-slate-700 glass-card p-2 shadow-2xl">
              <img src="https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=1000&q=80" alt="Executive Vitality" class="w-full h-80 object-cover rounded-xl filter brightness-95">
              <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/40 to-transparent flex flex-col justify-end p-6">
                <span class="inline-block px-2.5 py-1 rounded bg-brand-500/20 text-brand-300 text-xs font-semibold w-max mb-2 border border-brand-500/30">
                  得到：怎樣成為精力管理的高手
                </span>
                <h3 class="text-lg font-bold text-white mb-1">主講人：張遇升 醫師</h3>
                <p class="text-xs text-slate-300 leading-relaxed">
                  北京協和醫學院醫學博士 · 約翰霍普金斯公共衛生/MBA雙碩士 · 曾輔導眾多上市公司董事長與企業家建立終身極限精力。
                </p>
                <div class="mt-4 flex items-center justify-between pt-3 border-t border-slate-800">
                  <span class="text-xs text-slate-400 flex items-center gap-1">
                    <i class="ph-bold ph-check-circle text-emerald-400"></i>已全面整合至大衛人生知識庫
                  </span>
                  <a href="slides.html" class="text-xs text-brand-400 hover:text-brand-300 font-semibold flex items-center gap-1">
                    點擊開啟簡報 <i class="ph-bold ph-arrow-right"></i>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </section>

  <!-- Interactive Search & Filter Section -->
  <section id="search-section" class="py-12 bg-slate-900/50 border-b border-slate-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-8">
        <div>
          <div class="flex items-center gap-2 text-xs font-bold text-brand-400 uppercase tracking-wider mb-1">
            <i class="ph-bold ph-magnifying-glass"></i> Instant Knowledge Retrieval
          </div>
          <h2 class="text-2xl font-black text-white tracking-tight">
            知識庫智慧檢索中心
          </h2>
          <p class="text-sm text-slate-400">即時檢索 13 講課程精華、醫學機制、1978 高管心法與日常行動指引</p>
        </div>
        
        <!-- Live Count Indicator -->
        <div id="search-stats" class="text-xs font-semibold text-slate-400 bg-slate-800/80 px-3 py-1.5 rounded-lg border border-slate-700">
          顯示中：<span id="matched-count" class="text-brand-400 font-bold">13</span> / 13 篇知識模組
        </div>
      </div>

      <!-- Search Input Bar -->
      <div class="relative mb-6">
        <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-slate-400 text-lg">
          <i class="ph-bold ph-magnifying-glass"></i>
        </div>
        <input 
          type="text" 
          id="search-input" 
          placeholder="輸入關鍵字檢索，例如：海馬體、幽門螺旋桿菌、48歲、血糖、深睡、熱啟動、ONQI、深蹲、西點軍校..."
          class="w-full pl-12 pr-12 py-3.5 rounded-xl bg-slate-800/90 border border-slate-700 focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 text-white placeholder-slate-400 text-sm transition outline-none shadow-inner"
        >
        <button id="clear-search" class="hidden absolute inset-y-0 right-0 pr-4 flex items-center text-slate-400 hover:text-white transition">
          <i class="ph-bold ph-x-circle text-lg"></i>
        </button>
      </div>

      <!-- Category Filter Chips -->
      <div class="flex flex-wrap items-center gap-2" id="filter-chips">
        <button class="filter-chip active px-3 py-1.5 rounded-lg text-xs font-semibold bg-brand-600 text-white transition" data-tag="ALL">全部模組</button>
        <button class="filter-chip px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition" data-tag="高管專章">👔 1978 高管專章</button>
        <button class="filter-chip px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition" data-tag="精力金字塔">🏛️ 精力金字塔</button>
        <button class="filter-chip px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition" data-tag="運動方案">🏃 體能與運動</button>
        <button class="filter-chip px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition" data-tag="血糖管理">🥗 能量飲食與水化</button>
        <button class="filter-chip px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition" data-tag="睡眠醫學">🌙 深度睡眠修復</button>
        <button class="filter-chip px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition" data-tag="情緒管理">🔥 情緒掌控與焦慮</button>
        <button class="filter-chip px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition" data-tag="行動清單">📋 全天行動清單</button>
      </div>

    </div>
  </section>

  <!-- Knowledge Modules Grid Section -->
  <section class="py-14">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <!-- Module Cards Container -->
      <div id="modules-container" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Rendered dynamically by JavaScript -->
      </div>

      <!-- Empty Search State -->
      <div id="empty-state" class="hidden py-16 text-center">
        <div class="w-16 h-16 mx-auto mb-4 rounded-2xl bg-slate-800 flex items-center justify-center text-slate-500 text-2xl">
          <i class="ph-bold ph-magnifying-glass"></i>
        </div>
        <h3 class="text-lg font-bold text-white mb-2">未找到符合「<span id="search-query-display" class="text-amber-400"></span>」的知識內容</h3>
        <p class="text-sm text-slate-400 mb-6">請嘗試其他關鍵字，例如「睡眠」、「海馬體」、「血糖」、「深蹲」、「熱啟動」</p>
        <button id="reset-search-btn" class="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition">
          重置搜尋條件
        </button>
      </div>

    </div>
  </section>

  <!-- DEDICATED EXECUTIVE CHAPTER (1978 高階經理人專章) -->
  <section id="executive-part" class="py-20 bg-gradient-to-b from-slate-900 via-executive-900 to-slate-950 border-t border-b border-amber-500/20 relative">
    <div class="absolute inset-0 bg-[radial-gradient(circle_at_50%_20%,rgba(245,158,11,0.06),transparent_60%)] pointer-events-none"></div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
      
      <!-- Executive Header Badge -->
      <div class="text-center max-w-3xl mx-auto mb-14">
        <div class="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-gold-500/10 border border-gold-500/30 text-gold-400 text-xs font-bold tracking-wider mb-4">
          <i class="ph-bold ph-crown text-sm"></i>
          <span>DEDICATED EXECUTIVE CHAPTER · 1978 特企</span>
        </div>
        <h2 class="text-3xl sm:text-4xl font-black text-white tracking-tight mb-4">
          1978 年次高階經理人：<br>
          <span class="bg-gradient-to-r from-amber-200 via-amber-400 to-emerald-400 bg-clip-text text-transparent">
            中年逆齡與極限精力突破指南
          </span>
        </h2>
        <p class="text-base text-slate-300 leading-relaxed">
          現年 48 歲，您正處於職場成就與家庭責任的最高峰，同時迎面撞上生理代謝與荷爾蒙的轉折暗礁。本專章為您重構底層心智模型，提供立即可落地的戰略行動代碼。
        </p>
      </div>

      <!-- Part A: 48歲生理與事業的雙重暗礁 -->
      <div class="glass-card rounded-2xl p-6 sm:p-8 mb-8 gold-border">
        <div class="flex items-center gap-3 mb-6">
          <div class="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center text-xl font-bold">
            <i class="ph-bold ph-warning-octagon"></i>
          </div>
          <div>
            <h3 class="text-xl font-bold text-white">暗礁剖析：48 歲經理人面臨的生理與環境夾擊</h3>
            <p class="text-xs text-slate-400">客觀生理規律 + 三明治世代重壓</p>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
            <div class="text-sm font-bold text-amber-400 mb-1">1. 代謝與荷爾蒙轉折</div>
            <p class="text-xs text-slate-300 leading-relaxed">
              基礎代謝率下降 15~20%，睪固酮與生長激素減退，肌肉每十年自然流失 3~8%，內臟脂肪極易堆積形成啤酒肚與脂肪肝。
            </p>
          </div>
          <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
            <div class="text-sm font-bold text-amber-400 mb-1">2. 認知海馬體萎縮</div>
            <p class="text-xs text-slate-300 leading-relaxed">
              30歲起海馬體每年自然萎縮 0.5%，48歲已累積近 9%。短期工作記憶帶寬縮窄，多工切換易引發嚴重決策疲勞。
            </p>
          </div>
          <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
            <div class="text-sm font-bold text-amber-400 mb-1">3. 深睡修復窗口縮減</div>
            <p class="text-xs text-slate-300 leading-relaxed">
              深層慢波睡眠佔比下降，夜醒次數增加。高壓與應酬飲酒進一步摧毀快速動眼期（REM），導致「晨起未充飽電」。
            </p>
          </div>
          <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800">
            <div class="text-sm font-bold text-amber-400 mb-1">4. 職場三明治蠟燭雙頭燒</div>
            <p class="text-xs text-slate-300 leading-relaxed">
              上有高齡父母、下有青少年子女，職場承擔千萬級營收戰略考核，外在要求達到人生頂點，時間管理已徹底失效。
            </p>
          </div>
        </div>
      </div>

      <!-- Part B: 經理人三大思考架構 (Mental Models) -->
      <div class="mb-10">
        <h3 class="text-xl font-bold text-white mb-6 flex items-center gap-2">
          <i class="ph-bold ph-brain text-emerald-400"></i>
          <span>思考架構：48 歲經理人三大高能心智模型 (Mental Models)</span>
        </h3>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          
          <!-- Model 1 -->
          <div class="glass-card rounded-2xl p-6 border-slate-800 hover:border-emerald-500/40 transition">
            <div class="w-12 h-12 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center text-2xl mb-4">
              <i class="ph-bold ph-car-profile"></i>
            </div>
            <h4 class="text-lg font-bold text-white mb-2">模型一：F1 賽車底盤觀</h4>
            <div class="text-xs font-semibold text-emerald-400 mb-3">The F1 Chassis Philosophy</div>
            <p class="text-xs text-slate-300 leading-relaxed mb-4">
              高管是賽車手，更是車隊經理。年度競爭如同 20 場 F1 大獎賽。獲勝的關鍵不是司機踩油門有多用力，而是賽車底盤、散熱器與輪胎的機械極限。定期進站換胎保養，才能跑完全程。
            </p>
            <div class="p-2.5 rounded-lg bg-slate-900 text-xs text-slate-400 border border-slate-800">
              <span class="text-white font-semibold">高管心法：</span> 不與年輕人比熬夜，比的是誰的底盤穩定度與能量利用效率更高。
            </div>
          </div>

          <!-- Model 2 -->
          <div class="glass-card rounded-2xl p-6 border-slate-800 hover:border-amber-500/40 transition">
            <div class="w-12 h-12 rounded-xl bg-amber-500/10 text-amber-400 flex items-center justify-center text-2xl mb-4">
              <i class="ph-bold ph-shield-check"></i>
            </div>
            <h4 class="text-lg font-bold text-white mb-2">模型二：認知帶寬保護法則</h4>
            <div class="text-xs font-semibold text-amber-400 mb-3">Cognitive Bandwidth Preservation</div>
            <p class="text-xs text-slate-300 leading-relaxed mb-4">
              高管的百萬年薪是為了每天「2~3 個牽動公司未來的關鍵戰略決策」而支付。絕不容許瑣碎郵件、下屬日常情緒或暴飲暴食引發的低血糖奪走前額葉頻寬。
            </p>
            <div class="p-2.5 rounded-lg bg-slate-900 text-xs text-slate-400 border border-slate-800">
              <span class="text-white font-semibold">高管心法：</span> 戰略清晰的第一步，是敢於對 90% 的低維資訊雜訊說「不」。
            </div>
          </div>

          <!-- Model 3 -->
          <div class="glass-card rounded-2xl p-6 border-slate-800 hover:border-sky-500/40 transition">
            <div class="w-12 h-12 rounded-xl bg-sky-500/10 text-sky-400 flex items-center justify-center text-2xl mb-4">
              <i class="ph-bold ph-chart-line-up"></i>
            </div>
            <h4 class="text-lg font-bold text-white mb-2">模型三：能量 ROI 投資觀</h4>
            <div class="text-xs font-semibold text-sky-400 mb-3">Energy Return on Investment</div>
            <p class="text-xs text-slate-300 leading-relaxed mb-4">
              每天投資 1.5 小時在精力管理（充足睡眠 7.5h、倒序進食、碎片化運動 30m、熱啟動 15m），產出的不是抽象的健康，而是每週多出 20 小時具備絕對清醒度的頂級戰鬥力。
            </p>
            <div class="p-2.5 rounded-lg bg-slate-900 text-xs text-slate-400 border border-slate-800">
              <span class="text-white font-semibold">高管心法：</span> 這是全宇宙回報率最高的投資，ROI 高達數百倍。
            </div>
          </div>

        </div>
      </div>

      <!-- Part C: 48歲高管極限行動手冊 (Action Playbook) -->
      <div class="glass-card rounded-2xl p-6 sm:p-8 gold-border mb-8">
        <h3 class="text-xl font-bold text-white mb-6 flex items-center gap-2">
          <i class="ph-bold ph-clipboard-text text-amber-400"></i>
          <span>行動手冊：48 歲經理人四大全天極限作戰 SOP (Action Playbook)</span>
        </h3>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          
          <!-- SOP 1: 晨間超能啟動 -->
          <div class="p-5 rounded-xl bg-slate-900/90 border border-slate-800">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-bold px-2 py-0.5 rounded bg-brand-500/20 text-brand-400 border border-brand-500/30">06:30 - 07:30</span>
              <span class="text-xs text-slate-400 font-medium">晨間儀軌</span>
            </div>
            <h4 class="text-base font-bold text-white mb-2">🌅 晨間高管超能啟動 SOP</h4>
            <ul class="text-xs text-slate-300 space-y-2">
              <li class="flex items-start gap-2">
                <i class="ph-bold ph-check text-brand-400 mt-0.5"></i>
                <span><strong>600ml 溫水補水：</strong>加少許海鹽或檸檬，打破整夜微脫水，激活腸胃供血。</span>
              </li>
              <li class="flex items-start gap-2">
                <i class="ph-bold ph-check text-brand-400 mt-0.5"></i>
                <span><strong>晨光照射 10 分鐘：</strong>戶外冷光照射，抑制褪黑素，錨定 14 小時後的入睡生理鐘。</span>
              </li>
              <li class="flex items-start gap-2">
                <i class="ph-bold ph-check text-brand-400 mt-0.5"></i>
                <span><strong>三大戰略決策錨定：</strong>手機備忘錄寫下今日最核心的 3 件事，想像達成場景。</span>
              </li>
              <li class="flex items-start gap-2">
                <i class="ph-bold ph-check text-brand-400 mt-0.5"></i>
                <span><strong>高蛋白低 GI 早餐：</strong>無糖豆漿/乳清 + 雞蛋 + 堅果燕麥，杜絕高熱量精緻包子。</span>
              </li>
            </ul>
          </div>

          <!-- SOP 2: 高壓會議戰場能量防禦 -->
          <div class="p-5 rounded-xl bg-slate-900/90 border border-slate-800">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-bold px-2 py-0.5 rounded bg-sky-500/20 text-sky-400 border border-sky-500/30">09:00 - 18:00</span>
              <span class="text-xs text-slate-400 font-medium">職場戰場</span>
            </div>
            <h4 class="text-base font-bold text-white mb-2">⚡ 高壓戰場日程能量防禦</h4>
            <ul class="text-xs text-slate-300 space-y-2">
              <li class="flex items-start gap-2">
                <i class="ph-bold ph-check text-sky-400 mt-0.5"></i>
                <span><strong>上午認知波峰：</strong>最棘手的戰略推演安排在 09:30~11:30，此時皮質醇與專注力處於頂點。</span>
              </li>
              <li class="flex items-start gap-2">
                <i class="ph-bold ph-check text-sky-400 mt-0.5"></i>
                <span><strong>倒序午餐法抗昏睡：</strong>嚴格遵循「深綠蔬菜一大碗 → 肉魚蛋白質 → 少量碳水」，七分飽。</span>
              </li>
              <li class="flex items-start gap-2">
                <i class="ph-bold ph-check text-sky-400 mt-0.5"></i>
                <span><strong>下午低谷破局：</strong>14:00 犯困時以冷水洗臉，插耳機邊走動邊打電話，絕不吃甜點。</span>
              </li>
              <li class="flex items-start gap-2">
                <i class="ph-bold ph-check text-sky-400 mt-0.5"></i>
                <span><strong>15:00 咖啡因硬斷點：</strong>下午三點後嚴格禁絕咖啡因，防止半衰期干擾深睡。</span>
              </li>
            </ul>
          </div>

          <!-- SOP 3: 商務應酬與差旅生存守則 -->
          <div class="p-5 rounded-xl bg-slate-900/90 border border-slate-800">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-bold px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 border border-amber-500/30">18:00 - 22:00</span>
              <span class="text-xs text-slate-400 font-medium">社交應酬</span>
            </div>
            <h4 class="text-base font-bold text-white mb-2">🍷 高管商務應酬與差旅生存</h4>
            <ul class="text-xs text-slate-300 space-y-2">
              <li class="flex items-start gap-2">
                <i class="ph-bold ph-check text-amber-400 mt-0.5"></i>
                <span><strong>胃黏膜防禦術：</strong>應酬前 30 分鐘飲用 300ml 溫水並吃 1 顆茶葉蛋或乳清蛋白，防止空腹吸收酒精。</span>
              </li>
              <li class="flex items-start gap-2">
                <i class="ph-bold ph-check text-amber-400 mt-0.5"></i>
                <span><strong>1:1 等量溫水交換：</strong>每喝一杯酒必配一杯溫開水，主動以氣泡水加檸檬片禮貌替代續杯。</span>
              </li>
              <li class="flex items-start gap-2">
                <i class="ph-bold ph-check text-amber-400 mt-0.5"></i>
                <span><strong>差旅商務包四寶：</strong>真絲遮光眼罩、高噪衰減耳塞、折疊筋膜球、便攜彈力繩。</span>
              </li>
              <li class="flex items-start gap-2">
                <i class="ph-bold ph-check text-amber-400 mt-0.5"></i>
                <span><strong>飯店微運動：</strong>入住後做 3 組 20 次深蹲加開肩拉伸，掃除舟車勞頓。</span>
              </li>
            </ul>
          </div>

          <!-- SOP 4: 夜間神經重置與深度修復 -->
          <div class="p-5 rounded-xl bg-slate-900/90 border border-slate-800">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-bold px-2 py-0.5 rounded bg-purple-500/20 text-purple-400 border border-purple-500/30">22:00 - 23:00</span>
              <span class="text-xs text-slate-400 font-medium">夜間閉環</span>
            </div>
            <h4 class="text-base font-bold text-white mb-2">🌙 夜間神經重置與修復閉環</h4>
            <ul class="text-xs text-slate-300 space-y-2">
              <li class="flex items-start gap-2">
                <i class="ph-bold ph-check text-purple-400 mt-0.5"></i>
                <span><strong>22:00 數位屏斷念：</strong>關閉工作群組推播，將充電手機移至臥室外，杜絕藍光。</span>
              </li>
              <li class="flex items-start gap-2">
                <i class="ph-bold ph-check text-purple-400 mt-0.5"></i>
                <span><strong>熱水泡腳降核心溫：</strong>40~42℃ 熱水泡腳 15 分鐘，誘導周圍血管擴張、核心溫度驟降引發睡意。</span>
              </li>
              <li class="flex items-start gap-2">
                <i class="ph-bold ph-check text-purple-400 mt-0.5"></i>
                <span><strong>20 分鐘不上床原則：</strong>上床 20 分鐘未入睡果斷離床，至暗處翻閱歷史書籍，困了再回床。</span>
              </li>
              <li class="flex items-start gap-2">
                <i class="ph-bold ph-check text-purple-400 mt-0.5"></i>
                <span><strong>床頭備妥明晨溫水：</strong>準備保溫壺，形成早晚生活神聖閉環。</span>
              </li>
            </ul>
          </div>

        </div>
      </div>

      <!-- Part D: 48歲體態與醫學監控紅線 -->
      <div class="p-6 rounded-2xl bg-slate-900 border border-slate-800 flex flex-col md:flex-row items-center justify-between gap-6">
        <div>
          <h4 class="text-base font-bold text-white mb-1 flex items-center gap-2">
            <i class="ph-bold ph-activity text-brand-400"></i>
            <span>48 歲體態與醫學指標「紅線監控表」</span>
          </h4>
          <p class="text-xs text-slate-400">
            體脂率 ≤ 22% (男) / ≤ 26% (女) ｜ 內臟脂肪等級 ≤ 8 ｜ 瘦體重守住 ≥ 60.5kg ｜ 靜息心率 ≤ 65 bpm ｜ 幽門桿菌吹氣陰性
          </p>
        </div>
        <div class="flex items-center gap-3 shrink-0">
          <a href="tracker.html" class="px-4 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold transition flex items-center gap-1.5 shadow-lg shadow-brand-600/30">
            <i class="ph-bold ph-chart-line-up"></i>前往 4 週追蹤儀表板
          </a>
          <a href="slides.html#slide-13" class="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-gold-300 text-xs font-semibold border border-gold-500/30 transition flex items-center gap-1.5">
            <i class="ph-bold ph-presentation"></i>在簡報中觀看本章
          </a>
        </div>
      </div>

    </div>
  </section>

  <!-- Scalable Curriculum Architecture (未來擴充架構) -->
  <section id="future-expansion" class="py-16 border-b border-slate-800">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      
      <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-10">
        <div>
          <div class="flex items-center gap-2 text-xs font-bold text-brand-400 uppercase tracking-wider mb-1">
            <i class="ph-bold ph-cards"></i> Extensible Curriculum Architecture
          </div>
          <h2 class="text-2xl font-black text-white tracking-tight">
            未來教材擴充架構與課程群
          </h2>
          <p class="text-sm text-slate-400">支援持續擴充多本得到大腦健康經典教材，具備統一 JSON 驅動與簡報直連結構</p>
        </div>
        <div class="text-xs text-slate-400 flex items-center gap-2">
          <span class="w-2.5 h-2.5 rounded-full bg-brand-400"></span>已上線 1 門
          <span class="w-2.5 h-2.5 rounded-full bg-amber-400 ml-2"></span>預備中 3 門
        </div>
      </div>

      <!-- Courses Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        
        <!-- Course 1 (Active) -->
        <div class="glass-card rounded-2xl overflow-hidden border border-brand-500/40 flex flex-col justify-between">
          <div>
            <div class="relative h-44 overflow-hidden">
              <img src="https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=600&q=80" alt="張遇升 精力管理" class="w-full h-full object-cover">
              <div class="absolute top-3 left-3 px-2 py-0.5 rounded bg-brand-600/90 text-white text-[11px] font-bold">
                B3.1.1 已上線
              </div>
            </div>
            <div class="p-5">
              <h3 class="text-base font-bold text-white mb-1">怎樣成為精力管理的高手</h3>
              <p class="text-xs text-brand-400 font-medium mb-2">張遇升 醫師 · 協和博士/JHU雙碩士</p>
              <p class="text-xs text-slate-300 leading-relaxed mb-4">
                四層金字塔理論、運動心率、血糖穩態抗昏睡、深度睡眠修復與 1978 高管專章。
              </p>
              <div class="flex items-center gap-3 text-[11px] text-slate-400 mb-4 pt-3 border-t border-slate-800">
                <span><i class="ph ph-book-open mr-1 text-emerald-400"></i>13 講精讀</span>
                <span><i class="ph ph-presentation mr-1 text-sky-400"></i>15 頁簡報</span>
              </div>
            </div>
          </div>
          <div class="p-5 pt-0">
            <a href="slides.html" class="w-full py-2.5 rounded-xl bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold transition flex items-center justify-center gap-1.5 shadow-md shadow-brand-600/20">
              <i class="ph-bold ph-play"></i>觀看互動簡報
            </a>
          </div>
        </div>

        <!-- Course 2 (Upcoming: 馮雪科學減肥) -->
        <div class="glass-card rounded-2xl overflow-hidden border border-slate-800 flex flex-col justify-between opacity-90 hover:opacity-100 transition">
          <div>
            <div class="relative h-44 overflow-hidden">
              <img src="https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=600&q=80" alt="馮雪 科學減肥" class="w-full h-full object-cover filter grayscale-[20%]">
              <div class="absolute top-3 left-3 px-2 py-0.5 rounded bg-amber-500/90 text-slate-950 text-[11px] font-bold">
                B3.1.2 預備中
              </div>
            </div>
            <div class="p-5">
              <h3 class="text-base font-bold text-white mb-1">馮雪·科學減肥16講</h3>
              <p class="text-xs text-amber-400 font-medium mb-2">馮雪 主任醫師 · 阜外醫院心臟康復主任</p>
              <p class="text-xs text-slate-300 leading-relaxed mb-4">
                從代謝醫學出發，擊退內臟脂肪，打破胰島素阻抗，為高壓經理人建立不反彈體脂閉環。
              </p>
              <div class="flex items-center gap-3 text-[11px] text-slate-400 mb-4 pt-3 border-t border-slate-800">
                <span><i class="ph ph-book-open mr-1 text-amber-400"></i>16 講架構</span>
                <span><i class="ph ph-clock mr-1 text-slate-400"></i>講義建置中</span>
              </div>
            </div>
          </div>
          <div class="p-5 pt-0">
            <button class="w-full py-2.5 rounded-xl bg-slate-800 text-slate-400 text-xs font-semibold cursor-not-allowed flex items-center justify-center gap-1">
              <i class="ph ph-lock"></i>資料庫建置中
            </button>
          </div>
        </div>

        <!-- Course 3 (Upcoming: 高質量睡眠) -->
        <div class="glass-card rounded-2xl overflow-hidden border border-slate-800 flex flex-col justify-between opacity-90 hover:opacity-100 transition">
          <div>
            <div class="relative h-44 overflow-hidden">
              <img src="https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?auto=format&fit=crop&w=600&q=80" alt="張遇升 高質量睡眠" class="w-full h-full object-cover filter grayscale-[20%]">
              <div class="absolute top-3 left-3 px-2 py-0.5 rounded bg-slate-700 text-slate-200 text-[11px] font-bold">
                B3.1.4 規劃中
              </div>
            </div>
            <div class="p-5">
              <h3 class="text-base font-bold text-white mb-1">怎樣獲得高質量睡眠</h3>
              <p class="text-xs text-sky-400 font-medium mb-2">張遇升 醫師 · 得到睡眠主理人</p>
              <p class="text-xs text-slate-300 leading-relaxed mb-4">
                拆解深睡期與REM修復機理，運用CBT-I認知行為療法重構晝夜節律，解決高管夜醒難題。
              </p>
              <div class="flex items-center gap-3 text-[11px] text-slate-400 mb-4 pt-3 border-t border-slate-800">
                <span><i class="ph ph-book-open mr-1 text-sky-400"></i>10 講架構</span>
                <span><i class="ph ph-clock mr-1 text-slate-400"></i>排程規劃中</span>
              </div>
            </div>
          </div>
          <div class="p-5 pt-0">
            <button class="w-full py-2.5 rounded-xl bg-slate-800 text-slate-400 text-xs font-semibold cursor-not-allowed flex items-center justify-center gap-1">
              <i class="ph ph-lock"></i>排程規劃中
            </button>
          </div>
        </div>

        <!-- Course 4 (Planned: 家庭健康100講) -->
        <div class="glass-card rounded-2xl overflow-hidden border border-slate-800 flex flex-col justify-between opacity-90 hover:opacity-100 transition">
          <div>
            <div class="relative h-44 overflow-hidden">
              <img src="https://images.unsplash.com/photo-1511895426328-dc8714191300?auto=format&fit=crop&w=600&q=80" alt="馮雪 家庭健康" class="w-full h-full object-cover filter grayscale-[20%]">
              <div class="absolute top-3 left-3 px-2 py-0.5 rounded bg-slate-700 text-slate-200 text-[11px] font-bold">
                B3.4.1 架構就緒
              </div>
            </div>
            <div class="p-5">
              <h3 class="text-base font-bold text-white mb-1">馮雪·家庭健康管理100講</h3>
              <p class="text-xs text-purple-400 font-medium mb-2">馮雪 主任醫師 · 國家心血管中心</p>
              <p class="text-xs text-slate-300 leading-relaxed mb-4">
                為企業經理人守護家庭成員健康底線，包含三代人慢性病防禦、體檢篩檢解讀與急症守護地圖。
              </p>
              <div class="flex items-center gap-3 text-[11px] text-slate-400 mb-4 pt-3 border-t border-slate-800">
                <span><i class="ph ph-book-open mr-1 text-purple-400"></i>100 講知識庫</span>
                <span><i class="ph ph-check mr-1 text-emerald-400"></i>大綱已就緒</span>
              </div>
            </div>
          </div>
          <div class="p-5 pt-0">
            <button class="w-full py-2.5 rounded-xl bg-slate-800 text-slate-400 text-xs font-semibold cursor-not-allowed flex items-center justify-center gap-1">
              <i class="ph ph-lock"></i>待轉化為簡報
            </button>
          </div>
        </div>

      </div>

      <!-- Expansion Protocol Box -->
      <div class="mt-8 p-5 rounded-xl bg-slate-900/60 border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div class="flex items-start sm:items-center gap-3">
          <i class="ph-bold ph-code text-xl text-brand-400"></i>
          <div>
            <h4 class="text-xs font-bold text-white">未來資料擴充架構說明 (Extensibility Guide)</h4>
            <p class="text-[11px] text-slate-400">
              所有課程模組皆由 <code class="text-brand-300 bg-slate-800 px-1.5 py-0.5 rounded">data/courses_data.js</code> 資料驅動。只需在數組中新增條目與簡報頁面，門戶與搜尋引擎將自動同步，實現零維護成本的知識庫持續擴展。
            </p>
          </div>
        </div>
        <a href="https://github.com/davidyeh51/david-vitality-plan" target="_blank" class="shrink-0 text-xs text-brand-400 hover:text-brand-300 font-semibold flex items-center gap-1">
          檢視 GitHub 源碼 <i class="ph-bold ph-arrow-up-right"></i>
        </a>
      </div>

    </div>
  </section>

  <!-- Module Detail Modal Dialog -->
  <div id="module-modal" class="fixed inset-0 z-50 hidden flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md">
    <div class="glass-card bg-slate-900 border border-slate-700 rounded-2xl max-w-3xl w-full max-h-[90vh] overflow-hidden flex flex-col shadow-2xl">
      <!-- Modal Header -->
      <div class="p-5 border-b border-slate-800 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <span id="modal-category-badge" class="px-2.5 py-0.5 rounded text-xs font-bold bg-brand-500/20 text-brand-400 border border-brand-500/30">理論架構</span>
          <h3 id="modal-title" class="text-base sm:text-lg font-bold text-white truncate max-w-md">模組標題</h3>
        </div>
        <button id="close-modal-btn" class="w-8 h-8 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center transition">
          <i class="ph-bold ph-x text-lg"></i>
        </button>
      </div>

      <!-- Modal Body -->
      <div class="p-6 overflow-y-auto space-y-6 text-sm text-slate-300">
        <!-- Visual & Caption -->
        <div class="rounded-xl overflow-hidden border border-slate-800">
          <img id="modal-image" src="" alt="模組配圖" class="w-full h-64 object-cover">
          <div id="modal-caption" class="p-3 bg-slate-950 text-xs text-slate-400 italic"></div>
        </div>

        <!-- Summary -->
        <div>
          <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
            <i class="ph-bold ph-lightbulb text-amber-400"></i>核心摘要與原理
          </h4>
          <p id="modal-summary" class="leading-relaxed text-slate-200 bg-slate-800/40 p-4 rounded-xl border border-slate-800"></p>
        </div>

        <!-- Key Points -->
        <div>
          <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3 flex items-center gap-1.5">
            <i class="ph-bold ph-list-numbers text-emerald-400"></i>逐點深度解構
          </h4>
          <div id="modal-keypoints" class="space-y-3"></div>
        </div>

        <!-- Executive Takeaway -->
        <div class="p-4 rounded-xl bg-gold-500/10 border border-gold-500/30">
          <h4 class="text-xs font-bold text-gold-400 mb-1 flex items-center gap-1.5">
            <i class="ph-bold ph-crown text-gold-400"></i>1978 高階經理人專屬洞察 (48歲心智模型)
          </h4>
          <p id="modal-executive" class="text-xs text-slate-300 leading-relaxed"></p>
        </div>

        <!-- Action Items -->
        <div>
          <h4 class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center gap-1.5">
            <i class="ph-bold ph-check-square text-sky-400"></i>落地行動清單 (Action Protocol)
          </h4>
          <div id="modal-actions" class="space-y-2"></div>
        </div>
      </div>

      <!-- Modal Footer -->
      <div class="p-4 border-t border-slate-800 bg-slate-950/60 flex items-center justify-between">
        <span class="text-xs text-slate-400">大衛人生 · 精力管理知識庫</span>
        <div class="flex items-center gap-3">
          <a id="modal-slide-link" href="slides.html" class="px-4 py-2 rounded-xl bg-brand-600 hover:bg-brand-500 text-white text-xs font-bold transition flex items-center gap-1.5">
            <i class="ph-bold ph-presentation"></i>在簡報中查看
          </a>
        </div>
      </div>
    </div>
  </div>

  <!-- Footer -->
  <footer class="py-12 bg-slate-950 border-t border-slate-800/80 text-xs text-slate-500">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-6">
      
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 rounded-lg bg-brand-600 flex items-center justify-center text-white font-bold text-sm">
          <i class="ph-bold ph-lightning"></i>
        </div>
        <div>
          <span class="font-bold text-slate-300 text-sm">大衛人生 · 精力管理知識門戶</span>
          <p class="text-slate-500">B3.1 精力體態知識庫 · 得到大腦「怎樣成為精力管理的高手」定版</p>
        </div>
      </div>

      <div class="flex flex-wrap items-center gap-6">
        <a href="#overview" class="hover:text-slate-300 transition">回到頂部</a>
        <a href="slides.html" class="hover:text-emerald-400 transition">互動簡報</a>
        <a href="#executive-part" class="hover:text-gold-400 transition">1978 高管專章</a>
        <a href="tracker.html" class="hover:text-slate-300 transition">4週數據儀表板</a>
        <a href="https://github.com/davidyeh51/david-vitality-plan" target="_blank" class="hover:text-slate-300 transition flex items-center gap-1">
          <i class="ph-bold ph-github-logo"></i> GitHub
        </a>
      </div>

    </div>
  </footer>

  <!-- Core Knowledge Data Script -->
  <script src="data/courses_data.js"></script>

  <!-- Portal Interactive App Script -->
  <script>
    document.addEventListener('DOMContentLoaded', () => {
      const coursesData = window.ENERGY_KNOWLEDGE_BASE;
      if (!coursesData || !coursesData.courses) {
        console.error('Failed to load courses_data.js');
        return;
      }

      const activeCourse = coursesData.courses[0]; // zhang-vitality
      const allModules = activeCourse.modules;
      let currentFilterTag = 'ALL';
      let currentSearchQuery = '';

      const modulesContainer = document.getElementById('modules-container');
      const searchInput = document.getElementById('search-input');
      const clearSearchBtn = document.getElementById('clear-search');
      const filterChips = document.querySelectorAll('.filter-chip');
      const matchedCountEl = document.getElementById('matched-count');
      const emptyStateEl = document.getElementById('empty-state');
      const searchQueryDisplay = document.getElementById('search-query-display');
      const resetSearchBtn = document.getElementById('reset-search-btn');

      // Modal elements
      const modal = document.getElementById('module-modal');
      const closeModalBtn = document.getElementById('close-modal-btn');
      const modalBadge = document.getElementById('modal-category-badge');
      const modalTitle = document.getElementById('modal-title');
      const modalImage = document.getElementById('modal-image');
      const modalCaption = document.getElementById('modal-caption');
      const modalSummary = document.getElementById('modal-summary');
      const modalKeypoints = document.getElementById('modal-keypoints');
      const modalExecutive = document.getElementById('modal-executive');
      const modalActions = document.getElementById('modal-actions');
      const modalSlideLink = document.getElementById('modal-slide-link');

      // Helper to highlight search matches
      function highlightText(text, query) {
        if (!query || !query.trim()) return text;
        const escaped = query.trim().replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&');
        const regex = new RegExp(`(${escaped})`, 'gi');
        return text.replace(regex, '<mark class="highlight-match">$1</mark>');
      }

      // Render Modules
      function renderModules() {
        const query = currentSearchQuery.trim().toLowerCase();
        
        const filtered = allModules.filter(m => {
          // Tag Filter
          const matchTag = (currentFilterTag === 'ALL') || 
                           (m.category === currentFilterTag) || 
                           (m.tags && m.tags.includes(currentFilterTag));
          
          if (!matchTag) return false;

          // Keyword Filter
          if (!query) return true;

          const inTitle = m.title.toLowerCase().includes(query);
          const inShortTitle = m.shortTitle.toLowerCase().includes(query);
          const inSummary = m.summary.toLowerCase().includes(query);
          const inExec = m.executiveTakeaway.toLowerCase().includes(query);
          const inTags = m.tags.some(t => t.toLowerCase().includes(query));
          const inPoints = m.keyPoints.some(kp => 
            kp.label.toLowerCase().includes(query) || kp.desc.toLowerCase().includes(query)
          );
          const inActions = m.actionItems.some(act => act.toLowerCase().includes(query));

          return inTitle || inShortTitle || inSummary || inExec || inTags || inPoints || inActions;
        });

        matchedCountEl.textContent = filtered.length;

        if (filtered.length === 0) {
          modulesContainer.innerHTML = '';
          emptyStateEl.classList.remove('hidden');
          searchQueryDisplay.textContent = currentSearchQuery;
          return;
        } else {
          emptyStateEl.classList.add('hidden');
        }

        modulesContainer.innerHTML = filtered.map(m => {
          const isExecSpecial = m.id === 'module-12';
          const cardBorder = isExecSpecial ? 'border-amber-500/50 shadow-lg shadow-amber-500/10' : 'border-slate-800';
          const tagBg = isExecSpecial ? 'bg-amber-500/20 text-amber-300 border-amber-500/30' : 'bg-brand-500/10 text-brand-400 border-brand-500/20';

          return `
            <div class="glass-card rounded-2xl overflow-hidden border ${cardBorder} flex flex-col justify-between transition-all duration-300 hover:transform hover:-translate-y-1 hover:shadow-xl">
              <div>
                <!-- Card Header Visual -->
                <div class="relative h-48 overflow-hidden group">
                  <img src="${m.image}" alt="${m.title}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500">
                  <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/20 to-transparent"></div>
                  
                  <div class="absolute top-3 left-3 flex items-center gap-1.5">
                    <span class="px-2.5 py-0.5 rounded text-[11px] font-bold ${tagBg} border">
                      ${m.category}
                    </span>
                    ${isExecSpecial ? '<span class="px-2 py-0.5 rounded text-[10px] font-extrabold bg-gradient-to-r from-amber-500 to-yellow-400 text-slate-950">1978特企</span>' : ''}
                  </div>

                  <div class="absolute bottom-3 left-3 right-3">
                    <span class="text-[11px] font-semibold text-slate-400">講次 ${String(m.order).padStart(2, '0')}</span>
                    <h3 class="text-base font-bold text-white leading-snug truncate">
                      ${highlightText(m.shortTitle, currentSearchQuery)}
                    </h3>
                  </div>
                </div>

                <!-- Card Body -->
                <div class="p-5">
                  <p class="text-xs text-slate-300 leading-relaxed mb-4 line-clamp-3">
                    ${highlightText(m.summary, currentSearchQuery)}
                  </p>

                  <!-- Key Points Preview -->
                  <div class="space-y-1.5 mb-4">
                    ${m.keyPoints.slice(0, 2).map(kp => `
                      <div class="text-[11px] text-slate-400 flex items-start gap-1.5">
                        <i class="ph-bold ph-caret-right text-brand-400 mt-0.5 shrink-0"></i>
                        <span class="truncate"><strong>${highlightText(kp.label, currentSearchQuery)}：</strong>${highlightText(kp.desc, currentSearchQuery)}</span>
                      </div>
                    `).join('')}
                  </div>

                  <!-- Executive Takeaway preview -->
                  <div class="p-3 rounded-xl ${isExecSpecial ? 'bg-amber-500/10 border-amber-500/20 text-amber-200' : 'bg-slate-900/80 border-slate-800 text-slate-300'} border text-[11px] leading-relaxed mb-3">
                    <div class="font-bold text-gold-400 mb-0.5 flex items-center gap-1">
                      <i class="ph-bold ph-crown text-xs"></i> 48歲高管心法：
                    </div>
                    <div class="line-clamp-2">${highlightText(m.executiveTakeaway, currentSearchQuery)}</div>
                  </div>

                  <!-- Tags -->
                  <div class="flex flex-wrap gap-1.5">
                    ${m.tags.slice(0, 3).map(t => `
                      <span class="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-400">#${t}</span>
                    `).join('')}
                  </div>
                </div>
              </div>

              <!-- Card Action Bar -->
              <div class="p-5 pt-0 border-t border-slate-800/80 mt-2 flex items-center justify-between gap-2">
                <button class="open-detail-btn text-xs text-slate-300 hover:text-white font-medium flex items-center gap-1 py-1.5" data-id="${m.id}">
                  <i class="ph ph-article"></i> 閱讀筆記
                </button>
                <a href="slides.html#slide-${m.order + 1}" class="px-3 py-1.5 rounded-lg bg-brand-600/90 hover:bg-brand-500 text-white text-xs font-semibold flex items-center gap-1 transition">
                  <i class="ph-bold ph-presentation"></i> 在簡報中查看
                </a>
              </div>
            </div>
          `;
        }).join('');

        // Attach modal listeners
        document.querySelectorAll('.open-detail-btn').forEach(btn => {
          btn.addEventListener('click', (e) => {
            const id = e.currentTarget.getAttribute('data-id');
            openModal(id);
          });
        });
      }

      // Open Modal Function
      function openModal(moduleId) {
        const m = allModules.find(item => item.id === moduleId);
        if (!m) return;

        modalBadge.textContent = m.category;
        modalTitle.textContent = m.title;
        modalImage.src = m.image;
        modalCaption.textContent = m.imageCaption;
        modalSummary.textContent = m.summary;

        modalKeypoints.innerHTML = m.keyPoints.map(kp => `
          <div class="p-3 rounded-lg bg-slate-800/60 border border-slate-800">
            <div class="font-bold text-white text-xs mb-1 flex items-center gap-1.5 text-brand-300">
              <i class="ph-bold ph-check text-brand-400"></i> ${kp.label}
            </div>
            <p class="text-xs text-slate-300 leading-relaxed">${kp.desc}</p>
          </div>
        `).join('');

        modalExecutive.textContent = m.executiveTakeaway;

        modalActions.innerHTML = m.actionItems.map(act => `
          <div class="flex items-start gap-2 p-2.5 rounded-lg bg-slate-900 border border-slate-800 text-xs text-slate-300">
            <input type="checkbox" class="mt-0.5 rounded border-slate-700 text-brand-600 focus:ring-brand-500 cursor-pointer">
            <span>${act}</span>
          </div>
        `).join('');

        modalSlideLink.href = `slides.html#slide-${m.order + 1}`;
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
      }

      // Close Modal Function
      function closeModal() {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
      }

      closeModalBtn.addEventListener('click', closeModal);
      modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
      });

      // Filter Chips handler
      filterChips.forEach(chip => {
        chip.addEventListener('click', (e) => {
          filterChips.forEach(c => {
            c.classList.remove('bg-brand-600', 'text-white', 'active');
            c.classList.add('bg-slate-800', 'text-slate-300');
          });
          e.currentTarget.classList.remove('bg-slate-800', 'text-slate-300');
          e.currentTarget.classList.add('bg-brand-600', 'text-white', 'active');

          currentFilterTag = e.currentTarget.getAttribute('data-tag');
          renderModules();
        });
      });

      // Search input handler
      searchInput.addEventListener('input', (e) => {
        currentSearchQuery = e.target.value;
        if (currentSearchQuery.trim()) {
          clearSearchBtn.classList.remove('hidden');
        } else {
          clearSearchBtn.classList.add('hidden');
        }
        renderModules();
      });

      clearSearchBtn.addEventListener('click', () => {
        searchInput.value = '';
        currentSearchQuery = '';
        clearSearchBtn.classList.add('hidden');
        renderModules();
      });

      resetSearchBtn.addEventListener('click', () => {
        searchInput.value = '';
        currentSearchQuery = '';
        clearSearchBtn.classList.add('hidden');
        currentFilterTag = 'ALL';
        filterChips.forEach(c => {
          c.classList.remove('bg-brand-600', 'text-white', 'active');
          c.classList.add('bg-slate-800', 'text-slate-300');
        });
        filterChips[0].classList.add('bg-brand-600', 'text-white', 'active');
        renderModules();
      });

      // Initial render
      renderModules();
    });
  </script>
</body>
</html>
'''

# HTML Template for slides.html (Full Featured Presentation Deck)
slides_html_content = '''<!DOCTYPE html>
<html lang="zh-TW" class="h-full">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>精力管理的高手 | 1978 高階經理人極限精力簡報 (全圖解 15 頁)</title>
  <meta name="description" content="張遇升醫師《怎樣成為精力管理的高手》與1978高階經理人專章全圖解簡報，含體能、情緒、思維、意義金字塔與落地方案。">

  <!-- Google Fonts & Tailwind CSS CDN -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=Noto+Sans+TC:wght@300;400;500;600;700;900&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  
  <!-- Phosphor Icons CDN -->
  <script src="https://unpkg.com/@phosphor-icons/web"></script>

  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', '"Noto Sans TC"', 'sans-serif'],
          },
          colors: {
            brand: {
              400: '#34d399',
              500: '#10b981',
              600: '#059669',
              700: '#047857',
            },
            executive: {
              800: '#1e293b',
              900: '#0f172a',
              950: '#060a12',
            },
            gold: {
              400: '#fbbf24',
              500: '#f59e0b',
              600: '#d97706',
            }
          }
        }
      }
    }
  </script>
  <style>
    .slide-enter {
      animation: fadeInSlide 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    @keyframes fadeInSlide {
      from { opacity: 0; transform: scale(0.985) translateY(8px); }
      to { opacity: 1; transform: scale(1) translateY(0); }
    }
    .aspect-16-9 {
      aspect-ratio: 16 / 9;
    }
    /* Hide scrollbar for clean presentation */
    .no-scrollbar::-webkit-scrollbar { display: none; }
    .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
  </style>
</head>
<body class="bg-executive-950 text-slate-100 h-full flex flex-col font-sans select-none overflow-hidden">

  <!-- Top Progress Bar -->
  <div class="w-full bg-slate-900 h-1.5 fixed top-0 left-0 z-50">
    <div id="progress-bar" class="h-full bg-gradient-to-r from-emerald-500 to-amber-400 transition-all duration-300 w-[6.6%]"></div>
  </div>

  <!-- Header Controls -->
  <header class="h-14 px-4 sm:px-6 bg-slate-900/90 border-b border-slate-800 flex items-center justify-between z-40 shrink-0">
    <div class="flex items-center gap-3">
      <a href="index.html" class="w-8 h-8 rounded-lg bg-slate-800 hover:bg-slate-700 flex items-center justify-center text-slate-300 hover:text-white transition" title="返回知識門戶">
        <i class="ph-bold ph-arrow-left text-base"></i>
      </a>
      <div class="flex items-center gap-2">
        <span class="font-bold text-sm text-white">大衛人生 · 精力管理簡報</span>
        <span class="text-xs px-2 py-0.5 rounded bg-brand-500/20 text-brand-300 border border-brand-500/30 font-semibold hidden sm:inline-block">15 頁全圖解</span>
      </div>
    </div>

    <!-- Center Slide Counter -->
    <div class="flex items-center gap-3 bg-slate-950/80 px-3 py-1 rounded-full border border-slate-800 text-xs font-semibold">
      <span id="slide-num-current" class="text-emerald-400 font-extrabold text-sm">01</span>
      <span class="text-slate-600">/</span>
      <span id="slide-num-total" class="text-slate-400">15</span>
      <span id="slide-title-preview" class="hidden md:inline-block text-slate-300 font-normal pl-2 border-l border-slate-800 truncate max-w-xs">封面導讀</span>
    </div>

    <!-- Right Presentation Utilities -->
    <div class="flex items-center gap-2">
      <!-- Notes Toggle -->
      <button id="toggle-notes-btn" class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold flex items-center gap-1 border border-slate-700 transition" title="切換逐頁解讀筆記 (N)">
        <i class="ph-bold ph-note-pencil text-amber-400"></i>
        <span class="hidden sm:inline">講義筆記</span>
      </button>

      <!-- Thumbnails Drawer Toggle -->
      <button id="toggle-drawer-btn" class="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold flex items-center gap-1 border border-slate-700 transition" title="瀏覽所有頁面縮圖 (T)">
        <i class="ph-bold ph-squares-four text-sky-400"></i>
        <span class="hidden sm:inline">頁面目錄</span>
      </button>

      <!-- Fullscreen Toggle -->
      <button id="fullscreen-btn" class="w-8 h-8 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white flex items-center justify-center transition" title="全螢幕切換 (F)">
        <i class="ph-bold ph-corners-out text-base"></i>
      </button>
    </div>
  </header>

  <!-- Main Slide Viewing Area -->
  <main class="flex-1 relative overflow-hidden flex items-center justify-center p-2 sm:p-4 md:p-6 bg-radial-gradient">
    
    <!-- Slide Container (Responsive 16:9 Screen) -->
    <div id="slide-viewport" class="w-full max-w-6xl aspect-16-9 bg-slate-900 rounded-2xl border border-slate-800 shadow-2xl overflow-hidden relative flex flex-col md:flex-row slide-enter">
      <!-- Injected dynamically by renderCurrentSlide() -->
    </div>

    <!-- Floating Navigation Arrows -->
    <button id="prev-btn" class="absolute left-2 sm:left-6 top-1/2 -translate-y-1/2 w-11 h-11 rounded-full bg-slate-900/80 hover:bg-brand-600 text-slate-300 hover:text-white flex items-center justify-center shadow-xl border border-slate-700/80 transition duration-200 z-30" title="上一頁 (← / PageUp)">
      <i class="ph-bold ph-caret-left text-xl"></i>
    </button>
    <button id="next-btn" class="absolute right-2 sm:right-6 top-1/2 -translate-y-1/2 w-11 h-11 rounded-full bg-slate-900/80 hover:bg-brand-600 text-slate-300 hover:text-white flex items-center justify-center shadow-xl border border-slate-700/80 transition duration-200 z-30" title="下一頁 (→ / Space / PageDown)">
      <i class="ph-bold ph-caret-right text-xl"></i>
    </button>

  </main>

  <!-- Bottom Floating Speaker Notes Drawer -->
  <div id="notes-panel" class="hidden fixed bottom-14 left-1/2 -translate-x-1/2 max-w-3xl w-[92%] bg-slate-900/95 backdrop-blur-md border border-amber-500/40 rounded-2xl p-4 shadow-2xl z-40 text-xs text-slate-200 transition-all">
    <div class="flex items-center justify-between border-b border-slate-800 pb-2 mb-2">
      <span class="font-bold text-amber-400 flex items-center gap-1.5">
        <i class="ph-bold ph-crown"></i> 講義導讀與 1978 高管心法實戰備忘
      </span>
      <button id="close-notes-btn" class="text-slate-400 hover:text-white">
        <i class="ph-bold ph-x"></i>
      </button>
    </div>
    <div id="notes-content" class="leading-relaxed space-y-1.5 max-h-36 overflow-y-auto pr-1"></div>
  </div>

  <!-- Bottom Thumbnails Drawer (Overlay) -->
  <div id="drawer-panel" class="hidden fixed inset-0 bg-slate-950/80 backdrop-blur-md z-50 flex flex-col justify-end">
    <div class="bg-slate-900 border-t border-slate-800 p-6 max-h-[85vh] overflow-y-auto">
      <div class="flex items-center justify-between mb-4">
        <h3 class="font-bold text-white text-base flex items-center gap-2">
          <i class="ph-bold ph-squares-four text-brand-400"></i>
          <span>簡報頁面目錄速查 (點擊跳轉)</span>
        </h3>
        <button id="close-drawer-btn" class="w-8 h-8 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 flex items-center justify-center">
          <i class="ph-bold ph-x text-lg"></i>
        </button>
      </div>

      <div id="drawer-thumbnails-grid" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
        <!-- Injected dynamically -->
      </div>
    </div>
  </div>

  <!-- Footer Navigation Bar -->
  <footer class="h-10 bg-slate-950 border-t border-slate-800/80 px-4 flex items-center justify-between text-[11px] text-slate-400 z-30 shrink-0">
    <div class="flex items-center gap-4">
      <span>快速鍵：<kbd class="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">←</kbd> / <kbd class="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">→</kbd> 翻頁</span>
      <span><kbd class="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">F</kbd> 全螢幕</span>
      <span><kbd class="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">N</kbd> 筆記</span>
      <span><kbd class="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">T</kbd> 目錄</span>
    </div>

    <div class="flex items-center gap-3">
      <a href="index.html" class="hover:text-brand-400 transition">回到知識門戶</a>
      <span class="text-slate-700">|</span>
      <a href="tracker.html" class="hover:text-brand-400 transition">4週追蹤儀表板</a>
    </div>
  </footer>

  <!-- Slide Deck Data & Engine Script -->
  <script>
    const SLIDES = [
      {
        id: 1,
        badge: "大衛人生 · 精力管理專案",
        title: "怎樣成為精力管理的高手",
        subtitle: "企業高階經理人逆齡與極限效能系統",
        image: "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=1200&q=80",
        imageCaption: "頂尖決策者的第一核心資產：充沛體能、平穩情緒、極致專注與明確意義感",
        layout: "cover",
        highlights: [
          { title: "主講導師", desc: "張遇升 醫師（北京協和醫學院醫學博士 · 約翰霍普金斯公共衛生/MBA雙碩士）" },
          { title: "專案受眾", desc: "1978 年次（現年 48 歲）企業高階主管、創業家與核心決策者" },
          { title: "核心使命", desc: "以循證醫學重塑身體底盤性能，終結中年疲勞，保障百萬年薪高質量決策" }
        ],
        speakerNotes: "【開場導讀】歡迎進入精力管理互動簡報。本套系統並非空洞心靈雞湯，而是由協和醫學博士張遇升經過 10 年實戰打磨、輔導無數 500 強企業家驗證的醫學級精力重塑系統。對於 48 歲的高階主管而言，這是實現中年逆齡翻盤的戰略地圖。"
      },
      {
        id: 2,
        badge: "發刊詞 ｜ 賽車維護觀",
        title: "為什麼高管需要精力管理？",
        subtitle: "時間是剛性的，精力卻如肌肉般可訓練",
        image: "https://images.unsplash.com/photo-1511919884226-fd3cad34687c?auto=format&fit=crop&w=1200&q=80",
        imageCaption: "時間管理只是排定賽程，精力管理才是調校賽車底盤與引擎馬力",
        layout: "content",
        highlights: [
          { title: "30歲後的精力斷崖", desc: "海馬體每年自然萎縮 0.5%，體能下滑與外界 KPI 雙向撕裂，形成中年危機。" },
          { title: "時間管理的天花板", desc: "每日固定24小時彈性極小；一輛頻繁拋錨的賽車，賽程規劃再精細也注定落敗。" },
          { title: "黃同學的職業級震撼", desc: "約翰霍普金斯同窗（40多歲、軍隊急救200人主管、課業第一），展現如職業選手般從容控場。" }
        ],
        speakerNotes: "【高管痛點】48歲高管普遍面臨時間不夠用的焦慮。但時間管理無法解決根本問題。我們必須將關注點從「拉長工作時間」轉變為「提升單位時間的能量輸出」，把自己當成 F1 賽車精準維護。"
      },
      {
        id: 3,
        badge: "核心模型 ｜ 四層金字塔",
        title: "精力管理的金字塔模型",
        subtitle: "體能·情緒·注意力·意義感逐層支撐",
        image: "https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&w=1200&q=80",
        imageCaption: "體能是馬力，情緒是火花塞，注意力是前進道路，意義感是終極燈塔",
        layout: "content",
        highlights: [
          { title: "底層·體能（基礎）", desc: "提供大腦運轉的馬力。西點軍校培育最多 500 強 CEO，體能訓練是高壓承受力基石。" },
          { title: "二層·情緒（火花塞）", desc: "啟動精力的關鍵。若深陷負面情緒，體能再好也無法點火；正面情緒激發創造力波峰。" },
          { title: "三層·注意力（道路）", desc: "引導精力有效輸出。心流理論：多執行緒只是被動應付，深度專注才能啃下戰略難題。" },
          { title: "頂層·意義感（燈塔）", desc: "人生的終極源泉。李曉峰（SKY）世界冠軍之路；具意義感者患阿茲海默症風險降 58%。" }
        ],
        speakerNotes: "【架構解析】好精力公式 = 充沛體能 + 積極情緒 + 隨時聚焦的注意力 + 明確意義感。診斷自己的狀態時，先看是哪一層出現了破口。"
      },
      {
        id: 4,
        badge: "體能基石 ｜ 最佳運動方案",
        title: "打破久坐的進化失配",
        subtitle: "中等強度心率與碎片化 HIIT 奇蹟",
        image: "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?auto=format&fit=crop&w=1200&q=80",
        imageCaption: "運動不是消耗體能，而是為大腦注入新鮮氧氣與葡萄糖，清理代謝廢物",
        layout: "content",
        highlights: [
          { title: "進化失配性疾病", desc: "哈佛 Lieberman 指出：人類百萬年為長跑進化，現代久坐超9小時死亡風險飆升 50%。" },
          { title: "48歲靶心率公式", desc: "世衛每週 150~300 分鐘有氧。中等強度心率 = (220 - 48) × 60%~70% = 103~120 bpm。" },
          { title: "碎片化運動革命", desc: "1分鐘高強度間歇每週3天降血糖15%、擴大記憶海馬體；八段錦、電話中走動、深蹲50次。" }
        ],
        speakerNotes: "【運動實踐】高管不需要大把時間去健身房。將運動「寄生」在日常中：電話會議時走動、上午 11:00 打一套八段錦、辦公室做米字操與深蹲，隨時為大腦打通血流。"
      },
      {
        id: 5,
        badge: "能量燃油 ｜ 飲食與水化",
        title: "吃對了，就不會累",
        subtitle: "穩住血糖波峰、ONQI指數與精準補水",
        image: "https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=1200&q=80",
        imageCaption: "吃飽昏睡源自高碳水刺激胰島素與色氨酸入腦：深綠蔬菜為先，嚴守體重÷32補水法",
        layout: "content",
        highlights: [
          { title: "飯後昏睡的生理真相", desc: "午後低潮節律 + 精緻米麵促使胰島素激增，色氨酸轉化褪黑素，大腦血流被腸胃搶奪。" },
          { title: "少吃多餐與倒序進食", desc: "一天五頓微節奏。午餐嚴守「深綠蔬菜一大碗 → 蛋白質肉類 → 少量碳水」進食順序。" },
          { title: "精準水化與咖啡因斷點", desc: "飲水量(L) = 體重(kg) ÷ 32（約2.2L）；尿色清淡為準；下午 15:00 後嚴格切斷咖啡因。" }
        ],
        speakerNotes: "【飲食防禦】48歲經理人胰島素抗性升高，午餐一碗牛肉麵下午保證昏睡。落實倒序進食法，確保全天血糖平穩，下午開會才能保持刀鋒般的思維。"
      },
      {
        id: 6,
        badge: "決策修復 ｜ 深度睡眠機制",
        title: "睡得好提升決策水平",
        subtitle: "大腦膠質淋巴清洗與 CBT-I 四字訣",
        image: "https://images.unsplash.com/photo-1541781774459-bb2af2f05b55?auto=format&fit=crop&w=1200&q=80",
        imageCaption: "頂尖高手不睡得少：柏林愛樂天才演奏家平均睡眠 8 小時 36 分，深睡排毒，REM修復大腦",
        layout: "content",
        highlights: [
          { title: "決策代價與醫學實證", desc: "《柳葉刀》缺覺醫師出錯率增20%；比爾蓋茨重大決策失誤皆因缺覺；睡眠洗滌類澱粉蛋白。" },
          { title: "沒事別上床 & 戶外多活動", desc: "床只用於睡覺，醒著躺床超20分鐘離床；白天充足陽光刺激松果體夜間分泌褪黑激素。" },
          { title: "睡前做準備 & 小心酒和鼾", desc: "熱水泡腳誘導核心體溫驟降；酒精破壞深睡；嚴重打鼾伴隨呼吸暫停>5秒警惕 OSAS。" }
        ],
        speakerNotes: "【睡眠策略】睡眠是高管最好的投資。守住 23:00~07:00 睡眠窗口，睡前 1 小時遠離手機螢幕。若有嚴重打鼾，應排查阻塞性睡眠呼吸暫停。"
      },
      {
        id: 7,
        badge: "底盤防禦 ｜ 擊退職場隱患",
        title: "擊退消磨意志的慢性隱患",
        subtitle: "人體工學坐姿、代謝症候群與第二大腦",
        image: "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1200&q=80",
        imageCaption: "慢性頸肩痛與腸胃潰瘍會盜走 30% 注意力頻寬：保持雙90度坐姿，排查幽門螺旋桿菌",
        layout: "content",
        highlights: [
          { title: "脊椎久坐毀損與米字操", desc: "螢幕平視、腰靠支撐、肘膝雙90度；米字操、小燕飛、蛙泳鍛鍊背肌；手麻腳麻立即就醫。" },
          { title: "代謝症候群萎縮大腦", desc: "《大腦研究》證實體重指數越大海馬體越小（腦萎縮加速）；每天清晨量體重是最便宜監控儀。" },
          { title: "第二大腦消化道防禦", desc: "胃腸與神經緊密相連，高壓誘發潰瘍；幽門螺旋桿菌(HP)一類致癌物，需吹氣排查四聯根除。" }
        ],
        speakerNotes: "【慢性病防禦】高階主管最忌被慢性疼痛鈍刀子割肉。定期吹氣檢查幽門螺旋桿菌、維護好辦公桌人體工學，是消除精力漏斗的基礎工程。"
      },
      {
        id: 8,
        badge: "點火開關 ｜ 情緒與焦慮",
        title: "控制情緒，緩解焦慮",
        subtitle: "單頻道原理、3:1黃金比與標籤化技術",
        image: "https://images.unsplash.com/photo-1518241353330-0f7941c2d9b5?auto=format&fit=crop&w=1200&q=80",
        imageCaption: "情緒是火花塞：運用單頻道原理與客觀貼標籤法，將焦慮轉化為可執行的具體對策",
        layout: "content",
        highlights: [
          { title: "三大底層心理學定律", desc: "單頻道原理（一次只能有一種主情緒）、負面偏好（進化警惕危險）、情緒可訓練性。" },
          { title: "芭芭拉 3:1 黃金比例", desc: "每日正面情緒與負面情緒大於 3:1，心理資本才能持續向上螺旋。" },
          { title: "焦慮降伏三板斧", desc: "放鬆呼吸 + 客觀標籤法（抽離觀察「這是心跳加快」） + 寫下最壞結果列出對策；跑步抗抑鬱。" }
        ],
        speakerNotes: "【情緒點火】大腦天生有負面偏好。高管面臨 KPI 重壓時，千萬不要任由焦慮蔓延。拿出白紙把焦慮寫下來，列出三步對策，焦慮就會被前額葉降伏。"
      },
      {
        id: 9,
        badge: "輸出導向 ｜ 注意力與意義感",
        title: "專注力訓練與意義感燈塔",
        subtitle: "創造性輸出、45分脈衝與意義四問",
        image: "https://images.unsplash.com/photo-1499750310107-5fef28a66643?auto=format&fit=crop&w=1200&q=80",
        imageCaption: "意義感回答「去哪裡」，注意力回答「怎麼去」：保護創造性輸出，為雜念建立停車場",
        layout: "content",
        highlights: [
          { title: "創造性 vs 事務性輸出", desc: "回信開雜會屬於低維事務性輸出；戰略思考與組織構建才是不可替代的創造性輸出。" },
          { title: "注意力三大外掛訓練", desc: "清晰具體目標（引導心流） + 雜念停車場（數位備忘錄暫存） + 黃金時段攻克硬骨頭。" },
          { title: "意義感終極四問", desc: "我擅長什麼？我服務誰？他得到什麼？有何不同？朱祖懿博士轉身投入家庭基層醫療案例。" }
        ],
        speakerNotes: "【高維產出】48歲高管必須捍衛上午的創造性時間，不要一上班就淹沒在通訊軟體裡。45分鐘高強度衝刺 + 5分鐘生理重置，將精力釋放在最高槓桿的戰略上。"
      },
      {
        id: 10,
        badge: "日常閉環 ｜ 全天行動清單",
        title: "早晚各半小時的神聖結界",
        subtitle: "晨間七件事、日間工作節律與睡前七件事",
        image: "https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?auto=format&fit=crop&w=1200&q=80",
        imageCaption: "將科學精力管理轉化為全天自動化運行的習慣閉環，如同肌肉記憶般運作",
        layout: "content",
        highlights: [
          { title: "晨起 30 分鐘七件事", desc: "床上熱身 → 疊被 → 600ml溫水 → 非慣用手刷牙單腿站 → 10分熱啟動 → 記今日三事 → 高蛋白低GI早餐。" },
          { title: "日間 45 分鐘脈衝循環", desc: "通勤走樓梯覆盤 → 到崗先啃核心三事 → 45分衝刺+5分拉伸 → 倒序午餐 → 下班覆盤閉環。" },
          { title: "睡前 30 分鐘七件事", desc: "正念呼吸 → 熱水泡腳 → 備明晨溫水 → 回顧目標 → 檢視日曆 → 排定明日 → 床頭讀書入眠。" }
        ],
        speakerNotes: "【習慣閉環】習慣是節省大腦意志力的神經捷徑。早晚各半小時是高管完全能自主掌控的領地，將這 14 件事固化為肌肉記憶，終身受益。"
      },
      {
        id: 11,
        badge: "實操演練 ｜ 練習一：熱啟動",
        title: "15分鐘情緒熱啟動練習 (Priming)",
        subtitle: "三組呼吸、心跳連結、感恩釋放與目標可視化",
        image: "https://images.unsplash.com/photo-1506126613408-eca07ce68773?auto=format&fit=crop&w=1200&q=80",
        imageCaption: "源自 Tony Robbins 的熱啟動法：透過強力呼吸打開胸腔，以感恩能量灌注三大戰略目標",
        layout: "content",
        highlights: [
          { title: "步驟一：三組強力呼吸", desc: "雙手高舉過頭打開胸腔，用力配合擺臂大口呼氣，體會身體發熱、能量貫通。" },
          { title: "步驟二：心跳與生命感恩", desc: "撫胸感謝心臟不知疲倦跳動；腦海重溫生命中 3 件最感激的人事物（貴人、轉折、溫情）。" },
          { title: "步驟三：身心治癒與能量外放", desc: "將生命能量導向緊繃疼痛器官給予療癒；主動化解緊張關係；將慈悲勇氣釋放給團隊。" },
          { title: "步驟四：三大目標達成可視化", desc: "花 2 分鐘凝視近期 3 個核心目標，具體感受實現時的喜悅與歡慶場景，深度錨定神經系統。" }
        ],
        speakerNotes: "【實操指南】在重大戰略會議、登台演講或談判前，花 10 分鐘做完這套熱啟動。氣場將立刻從焦慮疲憊切換為掌控全局的強大自信。"
      },
      {
        id: 12,
        badge: "實操演練 ｜ 練習二：正念冥想",
        title: "正念呼吸冥想練習 (Meditation)",
        subtitle: "穩坐不靠背、吸氣計數 1~10 與客觀貼標籤",
        image: "https://images.unsplash.com/photo-1545205597-3d9d02c29597?auto=format&fit=crop&w=1200&q=80",
        imageCaption: "正念呼吸不是放空，而是讓交感神經降溫、副交感神經重置的精密醫學技術",
        layout: "content",
        highlights: [
          { title: "準備姿態：清醒與放鬆", desc: "背挺直、不靠椅背、雙腳踏地、雙手平放腿上，微閉雙眼，讓脊椎自然承托重量。" },
          { title: "全身由上至下掃描放鬆", desc: "眼周放鬆 → 雙肩下沉 → 雙腿放鬆；透過雙腳踏地與坐骨觸感將心神拉回身體。" },
          { title: "鼻吸嘴呼與吸氣計數", desc: "鼻子吸嘴巴呼；心念「吸氣、呼氣」；只數吸氣，由 1 數至 10，連續進行兩輪。" },
          { title: "情緒與念頭客觀貼標籤", desc: "冒出焦慮或雜念時不自責推開，客觀標記「焦慮」或「雜念」，觀察後溫柔回歸呼吸。" }
        ],
        speakerNotes: "【正念心法】每天中午或睡前 10 分鐘正念冥想。練習時走神是完全正常的，每一次把注意力牽引回呼吸，就是在鍛鍊前額葉專注力肌肉。"
      },
      {
        id: 13,
        badge: "1978 高管專章 ｜ 思考架構篇",
        title: "1978 高階主管三大心智模型",
        subtitle: "突破 48 歲雙重暗礁，建立戰略精力護城河",
        image: "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80",
        imageCaption: "專為 1978 年次經理人訂製：跳出加班陷阱，重構 F1 賽車底盤觀、認知帶寬與能量 ROI",
        layout: "content",
        highlights: [
          { title: "48歲生理與事業暗礁", desc: "基礎代謝降15%、海馬體累計萎縮9%、內臟脂肪易堆積、深睡縮減；事業家庭責任達峰。" },
          { title: "模型一：F1賽車底盤觀", desc: "高管是賽車手也是車隊經理。獲勝靠機械極限與定期進站保養，不靠蠻力狂踩油門。" },
          { title: "模型二：認知帶寬保護法則", desc: "百萬年薪只為每日 2~3 個高維戰略決策而付。絕不容許瑣事與血糖崩潰掠奪前額葉。" },
          { title: "模型三：能量 ROI 投資觀", desc: "每日投資 1.5 小時在精力系統，換回每週多出 20 小時具備絕對清醒度的頂級戰鬥力。" }
        ],
        speakerNotes: "【專章核心】1978 年次的經理人，48歲不是衰退的起點，而是將沉澱經驗與極限精力整合為王牌優勢的起點。這套心智模型將助您徹底拉開與同儕的差距。"
      },
      {
        id: 14,
        badge: "1978 高管專章 ｜ 極限行動篇",
        title: "48 歲經理人四大實戰作戰 SOP",
        subtitle: "晨間超能啟動、戰場防禦、應酬生存與指標紅線",
        image: "https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=1200&q=80",
        imageCaption: "落地的四大高管作戰手冊：守住上午 9:30~11:30 決策波峰，守住內臟脂肪 ≤ 8 與瘦體重",
        layout: "content",
        highlights: [
          { title: "晨間超能啟動 (06:30-07:30)", desc: "600ml溫水鹽檸檬 → 晨光照射10分 → 鎖定今日 3 大戰略決策 → 深蹲心率啟動 → 高蛋白早餐。" },
          { title: "高壓會議戰場能量防禦", desc: "戰略重會安排在上午 09:30~11:30 認知峰值；午餐菜肉倒序抗昏睡；15:00 咖啡因斷點。" },
          { title: "商務應酬與差旅生存", desc: "應酬前30分溫水加蛋保護胃壁；酒水 1:1 溫水交換；差旅包備齊眼罩耳塞筋膜球彈力繩。" },
          { title: "48歲體態監控紅線", desc: "體脂率 ≤ 22% (男) / ≤ 26% (女)；內臟脂肪 ≤ 8；瘦體重 ≥ 60.5kg；安檢HP吹氣與HOMA-IR。" }
        ],
        speakerNotes: "【作戰清單】這四條 SOP 是您身為 48 歲經理人的行動守則。無論出差或應酬，嚴格執行胃壁保護與 1:1 溫水交換，讓您隔天依然能在董事會精力充沛、從容掌舵。"
      },
      {
        id: 15,
        badge: "結語與擴充 ｜ 終身巔峰",
        title: "精力像肌肉，練就終身巔峰體態",
        subtitle: "從業餘選手邁向職業選手 · 未來擴充知識群",
        image: "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=80",
        imageCaption: "大衛人生健康系統持續擴充：馮雪科學減肥、高質量睡眠、家庭健康三部曲陸續連動",
        layout: "cover",
        highlights: [
          { title: "從業餘邁向職業", desc: "告別野生摸索，將醫學級精力管理系統化為本能反應與生活風格。" },
          { title: "未來擴充課綱", desc: "即將連動《馮雪·科學減肥16講》、《怎樣獲得高質量睡眠》、《家庭健康100講》。" },
          { title: "立即行動建議", desc: "從今日午餐先吃菜、今晚熱水泡腳 15 分鐘開始，開啟您的精力逆齡正循環！" }
        ],
        speakerNotes: "【總結致意】感謝閱讀。精力管理不是短跑，而是一場優雅從容的終身超級馬拉松。回到知識門戶可進行全文檢索，或前往 4 週追蹤儀表板記錄每日數據。"
      }
    ];

    let currentSlideIndex = 0; // 0-based
    const totalSlides = SLIDES.length;

    // DOM Elements
    const slideViewport = document.getElementById('slide-viewport');
    const progressBar = document.getElementById('progress-bar');
    const slideNumCurrent = document.getElementById('slide-num-current');
    const slideNumTotal = document.getElementById('slide-num-total');
    const slideTitlePreview = document.getElementById('slide-title-preview');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');

    const toggleNotesBtn = document.getElementById('toggle-notes-btn');
    const notesPanel = document.getElementById('notes-panel');
    const notesContent = document.getElementById('notes-content');
    const closeNotesBtn = document.getElementById('close-notes-btn');

    const toggleDrawerBtn = document.getElementById('toggle-drawer-btn');
    const drawerPanel = document.getElementById('drawer-panel');
    const closeDrawerBtn = document.getElementById('close-drawer-btn');
    const drawerGrid = document.getElementById('drawer-thumbnails-grid');
    const fullscreenBtn = document.getElementById('fullscreen-btn');

    slideNumTotal.textContent = totalSlides;

    function renderCurrentSlide() {
      const s = SLIDES[currentSlideIndex];
      
      // Update header
      slideNumCurrent.textContent = String(s.id).padStart(2, '0');
      slideTitlePreview.textContent = s.title;
      progressBar.style.width = `${((currentSlideIndex + 1) / totalSlides) * 100}%`;

      // Update notes
      notesContent.innerHTML = `
        <p class="text-amber-300 font-semibold mb-1">【第 ${s.id} 頁 · ${s.title}】</p>
        <p class="text-slate-300 leading-relaxed">${s.speakerNotes}</p>
      `;

      // Check if cover or content layout
      const isCover = s.layout === 'cover';
      const isExecSpecial = s.id === 13 || s.id === 14;

      const badgeColor = isExecSpecial 
        ? 'bg-amber-500/20 text-amber-300 border-amber-500/30' 
        : 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30';

      const contentHtml = `
        <!-- Left Visual Side (50%) -->
        <div class="w-full md:w-1/2 h-48 md:h-full relative overflow-hidden bg-slate-950 shrink-0">
          <img src="${s.image}" alt="${s.title}" class="w-full h-full object-cover filter brightness-95">
          <div class="absolute inset-0 bg-gradient-to-t md:bg-gradient-to-r from-slate-900/90 via-slate-900/30 to-transparent"></div>
          
          <div class="absolute top-4 left-4">
            <span class="px-2.5 py-1 rounded-full text-xs font-bold ${badgeColor} border backdrop-blur-md">
              ${s.badge}
            </span>
          </div>

          <div class="absolute bottom-4 left-4 right-4">
            <p class="text-[11px] text-slate-300/90 bg-slate-950/70 backdrop-blur-sm p-2 rounded-lg border border-slate-800">
              <i class="ph-bold ph-image text-emerald-400 mr-1"></i>${s.imageCaption}
            </p>
          </div>
        </div>

        <!-- Right Content Side (50%) -->
        <div class="w-full md:w-1/2 h-full p-6 sm:p-8 flex flex-col justify-between overflow-y-auto no-scrollbar">
          <div>
            <div class="flex items-center justify-between text-xs text-slate-400 mb-2">
              <span class="font-mono text-emerald-400 font-bold">SLIDE ${String(s.id).padStart(2, '0')}</span>
              <span class="text-slate-500">${isExecSpecial ? '★ 1978高管專章' : '張遇升·精力管理高手'}</span>
            </div>

            <h2 class="text-2xl sm:text-3xl font-black text-white tracking-tight leading-tight mb-1.5">
              ${s.title}
            </h2>
            <p class="text-xs sm:text-sm text-brand-400 font-medium mb-6">
              ${s.subtitle}
            </p>

            <!-- Highlights list -->
            <div class="space-y-3 mb-6">
              ${s.highlights.map(h => `
                <div class="p-3 sm:p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 hover:border-slate-700 transition">
                  <div class="text-xs font-bold text-white mb-0.5 flex items-center gap-1.5">
                    <span class="w-1.5 h-1.5 rounded-full ${isExecSpecial ? 'bg-amber-400' : 'bg-emerald-400'}"></span>
                    <span class="${isExecSpecial ? 'text-amber-300' : 'text-emerald-300'}">${h.title}</span>
                  </div>
                  <p class="text-xs text-slate-300 leading-relaxed pl-3">${h.desc}</p>
                </div>
              `).join('')}
            </div>
          </div>

          <!-- Bottom Slide Footer Info -->
          <div class="pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
            <span>得到大腦知識庫 · 大衛人生</span>
            <button onclick="toggleNotes()" class="text-amber-400 hover:text-amber-300 font-semibold flex items-center gap-1">
              <i class="ph-bold ph-note-pencil"></i> 查看本頁講義解讀
            </button>
          </div>
        </div>
      `;

      slideViewport.innerHTML = contentHtml;

      // Update button states
      prevBtn.disabled = currentSlideIndex === 0;
      prevBtn.style.opacity = currentSlideIndex === 0 ? '0.3' : '1';
      nextBtn.disabled = currentSlideIndex === totalSlides - 1;
      nextBtn.style.opacity = currentSlideIndex === totalSlides - 1 ? '0.3' : '1';

      // Update URL hash without scroll
      history.replaceState(null, null, `#slide-${s.id}`);
    }

    function goToSlide(index) {
      if (index >= 0 && index < totalSlides) {
        currentSlideIndex = index;
        renderCurrentSlide();
      }
    }

    function nextSlide() {
      if (currentSlideIndex < totalSlides - 1) {
        goToSlide(currentSlideIndex + 1);
      }
    }

    function prevSlide() {
      if (currentSlideIndex > 0) {
        goToSlide(currentSlideIndex - 1);
      }
    }

    function toggleNotes() {
      notesPanel.classList.toggle('hidden');
    }

    function toggleDrawer() {
      if (drawerPanel.classList.contains('hidden')) {
        renderDrawerThumbnails();
        drawerPanel.classList.remove('hidden');
      } else {
        drawerPanel.classList.add('hidden');
      }
    }

    function renderDrawerThumbnails() {
      drawerGrid.innerHTML = SLIDES.map((s, idx) => {
        const activeClass = idx === currentSlideIndex ? 'ring-2 ring-emerald-400 border-emerald-400' : 'border-slate-800';
        return `
          <div onclick="goToSlide(${idx}); toggleDrawer();" class="cursor-pointer group rounded-xl overflow-hidden bg-slate-950 border ${activeClass} hover:border-brand-500 transition">
            <div class="h-20 overflow-hidden relative">
              <img src="${s.image}" alt="${s.title}" class="w-full h-full object-cover group-hover:scale-105 transition">
              <span class="absolute top-1 left-1 px-1.5 py-0.5 rounded text-[9px] font-bold bg-slate-900/80 text-white">
                ${String(s.id).padStart(2, '0')}
              </span>
            </div>
            <div class="p-2">
              <div class="text-[11px] font-bold text-white truncate">${s.title}</div>
              <div class="text-[10px] text-slate-400 truncate">${s.badge}</div>
            </div>
          </div>
        `;
      }).join('');
    }

    // Keyboard navigation
    window.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
        e.preventDefault();
        nextSlide();
      } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault();
        prevSlide();
      } else if (e.key === 'Home') {
        e.preventDefault();
        goToSlide(0);
      } else if (e.key === 'End') {
        e.preventDefault();
        goToSlide(totalSlides - 1);
      } else if (e.key === 'f' || e.key === 'F') {
        toggleFullscreen();
      } else if (e.key === 'n' || e.key === 'N') {
        toggleNotes();
      } else if (e.key === 't' || e.key === 'T') {
        toggleDrawer();
      } else if (e.key === 'Escape') {
        if (!drawerPanel.classList.contains('hidden')) toggleDrawer();
        if (!notesPanel.classList.contains('hidden')) toggleNotes();
      }
    });

    // Touch Swipe Navigation
    let touchStartX = 0;
    window.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
    }, false);
    window.addEventListener('touchend', (e) => {
      const touchEndX = e.changedTouches[0].screenX;
      if (touchEndX < touchStartX - 50) nextSlide();
      if (touchEndX > touchStartX + 50) prevSlide();
    }, false);

    // Fullscreen toggle
    function toggleFullscreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
      } else {
        if (document.exitFullscreen) document.exitFullscreen();
      }
    }

    fullscreenBtn.addEventListener('click', toggleFullscreen);
    toggleNotesBtn.addEventListener('click', toggleNotes);
    closeNotesBtn.addEventListener('click', toggleNotes);
    toggleDrawerBtn.addEventListener('click', toggleDrawer);
    closeDrawerBtn.addEventListener('click', toggleDrawer);
    prevBtn.addEventListener('click', prevSlide);
    nextBtn.addEventListener('click', nextSlide);

    // Initial slide from hash
    const hash = window.location.hash;
    if (hash && hash.startsWith('#slide-')) {
      const parsed = parseInt(hash.replace('#slide-', ''), 10);
      if (!isNaN(parsed) && parsed >= 1 && parsed <= totalSlides) {
        currentSlideIndex = parsed - 1;
      }
    }

    renderCurrentSlide();
  </script>
</body>
</html>
'''

# Write files
with open(os.path.join(base_dir, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html_content)

with open(os.path.join(base_dir, "slides.html"), "w", encoding="utf-8") as f:
    f.write(slides_html_content)

print("Generated index.html and slides.html successfully.")
