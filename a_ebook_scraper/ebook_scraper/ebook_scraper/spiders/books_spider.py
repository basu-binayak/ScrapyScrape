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
        
        # each book is inside an article container with class = "product_pod"
        ebooks = response.css('article.product_pod')
        
        # ebooks is a Nodelist and each node is an ebook
        for ebook in ebooks:
            title = ebook.css('h3>a::attr(title)').get()
            rating = ebook.css('p.star-rating::attr(class)').get().split(' ')[1]
            price = ebook.css('div.product_price>p.price_color::text').get()
            stock_status = ebook.css('p.instock.availability::text').getall()
            stock_status = ''.join(stock_status).strip()
            print(stock_status)
        
        

        
