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
    title = Column(String(1024))
    pre_title = Column(String(2048))
    author = Column(String(255))
    pub_time = Column(String(255))
    preview_img_link = Column(String(2048))
    content = Column(Text)
    categories = Column(String(255))
    crawl_time = Column(String(255))
    url = Column(String(1024))


class CnpcNews(Base):
    __tablename__ = 'cnpc_news'
    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    pre_title = Column(String(2048))
    author = Column(String(255))
    pub_time = Column(String(255))
    preview_img_link = Column(String(2048))
    content = Column(Text)
    categories = Column(String(255))
    crawl_time = Column(String(255))
    url = Column(String(1024))


class HartEnergy(Base):
    __tablename__ = 'hart_energy'
    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    pre_title = Column(String(2048))
    author = Column(String(255))
    pub_time = Column(String(255))
    preview_img_link = Column(String(2048))
    content = Column(Text)
    categories = Column(String(255))
    crawl_time = Column(String(255))
    url = Column(String(1024))


class OilFieldTech(Base):
    __tablename__ = 'oilfield_tech'
    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    pre_title = Column(String(2048))
    author = Column(String(255))
    pub_time = Column(String(255))
    preview_img_link = Column(String(2048))
    content = Column(Text)
    categories = Column(String(255))
    crawl_time = Column(String(255))
    url = Column(String(1024))


class OilAndGas(Base):
    __tablename__ = 'oil_and_gas'
    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    pre_title = Column(String(2048))
    author = Column(String(255))
    pub_time = Column(String(255))
    preview_img_link = Column(String(2048))
    content = Column(Text)
    categories = Column(String(255))
    crawl_time = Column(String(255))
    url = Column(String(1024))


class InEnStorage(Base):
    __tablename__ = 'in_en_storage'
    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    pre_title = Column(String(2048))
    author = Column(String(255))
    pub_time = Column(String(255))
    preview_img_link = Column(String(2048))
    content = Column(Text)
    categories = Column(String(255))
    crawl_time = Column(String(255))
    url = Column(String(1024))


class JptLatest(Base):
    __tablename__ = 'jpt_latest'
    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    pre_title = Column(String(2048))
    author = Column(String(255))
    pub_time = Column(String(255))
    preview_img_link = Column(String(2048))
    content = Column(Text)
    categories = Column(String(255))
    crawl_time = Column(String(255))
    url = Column(String(1024))


class EnergyVoice(Base):
    __tablename__ = 'energy_voice'
    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    pre_title = Column(String(2048))
    author = Column(String(255))
    pub_time = Column(String(255))
    preview_img_link = Column(String(2048))
    content = Column(Text)
    categories = Column(String(255))
    crawl_time = Column(String(255))
    url = Column(String(1024))


class UpStream(Base):
    __tablename__ = 'up_stream'
    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    pre_title = Column(String(2048))
    author = Column(String(255))
    pub_time = Column(String(255))
    preview_img_link = Column(String(2048))
    content = Column(Text)
    categories = Column(String(255))
    crawl_time = Column(String(255))
    url = Column(String(1024))


class OilPrice(Base):
    __tablename__ = 'oil_price'
    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    pre_title = Column(String(2048))
    author = Column(String(255))
    pub_time = Column(String(255))
    preview_img_link = Column(String(2048))
    content = Column(Text)
    categories = Column(String(255))
    crawl_time = Column(String(255))
    url = Column(String(1024))

class GulfOilGas(Base):
    __tablename__ = 'gulf_oil_gas'
    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    pre_title = Column(String(2048))
    author = Column(String(255))
    pub_time = Column(String(255))
    preview_img_link = Column(String(2048))
    content = Column(Text)
    categories = Column(String(255))
    crawl_time = Column(String(255))
    url = Column(String(1024))

class EnergyPedia(Base):
    __tablename__ = 'energy_pedia'
    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    pre_title = Column(String(2048))
    author = Column(String(255))
    pub_time = Column(String(255))
    preview_img_link = Column(String(2048))
    content = Column(Text)
    categories = Column(String(255))
    crawl_time = Column(String(255))
    url = Column(String(1024))

class InenTech(Base):
    __tablename__ = 'inen_tech'
    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    pre_title = Column(String(2048))
    author = Column(String(255))
    pub_time = Column(String(255))
    preview_img_link = Column(String(2048))
    content = Column(Text)
    categories = Column(String(255))
    crawl_time = Column(String(255))
    url = Column(String(1024))

class InenNewEnergy(Base):
    __tablename__ = 'inen_newenergy'
    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    pre_title = Column(String(2048))
    author = Column(String(255))
    pub_time = Column(String(255))
    preview_img_link = Column(String(2048))
    content = Column(Text)
    categories = Column(String(255))
    crawl_time = Column(String(255))
    url = Column(String(1024))


if __name__ == "__main__":
    db_connect()
