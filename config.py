import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # ✅ เปลี่ยนจาก MySQL เป็น SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///shop_shirt.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads")
    SLIP_FOLDER = os.path.join(os.path.dirname(__file__), "static", "slips")
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
    PAYMENT_TIMEOUT_MINUTES = 15