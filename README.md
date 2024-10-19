# ScrapyScrape
ScrapyScrape is a repository for web scraping projects using Scrapy, a powerful Python framework. It focuses on building efficient spiders to extract data from various websites, automate crawling processes, and collect structured information for data analysis, research, or application development.


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
