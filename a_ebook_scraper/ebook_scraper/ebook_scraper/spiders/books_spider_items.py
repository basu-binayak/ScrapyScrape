import scrapy  # Importing the Scrapy framework for web scraping
from ebook_scraper.items import EbookItem # Import the EbookItem from items.py
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

# Define a new spider class that inherits from scrapy.Spider
class BookSpider(scrapy.Spider):
    # The name of the spider, which is used when running the spider via the command line
    name = "books_items"

    # The list of URLs where the spider will start scraping
    start_urls = ["https://books.toscrape.com/"]
    
    # This is the main callback method that will process the response from the start URLs
    def parse(self, response):
        # Print a message to indicate that the response object has been received
        print("[PARSE]")
        
        # #Create an instance of the EbookItem 
        # item = EbookItem()
        
        # each book is inside an article container with class = "product_pod"
        ebooks = response.css('article.product_pod')
        
        # 'ebooks' is assumed to be a list of HTML nodes, each representing an individual ebook.
        for ebook in ebooks:
            
            # Create an ItemLoader instance for each ebook
            loader = ItemLoader(item=EbookItem(), selector=ebook)
            
            # You don’t need to define processors here, just specify the fields
            loader.add_css('title', 'h3>a::attr(title)')
            loader.add_css('rating','p.star-rating::attr(class)')
            loader.add_css('price','div.product_price>p.price_color::text')
            
            # Handling stock_status
            check_stock = ebook.css('p.instock.availability>i::attr(class)').get()
            
            # If the class is not 'icon-ok', set stock_status to "Not In Stock".
            if check_stock!="icon-ok":
                loader.add_value('stock_status', "Not In Stock")
            else:
                # Extract the stock status from the <p> tag with classes 'instock availability'.
                # getall() retrieves all the text content inside this tag, which might be split by line breaks or spaces.
                # ''.join(stock_status) merges the list into a single string, and strip() removes any leading/trailing whitespace.
                stock_status = ebook.css('p.instock.availability::text').getall()
                loader.add_value('stock_status', stock_status)
            
            loader.default_output_processor = TakeFirst()
            
            # Yield the item (instead of a dictionary)
            yield loader.load_item()