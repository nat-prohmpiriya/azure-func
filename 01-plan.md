## PROJECT: ETL pipeline azure storage to mongodb
    - This project involves creating an ETL pipeline that extracts data from Azure Storage, transforms it as needed, and loads it into a MongoDB database.

## NOTE 
    - Azure Functions will be used to implement the ETL pipeline.
    - The pipeline will be triggered by events in Azure Storage (e.g., new blobs being added).
    - Data transformation will be performed using Python and relevant libraries (e.g., Pandas).
    - The final output will be stored in a MongoDB database hosted on Azure.

## TASK LIST 
    - [x] Set up Azure Storage account and container.
    - [x] Create a MongoDB database on Atlas
    - [x] Develop Azure Function to trigger on blob creation or timetigger
    - [x] Implement data extraction logic in the Azure Function.
    - [x] mock data
            | **Field Name** | **Description** |
            | --- | --- |
            | CRM_ID | Customer rm_id |
            | CL4 | Masked 16-digit card number |
            | CARD_MAILING_TRACKING_NO | Card mailing tracking number |
            | CARD_MAILING_DATE | Card mailing date (วันที่ส่งไปรษณีย์) |
    - [x] Load transformed data into MongoDB.
    - [x] Test the entire ETL pipeline end-to-end.
    - [x] Document the project setup, configuration, and usage instructions.
    - [x] Deploy the Azure Function to Azure.
        - [x] create script deploy_function.sh
        - [x] Run the script to deploy the Azure Function.
    - [] test upload fine
    - [ ] Set up monitoring and logging for the Azure Function.
    - [ ] Optimize the ETL pipeline for performance and scalability.
    - [ ] Implement error handling and retry logic in the Azure Function.
    - [ ] เพิ่ม trigger ให้รันตามเวลาที่กำหนด (เช่น ทุกวันเวลา 00:00 น.)

## CURRENT GOALS
