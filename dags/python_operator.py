from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd
import statistics as sts

dag = DAG('python_operator', description='python_operator',
          schedule_interval=None, start_date=datetime(2024, 11, 9),
          catchup=False)

def data_clear():
    dataset = pd.read_csv('/opt/airflow/data/Churn.csv', sep=';')
    dataset.columns = ['Id', 'score', 'estado', 'Genero', 'Idade', 'patrimonio', 'Saldo', 'Produtos', 'TemCartCredito', 'Ativo', 'Salario', 'Saiu']
    
    mediana = sts.median(dataset['Salario'])
    dataset['Salario'].fillna(mediana, inplace=True)
    dataset['Genero'].fillna('Masculino', inplace=True)
    
    mediana = sts.median(dataset['Idade'])
    dataset.loc[(dataset['Idade'] < 0) | (dataset['Idade'] > 120), 'Idade'] = mediana
    
    dataset.drop_duplicates(subset='Id', keep='first', inplace=True)
    
    dataset.to_csv('/opt/airflow/data/Churn_Clean.csv', sep=';', index=False)

task1 = PythonOperator(task_id='data_clear', python_callable=data_clear, dag=dag)
task1