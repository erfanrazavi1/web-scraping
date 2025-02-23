# from pymongo import MongoClient

# client = MongoClient("mongodb://localhost:27017/")
# db = client["flight_data"]
# collection = db["flights"]

# def save_to_db(start_city, end_city, flights):
#     """ذخیره اطلاعات پروازها در دیتابیس"""
#     data = {
#         "start": start_city,
#         "end": end_city,
#         "flights": flights
#     }
#     collection.insert_one(data)
#     print("✅ Data saved to MongoDB successfully!")
import sqlite3

# اتصال به دیتابیس (اگر فایل وجود نداشته باشه، خودش می‌سازه)
conn = sqlite3.connect("flights.db")
cursor = conn.cursor()

# ساخت جدول flights
cursor.execute("""
CREATE TABLE IF NOT EXISTS flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    details TEXT NOT NULL
)
""")

conn.commit()


