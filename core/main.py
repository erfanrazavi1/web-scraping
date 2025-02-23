from flask import Flask, render_template, request, jsonify
from scrapers.flight import *
from database_py.db import *
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def main():
    data = request.json
    inp_start = data['start']
    inp_end = data['end']
    """Main function to automate the flight search process."""
    driver = setup_driver()
    try:
        driver.get("https://www.alibaba.ir/")
        select_location(driver, "مبدا (شهر)", inp_start)
        select_location(driver, "مقصد (شهر)", inp_end)
        select_date(driver)
        click_button(driver, By.CLASS_NAME, "btn.is-nl.is-solid-secondary.px-6")  # Confirm button
        time.sleep(2)
        click_button(driver, By.XPATH, "//button[contains(text(),'جستجو')]")  # Search button
        flight_data = get_flight_results(driver)
        
    
    finally:
        driver.quit()
        save_to_html(flight_data)
        save_to_database(flight_data)
    return jsonify({
        "message": "Search completed successfully",
        "data": flight_data })


if __name__ == "__main__":
    app.run(debug=True)