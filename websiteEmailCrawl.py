
import asyncio
from crawl4ai import *
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.deep_crawling.filters import (
    FilterChain,
    URLPatternFilter,
    DomainFilter,
    ContentTypeFilter,
    ContentRelevanceFilter,
    SEOFilter
)
import re  # Import the regex module


from crawl4ai.async_dispatcher import MemoryAdaptiveDispatcher






dispatcher = MemoryAdaptiveDispatcher(
    memory_threshold_percent=90.0,  # Pause if memory exceeds this
    check_interval=1.0,             # How often to check memory
    max_session_permit=10,          # Maximum concurrent tasks
    rate_limiter=RateLimiter(       # Optional rate limiting
        base_delay=(1.0, 2.0),
        max_delay=30.0,
        max_retries=2
    ),
    monitor=CrawlerMonitor(
        )
)


async def process_result(result):
    # Extract emails from the HTML content
    emails = set()
    print(f"Processing result for URL: {result.url}")

    if result.success:
        html_content = result.cleaned_html
        # Use regex to find emails
        # emails.update(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(?!png|jpg|gif|jpeg)[a-zA-Z]{2,}', html_content))
        emails.update(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(?!png|jpg|gif|jpeg)[a-zA-Z]{2,}', html_content))
        # email = re.findall(r'/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(?!png|jpg|gif|jpeg)[a-zA-Z]{2,}/g', html_content)
        print(f"Found emails: {len(emails)}")
        return list(emails)
    else:
        print(f"Failed to crawl {result.url}: {result.error_message}")
        return []  # Return an empty list if the crawl fails

async def extract_emails_from_url(urls):
    # https://docs.crawl4ai.com/api/parameters/#1-browserconfig-controlling-the-browser
    browser_config = BrowserConfig(verbose=True,
                                   headless=True,  # Headless means no visible UI. False is handy for debugging.
                                   viewport_width=1080,  # Width of the browser window. Default is 1280.
                                   viewport_height=600,  # Height of the browser window. Default is 800.
                                   browser_type="chromium",  # Which browser engine to use. "chromium" is typical for many sites, "firefox" or "webkit" for specialized tests.
                                   use_persistent_context=False,  # If True, uses a persistent browser context (keep cookies, sessions across runs). Also sets use_managed_browser=True.
                                   user_data_dir=None,  # Directory to store user data (profiles, cookies). Must be set if you want permanent sessions.
                                   ignore_https_errors=True,  # If True, continues despite invalid certificates (common in dev/staging).
                                   java_script_enabled=False,  # Disable if you want no JS overhead, or if only static content is needed.
                                   cookies=[],  # Pre-set cookies, each a dict like {"name": "session", "value": "...", "url": "..."}.
                                   headers={},  # Extra HTTP headers for every request, e.g. {"Accept-Language": "en-US"}.
                                   user_agent='random',  # CYour custom or random user agent. user_agent_mode="random" can shuffle it.
                                   light_mode=True,  # Use light mode for faster crawling
                                   text_mode=True,  # If True, tries to disable images/other heavy content for speed.
                                   use_managed_browser=False,  # For advanced “managed” interactions (debugging, CDP usage). Typically set automatically if persistent context is on
                                #    extra_args=[],  # Additional flags for the underlying browser process, e.g. ["--disable-extensions"].
                                   extra_args=["--disable-dev-shm-usage", "--no-sandbox"],  # Add these arguments

    ) 
    # https://docs.crawl4ai.com/api/parameters/#2-crawlerrunconfig-controlling-each-crawl
    run_config = CrawlerRunConfig(
            stream=False,  # Process results immediately as they're discovered - Start working with early results while crawling continues - Better for real-time applications or progressive display - Reduces memory pressure when handling many pages
            # word_count_threshold=200,        # Skips text blocks below X words. Helps ignore trivial sections.
            # excluded_tags=['form', 'header', 'footer'],  # Tags to exclude from the content
            excluded_tags=['form'],  # Tags to exclude from the content

            # extraction_strategy=None,       # If set, extracts structured data (CSS-based, LLM-based, etc.).
            # markdown_generator=None,        # If you want specialized markdown output (citations, filtering, chunking, etc.).
            exclude_external_links=False,    # Remove external links
            remove_overlay_elements=True,   # Remove popups/modals
            process_iframes=True,           # Process iframe content
            cache_mode=CacheMode.BYPASS,  # Cache mode
            wait_until="domcontentloaded",  # Condition for navigation to “complete”. Often "networkidle" or "domcontentloaded".
    )   

    async with AsyncWebCrawler(config=browser_config) as crawler:
        # Get all results at once
        results = await crawler.arun_many(
            urls=urls,
            config=run_config,
            dispatcher=dispatcher
        )

        # print(f"Successfully crawled {results}")
        data = []

        # Process all results after completion
        for result in results:
            if result.success:
                emails = await process_result(result)
                data.append({"url": result.url, "emails": emails})

            else:
                print(f"Failed to crawl {result.url}: {result.error_message}")
                data.append({"url": result.url, "emails": [], "error": result.error_message})


        return data



async def main(urls_to_crawl):
    results = await extract_emails_from_url(urls_to_crawl)

    # Print the results
    print("\n\nCrawl Results:")
    for entry in results:
        print(f"URL: {entry['url']}")
        if "error" in entry:
            print(f"Error: {entry['error']}")
        else:
            print(f"Emails: {entry['emails']}")

    # Save results to JSON without overwriting and avoiding duplicates
    from helpers import save_results_to_json
    save_results_to_json(results)

    return results  # Return the results




if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python websiteEmailCrawl.py <url1> <url2> ...")
    else:
        urls_to_crawl = sys.argv[1:]
        asyncio.run(main(urls_to_crawl))





# if __name__ == "__main__":
#     # List of URLs to crawl
#     urls_to_crawl = [
#         "https://mahzedahrbakery.com",
#         "http://marvelousbyfred.com",
#         "http://barachou.com",
#         "http://millefeuille-nyc.com",
#         "http://fabriquebakery.com",
#         "http://anntremet.com",
#         "http://magnoliabakery.com",
#         "http://janiebakes.com"
#     ]

#     # Run the crawler
#     results = asyncio.run(extract_emails_from_url(urls_to_crawl))
#     # Print the results
#     print("\n\nCrawl Results:")

#     # saveToJson(results)

#     print("Results saved to crawl_results.json")
#     for entry in results:
#         print(f"URL: {entry['url']}")
#         if "error" in entry:
#             print(f"Error: {entry['error']}")
#         else:
#             print(f"Emails: {entry['emails']}")

#      # Save results to JSON without overwriting and avoiding duplicates
#     from helpers import save_results_to_json
#     save_results_to_json(results)