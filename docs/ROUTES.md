# 路由設計文件 (Routes) - 英文口說練習系統

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 / 輸出 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁** | GET | `/` | `templates/index.html` | 系統介紹與入口 |
| **儀表板** | GET | `/dashboard` | `templates/dashboard.html` | 顯示個人學習紀錄與分數走勢 |
| **註冊頁面** | GET | `/auth/register` | `templates/auth/register.html` | 顯示註冊表單 |
| **處理註冊** | POST | `/auth/register` | — (重導向至登入) | 接收表單並建立帳號 |
| **登入頁面** | GET | `/auth/login` | `templates/auth/login.html` | 顯示登入表單 |
| **處理登入** | POST | `/auth/login` | — (重導向至儀表板) | 驗證帳號密碼並建立 Session |
| **登出** | GET | `/auth/logout` | — (重導向至首頁) | 清除 Session |
| **題庫列表** | GET | `/practice/topics` | `templates/practice/topics.html` | 列出所有可用的口說練習題目 |
| **口說測驗頁** | GET | `/practice/<int:topic_id>` | `templates/practice/practice.html` | 顯示題目內容並提供錄音介面 |
| **錄音評分 API** | POST | `/api/upload_audio` | 回傳 JSON | 接收前端音檔，進行語音辨識、評分、存檔並回傳結果 |

## 2. 每個路由的詳細說明

### `main.py` (一般頁面)

*   `GET /`
    *   **輸入**：無
    *   **處理邏輯**：判斷若已登入，可顯示「進入儀表板」按鈕。
    *   **輸出**：渲染 `index.html`。
*   `GET /dashboard`
    *   **輸入**：Session 中的 `user_id`。
    *   **處理邏輯**：驗證登入狀態，若未登入導回 `/auth/login`。呼叫 `Record.get_by_user(user_id)` 取得歷史紀錄。
    *   **輸出**：渲染 `dashboard.html`，並傳入紀錄變數。

### `auth.py` (帳號系統)

*   `POST /auth/register`
    *   **輸入**：表單的 `username`, `email`, `password`。
    *   **處理邏輯**：驗證輸入是否空白、密碼長度，將密碼 hash 後呼叫 `User.create()`。
    *   **輸出**：註冊成功重導向 `/auth/login`，失敗則重新渲染帶有錯誤訊息的 `register.html`。
*   `POST /auth/login`
    *   **輸入**：表單的 `email`, `password`。
    *   **處理邏輯**：呼叫 `User.get_by_email()` 驗證密碼，成功則將 `user_id` 寫入 session。
    *   **輸出**：成功重導向 `/dashboard`，失敗則重新渲染帶有錯誤訊息的 `login.html`。

### `practice.py` (核心測驗系統)

*   `GET /practice/topics`
    *   **輸入**：無。
    *   **處理邏輯**：驗證登入狀態。呼叫 `Topic.get_all()` 取得題庫列表。
    *   **輸出**：渲染 `topics.html`，傳入題目列表。
*   `GET /practice/<int:topic_id>`
    *   **輸入**：URL 參數 `topic_id`。
    *   **處理邏輯**：呼叫 `Topic.get_by_id(topic_id)`，若找不到則回傳 404 錯誤。
    *   **輸出**：渲染 `practice.html`，傳入該題目的詳細內容。
*   `POST /api/upload_audio`
    *   **輸入**：Form Data (`audio_blob`, `topic_id`)。
    *   **處理邏輯**：驗證登入狀態。暫存音檔 -> 呼叫 STT API 辨識 -> 與 `Topic` 內容比對計算 `score` 與 `wrong_words` -> 呼叫 `Record.create()` 存檔 -> 刪除暫存檔。
    *   **輸出**：`{"status": "success", "score": 85, "wrong_words": ["apple"], "recognized_text": "I want an appl"}`。若失敗回傳 400 或 500 JSON 錯誤。

## 3. Jinja2 模板清單

所有的模板都將繼承自共用的 `base.html`，確保導覽列 (Navbar) 與樣式一致。

1.  `templates/base.html` (共用骨架)
2.  `templates/index.html` (首頁)
3.  `templates/dashboard.html` (個人儀表板)
4.  `templates/auth/register.html` (註冊表單)
5.  `templates/auth/login.html` (登入表單)
6.  `templates/practice/topics.html` (題庫列表)
7.  `templates/practice/practice.html` (錄音與測驗介面)
