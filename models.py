from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy()


# =========================================================
# USER
# =========================================================

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(256),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default="user",
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.now
    )

    orders = db.relationship(
        "Order",
        backref="user",
        lazy=True
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )

    @property
    def is_admin(self):
        return self.role == "admin"


# =========================================================
# CATEGORY
# =========================================================

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    products = db.relationship(
        "Product",
        backref="category",
        lazy=True
    )

    def __repr__(self):
        return f"<Category {self.name}>"


# =========================================================
# PRODUCT
# =========================================================

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    price = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    image = db.Column(
        db.String(255),
        default="shirt1.jpg"
    )

    stock = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    # RFID
    rfid_uid = db.Column(
        db.String(20),
        unique=True,
        nullable=True
    )

    # Category
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=True
    )

    # สถานะสินค้า
    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.now
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": float(self.price),
            "image": self.image,
            "stock": self.stock,
            "rfid_uid": self.rfid_uid,
            "category_id": self.category_id,
            "category": (
                self.category.name
                if self.category
                else None
            ),
            "is_active": self.is_active
        }


# =========================================================
# SITE SETTINGS
# =========================================================

class SiteSettings(db.Model):
    __tablename__ = "site_settings"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    promptpay_number = db.Column(
        db.String(20),
        default=""
    )

    promptpay_name = db.Column(
        db.String(120),
        default=""
    )

    qr_image = db.Column(
        db.String(255),
        default="qr_payment.png"
    )

    @staticmethod
    def get():

        settings = SiteSettings.query.first()

        if not settings:

            settings = SiteSettings()

            db.session.add(settings)
            db.session.commit()

        return settings


# =========================================================
# ORDER
# =========================================================

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    total = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="pending",
        nullable=False
    )

    shipping_name = db.Column(
        db.String(120)
    )

    shipping_phone = db.Column(
        db.String(20)
    )

    shipping_address = db.Column(
        db.Text
    )

    payment_slip = db.Column(
        db.String(255)
    )

    payment_expires_at = db.Column(
        db.DateTime
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.now
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now
    )

    items = db.relationship(
        "OrderItem",
        backref="order",
        lazy=True,
        cascade="all, delete-orphan"
    )

    STATUS_LABELS = {
        "pending": "รอชำระเงิน",
        "awaiting_verification": "รอตรวจสอบสลิป",
        "paid": "ชำระเงินแล้ว",
        "processing": "กำลังจัดเตรียม",
        "shipped": "จัดส่งแล้ว",
        "completed": "สำเร็จ",
        "cancelled": "ยกเลิก",
    }

    @property
    def status_label(self):
        return self.STATUS_LABELS.get(
            self.status,
            self.status
        )

    @property
    def is_payment_expired(self):

        if not self.payment_expires_at:
            return False

        return datetime.now() > self.payment_expires_at

    @property
    def payment_seconds_left(self):

        if not self.payment_expires_at:
            return 0

        delta = (
            self.payment_expires_at
            - datetime.now()
        )

        return max(
            0,
            int(delta.total_seconds())
        )


# =========================================================
# ORDER ITEM
# =========================================================

class OrderItem(db.Model):
    __tablename__ = "order_items"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("orders.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    price = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    product = db.relationship(
        "Product"
    )

    @property
    def subtotal(self):
        return float(self.price) * self.quantity


# =========================================================
# CART
# =========================================================

class Cart(db.Model):
    __tablename__ = "cart"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        default=1,
        nullable=False
    )

    product = db.relationship(
        "Product"
    )