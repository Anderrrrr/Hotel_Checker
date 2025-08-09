import time
from datetime import datetime, timedelta
import requests
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === 設定區 ===
WEBHOOK_URL = "https://discord.com/api/webhooks/1393843377170288700/l7iwgH95a0PdIFM5QSL2RchuWV4S3hDMomuY-xmY88BVbSlUwUjN9Tjy4ohz8P7mBsik"
CHECK_START = "2026-02-27"
CHECK_END = "2026-03-08"

HOTELS = [
    {
        "name": "銀山莊",
        "id": "ginzanso",
        "base_url": "https://reserve.489ban.net/client/ginzanso/2/plan/availability/daily",
        "reserve_link": "https://reserve.489ban.net/client/ginzanso/2/plan/search?date={date}&roomCount=1"
    },
    {
        "name": "古勢起屋別館",
        "id": "kosekiya",
        "base_url": "https://reserve.489ban.net/client/kosekiya/2/plan/availability/daily",
        "reserve_link": "https://reserve.489ban.net/client/kosekiya/2/plan/search?date={date}&roomCount=1"
    },
    {
        "name": "能登屋",
        "id": "notoyaryokan",
        "base_url": "https://reserve.489ban.net/client/notoyaryokan/4/plan/availability/daily",
        "reserve_link": "https://reserve.489ban.net/client/notoyaryokan/4/plan/search?date={date}&roomCount=1"
    }
]

def scroll_until_all_months_loaded(driver, start_date, end_date):
    wait = WebDriverWait(driver, 5)
    max_clicks = 12
    clicks = 0

    needed_months = set()
    cur = start_date
    while cur <= end_date:
        needed_months.add((cur.year, cur.month))
        cur += timedelta(days=1)

    while clicks < max_clicks:
        loaded_months = set()
        for i in range(3):
            try:
                header = driver.find_element(By.ID, f"yearMonth_{i}")
                ym = header.text.strip()
                if "年" in ym and "月" in ym:
                    year = int(ym.split("年")[0])
                    month = int(ym.split("年")[1].split("月")[0])
                    loaded_months.add((year, month))
            except:
                continue

        if needed_months.issubset(loaded_months):
            return True

        try:
            next_button = wait.until(EC.element_to_be_clickable((By.ID, "next")))
            next_button.click()
            time.sleep(1.2)
            clicks += 1
        except:
            break

    return False

def get_available_dates(driver, start_date, end_date):
    available = []

    if not scroll_until_all_months_loaded(driver, start_date, end_date):
        return []

    for table_idx in range(3):
        try:
            table = driver.find_element(By.ID, f"availabilityCalendar_{table_idx}")
            labels = table.find_elements(By.CSS_SELECTOR, "label[for='day']")
            for label in labels:
                day_text = label.text.strip()
                if not day_text.isdigit():
                    continue

                try:
                    td = label.find_element(By.XPATH, "./ancestor::td")
                    icons = td.find_elements(By.CSS_SELECTOR, "i.fa-circle")
                    if not icons:
                        continue

                    ym_header = driver.find_element(By.ID, f"yearMonth_{table_idx}")
                    ym = ym_header.text.strip()
                    year = int(ym.split("年")[0])
                    month = int(ym.split("年")[1].split("月")[0])
                    day = int(day_text)

                    date_obj = datetime(year, month, day)
                    if start_date <= date_obj <= end_date:
                        date_str = date_obj.strftime("%Y-%m-%d")
                        available.append(date_str)
                        print(f"[INFO] ✅ 有空房：{date_str}")
                except:
                    continue
        except:
            continue
    return available

def send_discord_message(hotel_name, reserve_link_template, dates):
    if not dates:
        return
    lines = [f"📢 **{hotel_name}** 有空房！"]
    for d in dates:
        display = datetime.strptime(d, "%Y-%m-%d").strftime("%m/%d")
        link = reserve_link_template.format(date=d.replace("-", "/"))
        lines.append(f"• {display} 👉 [點我訂房]({link})")
    payload = {"content": "\n".join(lines)}
    try:
        requests.post(WEBHOOK_URL, json=payload, timeout=5)
        print(f"[INFO] ✅ 已發送 Discord 通知 ({hotel_name})")
    except Exception as e:
        print(f"[ERROR] Discord 傳送失敗：{e}")

def check_hotel(hotel, s_date, e_date):
    print(f"[INFO] 🏨 正在檢查：{hotel['name']}")
    options = uc.ChromeOptions()
    options.headless = True
    driver = uc.Chrome(options=options)

    try:
        driver.get(hotel["base_url"])
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "availabilityCalendar_0"))
        )
        dates = get_available_dates(driver, s_date, e_date)
    except Exception as e:
        print(f"[ERROR] {hotel['name']} 載入錯誤：{e}")
        dates = []
    finally:
        driver.quit()

    if not dates:
        print(f"[INFO] ❌ 沒有空房：{hotel['name']}（{CHECK_START} 至 {CHECK_END}）")
    else:
        send_discord_message(hotel["name"], hotel["reserve_link"], dates)

# === 主程式 ===
if __name__ == "__main__":
    s_date = datetime.strptime(CHECK_START, "%Y-%m-%d")
    e_date = datetime.strptime(CHECK_END, "%Y-%m-%d")

    for hotel in HOTELS:
        check_hotel(hotel, s_date, e_date)
