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
        
        # 'ebooks' is assumed to be a list of HTML nodes, each representing an individual ebook.
        for ebook in ebooks:
            
            # Extract the title attribute from the <a> tag that is a direct child of the <h3> tag.
            # ::attr(title) is used to select the 'title' attribute.
            title = ebook.css('h3>a::attr(title)').get()
            
            # Extract the class attribute from the <p> tag with class "star-rating".
            # The class attribute contains both 'star-rating' and the rating itself (e.g., 'Three').
            # Split the class attribute by space and get the second part, which is the actual rating (e.g., 'Three').
            rating = ebook.css('p.star-rating::attr(class)').get().split(' ')[1]
            
            # Extract the text content inside the <p> tag with class "price_color" for the ebook price.
            # This selects the price text (e.g., '£45.17').
            price = ebook.css('div.product_price>p.price_color::text').get()
            
            # Extract the stock status from the <p> tag with classes 'instock availability'.
            # getall() retrieves all the text content inside this tag, which might be split by line breaks or spaces.
            # ''.join(stock_status) merges the list into a single string, and strip() removes any leading/trailing whitespace.
            stock_status = ebook.css('p.instock.availability::text').getall()
            stock_status = ''.join(stock_status).strip()
            
            # Yield a dictionary containing the extracted title, rating, price, and stock status.
            # 'yield' will return this dictionary to the calling function while keeping the state of the loop.
            yield {
                'title': title,           # Title of the ebook
                'rating': rating,         # Star rating of the ebook (e.g., 'Three', 'Four', etc.)
                'price': price,           # Price of the ebook (e.g., '£45.17')
                'stock_status': stock_status  # Stock availability (e.g., 'In stock')
            }

        
        

        
