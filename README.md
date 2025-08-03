# PSU Note - Flask & PostgreSQL Note-Taking App
ระบบจัดการโน้ตแบบครบวงจรพร้อมระบบแท็ก (Tag) ที่พัฒนาด้วย Flask และ PostgreSQL รองรับการทำงานผ่าน Docker พร้อม UI สมัยใหม่ด้วย Bootstrap 5 และ Select2

## คุณสมบัติหลัก
-ระบบจัดการโน้ตแบบครบวงจร (CRUD): สร้าง, อ่าน, แก้ไข, ลบโน้ต
-ระบบแท็กอัจฉริยะ: จัดกลุ่มโน้ตด้วยแท็กหลายๆ อันพร้อมกัน
-เพิ่มแท็กใหม่ได้ทันที ขณะสร้างหรือแก้ไขโน้ตผ่าน Modal
-UI สมัยใหม่ ด้วย Bootstrap 5 และ Select2 สำหรับการเลือกแท็ก
-รองรับ Docker สำหรับการพัฒนาที่สะดวก
-ฐานข้อมูล PostgreSQL พร้อมการจัดการผ่าน pgAdmin

## ภาพตัวอย่างการทำงาน

1. ตัวอย่างหน้าweb
   
blob:https://www.facebook.com/07a3c9b3-d0bb-4377-b1cd-596dc243225c<img width="2048" height="1330" alt="image" src="https://github.com/user-attachments/assets/e231981c-4356-4b87-bc31-789945cab0bb" />


3. การสร้างและแก้ไขโน้ต

blob:https://www.facebook.com/62ace405-f676-422d-b40c-eee01f2b9c2a<img width="2048" height="1291" alt="image" src="https://github.com/user-attachments/assets/2d20df7b-4705-49c8-9107-6782737d509b" />

blob:https://www.facebook.com/7de0df07-ff19-4371-ad02-c9d81b8ce5ee<img width="2048" height="1318" alt="image" src="https://github.com/user-attachments/assets/7b490e98-e80e-4426-b8a9-30d7fbf56817" />



4. การจัดการรายการโน้ต

blob:https://www.facebook.com/e7f6faef-428c-4dfd-9ff6-ecf9030ed825<img width="2048" height="1330" alt="image" src="https://github.com/user-attachments/assets/7f0a03ea-883a-4f72-9117-8354995f75d1" />


4. การสร้างแท็กใหม่

blob:https://www.facebook.com/3f13d06a-6851-4077-9ea4-5760dc9879a5<img width="2048" height="473" alt="image" src="https://github.com/user-attachments/assets/9a17d1ea-0f25-45e5-b56c-de3e3c274526" />


5. การแก้ไขและลบแท็ก

blob:https://www.facebook.com/e5d0e2c1-b9de-4390-963a-54b6b33ec014<img width="2048" height="1330" alt="image" src="https://github.com/user-attachments/assets/fcfa94c6-0842-4127-bf41-dc699d617c11" />


## การติดตั้งและใช้งาน

### 1. ติดตั้ง dependencies
```bash
# สร้างและเปิดใช้งาน virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
.\venv\Scripts\activate  # Windows

# ติดตั้ง packages ที่จำเป็น
pip install -r requirements.txt
```

### 2. ตั้งค่าฐานข้อมูล
ติดตั้ง PostgreSQL และ pgAdmin
สร้างฐานข้อมูลใหม่
แก้ไข connection string ใน psunote/noteapp.py


### 3. รันแอปพลิเคชัน
```bash
export FLASK_APP=psunote/noteapp.py
flask run
```


หรือ
```bash
python psunote/noteapp.py
```

#### 4. เปิดใช้งานแอป
เปิดเบราว์เซอร์ไปที่: http://localhost:5000


### โครงสร้างโปรเจกต์

<img width="242" height="288" alt="image" src="https://github.com/user-attachments/assets/16d09628-7a99-4a1b-8eda-9428d61e87dc" />



### ปัญหาที่พบ
#### ปัญหาแท็ก: ห้ามกำหนดค่า note.tags เป็น string โดยตรง ให้ใช้ append() หรือเชื่อมความสัมพันธ์ผ่าน SQLAlchemy

#### ปัญหาเชื่อมต่อฐานข้อมูล: ตรวจสอบว่า connection string ถูกต้องและฐานข้อมูลทำงาน







