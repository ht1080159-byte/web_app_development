# 系統流程圖與操作路徑 (Flowchart) - 英文口說練習系統

## 1. 使用者流程圖 (User Flow)

這張圖展示了使用者進入系統後，從瀏覽題目、進行測驗到查看成績的完整操作路徑。

```mermaid
flowchart TD
    A([使用者開啟系統]) --> B[首頁 / 登入頁面]
    B --> C{是否已登入？}
    C -->|否| D[進行註冊 / 登入]
    D --> E[進入儀表板 Dashboard]
    C -->|是| E
    
    E --> F[選擇練習課程 / 主題]
    F --> G[進入口說測驗頁面]
    
    G --> H[1. 聆聽標準發音範例]
    G --> I[2. 點擊錄音並朗讀]
    I --> J[結束錄音並送出]
    
    J --> K{系統處理與評分中...}
    K --> L[顯示分數與發音弱點回饋]
    
    L --> M{下一步？}
    M -->|下一題| G
    M -->|查看整體紀錄| E
```

## 2. 系統序列圖 (Sequence Diagram)

這張圖詳細描述了核心功能：「使用者點擊錄音並送出」到「取得分數並存入資料庫」背後的系統互動流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (前端 JS)
    participant Flask as 後端 Flask (practice.py)
    participant VoiceAPI as 第三方語音 API
    participant DB as SQLite 資料庫
    
    User->>Browser: 點擊「開始錄音」並講話
    Browser->>Browser: Web Audio API 擷取麥克風音訊
    User->>Browser: 點擊「結束錄音」
    Browser->>Browser: 將音訊打包為 Blob
    Browser->>Flask: POST /api/upload_audio (夾帶音檔與題目ID)
    
    activate Flask
    Flask->>VoiceAPI: 轉傳音檔請求文字轉語音 (STT) 辨識
    activate VoiceAPI
    VoiceAPI-->>Flask: 回傳辨識文本 (Text) 與信心分數 (Confidence)
    deactivate VoiceAPI
    
    Flask->>Flask: 邏輯比對：標準答案 vs 辨識文本<br>(找出錯字、計算最終得分)
    
    Flask->>DB: INSERT INTO records (user_id, question_id, score, wrong_words)
    activate DB
    DB-->>Flask: 儲存成功
    deactivate DB
    
    Flask->>Flask: 刪除 temp/ 目錄下的暫存音檔
    
    Flask-->>Browser: 回傳 JSON: {score: 85, wrong_words: [...]}
    deactivate Flask
    
    Browser->>User: 更新畫面，顯示分數與紅色標示錯字
```

## 3. 功能清單對照表

本表列出系統主要功能與其對應的 URL 路徑與 HTTP 方法，供後續 API 實作參考。

| 功能模組 | 操作描述 | HTTP 方法 | URL 路徑 | 對應的 Route 檔案 |
| :--- | :--- | :--- | :--- | :--- |
| **網頁載入** | 首頁 (歡迎畫面) | GET | `/` | `routes/main.py` |
| **帳號系統** | 註冊帳號 | POST | `/auth/register` | `routes/auth.py` |
| **帳號系統** | 登入帳號 | POST | `/auth/login` | `routes/auth.py` |
| **帳號系統** | 登出 | GET | `/auth/logout` | `routes/auth.py` |
| **學習追蹤** | 儀表板 (顯示歷史分數與列表) | GET | `/dashboard` | `routes/main.py` |
| **口說測驗** | 取得題目列表 | GET | `/practice/topics` | `routes/practice.py` |
| **口說測驗** | 進入特定題目測驗頁面 | GET | `/practice/<topic_id>` | `routes/practice.py` |
| **核心功能** | **上傳錄音檔並取得評分** | **POST** | `/api/upload_audio` | `routes/practice.py` |
| **學習追蹤** | 取得特定題目的歷史詳細紀錄 | GET | `/api/records/<topic_id>` | `routes/practice.py` |
