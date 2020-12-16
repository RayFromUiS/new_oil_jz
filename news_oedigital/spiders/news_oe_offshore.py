import os
import re
import scrapy
from datetime import datetime
from news_oedigital.items import NewsOedigitalItem,WorldOilItem,CnpcNewsItem
from news_oedigital.model import OeNews, db_connect, create_table,WorldOil,CnpcNews
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class NewsOeOffshoreSpider(scrapy.Spider):
    name = 'news_oe_offshore'
    allowed_domains = ['oedigital.com']
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
            yield scrapy.Request(url=url, callback=self.parse_cate_links)

    def parse_cate_links(self,response):
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
                href = sub_cate.attrib['href'] ##relative url of category
                # print(href)
                yield response.follow(url=href,callback=self.parse_page_links)

    def parse_page_links(self,response):
        '''
        parse page links
        :param response:
        :return:
        '''
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)
        results = [] ##storage for the checking of items of database
        preview_img_link = None
        pre_title = None

        #iterate all the element content and if this page is touched,then skip following the next page
        for item_content in response.css('a.snippet'):
            if item_content.css('img') is not None:
                preview_img_link = item_content.css('img::attr(src)').get()
            if item_content.css('h2') is not None:
                pre_title = item_content.css('h2::text').get()
            item_href = 'https://www.oedigital.com'+item_content.attrib['href']
            result = self.session.query(OeNews)\
                .filter(and_(OeNews.url == item_href,OeNews.pre_title==pre_title))\
                .first()
            results.append(result)
            if not result:  ##item not existed inside the database,then scraped
                yield response.follow(
                    url=item_content.attrib['href'],
                    callback=self.parse,
                    cb_kwargs={'preview_img_link': preview_img_link,'pre_title':pre_title}
                )
        # test if the page has been touched or not
        if len([result for result in results if result is None])==len(results): ## if all the element is not crawled
            next_page = response.css('a[title="Next"]::attr(href)')[0]
            if next_page is not None:
                    yield response.follow(url=next_page,callback=self.parse_page_links)

        # page_links.append(sub_url)

    def parse(self, response,preview_img_link,pre_title):
        # from scrapy.shell import inspect_response
        item = NewsOedigitalItem()
        item['url'] = response.url
        item['preview_img_link'] = preview_img_link
        item['pre_title'] = pre_title
        item['title'] = response.css('div.article h1::text').get().strip()
        if len(response.css('p.meta span'))==2:
            item['author'] = response.css('p.meta span::text')[0].get()
            item['pub_time'] = response.css('p.meta span::text')[1].get()
        elif len(response.css('p.meta span'))== 1:
            item['author'] = None
            item['pub_time'] = response.css('p.meta span::text').get()
        else:
            item['author'] = None
            item['pub_time'] = None
        item['categories'] = str(response.css('div.categories a::text').getall())
        item['crawl_time'] = datetime.now().strftime('%m/%d/%Y %H:%M')
        # item['categories'] = response.css('div.categories a::text').getall()
        item['content'] = str(response.css('div.article').get())
        # item['processed_marker'] = None


        yield item


class WorldOilSpider(scrapy.Spider):
    name='world_oil_spider'
    allowed_domains = ['worldoil.com']
    start_urls = ['http://www.worldoil.com/topics/offshore']
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

    def parse_cate_links(self,response):
            # category_names = response.css('ul.topic-list a::text').getall()
        category_hrefs = response.css('ul.topic-list li')
        for category_href in category_hrefs:
            cate_href = category_href.css('a').attrib['href']
            cate = category_href.css('a::text').get()
            yield response.follow(url=cate_href,callback=self.parse_page_links,cb_kwargs={'categories':cate})

    def parse_page_links(self,response,categories):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        results = []
        preview_img_link =None
        articles = response.css('div.article')
        for article in articles:
            title = article.css('h2 a::text').get()
            title_url = article.css('a').attrib['href']
            pub_time = article.css('div.source a::text').get().strip().split(' ')[-1]
            abstract = article.css('p::text').get()
            item_href = 'https://www.worldoil.com'+title_url
            result = self.session.query(WorldOil)\
                .filter(and_(WorldOil.url == item_href,WorldOil.title==title))\
                .first()
            results.append(result)
            if not result:
                yield response.follow(url=title_url, callback=self.parse,
                                      cb_kwargs={'title': title, 'title_url': title_url,
                                                 'pub_time': pub_time,
                                                 'abstract': abstract,
                                                 'category':categories,
                                                 'preview_img_link':preview_img_link})
        # if preview_img_link is not None:
        # if len([result for result in results if result is None]) == len(results):  ## if all the element is not crawled
        #skip the preview image links,since it's not been found generally
        if response.css('a#ContentPlaceHolderDefault_mainContent_btnNext') :
            next_page = response.css('a#ContentPlaceHolderDefault_mainContent_btnNext').attrib['href']
            yield response.follow(url=next_page,callback=self.parse_page_links,cb_kwargs={'categories':categories})

    def parse(self,response,title,pub_time,abstract,category,preview_img_link):
        # from scrapy.shell import inspect_response
        # inspect_response(response,self)
        item =WorldOilItem()

        item['url'] = response.url
        item['preview_img_link'] = preview_img_link
        item['pre_title'] = abstract
        item['title'] = title
        if len(response.css('div.author span')) == 2:
            item['author'] = response.css('div.author span::text')[0].get()
            item['pub_time'] = response.css('div.author span::text')[1].get()
        elif len(response.css('p.meta span')) == 1:
            item['author'] = None
            item['pub_time'] = response.css('div.author span::text')[0].get()
        else:
            item['author'] = None
            item['pub_time'] = None
        item['categories'] = str(category)
        item['crawl_time'] = datetime.now().strftime('%m/%d/%Y %H:%M')
        # item['categories'] = response.css('div.categories a::text').getall()
        # item['content'] = str(response.css('div#news p').getall()
        item['content'] = str(response.css('div#news').get())
        yield item

class CnpcNewsSpider(scrapy.Spider):
    name = 'cnpc_news'
    allowed_domains = ['news.cnpc.com.cn']
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
            li_links = sub_div.css(sub_ele) ## all the selector of sub div
            for li_link in li_links:
                # sub_cate = li_link.css('a::text').get()
                sub_cate_link = li_link.css('a::attr(href)').get()
                if re.match(r'\/', sub_cate_link):
                    yield SeleniumRequest(  ## to return a response with driver object
                        url=sub_cate_link,
                        callback=self.parse_page_links()
                    )

    ## grap all the url of each sub category
    def parse_page_links(self, response,sub_category):
        next_id = 'downpage'
        from scrapy.shell import inspect_response
        inspect_response(response, self)
        results = []
        articles = response.css('li.ejli a')
        for article in articles:
            title = article.css('a::text').get()
            title_url = article.css('a').attrib['href']
            result = self.session.query(CnpcNews) \
                .filter(and_(CnpcNews.url == title_url, CnpcNews.title == title)) \
                .first()
            results.append(result)
            if not result:
                yield scrapy.Request(url=title_url,callback=self.parse)

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
        from scrapy.shell import inspect_response
        inspect_response(response, self)
        item = CnpcNewsItem()
        item['url'] = response.url
        item['cate'] = response.css('div.sj-nav span.as06 a::text')[-1].get()
        item['pre_title'] = response.css('div.sj-title h4::text').get()
        item['title'] = response.css('div.sj-title h2 a::text').get()
        # news_item['sub_title'] = response.css('div.sj-title h6 a::text').get()
        item['sub_title'] = response.css('div.sj-title h6::text').get()
        item['dep'] = response.css('div.sj-n a::text').get()
        item['pub_time'] = '-'.join(response.url.split('/')[-4:-1])
        item['content'] = response.css('div.sj-main').getall()
        # news_item['content_other'] = response.css('div.sj-main p::text').getall()
        item['crawl_time'] = datetime.now().strftime('%m/%d/%Y %H:%M')
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        yield item


# class HartEnergySpider(scrapy.Spider):
#     name = 'hart_energy'
#     allowed_domains = ['hartenergy.com']
#     start_urls = ['http://www.hartenergy.com/']
#
#     def __init__(self):
#         """
#         Initializes database connection and sessionmaker.
#         Creates deals table.
#         """
#         self.engine = db_connect()
#         Session = sessionmaker(bind=self.engine)
#         self.session = Session()
#         create_table(self.engine)
#
#     def start_requests(self):
#         for url in self.start_urls:
#             yield scrapy.Request(url=url, callback=self.parse_cate_links)
#
#     def parse_cate_links(self,response):
#
#         cate_lis = response.css('li.nav-item')[:9] ## only extract 9 of category
#         for cate_li in cate_lis:
#             cate_url = cate_li.css('a').attrib['href']
#             cate_name =cate_li.css('a::text').get()  # main category name
#             yield response.follow(url=cate_url,callback=self.parse_subcate_links,cb_kwargs={'cate':cate_name})
#
#     def parse_subcate_links(self,response):
#
#         ignore_subcate = ['unconventional']
#             # category_names = response.css('ul.topic-list a::text').getall()
#         sub_cate_lis= response.css('div.taxonomy-page-header ul.nav').css('li a')
#         # for i  in range(len(sub_cate_lis)-1):
#         for sub_cate_li in sub_cate_lis:
#             if re.search('^/',sub_cate_li.attrib['href']):
#                 sub_cate = sub_cate_li.css('a::text').get().strip()
#                 sub_cate_link = sub_cate_li.attrib['href']
#                 if not sub_cate.lower() in ignore_subcate: ## screen out the subactegor with subscription
#
#





