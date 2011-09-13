import lxml.html
from lxml.cssselect import CSSSelector

from scrapy.http import Request
from scrapy.spider import BaseSpider
from scrapy.utils.url import urljoin_rfc, url_query_parameter

from pyconvideos.items import PyconvideosItem

# CSS Selectors
episode_sel = CSSSelector('ul.EpisodeList li.clearfix')
title_sel = CSSSelector('#TheaterLite h2')
link_sel = CSSSelector('div.Description h3 a')
desc_sel = CSSSelector('div.About p')
info_sel  = CSSSelector('ul.MetaDataPairs li h6')

page_sel = CSSSelector('div.Pagination span.CurrentPage')
last_page_sel = CSSSelector('div.Pagination span.LastPage')

class PyconvideosSpider(BaseSpider):
	name = "pycon"
	allowed_domains = ["blip.tv"] 
	start_urls = ["http://blip.tv/pycon-us-videos-2009-2010-2011"]


	def parse(self, response):
		lx = lxml.html.fromstring(response.body_as_unicode())
		episodes = episode_sel(lx)
		for episode in episodes:
			url = link_sel(episode)[0]
			url = urljoin_rfc(self.start_urls[0], url.attrib['href'])
			yield Request(url=url, callback=self.parse_video_page)

		# Simulate pagination
		if episodes:
			current = url_query_parameter(response.url, 'page')
			if not current:
				current = '2' # XHR request starts at page 2
			url = "http://blip.tv/pr/show_get_full_episode_list?"
			url += "users_id=348873&lite=1&esi=1&page=%s"
			url = url % str(int(current)+ 1)
			
			yield Request(url=url, callback=self.parse)
		
	
	def parse_video_page(self, response):
		""" Collect video information """
		lx = lxml.html.fromstring(response.body_as_unicode())
		title = title_sel(lx)[0].text.strip()
		desc = desc_sel(lx)[0].text.strip()
		date, runtime = [info.text for info in info_sel(lx)]
		
		video = PyconvideosItem()
		video['title'] = title
		video['description'] = desc
		video['date'] = date
		video['runtime'] = runtime
		video['url'] = response.url

		return video

