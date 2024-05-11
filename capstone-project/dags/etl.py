from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyDatasetOperator
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils import timezone
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

import os
import glob

with DAG(
    "etl",
    start_date=timezone.datetime(2024,5,10),
    schedule_interval="@daily",
    tags=["ds-525"],
) as dag:

# Dummy start task   
    start = DummyOperator(
        task_id='start',
        dag=dag,
    )


    # Task to load data into Google Cloud Storage
    upload_file_sales_to_gcs = GCSToGCSOperator(
        task_id="upload_file_sales_to_capstone",
        source_bucket="ds-525",
        source_objects=["Sales.csv"],
        destination_bucket="ds-525-cleaned",
        destination_object="Sales.csv",
        gcp_conn_id='my_gcp_conn'
    )

    # Task to load data into Google Cloud Storage
    upload_file_products_to_gcs = GCSToGCSOperator(
        task_id="upload_file_products_to_capstone",
        source_bucket="ds-525",
        source_objects=["Products.csv"],
        destination_bucket="ds-525-cleaned",
        destination_object="Products.csv",
        gcp_conn_id='my_gcp_conn'
    )

    # Task to load data into Google Cloud Storage
    upload_file_customers_to_gcs = GCSToGCSOperator(
        task_id="upload_file_customers_to_capstone",
        source_bucket="ds-525",
        source_objects=["Customers.csv"],
        destination_bucket="ds-525-cleaned",
        destination_object="Customers.csv",
        gcp_conn_id='my_gcp_conn'
    )

    # Task to load data into Google Cloud Storage
    upload_file_stores_to_gcs = GCSToGCSOperator(
        task_id="upload_file_stores_to_capstone",
        source_bucket="ds-525",
        source_objects=["Stores.csv"],
        destination_bucket="ds-525-cleaned",
        destination_object="Stores.csv",
        gcp_conn_id='my_gcp_conn'
    )

    # Task to load data into Google Cloud Storage
    upload_file_exchange_rates_to_gcs = GCSToGCSOperator(
        task_id="upload_file_exchange_rates_to_capstone",
        source_bucket="ds-525",
        source_objects=["Exchange_Rates.csv"],
        destination_bucket="ds-525-cleaned",
        destination_object="Exchange_Rates.csv",
        gcp_conn_id='my_gcp_conn'
    )

#------------------------------------------------------------------------------------------------------#
    create_sales_dataset = BigQueryCreateEmptyDatasetOperator(
        task_id='create_sales_dataset',
        dataset_id='sales',
        gcp_conn_id='my_gcp_conn',
    )

#------------------------------------------------------------------------------------------------------#
    gcs_load_to_bigquery_customers = GCSToBigQueryOperator(
    task_id                             = "gcs_load_to_bigquery_customers",
    bucket                              = 'ds-525-cleaned',
    source_objects                      = ['Customers.csv'],
    destination_project_dataset_table   ='sales.Customer',
    write_disposition='WRITE_TRUNCATE',
    create_disposition          = 'CREATE_IF_NEEDED',
    gcp_conn_id='my_gcp_conn'
    )

    gcs_load_to_bigquery_products = GCSToBigQueryOperator(
    task_id                             = "gcs_load_to_bigquery_products",
    bucket                              = 'ds-525-cleaned',
    source_objects                      = ['Products.csv'],
    destination_project_dataset_table   ='sales.Products',
    write_disposition='WRITE_TRUNCATE',
    create_disposition          = 'CREATE_IF_NEEDED',
    gcp_conn_id='my_gcp_conn'
    )   

gcs_load_to_bigquery_stores = GCSToBigQueryOperator(
    task_id                             = "gcs_load_to_bigquery_stores",
    bucket                              = 'ds-525-cleaned',
    source_objects                      = ['Stores.csv'],
    destination_project_dataset_table   ='sales.Stores',
    write_disposition='WRITE_TRUNCATE',
    create_disposition          = 'CREATE_IF_NEEDED',
    gcp_conn_id='my_gcp_conn'
    )   

gcs_load_to_bigquery_exchange_rates = GCSToBigQueryOperator(
    task_id                             = "gcs_load_to_bigquery_exchange_rates",
    bucket                              = 'ds-525-cleaned',
    source_objects                      = ['Exchange_Rates.csv'],
    destination_project_dataset_table   ='sales.Exchange_Rates',
    write_disposition='WRITE_TRUNCATE',
    create_disposition          = 'CREATE_IF_NEEDED',
    gcp_conn_id='my_gcp_conn'
    )   

# Dummy end task
end = DummyOperator(
        task_id='end',
        dag=dag,
    )

    # start >> get_files >> upload_file >> create_order_dataset >> load_dataset_order >> transform_bq >> end
start >> [upload_file_sales_to_gcs, upload_file_products_to_gcs, upload_file_customers_to_gcs, upload_file_stores_to_gcs ,upload_file_exchange_rates_to_gcs] >> create_sales_dataset >> [gcs_load_to_bigquery_customers, gcs_load_to_bigquery_products, gcs_load_to_bigquery_stores, gcs_load_to_bigquery_exchange_rates]