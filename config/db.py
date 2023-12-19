
from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, Float, MetaData

engine = create_engine("mysql+pymysql://root:admin@localhost:3306/procasa")



meta_data = MetaData()