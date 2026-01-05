# 🚀 วิธี Deploy Camera Security Management System

## Deploy ไปยัง Render.com (ฟรี - แนะนำ)

### ขั้นตอนที่ 1: สมัคร Render.com

1. ไปที่ https://render.com
2. คลิก **Sign Up** และสมัครด้วย GitHub account
3. อนุญาตให้ Render เข้าถึง GitHub repository

### ขั้นตอนที่ 2: Deploy

1. **เข้าสู่ Dashboard**
   - ไปที่ https://dashboard.render.com

2. **สร้าง Web Service ใหม่**
   - คลิก **New +** → เลือก **Web Service**
   - เชื่อมต่อ GitHub repository: `irapad/hospital`
   - Branch: `claude/hikscript-app-integration-dyl6D`

3. **ตั้งค่า Web Service**
   ```
   Name: camera-security-app
   Region: Singapore (ใกล้ที่สุด)
   Branch: claude/hikscript-app-integration-dyl6D
   Root Directory: camera_security_app
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```

4. **ตั้งค่า Environment Variables**
   - คลิก **Advanced**
   - เพิ่ม Environment Variables:
     ```
     SECRET_KEY = สุ่มค่าใหม่ (เช่น กดแป้นพิมพ์สุ่มๆ 30 ตัวอักษร)
     FLASK_ENV = production
     ```

5. **เลือก Free Plan**
   - Instance Type: **Free**
   - คลิก **Create Web Service**

### ขั้นตอนที่ 3: รอ Deploy เสร็จ

- Render จะ build และ deploy อัตโนมัติ (ใช้เวลา 3-5 นาที)
- เมื่อเสร็จจะได้ URL เช่น: `https://camera-security-app.onrender.com`

### ขั้นตอนที่ 4: เข้าใช้งาน

- เปิดเบราว์เซอร์ (บนมือถือได้เลย)
- ไปที่ URL ที่ได้รับ
- ระบบพร้อมใช้งาน!

---

## Deploy ไปยัง Railway.app (ทางเลือก)

### ขั้นตอน:

1. **สมัคร Railway**
   - ไปที่ https://railway.app
   - Sign up ด้วย GitHub

2. **สร้าง Project ใหม่**
   - คลิก **New Project** → **Deploy from GitHub repo**
   - เลือก repository: `irapad/hospital`
   - Branch: `claude/hikscript-app-integration-dyl6D`

3. **ตั้งค่า**
   - Root Directory: `camera_security_app`
   - เพิ่ม Environment Variables:
     ```
     SECRET_KEY = random-secret-key
     FLASK_ENV = production
     ```

4. **Deploy**
   - Railway จะ deploy อัตโนมัติ
   - ได้ URL เช่น: `https://camera-security-app.up.railway.app`

---

## Deploy ไปยัน PythonAnywhere (ทางเลือก)

### ขั้นตอน:

1. **สมัคร PythonAnywhere**
   - ไปที่ https://www.pythonanywhere.com
   - สมัคร Free account

2. **Clone Repository**
   - เปิด Bash console
   ```bash
   git clone https://github.com/irapad/hospital.git
   cd hospital
   git checkout claude/hikscript-app-integration-dyl6D
   ```

3. **ติดตั้ง Dependencies**
   ```bash
   cd camera_security_app
   pip install --user -r requirements.txt
   ```

4. **ตั้งค่า Web App**
   - ไปที่ **Web** tab
   - คลิก **Add a new web app**
   - เลือก **Manual configuration** → Python 3.10
   - ตั้งค่า:
     - Source code: `/home/yourusername/hospital/camera_security_app`
     - Working directory: `/home/yourusername/hospital/camera_security_app`
     - WSGI file: แก้ให้ชี้ไปที่ `app.py`

5. **Reload**
   - คลิก **Reload** button
   - เข้าใช้งานที่: `https://yourusername.pythonanywhere.com`

---

## 📱 ใช้งานผ่านมือถือ

หลังจาก deploy แล้ว คุณสามารถ:
- เปิดเบราว์เซอร์บนมือถือ
- ไปที่ URL ที่ได้รับจากการ deploy
- ใช้งานได้เลย ไม่ต้องมีคอมพิวเตอร์!

---

## ⚠️ หมายเหตุสำคัญ

### Free Plan Limitations:

**Render.com:**
- Service จะ sleep หลังไม่มีการใช้งาน 15 นาที
- ครั้งแรกที่เข้าอาจช้า (30 วินาที) เพราะต้อง wake up
- 750 ชั่วโมง/เดือน (พอใช้งาน)

**Railway.app:**
- $5 credit ฟรี/เดือน
- หมดจะต้องจ่ายเงิน

**PythonAnywhere:**
- 1 web app ฟรี
- Bandwidth จำกัด
- ไม่มี HTTPS สำหรับ custom domain

### แนะนำ:
- **Render.com** เหมาะสำหรับใช้งานจริง (ฟรี ไม่มีค่าใช้จ่าย)
- รองรับ HTTPS อัตโนมัติ
- ใช้งานง่าย เหมาะกับมือถือ

---

## 🔒 ความปลอดภัย

สำหรับ Production:
1. เปลี่ยน `SECRET_KEY` ให้ปลอดภัย
2. ตั้งค่า firewall ถ้าจำเป็น
3. ใช้ HTTPS (Render รองรับอัตโนมัติ)
4. อย่าแชร์ API keys หรือ credentials

---

## 🆘 แก้ปัญหา

**Build Failed:**
- ตรวจสอบ `requirements.txt`
- ดู Build Logs ใน Render Dashboard

**App ไม่ทำงาน:**
- ตรวจสอบ Environment Variables
- ดู Application Logs

**Database Error:**
- Render ใช้ ephemeral storage (ข้อมูลหายเมื่อ restart)
- ควรใช้ external database สำหรับ production จริงๆ

---

## 📞 ติดต่อ

หากมีปัญหา:
1. ดู Render Logs: Dashboard → Logs
2. ดูเอกสาร: https://render.com/docs
3. Discord: https://render.com/discord
