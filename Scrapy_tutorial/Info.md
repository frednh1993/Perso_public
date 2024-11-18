# Installation process and dependencies

Source : ***https://docs.scrapy.org/en/2.11/intro/tutorial.html* **

1. python -m venv virtual_environment_name  and  virtual_environment_name\Scripts\activate ( Get-ExecutionPolicy , Set-ExecutionPolicy RemoteSigned , Set-ExecutionPolicy Restricted )
2. pip install Scrapy
3. scrapy startproject project_name

# Project Architecture and notes

1. For most scraping code, you want it to be resilient to errors due to things not being found on a page, so that even if some parts fail to be scraped, you can at least get **some** data.
2. XPath expressions are very powerful, and are the foundation of Scrapy Selectors. In fact, CSS selectors are converted to XPath under-the-hood.

# Definitions

* Item Pipeline : After an item has been scraped by a spider, it is sent to the Item Pipeline which processes it through several components that are executed sequentially.
* Scrapy shell := Interactive shell where you can try and debug your scraping code very quickly, without having to run the spider. It’s meant to be used for testing data extraction code, but you can actually use it for testing any kind of code as it is also a regular Python shell.
* Spider := Classes that you define and that Scrapy uses to scrape information from a website (or a group of websites).


# Commands

* scrapy crawl spider_name := run the spider
* scrapy shell "url_to_use_the_shell"
