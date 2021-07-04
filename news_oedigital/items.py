# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsOedigitalItem(scrapy.Item):
    # define the fields for your item here like:
    preview_img_link = scrapy.Field()
    url = scrapy.Field()
    pre_title = scrapy.Field()
    title = scrapy.Field()
    # title = scrapy.Field()
    # sub_title = scrapy.Field()
    content = scrapy.Field()
    # img_content = scrapy.Field()
    categories = scrapy.Field()
    pub_time = scrapy.Field()
    author = scrapy.Field()
    crawl_time = scrapy.Field()
    # crawl_time = scrapy.Field()
    # processed_marker=scrapy.Field()

class WorldOilItem(NewsOedigitalItem):
    pass
    # define the fields for your item here like:
    # preview_img_link = scrapy.Field()
    # url = scrapy.Field()
    # pre_title = scrapy.Field()
    # title = scrapy.Field()
    # # title = scrapy.Field()
    # # sub_title = scrapy.Field()
    # content = scrapy.Field()
    # # img_content = scrapy.Field()
    # categories = scrapy.Field()
    # pub_time = scrapy.Field()
    # author = scrapy.Field()
    # crawl_time = scrapy.Field()
    # crawl_time = scrapy.Field()
    # processed_marker = scrapy.Field()


class HartEnergyItem(NewsOedigitalItem):
    pass

class CnpcNewsItem(NewsOedigitalItem):
    pass

class OilFieldTechItem(NewsOedigitalItem):
    pass

class OilAndGasItem(NewsOedigitalItem):
    pass

class InEnStorageItem(NewsOedigitalItem):
    pass

class JptLatestItem(NewsOedigitalItem):
    pass

class EnergyVoiceItem(NewsOedigitalItem):
    pass

class UpStreamItem(NewsOedigitalItem):
    pass
class OilPriceItem(NewsOedigitalItem):
    pass

class GulfOilGasItem(NewsOedigitalItem):
    pass

class EnergyPediaItem(NewsOedigitalItem):
    pass

class InenTechItem(NewsOedigitalItem):
    pass

class InenNewEnergyItem(NewsOedigitalItem):
    pass


class DrillContractorItem(NewsOedigitalItem):
    pass


class RogTechItem(NewsOedigitalItem):
    pass



class NaturalGasItem(NewsOedigitalItem):
    pass


class RigZoneItem(NewsOedigitalItem):
    pass


class OffshoreTechItem(NewsOedigitalItem):
    pass


class EnergyYearItem(NewsOedigitalItem):
    pass

class EnergyChinaItem(NewsOedigitalItem):
    pass

class ChinaFiveItem(NewsOedigitalItem):
    pass


class OffshoreEnergyItem(NewsOedigitalItem):
    pass


class EinNewsItem(NewsOedigitalItem):
    pass


class JwnEnergyItem(NewsOedigitalItem):
    pass

class IranOilGasItem(NewsOedigitalItem):
    pass


class NengYuanItem(NewsOedigitalItem):
    pass

class WoodMacItem(NewsOedigitalItem):
    pass

class RystadEnergyItem(NewsOedigitalItem):
    pass

class WestwoodEnergyItem(NewsOedigitalItem):
    pass


class IeaNewsItem(NewsOedigitalItem):
    pass


class EvWindItem(NewsOedigitalItem):
    pass

class OffshoreWindItem(NewsOedigitalItem):
    pass
class EnergyTrendItem(NewsOedigitalItem):
    pass
