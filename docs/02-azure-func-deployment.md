# ตัวอย่าง Script สำหรับ Deploy Azure Function (ETL) ในประเทศไทย

## 1. กำหนดค่าตัวแปร
```sh
RESOURCE_GROUP=etl-th-group
LOCATION=southeastasia
STORAGE_ACCOUNT=etlstoragethai$RANDOM
FUNCTION_APP=etl-blob-func-thai$RANDOM
PYTHON_VERSION=3.11
```

## 2. สร้าง Resource Group
```sh
az group create --name $RESOURCE_GROUP --location $LOCATION
```

## 3. สร้าง Storage Account
```sh
az storage account create --name $STORAGE_ACCOUNT --location $LOCATION --resource-group $RESOURCE_GROUP --sku Standard_LRS
```

## 4. สร้าง Function App (Python)
```sh
az functionapp create \
  --resource-group $RESOURCE_GROUP \
  --consumption-plan-location $LOCATION \
  --runtime python \
  --runtime-version $PYTHON_VERSION \
  --functions-version 4 \
  --name $FUNCTION_APP \
  --storage-account $STORAGE_ACCOUNT
```

## 5. Deploy โค้ดขึ้น Azure Function App
```sh
func azure functionapp publish $FUNCTION_APP
```

## 6. ตั้งค่า Environment Variables (MongoDB, ฯลฯ)
```sh
az functionapp config appsettings set \
  --name $FUNCTION_APP \
  --resource-group $RESOURCE_GROUP \
  --settings MONGODB_URI="<your-mongodb-uri>" MONGODB_DB="<your-db>" MONGODB_COLLECTION="<your-collection>"
```

## หมายเหตุ
- LOCATION ที่เหมาะกับไทยคือ `southeastasia`
- สามารถเปลี่ยนชื่อ resource ตามต้องการ
- คำสั่งนี้เหมาะกับการรันบน macOS/Linux shell
