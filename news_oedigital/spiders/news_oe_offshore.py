import os
import re
import time
import scrapy
from datetime import datetime
from news_oedigital.items import \
    NewsOedigitalItem, WorldOilItem, CnpcNewsItem, HartEnergyItem, OilFieldTechItem, OilAndGasItem, InEnStorageItem, \
    JptLatestItem, EnergyVoiceItem, UpStreamItem, OilPriceItem, GulfOilGasItem, EnergyPediaItem, InenTechItem, \
    InenNewEnergyItem, DrillContractorItem, RogTechItem, NaturalGasItem, RigZoneItem, OffshoreTechItem,EnergyYearItem
from news_oedigital.model import OeNews, db_connect, create_table, WorldOil, CnpcNews, HartEnergy, OilFieldTech, \
    OilAndGas, InEnStorage, JptLatest, EnergyVoice, UpStream, OilPrice, GulfOilGas, EnergyPedia, InenTech, \
    InenNewEnergy, DrillContractor, RogTech, NaturalGas, RigZone, OffshoreTech,EnergyYear
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, or_
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver import PhantomJS
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
import pymongo
from scrapy_splash import SplashRequest


class NewsOeOffshoreSpider(scrapy.Spider):
    name = 'news_oe_offshore'
    # allowed_domains = ['oedigital.com']
    start_urls = ['http://www.oedigital.com/']
    custom_settings = {
        'ITEM_PIPELINES': {'news_oedigital.pipelines.NewsOedigitalPipeline': 300},
    }

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        self.engine = db_connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        create_table(self.engine)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url,
                                 callback=self.parse_cate_links)

    def parse_cate_links(self, response):
        '''
        parsed the sub category
        :param response:
        :return:
        '''
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)
        sub_cates = response.css('nav.hor a')
        for sub_cate in sub_cates:
            if len(re.findall('/', sub_cate.attrib['href'])) == 2:
                href = sub_cate.attrib['href']  ##relative url of category
                # print(href)
                yield response.follow(url=href, callback=self.parse_page_links)

    def parse_page_links(self, response):
        '''
        parse page links
        :param response:
        :return:
        '''
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)
        results = []  ##storage for the checking of items of database
        preview_img_link = None
        pre_title = None

        # iterate all the element content and if this page is touched,then skip following the next page
        for item_content in response.css('a.snippet'):
            if item_content.css('img') is not None:
                preview_img_link = item_content.css('img::attr(src)').get()
            if item_content.css('h2') is not None:
                pre_title = item_content.css('h2::text').get()
            item_href = 'https://www.oedigital.com' + item_content.attrib['href']
            result = self.session.query(OeNews) \
                .filter(or_(OeNews.url == item_href, OeNews.pre_title == pre_title)) \
                .first()
            results.append(result)
            if not result:  ##item not existed inside the database,then scraped
                yield response.follow(
                    url=item_content.attrib['href'],
                    callback=self.parse,
                    cb_kwargs={'preview_img_link': preview_img_link, 'pre_title': pre_title}
                )
        # test if the page has been touched or not
        if len([result for result in results if result is None]) == len(results):  ## if all the element is not crawled
            next_page = response.css('a[title="Next"]::attr(href)')[0]
            if next_page is not None:
                yield response.follow(url=next_page, callback=self.parse_page_links)

    def parse(self, response, preview_img_link, pre_title):
        # from scrapy.shell import inspect_response
        item = NewsOedigitalItem()
        item['url'] = response.url
        item['preview_img_link'] = preview_img_link
        item['pre_title'] = pre_title
        item['title'] = response.css('div.article h1::text').get().strip()
        if len(response.css('p.meta span')) == 2:
            item['author'] = response.css('p.meta span::text')[0].get()
            item['pub_time'] = response.css('p.meta span::text')[1].get()
        elif len(response.css('p.meta span')) == 1:
            item['author'] = None
            item['pub_time'] = response.css('p.meta span::text').get()
        else:
            item['author'] = None
            item['pub_time'] = None
        item['categories'] = str(response.css('div.categories a::text').getall())
        item['crawl_time'] = datetime.now().strftime('%m/%d/%Y %H:%M')
        # item['categories'] = response.css('div.categories a::text').getall()
        item['content'] = response.css('div.article').get()
        # item['processed_marker'] = None

        yield item


class WorldOilSpider(scrapy.Spider):
    name = 'world_oil_spider'
    # allowed_domains = ['worldoil.com']
    start_urls = ['http://www.worldoil.com']
    custom_settings = {
        'ITEM_PIPELINES': {'news_oedigital.pipelines.WorldOilPipeline': 301},
    }

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        self.engine = db_connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        create_table(self.engine)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_cate_links)

    def parse_cate_links(self, response):
        # category_names = response.css('ul.topic-list a::text').getall()
        category_hrefs = response.css('ul.topic-list li')
        for category_href in category_hrefs:
            cate_href = category_href.css('a').attrib['href']
            cate = category_href.css('a::text').get()
            yield response.follow(url=cate_href, callback=self.parse_page_links, cb_kwargs={'categories': cate})

    def parse_page_links(self, response, categories):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        results = []
        preview_img_link = None
        articles = response.css('div.article')
        for article in articles:
            title = article.css('h2 a::text').get()
            title_url = article.css('a').attrib['href']
            pub_time = article.css('div.source a::text').get().strip().split(' ')[-1] \
                if re.search(r'[0-9]', article.css('div.source a::text').get()) else None
            abstract = article.css('p::text').get()
            item_href = 'https://www.worldoil.com' + title_url
            result = self.session.query(WorldOil) \
                .filter(or_(WorldOil.url == item_href, WorldOil.title == title)) \
                .first()
            results.append(result)
            if not result:
                yield response.follow(url=title_url, callback=self.parse,
                                      cb_kwargs={'title': title,
                                                 'pub_time': pub_time,
                                                 'abstract': abstract,
                                                 'category': categories,
                                                 'preview_img_link': preview_img_link})
        # if preview_img_link is not None:
        if len([result for result in results if result is None]) == len(results):  ## if all the element is not crawled
            # skip the preview image links,since it's not been found generally
            if response.css('a#ContentPlaceHolderDefault_mainContent_btnNext'):
                next_page = response.css('a#ContentPlaceHolderDefault_mainContent_btnNext').attrib['href']
                yield response.follow(url=next_page, callback=self.parse_page_links,
                                      cb_kwargs={'categories': categories})

    def parse(self, response, title, pub_time, abstract, category, preview_img_link):
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)
        item = WorldOilItem()

        item['url'] = response.url
        item['preview_img_link'] = preview_img_link
        item['pre_title'] = abstract
        item['title'] = title
        if len(response.css('div.author span')) == 2:
            item['author'] = response.css('div.author span::text')[0].get()
            # item['pub_time'] = response.css('div.author span::text')[1].get()
        elif len(response.css('div.author span')) == 1:
            item['author'] = None

        item['pub_time'] = pub_time
        item['categories'] = str(category)
        item['crawl_time'] = datetime.now().strftime('%m/%d/%Y %H:%M')
        # item['categories'] = response.css('div.categories a::text').getall()
        # item['content'] = str(response.css('div#news p').getall()
        item['content'] = response.css('div#news').get()
        yield item


class CnpcNewsSpider(scrapy.Spider):
    name = 'cnpc_news'
    # allowed_domains = ['news.cnpc.com.cn']
    start_urls = ['http://news.cnpc.com.cn/']
    custom_settings = {
        'ITEM_PIPELINES': {'news_oedigital.pipelines.CnpcNewsPipeline': 302},
    }

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        self.engine = db_connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        create_table(self.engine)

    def start_requests(self):

        for url in self.start_urls:
            yield scrapy \
                .Request(url=url, callback=self.parse_sub_cate)

    # extract all the sub category url
    def parse_sub_cate(self, response):
        main_ele = 'div.mysubnav'
        sub_ele = 'li a'
        # id = 'downpage'
        sub_divs = response.css(main_ele)
        for sub_div in sub_divs:
            li_links = sub_div.css(sub_ele)  ## all the selector of sub div
            for li_link in li_links:
                # sub_cate = li_link.css('a::text').get()
                sub_cate_link = li_link.css('a::attr(href)').get()
                if re.match(r'\/', sub_cate_link):
                    yield SeleniumRequest(  ## to return a response with driver object
                        url=response.urljoin(sub_cate_link),
                        callback=self.parse_page_links
                    )

    ## grap all the url of each sub category
    def parse_page_links(self, response):
        next_id = 'downpage'
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        results = []
        articles = response.css('li.ejli a')
        for article in articles:
            title = article.css('a::text').get()
            title_url = article.css('a').attrib['href']
            result = self.session.query(CnpcNews) \
                .filter(or_(CnpcNews.url == title_url, CnpcNews.title == title)) \
                .first()
            results.append(result)
            if not result:
                yield scrapy.Request(url=title_url, callback=self.parse)

        # if len([result for result in results if result is None]) == len(results):  ## if all the element is
        driver = response.request.meta['driver']
        while driver.find_element_by_id(next_id) is not None:
            driver.find_element_by_id(next_id).click()

            # print('current url is once clicked', driver.current_url)
            yield SeleniumRequest \
                (url=driver.current_url,
                 wait_time=10,
                 callback=self.parse_page_links,
                 wait_until=EC.element_to_be_clickable((By.ID, id))
                 )
        # time.sleep(10)

    def parse(self, response):
        # from scrapy.shell import inquitself)
        item = CnpcNewsItem()
        item['url'] = response.url
        item['categories'] = response.css('div.sj-nav span.as06 a::text')[-1].get()
        item['pre_title'] = response.css('div.sj-title h4::text').get()
        item['title'] = response.css('div.sj-title h2 a::text').get()
        # news_item['sub_title'] = response.css('div.sj-title h6 a::text').get()
        # item['sub_title'] = response.css('div.sj-title h6::text').get()
        item['author'] = response.css('div.sj-n a::text').get()
        item['pub_time'] = '-'.join(response.url.split('/')[-4:-1])
        item['content'] = response.css('div.sj-main').get()
        # news_item['content_other'] = response.css('div.sj-main p::text').getall()
        item['crawl_time'] = datetime.now().strftime('%m/%d/%Y %H:%M')
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        yield item


class HartEnergySpider(scrapy.Spider):
    name = 'hart_energy'
    # allowed_domains = ['hartenergy.com']
    start_urls = ['http://www.hartenergy.com/']
    custom_settings = {
        'ITEM_PIPELINES': {'news_oedigital.pipelines.HartEnergyPipeline': 303},
    }

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        self.engine = db_connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        create_table(self.engine)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_cate_links)

    def parse_cate_links(self, response):

        cate_lis = response.css('li.nav-item')[:9]  ## only extract 9 of category
        for cate_li in cate_lis:
            cate_url = cate_li.css('a').attrib['href']
            cate_name = cate_li.css('a::text').get()  # main category name
            yield response.follow(url=cate_url, callback=self.parse_subcate_links)

    def parse_subcate_links(self, response, ):

        sub_cate_lis = response.css('div.taxonomy-page-header ul.nav').css('li a')
        # for i  in range(len(sub_cate_lis)-1):
        for sub_cate_li in sub_cate_lis:
            if re.search('^/', sub_cate_li.attrib['href']):
                sub_cate = sub_cate_li.css('a::text').get().strip()
                sub_cate_link = sub_cate_li.attrib['href']
                # if not sub_cate.lower() in ignore_subcate: ## screen out the subactegor with subscription
                yield response.follow(url=sub_cate_link, callback=self.parse_page_links
                                      )

    def parse_page_links(self, response):
        results = []  # list for saving the crawled items preview
        view_rows = response.css('div.views-row')
        base_url = 'https://www.hartenergy.com/'
        preview_img_link = None
        for view_row in view_rows:
            if view_row.css('div.img-wrap'):
                preview_img_link = response.urljoin(response.css('div.img-wrap img').attrib['src'])
            categories = view_row.css('div.text-wrap h2.he-category a::text').getall()
            rel_title_url = view_row.css('div.text-wrap h3 a').attrib['href']
            title = view_row.css('div.text-wrap h3 a::text').get()
            abstracts = view_row.css('div.text-wrap p::text').get()
            pub_time = view_row.css('div.text-wrap div.field_published_on::text').get()
            title_url = base_url + rel_title_url
            result = self.session.query(HartEnergy) \
                .filter(or_(HartEnergy.url == title_url, HartEnergy.title == title)) \
                .first()
            results.append(result)
            if not result:
                yield response.follow(url=rel_title_url, callback=self.parse,
                                      cb_kwargs={'title': title, 'title_url': title_url,
                                                 'pub_time': pub_time,
                                                 'abstracts': abstracts,
                                                 'categories': categories,
                                                 'preview_img_link': preview_img_link})
        if len([result for result in results if result is None]) == len(results):  ## if all the element is not crawled
            next_page_indicator = response.css('ul.js-pager__items a').attrib.get('rel')
            if next_page_indicator == 'next':
                next_page = response.css('ul.js-pager__items a').attrib['href']
                yield response.follow(url=next_page, callback=self.parse_page_links)

    def parse(self, response, title, title_url, pub_time, abstracts, categories, preview_img_link):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        item = HartEnergyItem()
        item['url'] = response.url
        item['categories'] = str(categories)
        item['preview_img_link'] = preview_img_link
        item['pre_title'] = abstracts
        item['title'] = title
        item['author'] = response.css('div.field_first_name::text').get().strip() + ' ' + \
                         response.css('div.field_last_name::text').get().strip()
        # news_item['sub_title'] = response.css('div.sj-title h6 a::text').get()
        # item['sub_title'] = response.css('div.sj-title h6::text').get()
        # item['dep'] = response.css('div.sj-n a::text').get()
        item['pub_time'] = pub_time
        item['content'] = str(response.css('div.article-content-wrapper').get())
        # news_item['content_other'] = response.css('div.sj-main p::text').getall()
        item['crawl_time'] = datetime.now().strftime('%m/%d/%Y %H:%M')
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        yield item


class OilFieldTechSpider(scrapy.Spider):
    name = 'oilfield_tech'
    # allowed_domains = 'oilfieldtechnology.com'
    start_urls = ['https://www.oilfieldtechnology.com']
    custom_settings = {
        'ITEM_PIPELINES': {'news_oedigital.pipelines.OilFieldTechPipeline': 304},
    }

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        self.engine = db_connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        create_table(self.engine)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_cate_links
            )

    def parse_cate_links(self, response):
        # from scrapy.shell import in
        # elf)
        cate_lis = response.css('ul.list-unstyled')[1].css('li')
        for cate_li in cate_lis:
            cate_url = cate_li.css('a').attrib['href']
            cate_name = cate_li.css('a::text').get()  # main category name
            yield response.follow(url=cate_url,
                                  callback=self.parse_page_links,
                                  cb_kwargs={'category': cate_name}
                                  )
        # print(cate_lis)
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

    def parse_page_links(self, response, category):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        results = []  # list for saving the crawled items preview
        feature_articles = []
        top_articles = []
        tripple_articles = response.css('article.article-list.article')  ##  all the articles include others
        if response.css('article.article-featured.article') is not None:
            feature_articles = response.css('article.article-featured.article')
        if response.css('article.article-top.article'):
            top_articles = response.css('article.article-top.article')
        articles = tripple_articles + feature_articles + top_articles
        preview_img_link = None
        for article in articles:
            if article.css('p.text-center img::attr(data-src)') is not None \
                    and len(article.css('p.text-center img::attr(data-src)')) > 0:
                preview_img_link = article.css('p.text-center img::attr(data-src)')[0].get()
            title = article.css('header a::text').get()
            abstracts = article.css('p::text')[-1].get()
            rel_title_url = article.css('header a::attr(href)').get()
            title_url = 'https://www.oilfieldtechnology.com' + rel_title_url
            result = self.session.query(OilFieldTech) \
                .filter(or_(OilFieldTech.url == title_url, OilFieldTech.title == title)) \
                .first()
            results.append(result)
            if not result:
                yield response.follow(url=rel_title_url,
                                      callback=self.parse,
                                      cb_kwargs={'preview_img_link': preview_img_link,
                                                 'abstracts': abstracts,
                                                 'categories': category,
                                                 'title': title}
                                      )

        if len([result for result in results if result is None]) == len(results):  ## if all the element is not crawled
            if len(response.css('li.previous a::attr(href)')) >= 1:
                next_page = response.css('li.previous a::attr(href)').get()
                yield response.follow(url=next_page,
                                      callback=self.parse_page_links, cb_kwargs={'category': category})
            elif len(response.css('div.pager a[rel="next"]')) >= 1:
                next_page = response.css('div.pager a[rel="next"]').attrib['href']
                yield response.follow(url=next_page,
                                      callback=self.parse_page_links, cb_kwargs={'category': category})

    def parse(self, response, abstracts, categories, preview_img_link, title):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        item = OilFieldTechItem()
        item['url'] = response.url
        item['categories'] = categories.strip()
        item['preview_img_link'] = preview_img_link
        item['pre_title'] = abstracts
        item['title'] = title
        item['pub_time'] = response.css('article.article.article-detail header')[0].css('time::text').get()
        # .datetime.strptime(,'%A-%d-%B-%Y-%H:%M').strftime('%Y-%m-%d %H:%M')
        if response.css('article.article.article-detail header')[0].css('a::attr(rel)'):
            item['author'] = response.css('article.article.article-detail header')[0].css('a::text').get()
        else:
            item['author'] = None
        item['content'] = response.css('div[itemprop="articleBody"]').get()
        item['crawl_time'] = datetime.now().strftime('%m/%d/%Y %H:%M')

        yield item


class OilAndGasSpider(scrapy.Spider):
    name = 'oil_and_gas'
    # allowed_domains = 'oilfieldtechnology.com'
    start_urls = ['https://www.oilandgas360.com']
    custom_settings = {
        'ITEM_PIPELINES': {'news_oedigital.pipelines.OilAndGasPipeline': 305},
    }

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        self.engine = db_connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        create_table(self.engine)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_cate_links
            )

    def parse_cate_links(self, response):
        # from scrapy.shell import in
        # elf)
        eles = response.css('ul#mainmenu li a::attr(href)')[1:-16].getall()
        cate_lis = set(ele for ele in eles if re.match('http', ele))

        for cate_li in cate_lis:
            # cate_url = cate_li.attrib['href']
            # cate_name = cate_li.css('a::text').get()  # main category name
            yield scrapy.Request(url=cate_li, callback=self.parse_page_links
                                 )

    def parse_page_links(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        results = []
        divs = response.css('div#recent-posts div')
        articles = [div for div in divs if (div.attrib.get('id') \
                                            is not None and re.search(r'post-\d', div.attrib.get('id')))]
        for article in articles:
            preview_img_link = article.css('div.post-thumb img').attrib['src'] if articles[0] \
                .css('div.post-thumb').attrib.get('src') else None
            title_url = article.css('div.post-content h2 a').attrib['href'] \
                if article.css('div.post-content h2 a') else None
            # title = article.css('div.post-content h2 a::text').get() \
            #     if article.css('div.post-content h2 a') else None
            # abastracts = article.css('div.post-content div.entry p:last-child').xpath('desendant::text()').getall()
            abstracts = article.css('div.post-content div.entry p:last-child').xpath('descendant::text()').getall()
            abstracts = ' '.join([re.sub(r'\xa0', '', abstract) for abstract in abstracts if abstract])

            result = self.session.query(OilAndGas) \
                .filter(OilAndGas.url == title_url) \
                .first()
            results.append(result)
            if not result:
                yield scrapy.Request(url=title_url, callback=self.parse,
                                     cb_kwargs={'preview_img_link': preview_img_link,
                                                'abstracts': abstracts
                                                }
                                     )

        if len([result for result in results if result is None]) == len(results):  ## if all the element is not crawled
            # if len(response.css('li.previous a::attr(href)')) >= 1:
            next_page = response.css('a.next.page-numbers').attrib['href'] if \
                response.css('a.next.page-numbers').attrib.get('href') is not None else None
            if next_page is not None:
                yield scrapy.Request(url=next_page,
                                     callback=self.parse_page_links)

    def parse(self, response, abstracts, preview_img_link):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        item = OilAndGasItem()
        item['url'] = response.url
        item['categories'] = str(response.css('a[rel="category tag"]::text').getall()) \
            if response.css('a[rel="category tag"]::text') else None
        item['preview_img_link'] = preview_img_link
        item['pre_title'] = abstracts
        item['title'] = response.css('div#content_wrapper h1.title a::text').get()
        item['pub_time'] = response.css('div#share_wrapper').css('span.date_wrap::text').get()
        # .datetime.strptime(,'%A-%d-%B-%Y-%H:%M').strftime('%Y-%m-%d %H:%M')

        item['author'] = None
        item['content'] = response.css('div.entry').get()
        item['crawl_time'] = datetime.now().strftime('%m/%d/%Y %H:%M')

        yield item


class InEnStorageSpider(scrapy.Spider):
    name = 'in_en_storage'
    # allowed_domains = 'oilfieldtechnology.com'
    start_urls = ['https://www.in-en.com/tag/储气库']
    custom_settings = {
        'ITEM_PIPELINES': {'news_oedigital.pipelines.InEnEnergyPipeline': 307},
    }

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        self.engine = db_connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        create_table(self.engine)

    # def __init__(self):
    #     uri = 'mongodb://localhost:27017/petroleum_news'
    #     connection = pymongo.MongoClient(uri
    #     )
    #     self.db = connection["InEnStorage"]
    #     self.collection = self.db["Item"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_page_links
            )

    def parse_page_links(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        results = []
        # preview_img_link = None
        articles = response.css('ul.infoLists  li ')
        # articles= response.css('ul.infoLists  li div.listTxts ') + response.css('ul.infoLists  li div.listTxts_pic ')

        for article in articles:
            preview_img_link = article.css('div.imgBox img').attrib.get('src') if article.css(
                'div.imgBox') is not None else None
            title = article.css('div.listTxts h5 a::text').get() if article.css('div.listTxts') is not None \
                else article.css('div.listTxts_pic h5 a::text').get()
            title_url = article.css('div.listTxts h5 a').attrib.get('href').strip() if len(
                article.css('div.listTxts')) == 1 \
                else article.css('div.listTxts_pic h5 a').attrib.get('href')
            result = self.session.query(InEnStorage) \
                .filter(or_(InEnStorage.url == title_url, InEnStorage.title == title)) \
                .first()
            # result = self.db.getCollection("InEnStorage").findOne({"url" :title_url})
            # results.append(result)
            if not result:
                yield scrapy.Request(url=title_url, callback=self.parse,
                                     cb_kwargs={'preview_img_link': preview_img_link
                                                }
                                     )

        if len([result for result in results if result is None]) == len(results):  ## if all the element is not crawled
            # if len(response.css('li.previous a::attr(href)')) >= 1:
            next_page = response.css('div.pages').css('a')[-1] if response.css('div.pages') else None
            if next_page is not None and next_page.attrib['href'] is not None and re.search('下一页',
                                                                                            next_page.css(
                                                                                                'a::text').get()):
                yield scrapy.Request(url=next_page.attrib['href'],
                                     callback=self.parse_page_links)

    def parse(self, response, preview_img_link):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        item = InEnStorageItem()
        item['url'] = response.url
        item['categories'] = str(
            response.css('div.leftBox.fl').css('div.rightDetail.fr').css('p.keyWords a::text').getall())
        item['preview_img_link'] = preview_img_link
        item['pre_title'] = None  ## fixed for all the spiders
        item['title'] = response.css('div.leftBox.fl').css('h1::text').get()
        if len(response.css('div.leftBox.fl').css('p.source').css('b')) == 2:
            item['pub_time'] = response.css('div.leftBox.fl').css('p.source').css('b::text')[0].get().split('：')[
                -1].strip()
            item['author'] = response.css('div.leftBox.fl').css('p.source').css('b::text')[1].get().split('：')[
                -1].strip()
        # .datetime.strptime(,'%A-%d-%B-%Y-%H:%M').strftime('%Y-%m-%d %H:%M')
        if len(response.css('div.leftBox.fl').css('p.source').css('b')) == 1:
            item['pub_time'] = response.css('div.leftBox.fl').css('p.source').css('b::text')[0].get().split('：')[
                -1].strip()
        # item['author'] = None
        item['content'] = response.css('div#content').get()
        item['crawl_time'] = datetime.now().strftime('%m/%d/%Y %H:%M')

        yield item


class JptLatestSpider(scrapy.Spider):
    name = 'jpt_latest'
    # allowed_domains = 'oilfieldtechnology.com'
    start_urls = ['https://pubs.spe.org/en/jpt/latest-news/']
    custom_settings = {
        'ITEM_PIPELINES': {'news_oedigital.pipelines.JptLatestPipeline': 308},
    }

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        self.engine = db_connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        create_table(self.engine)

    def start_requests(self):

        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_page_links
            )

    def parse_page_links(self, response):
        # preview_img_link = None
        base_url = 'https://pubs.spe.org'
        articles = response.css('article.tile.story')
        for article in articles:
            preview_img_link = 'https://pubs.spe.org' + article.css('div.story-wrap'). \
                css('div.img-wrap').attrib['style'].split('(')[-1].split(')')[0]
            title = article.css('div.story-wrap').css('h3::text').get().strip()
            pub_time = article.css('div.story-wrap').css('span.pub-date::text').get().strip()
            title_url = article.css('a::attr(href)').get()
            pre_title = article.css('div.story-wrap').css('p::text').get().strip()
            result = self.session.query(JptLatest) \
                .filter(or_(JptLatest.url == base_url + title_url, JptLatest.title == title)) \
                .first()
            if not result:
                yield response.follow(url=title_url, callback=self.parse,
                                      cb_kwargs={'preview_img_link': preview_img_link,
                                                 'pub_time': pub_time,
                                                 'title': title,
                                                 'pre_title': pre_title
                                                 }
                                      )

    def parse(self, response, preview_img_link, pub_time, title, pre_title):
        item = JptLatestItem()
        item['url'] = response.url
        item['preview_img_link'] = preview_img_link
        item['pub_time'] = pub_time
        # item['title'] = response.css('div.articleTitleBox h2::text').get()
        item['title'] = title
        item['categories'] = response.css('span.topicItem a::text').get()
        item['content'] = response.css('div.articleBodyText').get()
        item['author'] = None
        item['pre_title'] = pre_title
        item['crawl_time'] = datetime.now().strftime('%m/%d/%Y %H:%M')

        yield item


class EnergyVoiceSpider(scrapy.Spider):
    name = 'energy_voice'
    # allowed_domains = 'oilfieldtechnology.com'
    start_urls = ['https://www.energyvoice.com/category/oilandgas']
    custom_settings = {
        'ITEM_PIPELINES': {'news_oedigital.pipelines.EnergyVoicePipeline': 309},
    }

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        self.engine = db_connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        create_table(self.engine)

    def start_requests(self):

        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_page_links
            )

    def parse_page_links(self, response):
        # preview_img_link = None
        results = []
        articles = response.css('article.post')
        for article in articles:
            preview_img_link = article.css('figure img').attrib.get('src')
            pub_time = article.css('div.timestamp::text').get()
            categoires = article.css('a.category-label::text').get()
            title_url = article.css('h2.title a').attrib.get('href')
            title = article.css('h2.title a::text').get()
            author = article.css('a.byline').attrib.get('title')

            result = self.session.query(EnergyVoice) \
                .filter(or_(EnergyVoice.url == title_url, EnergyVoice.title == title)) \
                .first()
            results.append(result)
            if not result:
                yield response.follow(url=title_url, callback=self.parse,
                                      cb_kwargs={'preview_img_link': preview_img_link,
                                                 'pub_time': pub_time,
                                                 'categories': categoires,
                                                 'title': title,
                                                 'author': author
                                                 }
                                      )
        if len([result for result in results if result is None]) == len(results):
            next_page = response.css('nav.navigation.pagination').css('a.next') \
                #     if response.css('nav.navigation.pagination').css('a.next') else None
            if next_page is not None and next_page.attrib['href'] is not None and \
                    re.search('Next', next_page.css('a::text').get()):
                yield scrapy.Request(url=next_page.attrib.get('href'),
                                     callback=self.parse_page_links)

    def parse(self, response, preview_img_link, pub_time, categories, title, author):
        item = EnergyVoiceItem()
        item['url'] = response.url
        item['preview_img_link'] = preview_img_link
        item['pub_time'] = pub_time
        item['title'] = title
        item['categories'] = categories
        item['content'] = response.css('div.entry-content').get()
        item['author'] = author
        item['pre_title'] = None
        item['crawl_time'] = datetime.now().strftime('%m/%d/%Y %H:%M')

        yield item


class UpStreamSpider(scrapy.Spider):
    name = 'upstream'
    # allowed_domains = 'oilfieldtechnology.com'
    start_urls = ['https://www.upstreamonline.com']
    custom_settings = {
        'ITEM_PIPELINES': {'news_oedigital.pipelines.UpStreamPipeline': 310},
        # 'DOWNLOADER_MIDDLEWARES': {'news_oedigital.middlewares.NewsOedigitalDownloaderMiddleware': 543}
    }

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        self.engine = db_connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        # self.driver = PhantomsJs('')
        create_table(self.engine)

    def start_requests(self):

        for url in self.start_urls:
            yield SeleniumRequest(
                url=url,
                callback=self.parse_page_links,
                script='window.scrollTo(0, document.body.scrollHeight);',
                wait_time=300
            )
            # yield scrapy.Request(url=url,callback=self.parse_page_links())
            # yield SplashRequest(url, self.parse_page_links,
            #                     endpoint='render.json',
            #                     args = {'timeout':600,'images':0,'render_all': 1,'wait':300,'dont_process_response':True})

    def parse_page_links(self, response):
        # pass
        # print(type(response),dir(response))
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)
        base_url = 'https://www.upstreamonline.com'
        articles = response.css('div.card-body')
        for article in articles:
            title_url = article.css('a.card-link').attrib.get('href')
            preview_img_link = article.css('div.img-wrapper').css('img').attrib.get('src')
            title = article.css('h2.teaser-title::text').get().strip() if article.css('h2.teaser-title::text') \
                else None
            # print(preview_img_link)
            result = self.session.query(UpStream) \
                .filter(or_(UpStream.title == title, UpStream.url == base_url + title_url)) \
                .first()
            if not result:
                yield response.follow(url=title_url,
                                      callback=self.parse,
                                      cb_kwargs={'preview_img_link': preview_img_link}
                                      )

    def parse(self, response, preview_img_link):
        item = UpStreamItem()
        item['title'] = response.css('h1.article-title::text').get().strip() if response.css('h1.article-title::text') \
            else None
        item['url'] = response.url
        item['categories'] = response.url.split('com/')[1].split('/')[0]
        item['pre_title'] = response.css('p.article-lead-text::text').get()
        item['author'] = response.css('span.authors a::text').get().strip()
        item['pub_time'] = response.css('span.st-italic::text').get().strip().split('G')[0].strip()
        item['preview_img_link'] = response.css('div.img-wrapper ').extract_first()
        item['content'] = response.css('div.article-body').get()
        item['crawl_time'] = datetime.now().strftime('%m/%d/%Y %H:%M')

        yield item


class OilPriceSpider(scrapy.Spider):
    name = 'oil_price_spider'
    # allowed_domains = 'oilfieldtechnology.com'
    start_urls = ['https://oilprice.com/Latest-Energy-News/World-News/']
    custom_settings = {
        'ITEM_PIPELINES': {'news_oedigital.pipelines.OilPricePipeline': 311},
    }
    lua_script = '''
    function main(splash)
    local num_scrolls = 10
    local scroll_delay = 1.0

    local scroll_to = splash:jsfunc("window.scrollTo")
    local get_body_height = splash:jsfunc(
        "function() {return document.body.scrollHeight;}"
    )
    assert(splash:go(splash.args.url))
    splash:wait(splash.args.wait)

    for _ = 1, num_scrolls do
        scroll_to(0, get_body_height())
        splash:wait(scroll_delay)
    end        
    return splash:html()
    end
    
    '''

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        self.engine = db_connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        create_table(self.engine)

    def start_requests(self):
        for url in self.start_urls:
            # yield SplashRequest(url, self.parse_page_links, endpoint='execute',
            #                 args={'wait':2, 'lua_source': self.lua_script})

            yield scrapy.Request(url=url, callback=self.parse_page_links)

    def parse_page_links(self, response):
        results = []
        articles = response.css('div.categoryArticle')
        for article in articles:
            title = article.css('h2.categoryArticle__title::text').get()
            pub_time = article.css('p.categoryArticle__meta::text').get().split('|')[0].strip().replace('at', '')
            author = article.css('p.categoryArticle__meta::text').get().split('|')[-1]
            pre_title = article.css('p.categoryArticle__excerpt::text').get().strip()
            preview_img_link = article.css('a.categoryArticle__imageHolder img').attrib.get('src')
            title_url = article.css('div.categoryArticle__content a ').attrib.get('href')
            result = self.session.query(OilPrice) \
                .filter(or_(OilPrice.url == title, OilPrice.url == title_url)) \
                .first()

            results.append(result)
            if not result:
                yield scrapy.Request(url=title_url, callback=self.parse,
                                     cb_kwargs={
                                         'title': title,
                                         'pub_time': pub_time,
                                         'author': author,
                                         'pre_title': pre_title,
                                         'preview_img_link': preview_img_link
                                     })
        # time.sleep(7200)  ## give it a long sleep
        # if len([result for result in results if result is None]) == len(results):
        # page_number = int(response.css('div.pagination span.num_pages').get().replace('/')
        next_page = response.css('div.pagination a.next').attrib.get('href')
        #
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse_page_links)

    def parse(self, response, title, pub_time, author, pre_title, preview_img_link):
        item = OilPriceItem()
        item['title'] = title
        item['url'] = response.url
        item['categories'] = None
        item['pre_title'] = pre_title
        item['author'] = author
        item['pub_time'] = pub_time
        item['preview_img_link'] = preview_img_link
        item['content'] = response.css('div.singleArticle__content').get()
        item['crawl_time'] = datetime.now().strftime('%m/%d/%Y %H:%M')

        yield item


class GulfOilGasSpider(scrapy.Spider):
    name = 'gulf_oil_gas'
    # allowed_domains = 'oilfieldtechnology.com'
    start_urls = ['https://www.gulfoilandgas.com/webpro1/main/newshome.asp']
    custom_settings = {
        'ITEM_PIPELINES': {'news_oedigital.pipelines.GulfOilGasPipeline': 312},
    }

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        self.engine = db_connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        create_table(self.engine)

    def start_requests(self):

        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_page_links,

            )
            # yield SplashRequest(url, self.parse_page_links,
            #                     endpoint='render.json',
            #                     args = {'timeout':600,'images':0,'render_all': 1,'wait':300})

    def parse_page_links(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        abs_url = 'https://www.gulfoilandgas.com'
        articles = response.css('div.newsblock')
        for article in articles:
            title_url = article.css('a.newslinkgog').attrib.get('href')
            title = article.css('a.newslinkgog b::text').get()
            pre_title = article.css('td.newssubblock::text').get().strip().replace('\xa0', '')[1:-3]
            # preview_img_link = article.css('div.img-wrapper').css('img').attrib.get('src')
            categories = article.css('span.lblues::text')[0].get().split('>>')[0].strip()
            pub_time = article.css('div.newsblock').css('span.lblues::text')[0].get().split('>>')[1].strip()

            # print(preview_img_link)
            result = self.session.query(GulfOilGas).filter(
                or_(GulfOilGas.url == abs_url + title_url, GulfOilGas.title == title)
            ).first()
            # .filter(or_(GulfOilGas.title == title, GulfOilGas.url == abs_url+title_url)) \
            if not result:
                yield response.follow(url=title_url,
                                      callback=self.parse,
                                      cb_kwargs={'title': title,
                                                 'pre_title': pre_title,
                                                 'categories': categories,
                                                 'pub_time': pub_time}
                                      )

    def parse(self, response, title, pre_title, categories, pub_time):
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)
        item = GulfOilGasItem()
        # pass
        item['title'] = title
        item['url'] = response.url
        item['categories'] = categories
        item['pre_title'] = pre_title
        item['author'] = None
        item['pub_time'] = pub_time
        item['preview_img_link'] = None
        item['content'] = response.css('div.newsbodytext').get()
        item['crawl_time'] = datetime.now().strftime('%m/%d/%Y %H:%M')

        yield item


class EnergyPediaSpider(scrapy.Spider):
    name = 'energy_pedia'
    # allowed_domains = 'oilfieldtechnology.com'
    start_urls = ['https://www.energy-pedia.com/articles.aspx?filter1=1&filter2=0']
    custom_settings = {
        'ITEM_PIPELINES': {'news_oedigital.pipelines.EnergyPediaPipeline': 313},
    }

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        self.engine = db_connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        create_table(self.engine)

    def start_requests(self):

        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_page_links,

            )

    def parse_page_links(self, response):
        response.css('table.listing tr')

        articles = response.css('table.listing tr')
        for article in articles:
            pub_time = article.css('td::text')[0].get()
            preview_img_link = article.css('td')[0].css('img').attrib.get('src')
            title = article.css('td')[1].css('a::text').get()
            pre_title = article.css('td::text')[1].get()
            title_url = article.css('td ')[1].css('a').attrib.get('href')
            result = self.session.query(EnergyPedia).filter(
                or_(EnergyPedia.url == title_url, EnergyPedia.title == title)
            ).first()
            # .filter(or_(GulfOilGas.title == title, GulfOilGas.url == abs_url+title_url)) \
            if not result:
                yield response.follow(url=title_url,
                                      callback=self.parse,
                                      cb_kwargs={'title': title,
                                                 'pre_title': pre_title,
                                                 # 'categories': categories,
                                                 'preview_img_link': preview_img_link,
                                                 'pub_time': pub_time}
                                      )
        # for next_page in response.css('div#pagedrecordset a::text'):

        next_pages = response.css('div#pagedrecordset a::text').getall()
        if 'Next' in next_pages:
            next_page_index = next_pages.index('Next')
            next_page_link = response.css('div#pagedrecordset a')[next_page_index].attrib.get('href')
            yield response.follow(url=next_page_link, callback=self.parse_page_links)

    def parse(self, response, title, pre_title, pub_time, preview_img_link):
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)
        item = EnergyPediaItem()
        item['url'] = response.url
        item['title'] = title
        item['pre_title'] = pre_title
        item['pub_time'] = pub_time
        item['author'] = None
        item['content'] = response.css('div.articlepreview').get()
        item['crawl_time'] = datetime.now().strftime('%m/%d/%Y %H:%M')
        item['preview_img_link'] = preview_img_link
        item['categories'] = None

        yield item


class InenTechSpider(scrapy.Spider):
    name = 'inen_tech'
    # allowed_domains = 'oilfieldtechnology.com'
    start_urls = ['https://oil.in-en.com/technology/']
    custom_settings = {
        'ITEM_PIPELINES': {'news_oedigital.pipelines.InenTechPipeline': 314}
    }

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        self.engine = db_connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        create_table(self.engine)

    def start_requests(self):

        for url in self.start_urls:
            yield scrapy.Request(url=url,
                                 callback=self.parse_cate_links)

    def parse_cate_links(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        cate_links = response.css('a.moreBtn')
        for cate_link in cate_links:
            yield scrapy.Request(url=cate_link.attrib.get('href'),
                                 callback=self.parse_page_links)

    def parse_page_links(self, response):
        results = []
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        articles = response.css('ul.infoList  li ')
        # articles= response.css('ul.infoLists  li div.listTxts ') + response.css('ul.infoLists  li div.listTxts_pic ')

        for article in articles:
            preview_img_link = article.css('div.imgBox img').attrib.get('src') if article.css( \
                'div.imgBox') is not None else None
            title = article.css('div.listTxt h5 a::text').get() if article.css('div.listTxt') is not None \
                else article.css('div.listTxt h5 a::text').get()
            title_url = article.css('div.listTxt h5 a').attrib.get('href').strip()
            result = self.session.query(InenTech) \
                .filter(or_(InenTech.url == title_url, InenTech.title == title)) \
                .first()
            # result = self.db.getCollection("InEnStorage").findOne({"url" :title_url})
            print(title_url)
            results.append(result)
            if not result:
                yield scrapy.Request(url=title_url,
                                     callback=self.parse,
                                     cb_kwargs={'preview_img_link': preview_img_link
                                                }
                                     )

        if len([result for result in results if result is None]) == len(results):  ## if all the element is not crawled
            # if len(response.css('li.previous a::attr(href)')) >= 1:
            next_page = response.css('div.pages').css('a')[-1] if response.css('div.pages') else None
            if next_page is not None and next_page.attrib['href'] is not None and re.search('下一页',
                                                                                            next_page.css(
                                                                                                'a::text').get()):
                yield scrapy.Request(url=next_page.attrib.get('href'),
                                     callback=self.parse_page_links)

    def parse(self, response, preview_img_link):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        item = InenTechItem()
        item['url'] = response.url
        item['categories'] = str(
            response.css('div.leftBox.fl').css('div.rightDetail.fr').css('p.keyWords a::text').getall())
        item['preview_img_link'] = preview_img_link
        item['pre_title'] = None  ## fixed for all the spiders
        item['title'] = response.css('div.leftBox.fl').css('h1::text').get()
        if len(response.css('div.leftBox.fl').css('p.source').css('b')) == 2:
            item['pub_time'] = response.css('div.leftBox.fl').css('p.source').css('b::text')[0].get().split('：')[
                -1].strip()
            item['author'] = response.css('div.leftBox.fl').css('p.source').css('b::text')[1].get().split('：')[
                -1].strip()
        # .datetime.strptime(,'%A-%d-%B-%Y-%H:%M').strftime('%Y-%m-%d %H:%M')
        if len(response.css('div.leftBox.fl').css('p.source').css('b')) == 1:
            item['pub_time'] = response.css('div.leftBox.fl').css('p.source').css('b::text')[0].get().split('：')[
                -1].strip()
        # item['author'] = None
        item['content'] = response.css('div#content').get()
        item['crawl_time'] = datetime.now().strftime('%m/%d/%Y %H:%M')

        yield item


class InenNewEnergySpider(scrapy.Spider):
    name = 'inen_newenergy'
    # allowed_domains = 'oilfieldtechnology.com'
    start_urls = ['https://newenergy.in-en.com/news/intl/']
    custom_settings = {
        'ITEM_PIPELINES': {'news_oedigital.pipelines.InenNewEnergyPipeline': 315}
    }

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        self.engine = db_connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        create_table(self.engine)

    def start_requests(self):

        for url in self.start_urls:
            yield SeleniumRequest(url=url,
                                  callback=self.parse_page_links)

    # def parse_cate_links(self,response):
    #     # from scrapy.shell import inspect_response
    #     # inspect_response(response, self)
    #     cate_link = response.css('a.moreBtn')[0]
    #     yield scrapy.Request(url=cate_link,callback=self.parse_page_links())
    #     # for cate_link in cate_links:
    #     yield scrapy.Request(url=cate_link.attrib.get('href'),
    #                          callback=self.parse_page_links)

    def parse_page_links(self, response):
        results = []
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        articles = response.css('ul.infoList  li')
        # articles= response.css('ul.infoLists  li div.listTxts ') + response.css('ul.infoLists  li div.listTxts_pic ')

        for article in articles:
            preview_img_link = article.css('div.imgBox img').attrib.get('src') if article.css( \
                'div.imgBox') is not None else None
            title = article.css('div.listTxt h5 a::text').get() if article.css('div.listTxt') is not None \
                else article.css('div.listTxt h5 a::text').get()
            title_url = article.css('div.listTxt h5 a').attrib.get('href').strip()
            result = self.session.query(InenNewEnergy) \
                .filter(or_(InenNewEnergy.url == title_url, InenNewEnergy.title == title)) \
                .first()
            # result = self.db.getCollection("InEnStorage").findOne({"url" :title_url})
            # print(title_url)
            results.append(result)
            if not result:
                yield scrapy.Request(url=title_url,
                                     callback=self.parse,
                                     cb_kwargs={'preview_img_link': preview_img_link
                                                }
                                     )

        # if len([result for result in results if result is None]) == len(results):  ## if all the element is not crawled
        # if len(response.css('li.previous a::attr(href)')) >= 1:
        next_page = response.css('div.pages').css('a')[-1] if response.css('div.pages') else None
        if next_page is not None and next_page.attrib['href'] is not None and re.search('下一页',
                                                                                        next_page.css(
                                                                                            'a::text').get()):
            yield scrapy.Request(url=next_page.attrib.get('href'),
                                 callback=self.parse_page_links)

    def parse(self, response, preview_img_link):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        item = InenNewEnergyItem()
        item['url'] = response.url
        item['categories'] = str(
            response.css('div.leftBox.fl').css('div.rightDetail.fr').css('p.keyWords a::text').getall())
        item['preview_img_link'] = preview_img_link
        item['pre_title'] = None  ## fixed for all the spiders
        item['title'] = response.css('div.leftBox.fl').css('h1::text').get()
        if len(response.css('div.leftBox.fl').css('p.source').css('b')) == 2:
            item['pub_time'] = response.css('div.leftBox.fl').css('p.source').css('b::text')[0].get().split('：')[
                -1].strip()
            item['author'] = response.css('div.leftBox.fl').css('p.source').css('b::text')[1].get().split('：')[
                -1].strip()
        # .datetime.strptime(,'%A-%d-%B-%Y-%H:%M').strftime('%Y-%m-%d %H:%M')
        if len(response.css('div.leftBox.fl').css('p.source').css('b')) == 1:
            item['pub_time'] = response.css('div.leftBox.fl').css('p.source').css('b::text')[0].get().split('：')[
                -1].strip()
        # item['author'] = None
        item['content'] = response.css('div#content').get()
        item['crawl_time'] = datetime.now().strftime('%m/%d/%Y %H:%M')

        yield item


class DrillContractorSpider(scrapy.Spider):
    name = 'drill_contractor'
    # allowed_domains = 'oilfieldtechnology.com'
    start_urls = ['https://www.drillingcontractor.org/news']
    custom_settings = {
        'ITEM_PIPELINES': {'news_oedigital.pipelines.DrillContractorPipeline': 316}
    }

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        self.engine = db_connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        create_table(self.engine)

    def start_requests(self):

        for url in self.start_urls:
            yield scrapy.Request(url=url,
                                 callback=self.parse_page_links)

    def parse_page_links(self, response):
        results = []
        articles = response.css('div.post-listing ').css('article.item-list')
        for article in articles:
            title = article.css('h2.post-title a::text').get()
            title_url = article.css('h2.post-title a').attrib.get('href')
            pub_time = article.css('p.post-meta span.tie-date::text ').get()
            preview_img_link = article.css('div.post-thumbnail').css('img').attrib.get('src')
            pre_title = article.css('div.entry p::text').extract_first()
            result = self.session.query(DrillContractor) \
                .filter(or_(DrillContractor.url == title_url, DrillContractor.title == title)) \
                .first()
            # result = self.db.getCollection("InEnStorage").findOne({"url" :title_url})
            # print(title_url)
            results.append(result)
            if not result:
                yield scrapy.Request(url=title_url,
                                     callback=self.parse,
                                     cb_kwargs={'preview_img_link': preview_img_link,
                                                'title': title,
                                                'pub_time': pub_time,
                                                'pre_title': pre_title
                                                }
                                     )

        if len([result for result in results if result is None]) == len(results):
            # print(next_page)
            page_numbers = int(response.css('div.pagination').css('span.pages::text').get().split(' ')[-1])
            for page in range(2, page_numbers + 1):
                next_page = 'https://www.drillingcontractor.org/news/page' + '/' + str(page)
                # if next_page is not None:
                yield scrapy.Request(url=next_page,
                                     callback=self.parse_page_links)

    def parse(self, response, preview_img_link, title, pub_time, pre_title):
        item = DrillContractorItem()

        item['url'] = response.url
        item['author'] = None
        item['title'] = title
        item['preview_img_link'] = preview_img_link
        item['content'] = str(response.css('div.entry p').getall())
        item['pre_title'] = pre_title
        item['pub_time'] = pub_time
        item['categories'] = None
        item['crawl_time'] = datetime.now().strftime('%m/%d/%Y %H:%M')

        yield item


class RogTechSpider(scrapy.Spider):
    name = 'rog_tech'
    # allowed_domains = 'oilfieldtechnology.com'
    start_urls = ['https://rogtecmagazine.com/oil_gas_industry_news/']
    custom_settings = {
        'ITEM_PIPELINES': {'news_oedigital.pipelines.RogTechPipeline': 317}
    }

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        self.engine = db_connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        create_table(self.engine)

    def start_requests(self):

        for url in self.start_urls:
            yield scrapy.Request(url=url,
                                 callback=self.parse_page_links)

    def parse_page_links(self, response):
        articles = response.css('div.vw-column-shortcode.vw-one-half').css('div.block-grid-item')
        for article in articles:
            title = article.css('h5.vw-post-box-post-title a::text').get()
            title_url = article.css('h5.vw-post-box-post-title a').attrib.get('href')
            preview_img_link = article.css('a.vw-post-box-thumbnail').css('img').attrib.get('src')
            pub_time = article.css('div.vw-post-meta-left').css('a::text').get()

            result = self.session.query(RogTech) \
                .filter(or_(RogTech.url == title_url, RogTech.title == title)) \
                .first()
            # result = self.db.getCollection("InEnStorage").findOne({"url" :title_url})
            # print(title_url)
            if not result:
                yield scrapy.Request(url=title_url,
                                     callback=self.parse,
                                     cb_kwargs={'preview_img_link': preview_img_link,
                                                'title': title,
                                                'pub_time': pub_time,
                                                # 'pre_title': pre_title
                                                }
                                     )

    def parse(self, response, title, preview_img_link, pub_time):

        item = RogTechItem()
        item['url'] = response.url
        item['title'] = title
        item['pub_time'] = pub_time
        item['preview_img_link'] = preview_img_link
        item['pre_title'] = response.css('div.vw-featured-image').css('img').attrib.get('src')  ##saving img tag tempor
        item['author'] = None
        item['categories'] = None
        item['content'] = str(response.css('div.entry-content p').getall())
        item['crawl_time'] = datetime.now().strftime('%m/%d/%Y %H:%M')

        yield item


class NaturalGasSpider(scrapy.Spider):
    name = 'natural_gas'
    # allowed_domains = 'oilfieldtechnology.com'
    start_urls = ['https://www.naturalgasintel.com/topics/e&p']
    custom_settings = {
        'ITEM_PIPELINES': {'news_oedigital.pipelines.NaturalGasPipeline': 318}
    }

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        self.engine = db_connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        create_table(self.engine)

    def start_requests(self):

        for url in self.start_urls:
            yield scrapy.Request(url=url,
                                 callback=self.parse_page_links)

    def parse_page_links(self, response):
        articles = response.css('div.py-6')
        for article in articles:
            preview_img_link = article.css('a img').attrib.get('src')
            categories = article.css('p.c-section-category a::text ').get()
            title_url = article.css('h3.h4 a').attrib.get('href')
            title = article.css('h3.h4 a::text').get().strip()
            pub_time = article.css('div.mt-2::text').get()
            pre_title = article.css('div.c-content-body p::text').get()

            result = self.session.query(NaturalGas) \
                .filter(or_(NaturalGas.url == title_url, NaturalGas.title == title)) \
                .first()
            # result = self.db.getCollection("InEnStorage").findOne({"url" :title_url})
            # print(title_url)
            if not result:
                yield scrapy.Request(url=title_url,
                                     callback=self.parse,
                                     cb_kwargs={'preview_img_link': preview_img_link,
                                                'title': title,
                                                'pub_time': pub_time,
                                                'pre_title': pre_title,
                                                'categories': categories
                                                }
                                     )
        next_page = response.css('div.c-pagination').css('a.next').attrib.get('href')
        if next_page:
            yield scrapy.Request(url=next_page,
                                 callback=self.parse_page_links)

    def parse(self, response, preview_img_link, pre_title, title, pub_time, categories):
        # pass

        item = NaturalGasItem()
        item['url'] = response.url
        item['title'] = title
        item['pub_time'] = pub_time
        item['preview_img_link'] = preview_img_link
        item['pre_title'] = pre_title
        item['author'] = response.css('span.c-story-author__name::text').get()
        item['categories'] = categories
        item['content'] = response.css('div.article-body').get()
        item['crawl_time'] = datetime.now().strftime('%m/%d/%Y %H:%M')

        yield item


class RigZoneSpider(scrapy.Spider):
    name = 'rig_zone'
    # allowed_domains = 'oilfieldtechnology.com'
    start_urls = ['https://www.rigzone.com/news/']
    custom_settings = {
        'ITEM_PIPELINES': {'news_oedigital.pipelines.RigZonePipeline': 319}
    }

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        self.engine = db_connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        create_table(self.engine)

    def start_requests(self):

        for url in self.start_urls:
            yield scrapy.Request(url=url,
                                 callback=self.parse_more)

    def parse_more(self, response):

        more_articles = response.css('a.rz-sponsors-all-button')
        for more_article in more_articles:
            yield response.follow(more_article,
                                  callback=self.parse_page_links)

    def parse_page_links(self, response):
        articles = response.css('div.smallHeadline')
        base_url = 'https://www.rigzone.com/news'
        for article in articles:
            title = article.css('a::text').get()
            title_url = article.css('a').attrib.get('href')
            abs_url = base_url + title_url
            pre_title = article.css('div.description::text').get().strip()
            pub_time = article.css('div.articleSource span.date::text').get()
            result = self.session.query(RigZone) \
                .filter(or_(RigZone.url == abs_url, RigZone.title == title)) \
                .first()
            # result = self.db.getCollection("InEnStorage").findOne({"url" :title_url})
            # print(title_url)
            if not result:
                yield response.follow(url=title_url,
                                      callback=self.parse,
                                      cb_kwargs={'title': title,
                                                 'pre_title': pre_title}
                                      )

    def parse(self, response, title, pre_title):
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)
        item = RigZoneItem()
        item['url'] = response.url
        item['title'] = title
        item['pub_time'] = response.css('div.articleDate::text').get()
        item['preview_img_link'] = response.css('div#content').css('div#c_img_wrapper img').get()  # main img link
        item['pre_title'] = pre_title
        item['author'] = response.css('div.articleAuthor a::text').get() \
            if response.css('div.articleAuthor a') else \
            response.css('div.articleAuthor::text').get().replace('\xa0', '').split('by')[-1]
        item['categories'] = None
        item['content'] = response.css('div.divArticleText').get()
        item['crawl_time'] = datetime.now().strftime('%m/%d/%Y %H:%M')

        yield item


class OffshoreTechSpider(scrapy.Spider):
    name = 'offshore_tech'
    # allowed_domains = 'oilfieldtechnology.com'
    start_urls = ['https://www.offshore-technology.com/latest-news']
    custom_settings = {
        'ITEM_PIPELINES': {'news_oedigital.pipelines.OffshoreTechPipeline': 320},
        'COOKIES_DEBUG ':True,
        'COOKIES_ENABLED' :True,
        # 'CookiesMiddleware':{'news_oedigital.middlewares.PersistentCookiesMiddleware':751}
    }

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        self.engine = db_connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        create_table(self.engine)

    def start_requests(self):

        for url in self.start_urls:
            yield SeleniumRequest(url=url,
                                  callback=self.parse_more,
                                  # wait_until=EC.element_to_be_clickable((By.ID, 'ajax-load-more'))
                                  wait_time=10,
                                  wait_until=EC.element_to_be_clickable((By.ID, 'ajax-load-more'))
                                  )


    def parse_more(self, response):

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        articles = response.css('div.grid-x.side-shadow').css('article.c-posts-grid__post')
        for article in articles:
            preview_img_link = article.css('figure img').attrib.get('src') \
                if article.css('figure img') else None
            title = article.css('div.c-post-content h3.c-post-content__title a::text').get()
            title_url = article.css('div.c-post-content h3.c-post-content__title a').attrib.get('href')
            pre_title = article.css('div.c-post-content p.c-post-content__excerpt::text ').get()
            pub_time = article.css('div.c-post-content span.c-post-content__publish-date::text').get()

            result = self.session.query(OffshoreTech) \
                .filter(or_(OffshoreTech == title_url, OffshoreTech.title == title)) \
                .first()
            if not result:
                yield scrapy.Request(url=title_url,
                                      callback=self.parse,
                                      cb_kwargs={'title': title,
                                                 'pre_title': pre_title,
                                                 'pub_time': pub_time,
                                                 'preview_img_link': preview_img_link
                                                 }
                                      )

        # more_articles = response.css('a.rz-sponsors-all-button')
        # driver = response.request.meta['driver']
        # driver.maximize_window()
        # ele = driver.find_element_by_id('ajax-load-more') if driver.find_element_by_id('ajax-load-more') else None
        # while ele:
        #     ele.click()
        #     res = HtmlResponse(url=driver.current_url, body=driver.page_source)
        #     # print('get the response from clickable action')
        #     yield SeleniumRequest(url=res.url,
        #                           callback=self.parse_more,
        #                           wait_time=10,
        #                           wait_until=EC.element_to_be_clickable((By.ID, 'ajax-load-more'))
        #                           )

    def parse(self, response, title, pre_title,preview_img_link,pub_time):
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)
        item = OffshoreTechItem()
        item['url'] = response.url
        item['title'] = title
        item['pub_time'] = pub_time
        item['preview_img_link'] = preview_img_link
        item['pre_title'] = pre_title
        item['author'] = response.css('p.c-post-single__standfirst::text').get()  ## abstract
        item['categories'] = response.css('article.c-post-single figure.c-post-figure img.c-post-figure__image') \
                                .extract_first() ## main image
        item['content'] = response.css('div.c-post-single__content').get() ## main content
        item['crawl_time'] = datetime.now().strftime('%m/%d/%Y %H:%M')

        yield item


class EnergyYearSpider(scrapy.Spider):
    name = 'energy_year'
    # allowed_domains = 'oilfieldtechnology.com'
    start_urls = ['https://theenergyyear.com/news']
    custom_settings = {
        'ITEM_PIPELINES': {'news_oedigital.pipelines.EnergyYearPipeline': 321},
        # 'COOKIES_DEBUG ':True,
        # 'COOKIES_ENABLED' :True,
        # 'CookiesMiddleware':{'news_oedigital.middlewares.PersistentCookiesMiddleware':751}
    }

    def __init__(self):
        """
        Initializes database connection and sessionmaker.
        Creates deals table.
        """
        self.engine = db_connect()
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        create_table(self.engine)

    def start_requests(self):

        for url in self.start_urls:
            yield scrapy.Request(url=url,
                                  callback=self.parse_more,
                                  # wait_until=EC.element_to_be_clickable((By.ID, 'ajax-load-more'))
                                  # wait_time=10,
                                  # wait_until=EC.element_to_be_clickable((By.ID, 'ajax-load-more'))
                                  )

    def parse_more(self, response):

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        articles = response.css('div.row.article-block')
        new_articles = [article for article in articles if not article.css('div.banner-row')]
        # print(len(new_articles))
        for article in new_articles:
            title =article.css('div.article-detail').css('h1 a::text').get()  \
                        if article.css('div.article-detail h1') else \
                            article.css('div.title a::text').get()
            title_url = article.css('div.article-detail').css('h1 a').attrib.get('href') \
                            if article.css('div.article-detail h1') else \
                            article.css('div.title a').attrib.get('href')
            pub_time =article.css('div.article-detail').css('div.news-date::text').getall()[-1]

            pre_title = article.css('div.article-detail').css('p::text').get()
            preview_img_link = article.css('div.img img')[0].attrib.get('data-src')
            result = self.session.query(EnergyYear) \
                .filter(or_(EnergyYear.url == title_url, EnergyYear.title == title)) \
                .first()
            # print(title_url)
            if not result and title_url :
                yield scrapy.Request(url=title_url,
                                     callback=self.parse,
                                     cb_kwargs={'title': title,
                                                'pre_title': pre_title,
                                                'pub_time': pub_time,
                                                'preview_img_link': preview_img_link
                                                }
                                     )

        # more_articles = response.css('a.rz-sponsors-all-button')
        # driver = response.request.meta['driver']
        # driver.maximize_window()
        # ele = driver.find_element_by_id('ajax-load-more') if driver.find_element_by_id('ajax-load-more') else None
        # while ele:
        #     ele.click()
        #     res = HtmlResponse(url=driver.current_url, body=driver.page_source)
        #     # print('get the response from clickable action')
        #     yield SeleniumRequest(url=res.url,
        #                           callback=self.parse_more,
        #                           wait_time=10,
        #                           wait_until=EC.element_to_be_clickable((By.ID, 'ajax-load-more'))
        #                           )

    def parse(self, response, title, pre_title,preview_img_link,pub_time):
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)
        item = EnergyYearItem()
        item['url'] = response.url
        item['title'] = title
        item['pub_time'] = pub_time
        item['preview_img_link'] = preview_img_link  # main img link
        item['pre_title'] = pre_title
        item['author'] = None
        item['categories'] = None
        item['content'] = response.css('div.page-interviews').get()
        item['crawl_time'] = datetime.now().strftime('%m/%d/%Y %H:%M')

        yield item