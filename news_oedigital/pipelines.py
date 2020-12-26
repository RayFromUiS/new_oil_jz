# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from news_oedigital.model import OeNews,WorldOil,CnpcNews,HartEnergy,OilFieldTech, db_connect, create_table,OilAndGas,InEnStorage
# from news_oedigital.spiders.oe_offshore import NewsOeOffshoreSpider

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
            spider.session.add(new_item)
            spider.session.commit()
        except:
            spider.session.rollback()
            raise
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


        try:
            spider.session.add(new_item)
            spider.session.commit()
        except:
            spider.session.rollback()
            raise
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
            spider.session.add(new_item)
            spider.session.commit()
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
            spider.session.add(new_item)
            spider.session.commit()
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
            spider.session.add(new_item)
            spider.session.commit()
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
            spider.session.add(new_item)
            spider.session.commit()
        except:
            spider.session.rollback()
            raise
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
            spider.session.add(new_item)
            spider.session.commit()
        except:
            spider.session.rollback()
            raise
        return item

    def close_spider(self, spider):
        spider.session.close()