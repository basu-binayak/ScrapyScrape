# ScrapyScrape
ScrapyScrape is a repository for web scraping projects using Scrapy, a powerful Python framework. It focuses on building efficient spiders to extract data from various websites, automate crawling processes, and collect structured information for data analysis, research, or application development.

# Getting started with Scrapy
### Create your virtual environment with Conda using the following command:

```bash
conda create --prefix ./venv python
```

### You now need to activate the environment and install Scrapy. Here's what to do next:

#### 1. Activate the Conda Environment:
Activate the environment you just created:
```bash
conda activate ./venv
```
#### 2. Install Scrapy:
Once the environment is active, install Scrapy by running:

```bash
pip install scrapy
```
#### 3. Verify Scrapy Installation:
After installation, verify it by running:

```bash
scrapy --version
```
If Scrapy is installed correctly, it will display the installed version. Now you're ready to start scraping with Scrapy in your Conda-managed environment!


# Using Scrapy Shell

The Scrapy shell is a powerful tool for interactively exploring and testing your Scrapy spiders and selectors. It allows you to fetch web pages, extract data, and debug your scraping logic. Here’s how to use it effectively:

## 1. **Starting the Scrapy Shell**

To open the Scrapy shell, navigate to your Scrapy project directory in your terminal and run:

```bash
scrapy shell
```

You can also open the shell with a specific URL to directly scrape data from that page:

```bash
scrapy shell <url>
```

For example:

```bash
scrapy shell https://quotes.toscrape.com/
```

## 2. **Fetching a URL**

If you have opened the shell without a URL, you can fetch a specific page using the `fetch()` method:

```python
fetch('https://quotes.toscrape.com/')
```

This command retrieves the page, and the response is stored in the `response` variable.

## 3. **Inspecting the Response**

Once you have the `response`, you can inspect various properties:

- **View the response body:**
  ```python
  print(response.body)  # Prints the raw HTML response
  ```

- **View the response URL:**
  ```python
  print(response.url)   # Prints the URL of the response
  ```

- **View the response status code:**
  ```python
  print(response.status)  # Prints the HTTP status code
  ```

## 4. **Using Selectors**

You can use CSS selectors or XPath expressions to extract data from the response:

- **Using CSS selectors:**
  ```python
  titles = response.css('h2.title::text').getall()  # Extracts all titles
  ```

- **Using XPath:**
  ```python
  titles = response.xpath('//h2[@class="title"]/text()').getall()  # Extracts all titles
  ```

## 5. **Testing Your Selectors**

You can quickly test and refine your selectors directly in the shell:

- **Print the results:**
  ```python
  print(titles)  # Displays the extracted titles
  ```

- **Check if a selector returns any results:**
  ```python
  if titles:
      print("Titles found:", titles)
  else:
      print("No titles found.")
  ```

## 6. **Using the Item Pipeline**

To test how items are processed through your item pipeline, import your item classes and create instances:

```python
from myproject.items import MyItem  # Adjust the import path based on your project structure

item = MyItem()
item['title'] = titles
print(item)
```

## 7. **Running Commands**

You can execute any Python commands and functions in the shell. For example, perform data cleaning or transformations:

```python
cleaned_titles = [title.strip() for title in titles]
print(cleaned_titles)
```

## 8. **Exiting the Shell**

To exit the Scrapy shell, simply type:

```python
exit()
```

or use the shortcut `Ctrl + D`.

## 9. **Help Commands**

If you need help while in the shell, you can use:

- **Get help on Scrapy commands:**
  ```python
  help(response)   # Provides help on the response object
  help(response.css)  # Provides help on the CSS selector
  ```

## 10. **Enhanced Shell - IPython with Scrapy***

### Steps:

1. **Install IPython** (if you haven't already):
   ```bash
   pip install ipython
   ```

2. **Run Scrapy Shell**:
   Once **IPython** is installed, simply running the Scrapy shell will automatically launch it with IPython's interactive features:
   ```bash
   scrapy shell 'https://quotes.toscrape.com/'
   ```

When you run this, Scrapy will automatically detect that IPython is installed and use it instead of the default Python shell.

This is the simplest way to use IPython with Scrapy!

## Example Usage

Here’s a complete example of using the Scrapy shell to extract quotes from a webpage:

1. Open the shell with a specific URL:
   ```bash
   scrapy shell https://quotes.toscrape.com/
   ```

2. Use CSS selectors to extract quotes:
   ```python
   quotes = response.css('div.quote span.text::text').getall()
   authors = response.css('div.quote span small.author::text').getall()
   ```

3. Print the quotes and authors:
   ```python
   for quote, author in zip(quotes, authors):
       print(f'"{quote}" - {author}')
   ```

## Conclusion

The Scrapy shell is an invaluable tool for testing and refining your scraping logic. It allows you to quickly interact with web pages, test selectors, and debug your code without running an entire spider. The ability to fetch specific URLs with `fetch()` makes it even more versatile for exploring different pages. Happy scraping!

--- 

This guide should help you get started with using the Scrapy shell effectively!

# CSS Selectors v/s XPath

## Let us look at an example first!
Let's break down an XPath expression and explain what it's doing:

### XPath:
```python
response.xpath("//h3/a[starts-with(@title,'S')]/@title").getall()
```

1. `//h3/a`:  
   This selects all `<a>` elements that are direct children of an `<h3>` element, anywhere in the document.

2. `[starts-with(@title, 'S')]`:  
   This filters the `<a>` elements by checking whether the `title` attribute starts with the letter `'S'`. Only the `<a>` elements that meet this condition will be selected.

3. `/@title`:  
   Once the filtering is done, this part extracts the value of the `title` attribute from the selected `<a>` elements.

4. `.getall()`:  
   This returns a list of all matching `title` attribute values.

### CSS Equivalent:

In CSS, we can use the `^=` operator to match attributes that start with a specific string. The CSS equivalent for this XPath would be:

```python
response.css('h3 > a[title^="S"]::attr(title)').getall()
```

### CSS Breakdown:
1. `'h3 > a'`:  
   This selects all `<a>` elements that are direct children of an `<h3>` element.

2. `[title^="S"]`:  
   This filters the `<a>` elements by checking if their `title` attribute starts with the letter `'S'`. The `^=` operator means "starts with."

3. `::attr(title)`:  
   This extracts the value of the `title` attribute from the selected `<a>` elements.

4. `.getall()`:  
   Similar to XPath, this returns a list of all matching `title` attribute values.

### Summary:
- **XPath**: `response.xpath("//h3/a[starts-with(@title,'S')]/@title").getall()`
- **CSS**: `response.css('h3 > a[title^="S"]::attr(title)').getall()`

Both methods achieve the same result: they return a list of `title` attribute values from `<a>` elements under `<h3>` tags, where the `title` starts with the letter `'S'`.

## Comprehensice Coverage
Here’s a **comprehensive table that matches each CSS selector with its equivalent XPath expression**.

| **CSS Selector**                     | **Description**                                            | **XPath Equivalent**                                            |
|--------------------------------------|------------------------------------------------------------|-----------------------------------------------------------------|
| `element`                            | Selects all elements with the given tag (e.g., `div`)       | `//element` (e.g., `//div`)                                     |
| `.class`                             | Selects all elements with the given class                   | `//*[contains(concat(' ', @class, ' '), ' class ')]`            |
| `#id`                                | Selects the element with the given ID                       | `//*[@id='id']`                                                 |
| `element.class`                      | Selects all elements with the tag and class                 | `//element[contains(concat(' ', @class, ' '), ' class ')]`       |
| `element#id`                         | Selects the element with the tag and ID                     | `//element[@id='id']`                                           |
| `element[attr]`                      | Selects all elements with the given attribute               | `//element[@attr]`                                              |
| `element[attr="value"]`              | Selects all elements where the attribute equals a value     | `//element[@attr='value']`                                      |
| `element[attr^="value"]`             | Selects all elements where the attribute starts with value  | `//element[starts-with(@attr, 'value')]`                        |
| `element[attr$="value"]`             | Selects all elements where the attribute ends with value    | `//element[substring(@attr, string-length(@attr) - string-length('value') + 1) = 'value']` |
| `element[attr*="value"]`             | Selects all elements where the attribute contains value     | `//element[contains(@attr, 'value')]`                           |
| `element > child`                    | Selects direct children of the element                      | `//element/child`                                               |
| `element child`                      | Selects all descendants of the element                      | `//element//child`                                              |
| `element + sibling`                  | Selects the next sibling of the element                     | `//element/following-sibling::*[1][self::sibling]`              |
| `element ~ sibling`                  | Selects all siblings after the element                      | `//element/following-sibling::sibling`                          |
| `:first-child`                       | Selects the first child of an element                       | `//element/*[1]`                                                |
| `:last-child`                        | Selects the last child of an element                        | `//element/*[last()]`                                           |
| `:nth-child(n)`                      | Selects the nth child of an element                         | `//element/*[n]`                                                |
| `:nth-last-child(n)`                 | Selects the nth child from the end                          | `//element/*[last() - n + 1]`                                   |
| `:nth-of-type(n)`                    | Selects the nth element of its type                         | `//element[n]`                                                  |
| `element:not(selector)`              | Selects elements that don’t match the given selector        | `//element[not(condition)]`                                     |
| `:first-of-type`                     | Selects the first element of its type                       | `//element[1]`                                                  |
| `:last-of-type`                      | Selects the last element of its type                        | `//element[last()]`                                             |
| `element:empty`                      | Selects elements with no children                           | `//element[not(node())]`                                        |
| `element:only-child`                 | Selects an element if it is the only child of its parent    | `//element[count(preceding-sibling::*) = 0 and count(following-sibling::*) = 0]` |
| `element:nth-child(odd)`             | Selects odd-numbered children                              | `//element[position() mod 2 = 1]`                               |
| `element:nth-child(even)`            | Selects even-numbered children                             | `//element[position() mod 2 = 0]`                               |

### Notes:
1. **Class Selector**: In XPath, class attributes are often space-separated, so to match exactly, XPath uses the `contains()` function with `concat()` to avoid partial matches.
   
2. **Nth Child Selectors**: XPath doesn't have a direct equivalent to CSS's `nth-child`, but it can be simulated using `position()` or `last()` functions.

3. **Sibling Selectors**: For adjacent siblings, XPath selects the first following sibling, while general sibling selectors get all following siblings.

4. **Attribute Selectors**: XPath handles attribute values using functions like `starts-with()`, `contains()`, and substring methods.

### Example
If you want to select all `<a>` elements with the class `button` and an `href` attribute that starts with `https` in both CSS and XPath:

- **CSS**:
   ```css
   a.button[href^="https"]
   ```

- **XPath**:
   ```xpath
   //a[contains(concat(' ', @class, ' '), ' button ')][starts-with(@href, 'https')]
   ```

This table should cover most common CSS selectors and their XPath equivalents! 