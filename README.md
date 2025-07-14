# Hotel Checker 🏨⏰

自動檢查「銀山莊」與「古勢起屋別館」等溫泉旅館的網站空房狀況，並透過 Discord 通知你有沒有房！

## 🔧 功能說明

- 每日自動檢查指定日期區間是否有空房（支援跨月）
- 支援多間飯店（目前支援：銀山莊、古勢起屋別館）
- 成功偵測到空房會自動傳送 Discord Webhook 通知
- 使用 `undetected_chromedriver` 模擬真實瀏覽器行為，避免網站封鎖
- 可透過 Windows 工作排程自動化執行

## 📌 使用前準備

1. 安裝 Python 套件：
```bash
pip install -r requirements.txt
```

2. 確保你的 Python 版本為 3.8，並安裝 Chrome 瀏覽器。
3. 修改 `WEBHOOK_URL` 來填入你自己的 Discord Webhook。

## 🗂 檔案結構

```
ginzanchecker/
├── ginzan_checker.py        # 主程式（銀山莊）
├── kosekiya_checker.py      # 主程式（古勢起屋別館）
├── requirements.txt         # 所需套件列表
├── README.md                # 專案說明
```

## 🖥 自動排程建議

建議使用 Windows 的「工作排程器」設定每天 23:05 自動執行：

- 動作：啟動程式
- 程式：`python`
- 引數：`ginzan_checker.py`

（建議搭配 VPN 使用，避免頻繁查詢導致 IP 封鎖）

## ✨ 範例通知

```
📢 銀山莊以下日期有空房：
• 2025-12-10 👉 https://reserve.489ban.net/client/ginzanso/2/plan/search?date=2025/12/10&roomCount=1
• 2025-12-11 👉 https://reserve.489ban.net/client/ginzanso/2/plan/search?date=2025/12/11&roomCount=1
```

## 🧊 其他注意事項

- 若網站封鎖 IP，建議使用 VPN 或切換網路。
- 若要增加其他旅館，只需仿照 `kosekiya_checker.py` 加入新頁面邏輯即可。

---

歡迎 fork、star ⭐ 或協助開發新功能！