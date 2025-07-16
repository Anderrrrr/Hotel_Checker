import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# === 參數設定 ===
URL = "https://reserve.489ban.net/client/ginzanso/2/plan/search?date=2025/12/10&roomCount=1"
MALE_SELECT_ID = "guests_6217"
FEMALE_SELECT_ID = "guests_6218"
TARGET_ROOM_CLASS = "planRoom_200831"

# === 啟動 Chrome 瀏覽器 ===
options = uc.ChromeOptions()
driver = uc.Chrome(options=options)
driver.get(URL)

wait = WebDriverWait(driver, 10)

# === 選擇男士人數 ===
male_select = wait.until(EC.presence_of_element_located((By.ID, MALE_SELECT_ID)))
Select(male_select).select_by_value("1")
print("👨 男士選擇 1")

# === 選擇女士人數 ===
female_select = wait.until(EC.presence_of_element_located((By.ID, FEMALE_SELECT_ID)))
Select(female_select).select_by_value("1")
print("👩 女士選擇 1")

# === 點擊「檢索」按鈕 ===
search_button = wait.until(EC.element_to_be_clickable((By.ID, "submit")))
search_button.click()
print("🔍 點擊檢索按鈕")

# === 點擊『日式客房』的『詳細內容／訂房』按鈕 ===
print("🛏️ 正在尋找『日式客房』...")

room_button = wait.until(EC.presence_of_element_located((
    By.XPATH,
    "//a[contains(@href, '/detail/200831')]"
)))

# ✅ 先滾動到畫面中間，確保可見
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", room_button)
time.sleep(0.5)  # 小等一下，確保動畫消失

# ✅ 強制用 JavaScript 點擊（繞過圖片遮擋）
driver.execute_script("arguments[0].click();", room_button)
print("✅ 成功點擊『日式客房』的訂房按鈕")

# === 點擊『金額確認／輸入個人資訊』按鈕 ===
print("📝 前往金額確認與個人資訊頁...")

confirm_btn = wait.until(EC.element_to_be_clickable((By.ID, "confirm_submit")))
confirm_btn.click()

print("✅ 已進入輸入個人資料頁")

