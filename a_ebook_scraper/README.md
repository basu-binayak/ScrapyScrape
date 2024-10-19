
# How to Start the `ebook_scraper` Scrapy Project

## 1. Activate Your Virtual Environment
Make sure your virtual environment (Conda or venv) is activated.

- If using Conda:
  ```bash
  conda activate ./venv
  ```

- If using a standard virtual environment:
  ```bash
  source venv/bin/activate  # macOS/Linux
  .\venv\Scripts\activate   # Windows
  ```

## 2. Start a New Scrapy Project
Create the `ebook_scraper` Scrapy project by running the following command:

```bash
scrapy startproject ebook_scraper
```

This command will generate the necessary folder structure and initial files for your project.

## 3. Navigate to Your Project Directory
Once the project is created, navigate into the `ebook_scraper` directory:

```bash
cd ebook_scraper
```

## 4. Project Structure
The project will have the following structure:
```
ebook_scraper/
    scrapy.cfg
    ebook_scraper/
        __init__.py
        items.py
        middlewares.py
        pipelines.py
        settings.py
        spiders/
            __init__.py
```

- **`spiders/`**: This folder is where you will define your spider(s).
- **`items.py`**: Here, you define the data structure (fields) to store the scraped data.
- **`middlewares.py`** and **`pipelines.py`**: For middleware and pipelines to process scraped data.
- **`settings.py`**: Contains project-wide settings, including user agents and download delays.

## 5. Create Your Spider to Scrape Books
Now you can create a spider to scrape data from `https://books.toscrape.com/`. Inside the `spiders/` folder, create a file called `books_spider.py`:

### Example Spider for Scraping Book Titles and Prices

```python
import scrapy

class BooksSpider(scrapy.Spider):
    name = 'books'
    start_urls = ['https://books.toscrape.com/']

    def parse(self, response):
        for book in response.css('article.product_pod'):
            title = book.css('h3 a::attr(title)').get()
            price = book.css('div.product_price p.price_color::text').get()
            yield {
                'title': title,
                'price': price
            }

        # Follow pagination links
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)
```

### Explanation:
- This spider starts on the main page of the site and extracts the **book titles** and **prices** using CSS selectors.
- It also follows pagination links to scrape all pages of books.

## 6. Run Your Spider
To run the `books` spider and start scraping data from the site, use the following command inside your project folder:

```bash
scrapy crawl books
```

This will run the spider and display the scraped book titles and prices in your terminal.

# Step-by-Step building of Scraper 

## STEP 1: A FIRST LOOK at the RESPONSE 
```python
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

        # Print the full response object, which contains all the HTML, headers, etc., from the requested page
        print(response)
```
### Detailed Breakdown:
- `import scrapy`: 

This imports the scrapy module, which provides the framework's core components for web scraping.

- `class BookSpider(scrapy.Spider):`:

Defines a new class BookSpider that inherits from scrapy.Spider. Every Scrapy spider must inherit from this base class.
name = "books":

This sets the name of the spider as "books". The name is important because it is how you will refer to and run this spider from the command line using scrapy crawl books.

- `start_urls = ["https://books.toscrape.com/"]`:

This defines the URL(s) where the spider will begin its scraping. In this case, it will start from the homepage of the Books to Scrape website.

- `def parse(self, response):`:

This is the method that handles the HTTP response returned from the start_urls. Every time a page is downloaded (i.e., every URL requested by the spider), Scrapy calls this method to process the response.

`print("[OUR RESPONSE]")`:

This prints the message "[OUR RESPONSE]" to the console as a simple indicator that the response has been received.

`print(response)`:

This prints the entire response object, which contains the HTML of the page that has been fetched. You can inspect this to see the content and use it for further data extraction.

## Scrapy Log Analysis for `BookSpider`

### Overview:
The <a href="">log</a> is from a Scrapy run of the `BookSpider` spider, which attempts to crawl `https://books.toscrape.com/`. Below is a step-by-step analysis of the log events:

### 1. Scrapy Start and Initialization
- **12:20:05 [scrapy.utils.log] INFO: Scrapy 2.11.2 started (bot: ebook_scraper)**:
  - Scrapy version 2.11.2 is successfully initialized, and the bot name is `ebook_scraper`.
  
- **12:20:05 [scrapy.utils.log] INFO: Versions: lxml 5.3.0.0, libxml2 2.11.7**:
  - Displays the versions of key libraries like `lxml`, `libxml2`, `cssselect`, and others that Scrapy uses for parsing HTML and handling network requests.

- **12:20:06 [scrapy.middleware] INFO: Enabled extensions**:
  - Several Scrapy extensions are enabled, such as `CoreStats`, `TelnetConsole`, and `LogStats`.

### 2. Spider Opened
- **12:20:06 [scrapy.core.engine] INFO: Spider opened**:
  - This confirms that the spider has been successfully opened and the crawling process is about to begin.

### 3. Requesting the robots.txt File
- **12:20:10 [scrapy.core.engine] DEBUG: Crawled (404) <GET https://books.toscrape.com/robots.txt>**:
  - The spider made a request to `https://books.toscrape.com/robots.txt` to check if any scraping rules exist. However, it received a `404 Not Found` status, meaning no `robots.txt` file is present, so no restrictions on scraping are imposed.

### 4. Requesting the Main Page
- **12:20:12 [scrapy.core.engine] DEBUG: Crawled (200) <GET https://books.toscrape.com/>**:
  - The spider successfully made a `GET` request to the main page of the site (`https://books.toscrape.com/`) and received a `200 OK` response. This indicates that the page was fetched successfully.

- **[OUR RESPONSE] <200 https://books.toscrape.com/>**:
  - This is the custom message printed by the `parse()` method in the spider. The `response` object for the main page was printed, showing that the page was loaded successfully.

### 5. Spider Closure
- **12:20:12 [scrapy.core.engine] INFO: Closing spider (finished)**:
  - The spider has finished its job and is closing down.

### 6. Scrapy Stats:
- **downloader/request_count: 2**:
  - A total of 2 requests were made (one for `robots.txt` and one for the main page).

- **downloader/response_status_count/200: 1**:
  - Out of the two requests, one resulted in a successful `200 OK` response (for the main page).

- **downloader/response_status_count/404: 1**:
  - One request (for `robots.txt`) resulted in a `404 Not Found` status.

- **elapsed_time_seconds: 5.155414**:
  - The entire spider run took about 5.15 seconds to complete.

### Conclusion:
The spider was able to successfully fetch the main page of `https://books.toscrape.com/`. The request to `robots.txt` returned a `404` error, which is not an issue, and the main page was crawled without any errors. The spider then finished its execution, and no items were scraped because the `parse()` method hasn't yet been set up to extract specific data from the page.

