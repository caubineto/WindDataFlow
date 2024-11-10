from airflow import DAG
from datetime import datetime
from big_data_operator import BigDataOperator

dag = DAG('bigdata', description='big_data',
          start_date=datetime(2021, 1, 1), 
          schedule_interval='@daily',
          catchup=False)

big_data = BigDataOperator(task_id='big_data', 
                           path_to_csv_file='/opt/airflow/data/Churn.csv',
                           path_to_save_file='/opt/airflow/data/Churn.json',
                           file_type='json',
                           dag=dag)

big_data