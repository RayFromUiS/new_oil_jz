# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from news_oedigital.model import OeNews, WorldOil, CnpcNews, HartEnergy, OilFieldTech, \
    db_connect, create_table, OilAndGas, InEnStorage, JptLatest, EnergyVoice, UpStream, OilPrice, GulfOilGas, \
    EnergyPedia, \
    InenTech, InenNewEnergy, DrillContractor, RogTech, NaturalGas, RigZone, OffshoreTech, EnergyYear, EnergyChina, \
    ChinaFive, \
    OffshoreEnergy, EinNews, JwnEnergy, IranOilGas,NengYuan,WoodMac,RystadEnergy,WestwoodEnergy,IeaNews
# from news_oedigital.spiders.oe_offshore import NewsOeOffshoreSpider

import pymongo
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter


class InEnMongoDBPipeline:
    collection_name = 'InEn_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if not self.db[self.collection_name].find_one({'url': item.get('url')}):
            self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item


class NewsOedigitalPipeline:
    def process_item(self, item, spider):
        # session = self.Session()
        # query_col = item.get('url')
        # result = session.query(OeNews).filter(OeNews.url == query_col).first()
        # try:
        # if not result:
        new_item = OeNews(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                          preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                          content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                          categories=item.get('categories'))

        try:

            if item.get('content') is not None or not len(item.get('pub_time')) == 4:
                spider.session.add(new_item)
                spider.session.commit()
            else:
                raise DropItem('no content is downloaded')
        except:
            spider.session.rollback()
            # raise
        return item

    def close_spider(self, spider):
        #     # We commit and save all items to DB when spider finished scraping.
        spider.session.close()


class WorldOilPipeline:
    def process_item(self, item, spider):

        new_item = WorldOil(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                            preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                            content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                            categories=item.get('categories'))

        adapter = ItemAdapter(item)

        try:
            if adapter.get('content') or len(item.get('pub_time')) > 4:
                spider.session.add(new_item)
                spider.session.commit()
            else:
                raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
        return item

    def close_spider(self, spider):
        spider.session.close()


class HartEnergyPipeline:
    def process_item(self, item, spider):
        new_item = HartEnergy(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                              preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                              content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                              categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()


class CnpcNewsPipeline:
    def process_item(self, item, spider):
        new_item = CnpcNews(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                            preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                            content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                            categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()


class OilFieldTechPipeline:
    def process_item(self, item, spider):
        new_item = OilFieldTech(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                                preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                                content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                                categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()


class OilAndGasPipeline:
    def process_item(self, item, spider):
        new_item = OilAndGas(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                             preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                             content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                             categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        finally:
            spider.session.close()
            return item

    def close_spider(self, spider):
        spider.session.close()


class InEnEnergyPipeline:
    def process_item(self, item, spider):
        new_item = InEnStorage(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                               preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                               content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                               categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        finally:
            spider.session.close()
        return item


class JptLatestPipeline:
    def process_item(self, item, spider):
        new_item = JptLatest(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                             preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                             content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                             categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

    def close_spider(self, spider):
        spider.session.close()


class EnergyVoicePipeline:
    def process_item(self, item, spider):
        new_item = EnergyVoice(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                               preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                               content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                               categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

    def close_spider(self, spider):
        spider.session.close()


class UpStreamPipeline:

    def process_item(self, item, spider):
        new_item = UpStream(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                            preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                            content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                            categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

    def close_spider(self, spider):
        spider.session.close()


class OilPricePipeline:
    def process_item(self, item, spider):
        new_item = OilPrice(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                            preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                            content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                            categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

    def close_spider(self, spider):
        spider.session.close()


class GulfOilGasPipeline:
    def process_item(self, item, spider):
        new_item = GulfOilGas(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                              preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                              content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                              categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

    def close_spider(self, spider):
        spider.session.close()


class EnergyPediaPipeline:
    def process_item(self, item, spider):
        new_item = EnergyPedia(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                               preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                               content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                               categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

    def close_spider(self, spider):
        spider.session.close()


class InenTechPipeline:
    def process_item(self, item, spider):
        new_item = InenTech(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                            preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                            content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                            categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

    def close_spider(self, spider):
        spider.session.close()


class InenNewEnergyPipeline:
    def process_item(self, item, spider):
        new_item = InenNewEnergy(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                                 preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                                 content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                                 categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

    def close_spider(self, spider):
        spider.session.close()


class DrillContractorPipeline:
    def process_item(self, item, spider):
        new_item = DrillContractor(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                                   preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                                   content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                                   categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

    def close_spider(self, spider):
        spider.session.close()


class RogTechPipeline:
    def process_item(self, item, spider):
        new_item = RogTech(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                           preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                           content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                           categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

    def close_spider(self, spider):
        spider.session.close()


class NaturalGasPipeline:
    def process_item(self, item, spider):
        new_item = NaturalGas(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                              preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                              content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                              categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

    def close_spider(self, spider):
        spider.session.close()


class RigZonePipeline:
    def process_item(self, item, spider):
        new_item = RigZone(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                           preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                           content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                           categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

    def close_spider(self, spider):
        spider.session.close()


class OffshoreTechPipeline:
    def process_item(self, item, spider):
        new_item = OffshoreTech(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                                preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                                content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                                categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

    def close_spider(self, spider):
        spider.session.close()


class EnergyYearPipeline:
    def process_item(self, item, spider):
        new_item = EnergyYear(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                              preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                              content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                              categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

    def close_spider(self, spider):
        spider.session.close()


class EnergyChinaPipeline:
    def process_item(self, item, spider):
        new_item = EnergyChina(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                               preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                               content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                               categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

    def close_spider(self, spider):
        spider.session.close()


class ChinaFivePipeline:
    def process_item(self, item, spider):
        new_item = ChinaFive(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                             preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                             content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                             categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

    def close_spider(self, spider):
        spider.session.close()


class OffshoreEnergyPipeline:
    def process_item(self, item, spider):
        new_item = OffshoreEnergy(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                                  preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                                  content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                                  categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

    def close_spider(self, spider):
        spider.session.close()


class EinNewsPipeline:
    def process_item(self, item, spider):
        new_item = EinNews(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                           preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                           content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                           categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

    def close_spider(self, spider):
        spider.session.close()


class JwnEnergyPipeline:
    def process_item(self, item, spider):
        new_item = JwnEnergy(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                             preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                             content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                             categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

    def close_spider(self, spider):
        spider.session.close()


class IranOilGasPipeline:
    def process_item(self, item, spider):
        new_item = IranOilGas(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                              preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                              content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                              categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

    def close_spider(self, spider):
        spider.session.close()


class NengYuanPipeline:
    def process_item(self, item, spider):
        new_item = NengYuan(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                              preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                              content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                              categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

    def close_spider(self, spider):
        spider.session.close()

class WoodMacPipeline:
    def process_item(self, item, spider):
        new_item = WoodMac(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                              preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                              content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                              categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

    def close_spider(self, spider):
        spider.session.close()

class RystadEnergyPipeline:
    def process_item(self, item, spider):
        new_item = RystadEnergy(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                              preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                              content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                              categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

    def close_spider(self, spider):
        spider.session.close()

class WestwoodEnergyPipeline:
    def process_item(self, item, spider):
        new_item = WestwoodEnergy(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                              preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                              content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                              categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

    def close_spider(self, spider):
        spider.session.close()

class IeaNewsPipeline:
    def process_item(self, item, spider):
        new_item = IeaNews(title=item.get('title'), author=item.get('author'), pre_title=item.get('pre_title'), \
                              preview_img_link=item.get('preview_img_link'), pub_time=item.get('pub_time'), \
                              content=item.get('content'), crawl_time=item.get('crawl_time'), url=item.get('url'), \
                              categories=item.get('categories'))

        try:
            # if item.get('content'):
            spider.session.add(new_item)
            spider.session.commit()
            # else:
            #     raise DropItem(f"Missing content in {item}")
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()

    def close_spider(self, spider):
        spider.session.close()
