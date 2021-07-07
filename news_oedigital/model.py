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

class DrillContractor(Base):
    __tablename__ = 'drill_contractor'
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


class RogTech(Base):
    __tablename__ = 'rog_tech'
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


class NaturalGas(Base):
    __tablename__ = 'natural_gas'
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


class RigZone(Base):
    __tablename__ = 'rig_zone'
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


class OffshoreTech(Base):
    __tablename__ = 'offshore_tech'
    id = Column(Integer, primary_key=True)
    title = Column(String(1024))
    pre_title = Column(String(2048))
    author = Column(String(1024))
    pub_time = Column(String(255))
    preview_img_link = Column(String(2048))
    content = Column(Text)
    categories = Column(String(1024))
    crawl_time = Column(String(255))
    url = Column(String(1024))


class EnergyYear(Base):
    __tablename__ = 'energy_year'
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

class EnergyChina(Base):
    __tablename__ = 'energy_china'
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

class ChinaFive(Base):
    __tablename__ = 'china_five'
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

class OffshoreEnergy(Base):
    __tablename__ = 'offshore_energy'
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


class EinNews(Base):
    __tablename__ = 'ein_news'
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

class JwnEnergy(Base):
    __tablename__ = 'jwn_energy'
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


class IranOilGas(Base):
    __tablename__ = 'iran_oil_gas'
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

class NengYuan(Base):
    __tablename__ = 'neng_yuan'
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

class WoodMac(Base):
    __tablename__ = 'wood_mac'
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

class RystadEnergy(Base):
    __tablename__ = 'rystad_energy'
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

class WestwoodEnergy(Base):
    __tablename__ = 'westwood_energy'
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

class IeaNews(Base):
    __tablename__ = 'iea_news'
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

class EvWind(Base):
    __tablename__ = 'ev_wind'
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

class OffshoreWind(Base):
    __tablename__ = 'offshore_wind'
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

class EnergyTrend(Base):
    __tablename__ = 'energy_trend'
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


class PvMagazine(Base):
    __tablename__ = 'pv_magazine'
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

class SolarZoom(Base):
    __tablename__ = 'solar_zoom'
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
