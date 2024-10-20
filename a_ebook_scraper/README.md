
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

 # Understand the RESPONSE when you run your Spider

 ## Spider for Scraping
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
The <a href="https://github.com/basu-binayak/ScrapyScrape/blob/38cc2688d5f06f3c513791682895e08d7c738d45/a_ebook_scraper/Logs/log_1.txt">log</a> is from a Scrapy run of the `BookSpider` spider, which attempts to crawl `https://books.toscrape.com/`. Below is a step-by-step analysis of the log events:

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

# Save scraped data(say as json)
To save the scraped data as JSON in Scrapy, you can use the `-o` option when running your Scrapy spider from the command line. Here’s how to do it:

### Command to Run Your Spider
Assuming your spider is named `your_spider_name`, you can execute the following command in your terminal:

```bash
scrapy crawl your_spider_name -o output.json
```

### Breakdown of the Command
- `scrapy crawl your_spider_name`: This part runs your Scrapy spider, where `your_spider_name` is the name you assigned to your spider class.
- `-o output.json`: This option tells Scrapy to output the scraped data to a file named `output.json`. Scrapy automatically determines the format based on the file extension you provide (in this case, JSON).

### Example
If your spider is defined in a file named `spider.py`, and the spider class is named `EbookSpider`, you would run:

```bash
scrapy crawl EbookSpider -o ebooks.json
```

### Result
After running this command, Scrapy will execute the spider and save the scraped data into a file named `ebooks.json` in the same directory from which you ran the command. The JSON file will contain the data structured according to the items yielded in your spider.

### Additional Options
- **Format**: You can specify other formats (e.g., CSV, XML) by changing the file extension. For example, `-o output.csv` would save the data in CSV format.
- **Overwrite**: If `output.json` already exists, it will be overwritten. If you want to append the new data instead, you can use the `-a` option along with the file name (e.g., `-o output.json -a`). 

# NOTES on some TOPICS ( to understand code better)!
# A NOTE on ::text and .get()/.getall()

In Scrapy, `::text` and `.get()` serve different purposes, and they are often used together but in different contexts. Here's when to use each:

### 1. **`::text` Selector**
The `::text` selector is used to extract the **text content** inside an HTML element. You use this to get the plain text between the opening and closing tags of an element. For example:

- Use `::text` when you want the actual visible content (text) inside an HTML element.

```python
response.css('a::text')
```

If you have the following HTML:

```html
<a href="book1.html" title="Book Title 1">Book 1</a>
```

The `::text` selector will return `"Book 1"` because it's the text inside the `<a>` tag.

### 2. **`.get()` Method**
`.get()` is a **method** that returns the first match of the selector. It is used when you want to **retrieve** the first result of your selection, whether you're working with attributes or text. For example:

- Use `.get()` when you want to extract a **single** result from the selector, like a text or an attribute value (e.g., `href`, `title`).

```python
response.css('a::attr(href)').get()
```

This will extract the `href` attribute of the first `<a>` tag.

### Common Scenarios

- **Getting text content (use `::text` + `.get()`):**
  
  To get the text inside a tag, use `::text` and then `.get()`:

  ```python
  response.css('a::text').get()  # Retrieves "Book 1"
  ```

- **Getting attribute value (use `::attr(attrname)` + `.get()`):**

  To get the value of an attribute (like `href`, `title`), use `::attr(attribute)` and then `.get()`:

  ```python
  response.css('a::attr(href)').get()  # Retrieves "book1.html"
  ```

### Comparison

| Purpose                       | Selector Syntax                     | Example Usage                     | Expected Result                  |
|-------------------------------|-------------------------------------|-----------------------------------|----------------------------------|
| Extract text content inside tag | `::text`                            | `response.css('a::text').get()`   | Extracts inner text (e.g., "Book 1") |
| Extract attribute value        | `::attr(attribute)`                 | `response.css('a::attr(href)').get()` | Extracts attribute value (e.g., "book1.html") |
| Get the first matched element   | `.get()`                            | `response.css('a::attr(href)').get()` | Returns the first matched result |

### When to Use `.getall()`
If you want to extract **multiple matches**, use `.getall()` instead of `.get()`:

```python
response.css('a::text').getall()  # Retrieves a list of all <a> text content
```

In summary:
- Use `::text` when you want to target the text inside an element.
- Use `::attr(attribute)` to extract specific attributes like `href`, `title`, etc.
- Use `.get()` to get the first result, and `.getall()` to get all results.

# Difference between ::attr(attribute_name) and tag[attribute_name]

### 1. **Using `::attr(title)`**
```python
title = ebook.css('h3>a::attr(title)').get()
```
- **Explanation**: This expression selects the `<a>` tag that is a direct child of the `<h3>` tag and retrieves the value of its `title` attribute. 
- **Output**: It will give you the value of the `title` attribute (e.g., "It's Only the Himalayas").

### 2. **Using Attribute Selector `a[title]`**
```python
title = ebook.css('h3>a[title]').get()
```
- **Explanation**: This expression selects the `<a>` tag that is a direct child of the `<h3>` tag, but it specifically checks if the `<a>` tag has a `title` attribute. 
- **Output**: It returns the entire `<a>` element if it exists and has a `title` attribute, not the value of the `title` attribute itself.

### Key Differences
- **Returned Value**:
  - `::attr(title)` returns the value of the `title` attribute.
  - `a[title]` returns the entire `<a>` element (as a NodeList or a Selector), not just the attribute value.
  
- **Use Case**:
  - Use `::attr(title)` when you want the specific value of the `title` attribute.
  - Use `a[title]` when you want to check for the existence of the `title` attribute or if you want to manipulate or further inspect the `<a>` element itself.

### Example
Given the following HTML:
```html
<h3>
    <a href="catalogue/its-only-the-himalayas_981/index.html" title="It's Only the Himalayas">It's Only the Himalayas</a>
</h3>
```
- The first expression will result in: `"It's Only the Himalayas"`.
- The second expression will result in: `<a href="catalogue/its-only-the-himalayas_981/index.html" title="It's Only the Himalayas">It's Only the Himalayas</a>`, which is the entire `<a>` element. 

### Conclusion
In summary, if your goal is to get the value of the `title` attribute, you should use the first expression with `::attr(title)`. If you need the `<a>` element itself, then you can use the second expression with `a[title]`.

# Difference between // and ./ in XPath

In XPath, `//` and `./` are used to navigate through an XML or HTML document, but they serve different purposes. Here's a breakdown of their differences:

### `//`
- **Definition**: The `//` selector is used to select nodes in the document from the current node that match the selection, regardless of their location in the hierarchy.
- **Usage**: It can be used to select nodes at any level of the tree structure.
- **Example**: 
    - `//div` selects all `<div>` elements in the document, regardless of their depth or parent elements.
    - `//a/@href` selects the `href` attributes of all `<a>` elements anywhere in the document.

### `./`
- **Definition**: The `./` selector is used to select nodes relative to the current node. It explicitly indicates that the selection should start from the current context node.
- **Usage**: It's generally used to specify that you want to look for child nodes or attributes directly under the current node.
- **Example**:
    - `./div` selects only the `<div>` elements that are direct children of the current node.
    - `./a/@href` selects the `href` attributes of `<a>` elements that are direct children of the current context node.

### Key Differences
- **Context**: `//` searches through the entire document tree, while `./` limits the search to the current context.
- **Scope**: `//` can traverse multiple levels up and down the tree, while `./` restricts itself to the immediate children or attributes of the current node.
- **Performance**: Using `//` may be less efficient than `./` when you want to limit the search to a specific subtree, as `//` checks all levels.

### Example Illustrating the Difference
Consider the following HTML structure:

```html
<div>
    <span>
        <a href="link1.html">Link 1</a>
    </span>
    <span>
        <a href="link2.html">Link 2</a>
    </span>
</div>
```

- `//a` will select both `<a>` elements in the document.
- `./a` (when executed in the context of a `<span>` element) will only select the `<a>` element that is a direct child of that specific `<span>`. If used in the context of the `<div>`, it won't return any results because there are no `<a>` elements that are direct children of the `<div>`.

### Summary
- Use `//` to search for nodes anywhere in the document.
- Use `./` to search for nodes that are directly related to the current context node.

# Items in Scrapy
In Scrapy, **Items** are used to ***define the structure of the data you want to scrape.*** Items provide a container for storing the scraped data in a structured way. You can think of ***Scrapy Items as lightweight data structures similar to Python dictionaries, but they provide additional benefits like validation and type checking***.

### Steps to Use Items in Scrapy:

1. **Define the Item**
2. **Use the Item in the Spider**
3. **Yield the Item in the Spider**

### 1. **Define the Item**

In your Scrapy project, create or modify the `items.py` file. This is where you'll define the data structure for the items you want to scrape.

Here’s an example for the books:

```python
# items.py
import scrapy

class EbookItem(scrapy.Item):
    title = scrapy.Field()         # To store the book title
    rating = scrapy.Field()        # To store the rating (e.g., 'Three', 'Four')
    price = scrapy.Field()         # To store the price of the ebook
    stock_status = scrapy.Field()  # To store the stock availability
```

### 2. **Use the Item in the Spider**

Now, in your spider, you can import the `EbookItem` class and use it to store the scraped data. You will populate the item with the extracted data and yield the item instead of a dictionary.

Here’s how you modify the spider:

```python
# spider.py
import scrapy
from myproject.items import EbookItem  # Import the EbookItem from items.py

class BookSpider(scrapy.Spider):
    name = "books"
    start_urls = ["https://books.toscrape.com/"]

    # This is the main callback method that will process the response from the start URLs
    def parse(self, response):
        print("[OUR RESPONSE]")

        # Each book is inside an article container with class = "product_pod"
        # Select all article elements with the class "product_pod" which represent individual ebooks
        ebooks = response.xpath('//article[@class="product_pod"]')

        # 'ebooks' is assumed to be a list of HTML nodes, each representing an individual ebook.
        for ebook in ebooks:
            # Create an instance of EbookItem
            item = EbookItem()

            # Extract the title attribute from the <a> tag that is a direct child of the <h3> tag.
            # @title is used to select the 'title' attribute.
            item['title'] = ebook.xpath('./h3/a/@title').get()

            # Extract the class attribute from the <p> tag with class "star-rating".
            # The class attribute contains both 'star-rating' and the rating itself (e.g., 'Three').
            item['rating'] = ebook.xpath('./p[contains(@class, "star-rating")]/@class').get().split(' ')[1]

            # Extract the text content inside the <p> tag with class "price_color" for the ebook price.
            item['price'] = ebook.xpath('./div[@class="product_price"]/p[@class="price_color"]/text()').get()

            # Check the class of the <i> tag within the <p> tag to determine stock availability.
            check_stock = ebook.xpath('./p[@class="instock availability"]/i/@class').get()

            # If the class is not 'icon-ok', set stock_status to "Not In Stock".
            if check_stock != "icon-ok":
                item['stock_status'] = "Not In Stock"
            else:
                # Extract the stock status from the <p> tag with classes 'instock availability'.
                stock_status = ebook.xpath('./p[@class="instock availability"]/text()').getall()
                item['stock_status'] = ''.join(stock_status).strip()

            # Yield the item (instead of a dictionary)
            yield item
```

### 3. **Yield the Item**

In the `parse()` method of the spider, you now create an instance of `EbookItem` for each ebook, populate it with the extracted data, and yield the item. This is very similar to yielding dictionaries, but with additional structure.

### Why Use Items Instead of Dictionaries?

- **Structure**: Items provide a more structured and well-defined way to organize your scraped data. Each field is clearly defined, making your code more readable and maintainable.
- **Validation**: With custom Items, you can add validation logic to ensure that the scraped data conforms to certain types or formats.
- **Extensibility**: Items can be extended with additional features, like default values, type checking, or pipelines that interact with the fields.

### Example Output Using `EbookItem`

When the spider runs, it will yield instances of `EbookItem` that contain the structured data. Here's an example of what the output might look like:

```json
{
    "title": "The Book Thief",
    "rating": "Five",
    "price": "£39.50",
    "stock_status": "In stock"
},
{
    "title": "Harry Potter",
    "rating": "Four",
    "price": "£20.00",
    "stock_status": "Not In Stock"
}
```

### Further Considerations:
- **Items in Pipelines**: Items are very useful when working with Scrapy pipelines, as they give a structured way to handle and manipulate data before saving it to a database or file.
  
- **Item Loaders**: Scrapy also provides `ItemLoader`, which allows for more advanced item population (e.g., handling missing values, cleaning up data, etc.). You can use `ItemLoader` if you need more control over the item creation process.

This is how you can refactor your spider to use Scrapy Items. The advantages of using Items become clearer when your project grows and you need better control over your data structure.

# **What are Item Loaders in Scrapy?**

**Item Loaders** in Scrapy provide a more flexible and convenient way to populate **Items**. They allow you to **pre-process** and **post-process** the data you scrape, making it easier to clean, format, and validate the data before saving or exporting it.

With **Item Loaders**, you can:
1. **Fill items dynamically**: Instead of directly assigning values to each field, Item Loaders allow you to load multiple fields with one line of code.
2. **Process data**: You can apply **input** and **output processors** to modify or clean data (e.g., stripping whitespace, formatting strings, converting prices).
3. **Handle missing or default values**: You can set default values for missing fields, or choose how to handle missing or malformed data.

### **Basic Structure of Item Loaders**
- **Input Processors**: Process data right after it is extracted (e.g., cleaning or transforming raw data).
- **Output Processors**: Process data right before assigning it to the item (e.g., further validation or transformation).

### **Creating an Item Loader**

Here’s how you can create and use an Item Loader in Scrapy:

1. **Define Your Item** in `items.py`:
   ```python
   import scrapy

   class EbookItem(scrapy.Item):
       title = scrapy.Field()
       rating = scrapy.Field()
       price = scrapy.Field()
       stock_status = scrapy.Field()
   ```

2. **Use an Item Loader in the Spider**:
   In your spider, use `ItemLoader` to load fields dynamically and apply processors:

   ```python
   from scrapy.loader import ItemLoader
   from myproject.items import EbookItem
   from scrapy.loader.processors import TakeFirst, MapCompose

   class BookSpider(scrapy.Spider):
       name = "books"
       start_urls = ["https://books.toscrape.com/"]

       def parse(self, response):
           # Each book is inside an article container with class = "product_pod"
           ebooks = response.xpath('//article[@class="product_pod"]')

           for ebook in ebooks:
               loader = ItemLoader(item=EbookItem(), selector=ebook)

               # Use 'add_xpath' or 'add_css' to populate fields
               loader.add_xpath('title', './h3/a/@title', MapCompose(str.strip))  # Remove leading/trailing spaces
               loader.add_xpath('rating', './p[contains(@class, "star-rating")]/@class', MapCompose(lambda x: x.split(' ')[1]))  # Extract the rating
               loader.add_xpath('price', './div[@class="product_price"]/p[@class="price_color"]/text()', MapCompose(lambda x: x.strip()))  # Strip whitespaces from price

               # Stock status is more complex, so we handle it differently
               check_stock = ebook.xpath('./p[@class="instock availability"]/i/@class').get()
               if check_stock != "icon-ok":
                   loader.add_value('stock_status', "Not In Stock")
               else:
                   stock_status = ebook.xpath('./p[@class="instock availability"]/text()').getall()
                   loader.add_value('stock_status', ''.join(stock_status).strip())

               # Yield the loaded item
               yield loader.load_item()
   ```

### **Why Define Processors in `items.py`?**

Defining processors inside the **Item** class in `items.py` allows you to keep all field-specific data cleaning and transformation logic within the item definition. This is more modular, and it makes it easy to maintain, as each field has its own processors for input and output transformations.

### **Defining Processors in `items.py`**

Here’s how you can define input and output processors **inside the Item class** in `items.py`:

1. **Define Your Item with Processors**:
   
In your `items.py` file, you can define both **input processors** (for cleaning or transforming the raw data) and **output processors** (for final data validation or formatting before the item is returned).

```python
# items.py
import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join

# Define the Item class and associate processors for each field
class EbookItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(str.strip),  # Strip leading/trailing whitespace
        output_processor=TakeFirst()  # Take the first non-null value
    )
    rating = scrapy.Field(
        input_processor=MapCompose(lambda x: x.split(' ')[1]),  # Extract rating from class attribute
        output_processor=TakeFirst()
    )
    price = scrapy.Field(
        input_processor=MapCompose(lambda x: x.replace('£', '').strip()),  # Remove currency symbol and strip
        output_processor=TakeFirst()
    )
    stock_status = scrapy.Field(
        input_processor=Join(),  # Join multiple values (if present) into a single string
        output_processor=TakeFirst()  # Take the first non-null value
    )
```

### **Explanation of the Processors in `items.py`**:

- **`MapCompose`**: This processor applies a series of functions to clean or modify the input data. You can chain multiple functions to apply them sequentially.
  - For example, `MapCompose(str.strip)` removes leading/trailing whitespace.
  - `MapCompose(lambda x: x.replace('£', '').strip())` removes the currency symbol (`£`) and strips any remaining whitespace.

- **`TakeFirst`**: This output processor ensures that only the first value from a list of values is taken. It's useful when you only need one value from a field (e.g., there’s only one title or price).

- **`Join`**: This processor joins multiple values into a single string. It is useful when a field can have multiple text parts, such as when the stock status spans multiple lines.

### **Use the Item Loader in the Spider**

Now, in your spider, you can use the `ItemLoader` without needing to define the processors again. The processors are already defined in the `EbookItem` class.

2. **Spider Code**:

```python
# spider.py
import scrapy
from scrapy.loader import ItemLoader
from myproject.items import EbookItem

class BookSpider(scrapy.Spider):
    name = "books"
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        # Each book is inside an article container with class = "product_pod"
        ebooks = response.xpath('//article[@class="product_pod"]')

        for ebook in ebooks:
            # Create an ItemLoader instance for each ebook
            loader = ItemLoader(item=EbookItem(), selector=ebook)

            # You don’t need to define processors here, just specify the fields
            loader.add_xpath('title', './h3/a/@title')
            loader.add_xpath('rating', './p[contains(@class, "star-rating")]/@class')
            loader.add_xpath('price', './div[@class="product_price"]/p[@class="price_color"]/text()')

            # Stock status handling
            check_stock = ebook.xpath('./p[@class="instock availability"]/i/@class').get()
            if check_stock != "icon-ok":
                loader.add_value('stock_status', "Not In Stock")
            else:
                stock_status = ebook.xpath('./p[@class="instock availability"]/text()').getall()
                loader.add_value('stock_status', ''.join(stock_status).strip())

            # Yield the item loaded with data and processed
            yield loader.load_item()
```

### **Explanation of the Spider Code**:

- **ItemLoader Usage**: The spider uses the `ItemLoader` to populate the `EbookItem`. Fields like `title`, `rating`, and `price` are populated using `add_xpath()`, and the `stock_status` is handled with a conditional statement. 
- **Predefined Processors**: Since the processors are already defined inside `EbookItem`, you don’t need to redefine them in the spider. The `ItemLoader` will automatically apply them.

### **Advantages of Defining Processors in `items.py`**:

1. **Separation of Concerns**: 
   - By defining processors inside `items.py`, you decouple data extraction from data processing. This makes the code easier to read and maintain.
   - The spider only focuses on **extracting data**, while the item is responsible for **cleaning and validating** the data.

2. **Reusability**:
   - If you use the same item in multiple spiders, you don't need to redefine processors in every spider. The data cleaning logic is centralized in the item itself.

3. **Cleaner Spider Code**:
   - The spider’s `parse()` method is simpler and easier to understand because the logic for processing the data is encapsulated within the item’s processors.

4. **Consistency**:
   - Since all data processing happens in a centralized place (`items.py`), you can ensure that the data is consistently cleaned and validated across different spiders and scraping sessions.

### **Complete Example Summary**

- **Define Processors in `items.py`**: You define input and output processors (like `MapCompose`, `TakeFirst`, and `Join`) inside the `EbookItem` class. This helps you clean and format the data globally for each field.
  
- **Use `ItemLoader` in the Spider**: When using the `ItemLoader` in the spider, you don’t need to redefine the processors for each field, as they are already defined in the `EbookItem`. The loader just populates the fields and automatically applies the processors.

- **Advantages**: Defining processors in `items.py` makes the code modular, reusable, and easier to maintain. You achieve a cleaner separation between data extraction and processing.

By setting up your Scrapy project this way, you create a robust, modular, and maintainable system for scraping, processing, and validating data.

### **Commonly Used Item Loader Processors**

Scrapy provides several built-in processors that you can use to clean and process your data:

#### 1. **`MapCompose`**
   - Allows you to apply multiple processing functions to the input data.
   - **Usage**: Used in the `add_xpath()` or `add_css()` methods.
   - **Example**:
     ```python
     from scrapy.loader.processors import MapCompose

     # Example to strip whitespace and convert price to float
     loader.add_xpath('price', './p[@class="price_color"]/text()', MapCompose(str.strip, lambda x: float(x.replace('£', ''))))
     ```

#### 2. **`TakeFirst`**
   - Takes the **first non-null** value from a list of values. It is useful when you are dealing with a field that may return multiple values but you only need the first one.
   - **Usage**: Commonly used for fields where only the first match matters.
   - **Example**:
     ```python
     from scrapy.loader.processors import TakeFirst

     # Example to always take the first value of the 'title'
     loader.add_xpath('title', './h3/a/@title', TakeFirst())
     ```

#### 3. **`Join`**
   - Joins a list of values into a single string, typically used for fields that return multiple values (e.g., text from multiple elements).
   - **Usage**: Often used with fields like descriptions or stock statuses that may span multiple elements.
   - **Example**:
     ```python
     from scrapy.loader.processors import Join

     # Example to join multiple lines of text
     loader.add_xpath('stock_status', './p[@class="instock availability"]/text()', Join())
     ```

#### 4. **`Identity`**
   - Simply returns the input without changing it. This is the default processor.
   - **Usage**: If you want to pass through values without any processing, this is the processor to use.
   - **Example**:
     ```python
     from scrapy.loader.processors import Identity

     # Example to leave values unprocessed
     loader.add_xpath('description', './div[@class="description"]/text()', Identity())
     ```
### Summary
- **Item Loaders** provide a powerful mechanism to dynamically load and process scraped data into `Items`.
- They allow you to apply **input/output processors** to clean and transform your data efficiently.
- Common processors like `MapCompose`, `TakeFirst`, and `Join` allow you to format data during scraping.

By leveraging Item Loaders, you can make your Scrapy spiders cleaner, more modular, and more flexible when handling different types of data.