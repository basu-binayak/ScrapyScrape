import scrapy  # Importing the Scrapy framework for web scraping
from ebook_scraper.items import EbookItem # Import the EbookItem from items.py

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
        
        #Create an instance of the EbookItem 
        item = EbookItem()
        
        # each book is inside an article container with class = "product_pod"
        ebooks = response.css('article.product_pod')
        
        # 'ebooks' is assumed to be a list of HTML nodes, each representing an individual ebook.
        for ebook in ebooks:
            
            # Extract the title attribute from the <a> tag that is a direct child of the <h3> tag.
            # ::attr(title) is used to select the 'title' attribute.
            item['title'] = ebook.css('h3>a::attr(title)').get()
            
            # Extract the class attribute from the <p> tag with class "star-rating".
            # The class attribute contains both 'star-rating' and the rating itself (e.g., 'Three') - Use attrib dictionary ( don't need get())
            # Split the class attribute by space and get the second part, which is the actual rating (e.g., 'Three').
            item['rating'] = ebook.css('p.star-rating').attrib['class'].split(' ')[1]
            
            # Extract the text content inside the <p> tag with class "price_color" for the ebook price.
            # This selects the price text (e.g., '£45.17').
            item['price'] = ebook.css('div.product_price>p.price_color::text').get()
            
            # Check the class of the <i> tag within the <p> tag to determine stock availability.
            # The class 'icon-ok' indicates that the item is in stock.
            check_stock = ebook.css('p.instock.availability>i::attr(class)').get()
            
            # If the class is not 'icon-ok', set stock_status to "Not In Stock".
            if check_stock!="icon-ok":
                item['stock_status'] = "Not In Stock"
            else:
                # Extract the stock status from the <p> tag with classes 'instock availability'.
                # getall() retrieves all the text content inside this tag, which might be split by line breaks or spaces.
                # ''.join(stock_status) merges the list into a single string, and strip() removes any leading/trailing whitespace.
                stock_status = ebook.css('p.instock.availability::text').getall()
                item['stock_status'] = ''.join(stock_status).strip()
            
            # Yield the item (instead of a dictionary)
            yield item