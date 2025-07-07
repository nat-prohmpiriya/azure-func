#!/bin/bash
# ลบ Resource Group และ resource ทั้งหมดที่เกี่ยวข้อง (Cleanup)
RESOURCE_GROUP="etl-th-group"

az group delete --name "$RESOURCE_GROUP" --yes --no-wait

echo "สั่งลบ Resource Group: $RESOURCE_GROUP แล้ว (อาจใช้เวลาสักครู่)"
