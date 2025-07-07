#!/bin/bash
# Deploy โค้ดและตั้งค่า Environment Variables ให้ Azure Function App

# โหลดค่าจาก config/.env.local
ENV_FILE="config/.env.local"
if [ -f "$ENV_FILE" ]; then
  # อ่านตัวแปรทั้งหมดในไฟล์ .env.local (ข้ามบรรทัดที่ขึ้นต้นด้วย # หรือว่าง)
  export $(grep -v '^#' "$ENV_FILE" | grep -v '^$' | xargs)
else
  echo "ไม่พบไฟล์ $ENV_FILE กรุณาตรวจสอบ!"
  exit 1
fi

RESOURCE_GROUP="etl-th-group"
# FUNCTION_APP จะถูก export มาจาก .env.local

# Deploy โค้ดขึ้น Azure Function App
func azure functionapp publish "$FUNCTION_APP"

# สร้าง string สำหรับ --settings จากตัวแปรทั้งหมดใน .env.local
SETTINGS_STRING=$(grep -v '^#' "$ENV_FILE" | grep -v '^$' | xargs -d '\n' -I {} echo {} | tr '\n' ' ')

# ตั้งค่า Environment Variables ทั้งหมด
az functionapp config appsettings set \
  --name "$FUNCTION_APP" \
  --resource-group "$RESOURCE_GROUP" \
  --settings $SETTINGS_STRING

echo "Deploy และตั้งค่า environment variable สำเร็จแล้ว"
