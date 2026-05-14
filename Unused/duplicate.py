
import asyncio
from crawl4ai import *


async def crawl_streaming(urls):
    browser_config = BrowserConfig(headless=True, verbose=False)
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        stream=True  # Enable streaming mode
    )

    dispatcher = MemoryAdaptiveDispatcher(
        memory_threshold_percent=70.0,
        check_interval=1.0,
        max_session_permit=10,

    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        # Process results as they become available
        async for result in await crawler.arun_many(
            urls=urls,
            config=run_config,
            dispatcher=dispatcher
        ):
            if result.success:
                # Process each result immediately
                print(f"Successfully crawled {result}")
            else:
                print(f"Failed to crawl {result.url}: {result.error_message}")

async def extract_emails_from_url(urls):
  

    async with AsyncWebCrawler() as crawler:
        # Get all results at once
        results = await crawler.arun_many(
            urls=urls,
        )

        print(f"Successfully crawled {results}")



if __name__ == "__main__":
    # List of URLs to crawl
    urls_to_crawl = [
        "https://mahzedahrbakery.com",
        # "http://marvelousbyfred.com",
        # "http://barachou.com",
        # "http://millefeuille-nyc.com",
        # "http://fabriquebakery.com",
        # "http://anntremet.com",
        # "http://magnoliabakery.com",
        # "http://janiebakes.com"
    ]
    # asyncio.run(extract_emails_from_url(urls_to_crawl))
    asyncio.run(crawl_streaming(urls_to_crawl))
  