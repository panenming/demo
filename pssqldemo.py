'''
pssql连接
'''
import psycopg2

conn = psycopg2.connect(database="enn_fnt",user="postgres",password="xinao",host="10.39.3.43",port="5432")

print("-")