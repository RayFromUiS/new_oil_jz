# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html


# useful for handling different item types with a single interface

from __future__ import absolute_import
from itemadapter import is_item, ItemAdapter
from scrapy import signals
import os
import os.path
import logging
import pickle
import scrapy
from scrapy.exceptions import IgnoreRequest
from scrapy.http.cookies import CookieJar

from scrapy.downloadermiddlewares.cookies import CookiesMiddleware
from scrapy.http import HtmlResponse
from news_oedigital import settings
import re



class NewsOedigitalSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.

        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class NewsOedigitalDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        # spider.driver.get(request.url)


        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        if response.status == 404 or response==403:
            raise IgnoreRequest('skip the request',response.url)
        if re.search('Click here to subscribe to Petroleum News',response.css('a::text').get()):
            raise IgnoreRequest
        # if response.css('div.article-fade'):
        #     formdata = {
        #         "ctl00$ctl00$ctl00$ctl00$ContentPlaceHolderDefault$mainContent$mainContent$txtEmail":
        #             "dongdong2_18@163.com",
        #         "ctl00$ctl00$ctl00$ctl00$ContentPlaceHolderDefault$mainContent$mainContent$txtPassword": \
        #             "woai5laopo"
        #     }
        #     log_in_url = response.css('div.article-fade').css('a')[0].attrib.get('href')
        #     log_in_url = response.urljoin(log_in_url)
        #     return scrapy.FormRequest.from_response(url=log_in_url,
        #                                             formdata=formdata,
        #                                             method='POST',
        #                                             )
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        # return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain

        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class PersistentCookiesMiddleware(CookiesMiddleware):
    def __init__(self, debug=False):
        super(PersistentCookiesMiddleware, self).__init__(debug)
        self.load()

    def process_response(self, request, response, spider):
        # TODO: optimize so that we don't do it on every response
        res = super(PersistentCookiesMiddleware, self).process_response(request, response, spider)
        self.save()
        return res

    def getPersistenceFile(self):
        return settings.COOKIES_STORAGE_FILE

    def save(self):
        logging.debug("Saving cookies to disk for reuse")
        with open(self.getPersistenceFile(), "wb") as f:
            pickle.dump(self.jars, f)
            f.flush()

    def load(self):
        filename = self.getPersistenceFile()
        logging.debug("Trying to load cookies from file '{0}'".format(filename))
        if not os.path.exists(filename):
            logging.info("File '{0}' for cookie reload doesn't exist".format(filename))
            return
        if not os.path.isfile(filename):
            raise Exception("File '{0}' is not a regular file".format(filename))

        with open(filename, "rb") as f:
            self.jars = pickle.load(f)