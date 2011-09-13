# Module for PyCon Video items
from scrapy.item import Item, Field

class PyconvideosItem(Item):
    title = Field()
    description = Field()
    date = Field()
    runtime = Field()
    url = Field()
    pass
