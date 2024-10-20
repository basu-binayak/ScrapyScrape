# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class EbookItem(Item):
    title = Field()         # To store the book title
    rating = Field()        # To store the rating (e.g., 'Three', 'Four')
    price = Field()         # To store the price of the ebook
    stock_status = Field()  # To store the stock availability
