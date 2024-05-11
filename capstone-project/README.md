# Capstone Project DS525 (2/66)

สมาชิกในกลุ่ม
น.ส.กมลทิพย์ มนตรีสา   รหัสนิสิต 65199160171
น.ส.กมลวรรณ เนียมเที่ยง รหัสนิสิต 65199160172


## Problem
บริษัทผู้ค้าปลีกอุปกรณ์อิเล็กทรอนิกส์ ต้องการทราบข้อมูลเกี่ยวกับประสิทธิภาพของการขายสินค้าของตน เพื่อใช้ในการวางแผนการผลิตและการตลาดในอนาคต 
- บริษัทจำหน่ายสินค้าประเภทใดบ้าง? 
- สินค้าไหนขายดี?
- มีลูกค้าอยู่ที่ไหนบ้าง?

### Data Source
Dataset จาก Kaggle [Global Electronics Retailers](https://www.kaggle.com/datasets/bhavikjikadara/global-electronics-retailers)

จำลองข้อมูลลงใน Google Cloud Storage เพื่อเป็น data source ในการดึงข้อมูลมาใช้งาน

การสร้าง bucket บน Google Cloud Storage
1. ในการเตรียมเริ่มจากเราต้องสร้าง โปรเจกต์ หรือเลือกโปรเจกต์ที่มีอยู่แล้วก็ได้ขึ้นมา 
2. เมื่ออยู่ในโปรเจกต์ที่ต้องการใช้งาน ไปที่ "Cloud Storage" โดยใช้เมนูด้านซ้ายมือเข้าหน้า Cloud Storage และไปที่เมนู Bucket
<img src="https://drive.google.com/file/d/1KqtvJJbbswg93Veoc-TVAEeRTosn-X8R/view?usp=sharing" width="100%"></img> 
3. คลิกที่ "Create Bucket" เพื่อเริ่มต้นการสร้าง Bucket ขึ้นมาใหม่ เราก็จะได้ Bucket หรือ Folder ขึ้นมาหนึ่งโฟลเดอร์
<img src="https://drive.google.com/file/d/1kx1ln4ZGUppPP7dFso-hF-xOKSEz3SEk/view?usp=sharing" width="100%"></img> 
5. กรอกข้อมูลเบื้องต้นของ Bucket ดังนี้
   - ชื่อ Bucket : ds-525
   - เลือกโปรเจกต์ที่สร้างไว้ : Capstone Project
   - เลือกโซนที่ต้องการให้ Bucket ถูกสร้างขึ้น
   - เลือก Storage Class ที่ต้องการใช้งาน : Standard
6. คลิก "CREATE" เพื่อสร้าง Bucket ใหม่
เมื่อได้ Bucket แล้วเราก็จะกำหนดสิทธิของคนที่จะเข้า Bucket เริ่มจากการเข้าไปที่ IAM & Admin เข้าที่ เมนู Service Account เพื่อเข้าไป สร้าง Service Accout และ Grant สิทธิ์ให้ Service Accout นั้นสามารถเข้าไป จัดการ File ใน Bucket ทื่เราสร้างขึ้นมาใหม่
<img src="https://drive.google.com/file/d/1bGMYCz5InSoaQwgnsSJKVO9LG7O89poy/view?usp=sharing" width="100%"></img> 

จากนั้นกด GRANT ACCESS เพื่อเข้าไป สร้าง Services Account และ กำหนดสิทธิ์
<img src="https://drive.google.com/file/d/1GT1cOtYha0T5F0hIjwvD4WVbT1ymQAz5/view?usp=sharing" width="100%"></img> 

จากนั้นเข้า Tab “KEYS” กด Dropdown ADD KEY และ เลือก Create Keys และเลือกเป็นไฟล์ Json เราจะได้ไฟล์ Json มาไว้ที่ Code ของเรา
<img src="https://drive.google.com/file/d/1Wez45hZkN77PiaWcQU4jIVcHV9St4WQM/view?usp=sharing" width="100%"></img> 
<img src="https://drive.google.com/file/d/1WBDApWt4bMZAW8XoCfPonLo61JSww7Fd/view?usp=sharing" width="100%"></img>
เมื่อ Bucket ถูกสร้างขึ้นแล้ว อัปโหลดไฟล์ข้อมูลลงใน Bucket นี้ 
<img src="https://drive.google.com/file/d/1RDFJXM5Mf92E5BATMA-1tI9V5fB2p3LD/view?usp=sharing" width="100%"></img> 

ใน Project นี้เราจะจัดการ Data Pipeline ด้วย Google Cloud Composer เป็นบริการจัดการ Workflow ของ Data Pipeline ที่สร้างขึ้นมาจาก Apache Airflow ซึ่งจะเขียน Workflow แบบเป็นกราฟ DAG (Directed Acyclic Graph = กราฟที่มีทิศทางเดียวและไม่วนกลับมาเป็นลูป)

### Data Pipeline
หลังจากที่มีทุกอย่างพร้อมแล้ว ต่อไปเราก็จะทำให้เป็น Automate ทั้งหมด ด้วยการสร้าง data pipeline ด้วยการทำ ETL ดังนี้
Extract — ทำการดึงข้อมูลทั้งหมดจาก database ที่สร้างไว้ใน Data Source เก็บไว้ใน data lake (ในที่นี้จะใช้ Google Cloud Storage ในการเก็บ) เพื่อรอไป transform หรือ cleaning
Transform — ทำการแปลง, ทำความสะอาด และ join ข้อมูลเข้าด้วยกัน โดยใช้ DBT
Load — เก็บไฟล์ผลลัพธ์ไว้ใน data lake และ load เข้า data warehouse (จะใช้ Google BigQuery เป็น data warehouse)


### Data Model

<img src="https://drive.google.com/file/d/11plaGpFGqaxTlgc74Mr42WNmJpjqzUdJ/view?usp=sharing" width="100%"></img> 


## Instruction
1. Get started
    cd Capstone_Project_Final

2. Prepare environment workspace by Docker (Airflow)

    mkdir -p ./dags ./logs ./plugins
    echo -e "AIRFLOW_UID=$(id -u)" > .env

3. create visual environment & install required libraries
    python -m venv ENV
    source ENV/bin/activate
    pip install -r requirements.txt

4. Start environment ในขณะที่อยู่ใน ENV เปิดใช้งาน Apache airflow port 8080
    docker-compose up

### Data Warehouse
นำข้อมูลจาก Google storage เข้า Google bigquery ใช้ Operator = GCSToBigQueryOperator

### Data Transformation (DBT)

Transform ข้อมูล raw data ไปเป็น Cleaned data

Download library dbt-core dbt-bigquery
    pip install dbt-core dbt-bigquery

สร้าง project profile dbt
    dbt init

สร้าง project profile สร้าง file ใน folder project-capstone/models ด้วยชื่อ profiles.yml
    code /home/codespace/.dbt/profiles.yml

ทดสอบการ connection กับ bigquery
    dbt debug
    dbt run
    dbt test

จบงานปิด Docker
    docker compose down

 

