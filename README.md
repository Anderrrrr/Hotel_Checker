# 🏨 Hotel Checker & Auto Booker

自動檢查「銀山莊」、「古勢起屋別館」等溫泉旅館的空房狀況，並透過 Discord 通知你有沒有房。也支援自動填入訂房資訊、進行預約流程。

---

## 🔧 功能說明

### ✅ 空房偵測（ginzan_checker.py、kosekiya_checker.py）
- 支援每日自動檢查指定日期區間是否有空房（含跨月）
- 支援多間飯店（目前：銀山莊、古勢起屋別館）
- 偵測到空房自動發送 Discord Webhook 通知
- 使用 `undetected_chromedriver` 模擬瀏覽器，降低被封鎖風險
- 可搭配 Windows 工作排程自動執行

### ✅ 自動訂房（ginzan_writer.py）
- 自動開啟查詢網址並填入日期、人數
- 自動選擇特定房型（如日式客房）
- 可自動點擊「詳細內容／訂房」並進入預約頁面
- 預留填寫姓名、電話等欄位的擴充空間

---

## 📦 使用前準備

1. 安裝必要套件：
   ```bash
   pip install -r requirements.txt
   ```

2. 確保 Python 為 **3.8 或以上**，並安裝 Chrome 瀏覽器。

3. 修改程式中的 `WEBHOOK_URL` 為你自己的 Discord Webhook。

---

## 🗂 專案結構

```
ginzanchecker/
├── ginzan_checker.py        # 銀山莊自動查房與通知
├── kosekiya_checker.py      # 古勢起屋別館自動查房與通知
├── ginzan_writer.py         # 自動填寫與預約流程腳本（WIP）
├── requirements.txt         # 所需套件列表
├── README.md                # 專案說明文件
```

---

## 📌 自動排程建議

建議使用 Windows 的「工作排程器」設定每天執行：

- 動作：啟動程式  
- 程式：`python`  
- 引數：`ginzan_checker.py`

🧠 可搭配 VPN 使用，以避免網站封鎖頻繁 IP 查詢。

---

## 🔔 範例 Discord 通知

```
📢 銀山莊以下日期有空房：
• 2025-12-10 👉 https://reserve.489ban.net/client/ginzanso/2/plan/search?date=2025/12/10&roomCount=1
• 2025-12-11 👉 https://reserve.489ban.net/client/ginzanso/2/plan/search?date=2025/12/11&roomCount=1
```

---

## 🧊 其他注意事項

- 若出現網站超時，可嘗試增加 `WebDriverWait` 等待秒數。
- 若被封鎖 IP，建議使用 VPN，或降低查詢頻率。
- 若要擴充其他旅館，只需仿照現有 `.py` 結構新增即可。
- ginzan_writer.py 屬於自動預約功能範例，請自行調整房型 ID 與資料填寫流程。

---

🛠 歡迎 fork、star ⭐ 或協助開發新功能！
