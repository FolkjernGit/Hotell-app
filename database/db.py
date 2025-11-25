from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

mysql_url = "mysql+pymysql://root:Admin1234@localhost:3306/hotell"
engine = create_engine(mysql_url)

My_Session = sessionmaker(engine)