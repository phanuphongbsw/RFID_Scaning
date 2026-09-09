import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret-key-change-in-production"
    )

    # Online Database
    # ใช้ DATABASE_URL จาก Hosting
    # ถ้าไม่มี จะกลับไปใช้ SQLite เดิม
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        # Render บางกรณีให้ URL เป็น postgres://
        if database_url.startswith("postgres://"):
            database_url = database_url.replace(
                "postgres://",
                "postgresql://",
                1
            )

        SQLALCHEMY_DATABASE_URI = database_url
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///shop_shirt.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(__file__),
        "static",
        "uploads"
    )

    SLIP_FOLDER = os.path.join(
        os.path.dirname(__file__),
        "static",
        "slips"
    )

    MAX_CONTENT_LENGTH = 5 * 1024 * 1024

    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "gif",
        "webp"
    }

    PAYMENT_TIMEOUT_MINUTES = 15
