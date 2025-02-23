import sqlite3
def fetch_flights():
    """دریافت تمام اطلاعات ذخیره‌شده از دیتابیس"""
    conn = sqlite3.connect("flights.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM flights")
    flights = cursor.fetchall()

    conn.close()    
    return flights

def save_to_text(flights, filename="flights.txt"):
    """ذخیره اطلاعات پرواز در یک فایل متنی"""
    with open(filename, "w", encoding="utf-8") as file:
        for flight in flights:
            line = " | ".join(map(str, flight))  # تبدیل هر مقدار به رشته و جدا کردن با "|"
            file.write(line + "\n")  # اضافه کردن هر پرواز به فایل

flights = fetch_flights()
save_to_text(flights)

print("اطلاعات پرواز در فایل flights.txt ذخیره شد.")