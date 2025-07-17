import time
import os
from dotenv import load_dotenv
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# === 載入帳號密碼 ===
load_dotenv()
USERMAIL = os.getenv("EMAIL")
USERPASSWORD = os.getenv("PASSWORD")

# === 參數設定 ===
URL = "https://reserve.489ban.net/client/ginzanso/2/plan/search?date=2025/12/10&roomCount=1"
MALE_SELECT_ID = "guests_6217"
FEMALE_SELECT_ID = "guests_6218"
TARGET_ROOM_CLASS = "planRoom_200831"

# === 表單預選參數（可改動） ===
CHECKIN_HOUR = "15"
CHECKIN_MIN = "00"
ARRIVAL_METHOD = "3119"   # 火車
PICKUP_TIME = "17512"     # JR大石田站 13:40 出發
RETURN_TIME = "17516"     # 銀山莊 12:30 出發

# === 啟動 Chrome 瀏覽器 ===
options = uc.ChromeOptions()
driver = uc.Chrome(options=options)
driver.get(URL)
wait = WebDriverWait(driver, 10)

# === 選擇人數 ===
male_select = wait.until(EC.presence_of_element_located((By.ID, MALE_SELECT_ID)))
Select(male_select).select_by_value("1")
print("👨 男士選擇 1")

female_select = wait.until(EC.presence_of_element_located((By.ID, FEMALE_SELECT_ID)))
Select(female_select).select_by_value("1")
print("👩 女士選擇 1")

# === 點擊「檢索」按鈕 ===
search_button = wait.until(EC.element_to_be_clickable((By.ID, "submit")))
search_button.click()
print("🔍 點擊檢索按鈕")

# === 點擊日式客房的「詳細內容／訂房」 ===
print("🛏️ 正在尋找『日式客房』...")

room_button = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/detail/200831')]")))
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", room_button)
time.sleep(0.5)
driver.execute_script("arguments[0].click();", room_button)
print("✅ 成功點擊『日式客房』的訂房按鈕")

# === 點擊金額確認／輸入個人資訊 ===
print("📝 前往金額確認與個人資訊頁...")

confirm_btn = wait.until(EC.element_to_be_clickable((By.ID, "confirm_submit")))
confirm_btn.click()
print("✅ 已進入輸入個人資料頁")

# === 登入帳號 ===
print("🔐 正在自動填入帳號密碼...")

email_input = wait.until(EC.presence_of_element_located((By.ID, "authEmailInput")))
email_input.send_keys(USERMAIL)

password_input = wait.until(EC.presence_of_element_located((By.ID, "authPasswordInput")))
password_input.send_keys(USERPASSWORD)

login_button = wait.until(EC.element_to_be_clickable((By.ID, "login")))
login_button.click()
print("✅ 登入送出完成")

# === 表單選擇下拉選單 ===
print("📝 填寫下拉選單表單選項...")

check_in_hour = wait.until(EC.presence_of_element_located((By.ID, "check_in_hour")))
Select(check_in_hour).select_by_value(CHECKIN_HOUR)
print(f"🕒 選擇入住時間（時）: {CHECKIN_HOUR}")

check_in_minute = wait.until(EC.presence_of_element_located((By.ID, "check_in_minute")))
Select(check_in_minute).select_by_value(CHECKIN_MIN)
print(f"🕒 選擇入住時間（分）: {CHECKIN_MIN}")

arrival_method = wait.until(EC.presence_of_element_located((By.ID, "customizeForm[1233]")))
Select(arrival_method).select_by_value(ARRIVAL_METHOD)
print("🚆 選擇抵達方式：火車")

pickup_time = wait.until(EC.presence_of_element_located((By.ID, "customizeForm[8088]")))
Select(pickup_time).select_by_value(PICKUP_TIME)
print("🚌 選擇接駁時間（大石田→銀山莊）：13:40")

return_time = wait.until(EC.presence_of_element_located((By.ID, "customizeForm[8089]")))
Select(return_time).select_by_value(RETURN_TIME)
print("🚌 選擇接駁時間（銀山莊→大石田）：12:30")

# === 保留畫面 15 秒查看 ===
print("🖥 保留畫面 15 秒讓你查看...")
time.sleep(15)
driver.quit()
