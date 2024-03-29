# Scrapy settings for news_oedigital project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html


import os
from shutil import which

BOT_NAME = 'news_oedigital'

SPIDER_MODULES = ['news_oedigital.spiders']
NEWSPIDER_MODULE = 'news_oedigital.spiders'

# DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True
SELENIUM_DRIVER_NAME = 'firefox'
SELENIUM_DRIVER_EXECUTABLE_PATH = which('geckodriver')
SELENIUM_DRIVER_ARGUMENTS = ['-headless']  # '--headless' if using chrome instead of firefox
RETRY_TIMES = 3
# Retry on most error codes since proxies fail for different reasons
RETRY_HTTP_CODES = [500, 503, 504, 400,  408] #403,404
PROXY_LIST = 'news_oedigital/spiders/proxies'
PROXY_MODE = 0  # different proxy for each request
RANDOM_UA_PER_PROXY = True
FAKEUSERAGENT_FALLBACK = 'Mozillapip install scrapy_proxies'
DOWNLOADER_MIDDLEWARES = {
    #    'news_oil_gas.middlewares.NewsOilGasDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 900,
    # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,
    'scrapy_proxies.RandomProxy': 700,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 710,
    'scrapy_selenium.SeleniumMiddleware': 750,
    # 'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    # 'scrapy.downloadermiddlewares.cookies.PersistentCookiesMiddleware': 751,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy_cookies.downloadermiddlewares.cookies.CookiesMiddleware': 711,
    # 'scrapy_splash.SplashCookiesMiddleware': 650,
    # 'scrapy_splash.SplashMiddleware': 652,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    # 'news_oedigital.middlewares.NewsOedigitalDownloaderMiddleware':751,
}

SQL_CONNECT_STRING = 'mysql+pymysql://root:jinzheng1706@139.198.191.224:3308/news_oil'
SQL_DB_NAME = 'news_oil'
MONGO_URI= 'mongodb://root:password@localhost:27017/'

MONGO_DATABASE='petroleum_news'
SPLASH_URL = 'http://127.0.0.1:8050/'

# SPIDER_MIDDLEWARES = {
#     'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
# }
# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
# HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'news_oedigital (+http://www.yourdomain.com)'

COOKIES_ENABLED = True
COOKIES_PERSISTENCE = True
COOKIES_PERSISTENCE_DIR = 'cookies'
COOKIES_STORAGE = 'scrapy_cookies.storage.in_memory.InMemoryStorage'
DOWNLOADER_MIDDLEWARES.update({
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy_cookies.downloadermiddlewares.cookies.CookiesMiddleware': 711,
})

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = True
# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'news_oedigital.middlewares.NewsOedigitalSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'news_oedigital.middlewares.NewsOedigitalDownloaderMiddleware': 543,
# }
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy_selenium.SeleniumMiddleware': 800
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'scrapy.pipelines.images.ImagesPipeline': 1,
    'news_oedigital.pipelines.NewsOedigitalPipeline': 300,
    'news_oedigital.pipelines.WorldOilPipeline': 301,
    'news_oedigital.pipelines.CnpcNewsPipeline': 302,
    'news_oedigital.pipelines.HartEnergyPipeline': 303,
    'news_oedigital.pipelines.OilFieldTechPipeline': 304,
    'news_oedigital.pipelines.OilAndGasPipeline': 305,
    'news_oedigital.pipelines.InEnEnergyPipeline': 306,
    'news_oedigital.pipelines.InEnMongoDBPipeline': 307,
    'news_oedigital.pipelines.JptLatestPipeline': 308,
    # 'news_oedigital.pipelines.JptLastestMongoPipeline': 308,
    'news_oedigital.pipelines.EnergyVoicePipeline': 309,
    'news_oedigital.pipelines.UpStreamPipeline': 310,
    'news_oedigital.pipelines.OilPricePipeline': 311,
    'news_oedigital.pipelines.GulfOilGasPipeline': 312,
    'news_oedigital.pipelines.EnergyPediaPipeline': 313,
    'news_oedigital.pipelines.InenTechPipeline': 314,
    'news_oedigital.pipelines.InenNewEnergyPipeline': 315,
    'news_oedigital.pipelines.DrillContractorPipeline': 316,
    'news_oedigital.pipelines.RogTechPipeline': 317,
    'news_oedigital.pipelines.NaturalGasPipeline': 318,
    'news_oedigital.pipelines.RigZonePipeline': 319,
    'news_oedigital.pipelines.OffshoreTechPipeline': 320,
    'news_oedigital.pipelines.EnergyYearPipeline': 321,
    'news_oedigital.pipelines.EnergyChinaPipeline': 322,
    'news_oedigital.pipelines.ChinaFivePipeline': 323,
    'news_oedigital.pipelines.OffshoreEnergyPipeline': 324,
    'news_oedigital.pipelines.EinNewsPipeline': 325,
    'news_oedigital.pipelines.JwnEnergyPipeline': 326,
    'news_oedigital.pipelines.IranOilGasPipeline': 327,
    'news_oedigital.pipelines.NengYuanPipeline': 328,
    'news_oedigital.pipelines.WoodMacPipeline': 329,
    'news_oedigital.pipelines.RystadEnergyPipeline': 330,
    'news_oedigital.pipelines.WestwoodEnergyPipeline': 331,
    'news_oedigital.pipelines.IeaNewsPipeline': 332,
    'news_oedigital.pipelines.EvWindPipeline': 333,
    'news_oedigital.pipelines.OffshoreWindPipeline': 334,
    'news_oedigital.pipelines.EnergyTrendPipeline': 335,
    'news_oedigital.pipelines.PvMagazinePipeline': 336,
    'news_oedigital.pipelines.SolarZoomPipeline': 337,
    'news_oedigital.pipelines.FbBjxPipeline': 338,
    'news_oedigital.pipelines.GfBjxPipeline': 339,
    'news_oedigital.pipelines.PetroEconomistPipeline': 340,
    'news_oedigital.pipelines.HydroProcessPipeline': 341,
    'news_oedigital.pipelines.ShaiPgxPipeline': 342,
    'news_oedigital.pipelines.MarineTechPipeline': 343,
    'news_oedigital.pipelines.MarineExecPipeline': 344,
    'news_oedigital.pipelines.SplashOffshorePipeline': 345,
    'news_oedigital.pipelines.AmericanNewsPipeline': 346,
    'news_oedigital.pipelines.OilGasIqPipeline': 347

}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
