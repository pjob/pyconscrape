# Scrapy settings for pyconvideos project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'pyconvideos'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['pyconvideos.spiders']
NEWSPIDER_MODULE = 'pyconvideos.spiders'
DEFAULT_ITEM_CLASS = 'pyconvideos.items.PyconvideosItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

