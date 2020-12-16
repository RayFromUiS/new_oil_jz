from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, SmallInteger, String, Date, DateTime, Float, Boolean, Text, LargeBinary)

from scrapy.utils.project import get_project_settings

Base = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    # print('uri',get_project_settings().get("SQL_CONNECT_STRING"))
    return create_engine(get_project_settings().get("SQL_CONNECT_STRING"))

def create_table(engine):
    Base.metadata.create_all(engine)

class OeNews(Base):
    __tablename__ = 'news_oil_oe'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    pre_title = Column(String(255))
    author = Column(String(255))
    pub_time = Column(String(255))
    preview_img_link = Column(String(255))
    content = Column(Text)
    categories = Column(String(255))
    crawl_time = Column(String(255))
    url = Column(String(255))
    # processed_marker = Column(String(64))


class WorldOil(Base):
    __tablename__ = 'world_oil'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    pre_title = Column(String(255))
    author = Column(String(255))
    pub_time = Column(String(255))
    preview_img_link = Column(String(255))
    content = Column(Text)
    categories = Column(String(255))
    crawl_time = Column(String(255))
    url = Column(String(255))


class CnpcNews(Base):
    __tablename__ = 'cnpc_news'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    pre_title = Column(String(255))
    author = Column(String(255))
    pub_time = Column(String(255))
    preview_img_link = Column(String(255))
    content = Column(Text)
    categories = Column(String(255))
    crawl_time = Column(String(255))
    url = Column(String(255))

if __name__ == "__main__":
    db_connect()
