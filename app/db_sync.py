from conf.config import CONFIG_INFO

from urllib import parse
from sqlalchemy import create_engine

from models.schemas import Base as AuthBase

MysqlEngine = None

def get_mysql_engine():
    if MysqlEngine is None:
        dbConf = CONFIG_INFO['Mysql']
        dbUrl = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(dbConf['Username'], parse.quote(dbConf['Password']), dbConf['Host'], dbConf['Port'], dbConf['DBName'])
        MysqlEngine = create_engine(dbUrl, echo=True, future=True)
    
    return MysqlEngine
    
def create():
    AuthBase.metadata.create_all(bind=get_mysql_engine())
    print('创建表结构')

def drop():
    AuthBase.metadata.drop_all(bind=get_mysql_engine())
    print('删除表结构')

def update():
    print('更新表结构')

if __name__ == '__main__':
    drop()
    create()