from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from airflow.models import Variable

dag = DAG('vars', description='vars',
          schedule_interval=None,
          start_date=datetime(2024, 11, 9), catchup=False)

def print_var(**context):
    minha_var = Variable.get("minha_var")
    print(f'Variável é: {minha_var}')

task1 = PythonOperator(task_id="tsk1", python_callable=print_var, dag=dag)

task1
