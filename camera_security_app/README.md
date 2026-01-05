# 🎥 Camera Security Management System

ระบบจัดการความปลอดภัยของกล้อง Hikvision ที่ใช้ HIKScript สำหรับตรวจสอบช่องโหว่และจัดการกล้อง

## ✨ คุณสมบัติหลัก

- 📊 **Dashboard** - แสดงภาพรวมของกล้องทั้งหมดในระบบ
- 🔍 **Camera Scanner** - สแกนหากล้อง Hikvision ผ่าน Shodan API
- 🔐 **Vulnerability Testing** - ตรวจสอบช่องโหว่ CVE-2017-7921 (Authentication Bypass)
- 📹 **RTSP Stream Testing** - ทดสอบ RTSP streams
- 🗄️ **Database Management** - จัดเก็บข้อมูลกล้องและผลการสแกน
- 🌐 **Web Interface** - อินเทอร์เฟซเว็บที่ใช้งานง่าย

## 🛠️ การติดตั้ง

### ข้อกำหนดของระบบ

- Python 3.8 ขึ้นไป
- OpenSSL (สำหรับถอดรหัส credentials)
- FFmpeg (ตัวเลือก, สำหรับทดสอบ RTSP)

### ติดตั้ง Dependencies

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip openssl ffmpeg

# macOS
brew install python openssl ffmpeg
```

### ติดตั้ง Python Packages

```bash
cd camera_security_app
pip install -r requirements.txt
```

## 🚀 การใช้งาน

### เริ่มต้นใช้งาน Web Application

```bash
python app.py
```

จากนั้นเปิดเบราว์เซอร์ไปที่: `http://localhost:5000`

### การใช้งานผ่าน Web Interface

#### 1. เพิ่มกล้อง
- ไปที่หน้า "กล้องทั้งหมด"
- คลิก "เพิ่มกล้องใหม่"
- กรอกข้อมูล IP Address, Port, และรายละเอียดอื่นๆ
- คลิก "เพิ่มกล้อง"

#### 2. ตรวจสอบกล้อง
- ในหน้า "กล้องทั้งหมด" หรือ "รายละเอียดกล้อง"
- คลิกปุ่ม "ตรวจสอบ"
- ระบบจะทำการตรวจสอบช่องโหว่และบันทึกผลลัพธ์

#### 3. สแกนกล้องผ่าน Shodan
- ไปที่หน้า "สแกนกล้อง"
- ใส่ Shodan API Key (รับฟรีที่ [shodan.io](https://shodan.io))
- เลือกตัวกรอง (เมือง, ประเทศ) หรือไม่ก็ได้
- คลิก "เริ่มสแกน"

## 📁 โครงสร้างโปรเจค

```
camera_security_app/
├── app.py                  # Flask application หลัก
├── hikscript_wrapper.py    # HIKScript integration wrapper
├── requirements.txt        # Python dependencies
├── README.md              # เอกสารนี้
├── templates/             # HTML templates
│   ├── base.html         # Template พื้นฐาน
│   ├── index.html        # หน้า Dashboard
│   ├── cameras.html      # รายการกล้อง
│   ├── camera_detail.html # รายละเอียดกล้อง
│   ├── add_camera.html   # เพิ่มกล้อง
│   ├── scan.html         # สแกนกล้อง
│   └── settings.html     # ตั้งค่า
├── static/               # Static files (CSS, JS, images)
└── models/              # Database models

hikscript-lib/           # HIKScript library (cloned)
└── HIKScript.py        # HIKScript main script
```

## 🔧 API Endpoints

### Cameras
- `GET /api/cameras` - ดึงรายการกล้องทั้งหมด
- `POST /api/cameras/<id>/check` - ตรวจสอบกล้อง

### Scanning
- `POST /api/scan/shodan` - สแกนผ่าน Shodan

## 🗄️ Database Schema

### Camera
- `id` - Primary key
- `ip_address` - IP address ของกล้อง
- `port` - Port number
- `location` - สถานที่ติดตั้ง
- `is_vulnerable` - สถานะช่องโหว่
- `last_checked` - วันที่ตรวจสอบล่าสุด
- `credentials` - ข้อมูล credentials (JSON)
- `notes` - หมายเหตุ
- `status` - สถานะ (unknown, vulnerable, secure, checking)

### ScanResult
- `id` - Primary key
- `camera_id` - Foreign key to Camera
- `scan_date` - วันที่สแกน
- `scan_type` - ประเภทการสแกน
- `result` - ผลลัพธ์ (JSON)
- `success` - สถานะความสำเร็จ

### ShodanScan
- `id` - Primary key
- `scan_date` - วันที่สแกน
- `query` - Query ที่ใช้
- `location_filter` - ตัวกรองสถานที่
- `results_count` - จำนวนผลลัพธ์
- `results_file` - ไฟล์ผลลัพธ์

## ⚠️ คำเตือนด้านกฎหมาย

**เครื่องมือนี้ควรใช้สำหรับการทดสอบความปลอดภัยที่ได้รับอนุญาตเท่านั้น**

- ต้องได้รับอนุญาตก่อนทดสอบระบบใดๆ
- ผู้ใช้งานต้องรับผิดชอบในการปฏิบัติตามกฎหมายที่เกี่ยวข้อง
- การใช้เครื่องมือนี้โดยไม่ได้รับอนุญาตอาจผิดกฎหมาย

## 🔒 ช่องโหว่ที่ตรวจสอบ

### CVE-2017-7921 - Hikvision Authentication Bypass

ช่องโหว่นี้อนุญาตให้ผู้โจมตีสามารถ:
- เข้าถึงกล้องโดยไม่ต้องมี credentials
- ดึงข้อมูล configuration file
- ดึง credentials ที่เข้ารหัส
- เข้าถึง RTSP streams
- จับภาพจากกล้อง

## 📚 เอกสารอ้างอิง

- [HIKScript GitHub](https://github.com/fracergu/HIKScript)
- [CVE-2017-7921](https://nvd.nist.gov/vuln/detail/CVE-2017-7921)
- [Shodan](https://shodan.io)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 🤝 การมีส่วนร่วม

หากพบข้อผิดพลาดหรือต้องการเพิ่มฟีเจอร์ใหม่ สามารถ:
1. สร้าง Issue
2. Fork โปรเจค
3. สร้าง Pull Request

## 📄 License

ใช้เพื่อการศึกษาและการทดสอบความปลอดภัยที่ได้รับอนุญาตเท่านั้น

## 👤 ผู้พัฒนา

- HIKScript: [@fracergu](https://github.com/fracergu)
- Integration App: Camera Security Management Team

## 🔄 Version

- Version: 1.0.0
- HIKScript Version: 2.1
- Last Updated: 2025-01-05
