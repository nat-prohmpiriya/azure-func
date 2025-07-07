# ETL Pipeline: Azure Storage to MongoDB

## Overview
โครงการนี้เป็น ETL pipeline ที่ใช้ Azure Functions สำหรับดึงข้อมูลจาก Azure Blob Storage, แปลงข้อมูล และโหลดเข้าสู่ MongoDB

## ขั้นตอนการใช้งาน

### 1. เตรียม Environment
- ติดตั้ง Python 3.11 ขึ้นไป
- สร้าง virtual environment และติดตั้ง dependencies
  ```sh
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

### 2. ตั้งค่าตัวแปรสภาพแวดล้อม
- แก้ไขไฟล์ `config/.env.local` ให้ระบุค่า MongoDB และ Azure Storage ให้ถูกต้อง

### 3. รัน Azure Functions Local
  ```sh
  func host start
  ```

### 4. ทดสอบ Pipeline
- อัปโหลดไฟล์ CSV (เช่น `card_delivery_track.csv`) ไปยัง Azure Blob Storage container ที่กำหนด
- ตรวจสอบ log ว่ามีการ extract, transform, และ load ข้อมูลสำเร็จ
- ตรวจสอบข้อมูลใน MongoDB

### 5. Deploy Azure Function to Azure
- ติดตั้ง Azure CLI และ Azure Functions Core Tools ถ้ายังไม่ได้ติดตั้ง
  ```sh
  npm install -g azure-functions-core-tools@4 --unsafe-perm true
  az login
  ```
- สร้าง Resource Group, Storage Account, และ Function App (ถ้ายังไม่มี)
  ```sh
  az group create --name <resource-group> --location <location>
  az storage account create --name <storage-account> --location <location> --resource-group <resource-group> --sku Standard_LRS
  az functionapp create --resource-group <resource-group> --consumption-plan-location <location> --runtime python --runtime-version 3.11 --functions-version 4 --name <function-app-name> --storage-account <storage-account>
  ```
- Deploy โค้ดขึ้น Azure Function App
  ```sh
  func azure functionapp publish <function-app-name>
  ```
- ตั้งค่า Environment Variables (เช่น MongoDB URI) ใน Azure Portal หรือใช้คำสั่ง
  ```sh
  az functionapp config appsettings set --name <function-app-name> --resource-group <resource-group> --settings MONGODB_URI="<your-mongodb-uri>" MONGODB_DB="<your-db>" MONGODB_COLLECTION="<your-collection>"
  ```

- ตรวจสอบผลการ deploy และทดสอบ pipeline บน Azure

## โครงสร้างไฟล์สำคัญ
- `etl_blob_trigger/__init__.py` : Logic หลักของ ETL
- `data/card_delivery_track.csv` : ตัวอย่าง mock data
- `config/.env.local` : ตัวแปรเชื่อมต่อ MongoDB และ Storage

## Troubleshooting
- ตรวจสอบ log หากเกิด error
- ตรวจสอบ connection string และสิทธิ์ของ Storage/MongoDB

## ข้อควรระวัง
- อย่า commit ข้อมูลสำคัญหรือ secret ลง git
- ทดสอบ pipeline ด้วย mock data ก่อนใช้งานจริง
