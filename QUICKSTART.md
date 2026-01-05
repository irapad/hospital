# 🚀 Quick Start Guide - Camera Security Management System

## การเริ่มต้นใช้งานอย่างรวดเร็ว

### 1. ติดตั้ง Dependencies

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y python3 python3-pip openssl ffmpeg

# macOS
brew install python openssl ffmpeg
```

### 2. ติดตั้ง Python Packages

```bash
cd camera_security_app
pip install -r requirements.txt
```

### 3. เริ่มต้นระบบ

#### วิธีที่ 1: ใช้ start script (แนะนำ)

```bash
./start.sh
```

#### วิธีที่ 2: รันด้วยตนเอง

```bash
python app.py
```

### 4. เปิดเบราว์เซอร์

ไปที่: **http://localhost:5000**

## 🎯 การใช้งานครั้งแรก

### เพิ่มกล้องเข้าระบบ

1. คลิก "กล้องทั้งหมด" ในเมนู
2. คลิก "เพิ่มกล้องใหม่"
3. กรอกข้อมูล:
   - IP Address: เช่น `192.168.1.100`
   - Port: `80` (default)
   - Location: เช่น "อาคาร A ชั้น 2"
4. คลิก "เพิ่มกล้อง"

### ตรวจสอบกล้อง

1. ในหน้ารายการกล้อง คลิก "ตรวจสอบ"
2. รอผลการตรวจสอบ
3. ดูรายละเอียดได้ที่หน้า "รายละเอียดกล้อง"

### สแกนหากล้องผ่าน Shodan

1. ไปที่หน้า "สแกนกล้อง"
2. ใส่ Shodan API Key
   - รับฟรีที่: https://shodan.io (ต้องสมัครสมาชิก)
3. เลือกตัวกรอง (ถ้าต้องการ):
   - เมือง: `Bangkok`
   - ประเทศ: `TH`
4. คลิก "เริ่มสแกน"

## 📊 ฟีเจอร์หลัก

- ✅ แดชบอร์ดแสดงสถิติภาพรวม
- ✅ จัดการกล้องทั้งหมดในที่เดียว
- ✅ ตรวจสอบช่องโหว่อัตโนมัติ
- ✅ สแกนหากล้อง Hikvision ผ่าน Shodan
- ✅ บันทึกประวัติการสแกน
- ✅ ดึง credentials จากกล้องที่มีช่องโหว่

## ⚠️ หมายเหตุสำคัญ

- ใช้เพื่อการทดสอบความปลอดภัยที่ได้รับอนุญาตเท่านั้น
- ต้องมี Shodan API Key สำหรับการสแกน
- ต้องติดตั้ง OpenSSL สำหรับถอดรหัส credentials
- FFmpeg เป็นตัวเลือก (สำหรับทดสอบ RTSP)

## 🔧 การแก้ปัญหา

### ไม่สามารถเริ่มระบบได้

```bash
# ตรวจสอบ Python version
python --version  # ต้อง 3.8+

# ติดตั้ง dependencies ใหม่
pip install -r requirements.txt
```

### ไม่สามารถถอดรหัส credentials

```bash
# ตรวจสอบ OpenSSL
openssl version

# ติดตั้ง OpenSSL
sudo apt install openssl  # Ubuntu/Debian
brew install openssl       # macOS
```

### ไม่สามารถทดสอบ RTSP

```bash
# ติดตั้ง FFmpeg
sudo apt install ffmpeg   # Ubuntu/Debian
brew install ffmpeg        # macOS
```

## 📞 ติดต่อและสนับสนุน

หากพบปัญหาหรือต้องการความช่วยเหลือ:
- อ่านเอกสารฉบับเต็มที่ `README.md`
- ดู HIKScript documentation: https://github.com/fracergu/HIKScript
