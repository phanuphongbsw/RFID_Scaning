-- สร้างฐานข้อมูล MySQL สำหรับร้านเสื้อผ้า
CREATE DATABASE IF NOT EXISTS shop_shirt CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE shop_shirt;

-- ตารางจะถูกสร้างอัตโนมัติโดย Flask-SQLAlchemy เมื่อรัน app.py
-- หรือสามารถรัน: python app.py เพื่อสร้างตารางและข้อมูลตัวอย่าง
