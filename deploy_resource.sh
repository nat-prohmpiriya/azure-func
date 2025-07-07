#!/bin/bash
# สร้าง Resource Group, Storage Account, Function App (Python) สำหรับ ETL
RESOURCE_GROUP="etl-th-group"
LOCATION="southeastasia"
STORAGE_ACCOUNT="etlstorage888"
FUNCTION_APP="etl-blob-func-888"
PYTHON_VERSION="3.11"

# 1. สร้าง Resource Group
az group create --name "$RESOURCE_GROUP" --location "$LOCATION"

# 2. สร้าง Storage Account
az storage account create --name "$STORAGE_ACCOUNT" --location "$LOCATION" --resource-group "$RESOURCE_GROUP" --sku Standard_LRS

# 3. สร้าง Function App (Python)
az functionapp create \
  --resource-group "$RESOURCE_GROUP" \
  --consumption-plan-location "$LOCATION" \
  --runtime python \
  --runtime-version "$PYTHON_VERSION" \
  --functions-version 4 \
  --name "$FUNCTION_APP" \
  --storage-account "$STORAGE_ACCOUNT" \
  --os-type Linux

echo "Resource สร้างเสร็จแล้ว ชื่อ Function App: $FUNCTION_APP"
