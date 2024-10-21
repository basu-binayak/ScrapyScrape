# METHOD - 1
import scrapy
from ebook_scraper.items import EbookItem
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst

class BookSpider(scrapy.Spider):
    name = "books_items"
    
    '''
    When to Use start_requests() Over start_urls:
        More Flexibility: The start_requests() method gives you greater control over how initial requests are generated, allowing you to dynamically construct URLs or add custom headers.
        
        Multiple Parameters: If you need to send POST requests or manipulate the initial requests (e.g., adding headers or parameters), you can do this inside start_requests().
    '''
        
    # This is where we manually define the initial URLs
    def start_requests(self):
        # Start with the first page of the website
        url = "https://books.toscrape.com/catalogue/page-1.html"
            
        # Send an initial request to the first page
        yield scrapy.Request(url=url, callback=self.parse)
    
    # This is the main callback method that will process the response from the start URLs
    def parse(self, response):

        # Each book is inside an article container with class = "product_pod"
        ebooks = response.css('article.product_pod')

        # 'ebooks' is assumed to be a list of HTML nodes, each representing an individual ebook.
        for ebook in ebooks:
            # Create an ItemLoader instance for each ebook
            loader = ItemLoader(item=EbookItem(), selector=ebook)

            # You don’t need to define processors here, just specify the fields
            loader.add_css('title', 'h3>a::attr(title)')
            loader.add_css('rating', 'p.star-rating::attr(class)')
            loader.add_css('price', 'div.product_price>p.price_color::text')

            # Handling stock_status
            check_stock = ebook.css('p.instock.availability>i::attr(class)').get()

            if check_stock != "icon-ok":
                loader.add_value('stock_status', "Not In Stock")
            else:
                stock_status = ebook.css('p.instock.availability::text').getall()
                loader.add_value('stock_status', stock_status)

            loader.default_output_processor = TakeFirst()

            # Yield the item (instead of a dictionary)
            yield loader.load_item()

        # Handle pagination by finding the next page link
        next_url = response.css('li.next a::attr(href)').get()

        if next_url:
            # Construct the full URL and make a new request
            next_page = response.urljoin(next_url)
            yield scrapy.Request(next_page, callback=self.parse)

# # METHOD - 2
# import scrapy
# from ebook_scraper.items import EbookItem
# from scrapy.loader import ItemLoader
# from itemloaders.processors import TakeFirst

# class BookSpider(scrapy.Spider):
#     name = "books_items"

#     # Define the initial page count using __init__
#     def __init__(self, *args, **kwargs):
#         super(BookSpider, self).__init__(*args, **kwargs)
#         self.start_page = 1  # Initial page number
#         self.end_page = 50   # Number of pages to scrape

#     # Use start_requests to send requests for all pages from start_page to end_page
#     def start_requests(self):
#         base_url = "https://books.toscrape.com/catalogue/page-{}.html"
        
#         # Loop through pages 1 to 50 (or however many you want)
#         for page_num in range(self.start_page, self.end_page + 1):
#             # Construct the URL for each page
#             url = base_url.format(page_num)
#             # Yield a request for each page
#             yield scrapy.Request(url=url, callback=self.parse)

#     # This is the main callback method that will process the response from each page
#     def parse(self, response):
#         print("[PARSE]")

#         # Each book is inside an article container with class = "product_pod"
#         ebooks = response.css('article.product_pod')

#         for ebook in ebooks:
#             # Create an ItemLoader instance for each ebook
#             loader = ItemLoader(item=EbookItem(), selector=ebook)

#             # Add fields to the loader
#             loader.add_css('title', 'h3>a::attr(title)')
#             loader.add_css('rating', 'p.star-rating::attr(class)')
#             loader.add_css('price', 'div.product_price>p.price_color::text')

#             # Handling stock_status
#             check_stock = ebook.css('p.instock.availability>i::attr(class)').get()
#             if check_stock != "icon-ok":
#                 loader.add_value('stock_status', "Not In Stock")
#             else:
#                 stock_status = ebook.css('p.instock.availability::text').getall()
#                 loader.add_value('stock_status', stock_status)

#             loader.default_output_processor = TakeFirst()

#             # Yield the item (instead of a dictionary)
#             yield loader.load_item()

