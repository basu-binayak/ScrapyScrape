import scrapy  # Importing the Scrapy framework for web scraping

# Define a new spider class that inherits from scrapy.Spider
class BookSpider(scrapy.Spider):
    # The name of the spider, which is used when running the spider via the command line
    name = "books"

    # The list of URLs where the spider will start scraping
    start_urls = ["https://books.toscrape.com/"]
    
    # This is the main callback method that will process the response from the start URLs
    def parse(self, response):
        # Print a message to indicate that the response object has been received
        print("[OUR RESPONSE]")
        
        

        print(response.css('p.star-rating').get())
        print(response.xpath('//p[contains(@class, "star-rating")]').get())
