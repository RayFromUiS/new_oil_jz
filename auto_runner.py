from twisted.internet.task import LoopingCall
from twisted.internet import reactor

from scrapy.crawler import CrawlerRunner,CrawlerProcess
from scrapy.utils.log import configure_logging

from news_oedigital.spiders.news_oe_offshore import NewsOeOffshoreSpider,WorldOilSpider,CnpcNewsSpider,HartEnergySpider

from scrapy.settings import Settings
from news_oedigital import settings


def run_scraper():
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    configure_logging()
    # runner = CrawlerRunner(settings=crawler_settings)
    # task = LoopingCall(lambda: runner.crawl(NewsOeOffshoreSpider))
    # task.start(6000 * 100)
    # reactor.run()
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(NewsOeOffshoreSpider)
    process.crawl(WorldOilSpider)
    process.crawl(CnpcNewsSpider)
    process.crawl(HartEnergySpider)
    process.start()


if __name__ == "__main__":
    run_scraper()
