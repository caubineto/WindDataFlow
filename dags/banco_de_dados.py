from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
from airflow.providers.postgres.operators.postgres import PostgresOperator

dag = DAG('banco_de_dados', description='Criando tabelas no banco de dados',
          schedule_interval=None, start_date=datetime(2021, 1, 1),
          catchup=False)

def print_result(ti):
    task_instance = ti.xcom_pull(task_ids='query_data')
    print('Resultado da consulta: ')
    for row in task_instance:
        print(row)

create_table = PostgresOperator(task_id='create_table', 
                                sql='create table if not exists teste(id int);', 
                                postgres_conn_id='postgres', 
                                dag=dag)

insert_data = PostgresOperator(task_id='insert_data', 
                                sql='insert into teste values(1);', 
                                postgres_conn_id='postgres', 
                                dag=dag)

query_data = PostgresOperator(task_id='query_data', 
                                sql='select * from teste;', 
                                postgres_conn_id='postgres', 
                                dag=dag)

print_result_task = PythonOperator(task_id='print_result_task',
                                   python_callable=print_result,
                                   dag=dag)

create_table >> insert_data >> query_data >> print_result_task  # Ordem de execução dos operadores

