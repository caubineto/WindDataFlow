from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

dag = DAG('xcon', description='exemplo xcon',
          schedule_interval=None,
          start_date=datetime(2024, 11, 9), catchup=False)

def task_write(**kwargs):
    """Pushes a value to XCom."""
    kwargs['ti'].xcom_push(key='valor', value=1328)

task1 = PythonOperator(task_id="tsk1", python_callable=task_write, dag=dag)

def task_read(**kwargs):
    """Reads a value from XCom and prints it."""
    valor = kwargs['ti'].xcom_pull(key='valor')
    print(f'valor recuperado: {valor}')

task2 = PythonOperator(task_id="tsk2", python_callable=task_read, dag=dag)

task1 >> task2
