from twisted.internet.task import LoopingCall
from twisted.internet import reactor

from scrapy.crawler import CrawlerRunner,CrawlerProcess
from scrapy.utils.log import configure_logging

from news_oedigital.spiders.news_oe_offshore import \
    NewsOeOffshoreSpider,WorldOilSpider,CnpcNewsSpider,HartEnergySpider,OilFieldTechSpider,\
    OilAndGasSpider,InEnStorageSpider,JptLatestSpider,EnergyVoiceSpider,UpStreamSpider,OilPriceSpider,\
    GulfOilGasSpider,InenTechSpider,InenNewEnergySpider,DrillContractorSpider,RogTechSpider,NaturalGasSpider, \
    RigZoneSpider,OffshoreTechSpider,EnergyYearSpider,EnergyChinaSpider,ChinaFiveSpider,OffshoreEnergySpider, \
    EnergyPediaSpider,JwnEnergySpider,IranOilGasSpider,NengyuanSpider,WoodMacSpider,RystadEnergySpider,\
    IeaNewsSpider,WestwoodEnergySpider,EvWindSpider,OffshoreWindSpider,EnergyTrendSpider,CnpcNewsSpiderUpdated,\
    SolarZoomSpider,FbBjxSpider,GfBjxSpider,HydroProcessSpider,ShaiPgxSpider,MarineTechSpider,SplashOffshoreSpider, \
    MarineExecSpider,PvMagazineSpide
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
    # process.crawl(CnpcNewsSpider)
    process.crawl(CnpcNewsSpiderUpdated)
    process.crawl(HartEnergySpider)
    process.crawl(OilFieldTechSpider)
    process.crawl(OilAndGasSpider)
    process.crawl(InEnStorageSpider)
    process.crawl(JptLatestSpider)
    process.crawl(EnergyVoiceSpider)
    process.crawl(UpStreamSpider)
    process.crawl(OilPriceSpider)
    process.crawl(GulfOilGasSpider)
    process.crawl(InenTechSpider)
    process.crawl(EnergyPediaSpider)
    process.crawl(InenNewEnergySpider)
    process.crawl(DrillContractorSpider)
    process.crawl(RogTechSpider)
    process.crawl(NaturalGasSpider)
    process.crawl(RigZoneSpider)
    process.crawl(OffshoreTechSpider)
    process.crawl(EnergyYearSpider)
    process.crawl(EnergyChinaSpider)
    process.crawl(ChinaFiveSpider)
    process.crawl(OffshoreEnergySpider)
    process.crawl(JwnEnergySpider)
    process.crawl(IranOilGasSpider)
    process.crawl(NengyuanSpider)
    process.crawl(WoodMacSpider)
    process.crawl(RystadEnergySpider)
    process.crawl(WestwoodEnergySpider)
    process.crawl(IeaNewsSpider)
    process.crawl(EvWindSpider)
    process.crawl(OffshoreWindSpider)
    process.crawl(EnergyTrendSpider)
    process.crawl(SolarZoomSpider)
    process.crawl(FbBjxSpider)
    process.crawl(GfBjxSpider)
    process.crawl(HydroProcessSpider)
    process.crawl(PvMagazineSpide)
    process.crawl(ShaiPgxSpider)
    process.crawl(MarineTechSpider)
    process.crawl(SplashOffshoreSpider)
    process.crawl(MarineExecSpider)
    # process.crawl(MarineTechSpider)
    process.start()


if __name__ == "__main__":
    run_scraper()
