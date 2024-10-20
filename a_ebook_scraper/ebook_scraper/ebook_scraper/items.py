# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# from scrapy import Item, Field


# class EbookItem(Item):
#     title = Field()         # To store the book title
#     rating = Field()        # To store the rating (e.g., 'Three', 'Four')
#     price = Field()         # To store the price of the ebook
#     stock_status = Field()  # To store the stock availability

# items.py
import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join

# Define the Item class and associate processors for each field
class EbookItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(lambda x: x.strip()),  # Strip leading/trailing whitespace
        # output_processor = TakeFirst()
    )
    rating = scrapy.Field(
        input_processor=MapCompose(lambda x: x.split(' ')[1]),  # Extract rating from class attribute
        # output_processor = TakeFirst()
    )
    price = scrapy.Field(
        input_processor=MapCompose(lambda x: x.replace('£', '').strip(),
                                   lambda x: float(x)),  # Remove currency symbol and strip
        # output_processor = TakeFirst()
    )
    stock_status = scrapy.Field(
        input_processor = MapCompose(lambda x: ''.join(x).strip()),
        # output_processor = TakeFirst()
    )