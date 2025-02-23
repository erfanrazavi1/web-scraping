from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import jdatetime
import time
import webbrowser
import sqlite3

def setup_driver():
    """Initialize and configure the Chrome WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=options)

def select_location(driver, label_text, city_name):
    """انتخاب شهر در کادر جستجو بر اساس متن label."""
    label = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, f"//label[contains(text(), '{label_text}')]"))
    )
    input_id = label.get_attribute("for")  # گرفتن id فیلد ورودی
    search_box = driver.find_element(By.ID, input_id)
    
    search_box.clear()
    search_box.send_keys(city_name)
    time.sleep(1)

    first_option = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@class, 'font-medium')]"))
    )
    first_option[0].click()



def select_date(driver):
    """Selects tomorrow's date from the calendar."""
    try:
        tomorrow = jdatetime.date.today() + jdatetime.timedelta(days=1)
        # date_input = int(input('enter the date: '))
        xpath = f"//span[@class='calendar-cell']/span[contains(text(), '{tomorrow.day}')]"

        date_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        driver.execute_script("arguments[0].classList.add('is-selected');", date_element)
        date_element.click()
    except Exception as e:
        print(f"Error selecting date: {e}")


def click_button(driver, by, value):
    """Clicks a button identified by the given locator."""
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((by, value))
    )
    button.click()

def get_flight_results(driver):
    """Retrieves flight search results."""
    try:
        results = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "available-card__content"))
        )
    except TimeoutException:
        return ["پروازی در این تاریخ وجود ندارد."]

    return [result.text.strip() for result in results] if results else ["پروازی در این تاریخ وجود ندارد."]



def save_to_html(data):
    import os
    os.makedirs("html_data", exist_ok=True)
    """Saves flight results to an HTML file and opens it in a browser."""
    html_template = """
    <!DOCTYPE html>
    <html lang="fa">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Flight Results</title>
        <style>
            body { font-family: Arial, sans-serif; direction: rtl; text-align: right; background: #f5f5f5; padding: 20px; }
            .container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); }
            h2 { color: #333; text-align: center; }
            .flight { background: #e3f2fd; padding: 15px; border-radius: 5px; margin-bottom: 10px; border-right: 5px solid #007bff; }
            .flight strong { color: #007bff; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Flight Results</h2>
            {flights}
        </div>
    </body>
    </html>
    """

    flights_html = "".join(f'<div class="flight">{flight}</div>' for flight in data)
    final_html = html_template.replace("{flights}", flights_html)

    with open("./core/html_data/flights.html", "w", encoding="utf-8") as f:
        f.write(final_html)
def save_to_database(data):
    """ذخیره اطلاعات پرواز در دیتابیس SQLite"""
    conn = sqlite3.connect("flights.db")
    cursor = conn.cursor()

    for flight in data:
        cursor.execute("INSERT INTO flights (details) VALUES (?)", (flight,))

    conn.commit()
    conn.close()




