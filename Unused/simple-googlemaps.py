
import asyncio
from crawl4ai import *
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.deep_crawling.filters import FilterChain, URLPatternFilter

# Only follow URLs containing "blog" or "docs"
url_filter = URLPatternFilter(patterns=["*blog*", "*docs*"])
# Create a scorer
scorer = KeywordRelevanceScorer(
    keywords=["crawl", "example", "async", "configuration"],
    weight=0.7
)

# The DFSDeepCrawlStrategy uses a depth-first approach, explores as far down a branch as possible before backtracking.
DFSstrategy = DFSDeepCrawlStrategy(
    max_depth=2,               # Crawl initial page + 2 levels deep
    filter_chain=FilterChain(filters=[url_filter]),  # Only follow URLs in filter patterns
    include_external=True,    # Stay within the same domain
    # url_scorer=None,  # Use the scorer to prioritize URLs
    # max_pages=30,              # Maximum number of pages to crawl (optional)
    # score_threshold=0.5,       # Minimum score for URLs to be crawled (optional)
)
# The BFSDeepCrawlStrategy uses a breadth-first approach, exploring all links at one depth before moving deeper:
BFSstrategy = BFSDeepCrawlStrategy(
            max_depth=2, # Crawl initial page + 2 levels deep
            filter_chain=FilterChain(filters=[url_filter]),  # Only follow URLs in filter patterns
            # url_scorer=scorer,  # Use the scorer to prioritize URLs
            include_external=True,   # Stay within the same domain Or not
            max_pages=50,              # Maximum number of pages to crawl (optional)
            score_threshold=0.3,       # Minimum score for URLs to be crawled (optional)

        )

# For more intelligent crawling, use BestFirstCrawlingStrategy with scorers to prioritize the most relevant pages:


# Configure the strategy
BFCstrategy = BestFirstCrawlingStrategy(
    max_depth=2,
    filter_chain=FilterChain(filters=[url_filter]),  # Only follow URLs in filter patterns
    # url_scorer=scorer,  # Use the scorer to prioritize URLs
    include_external=False,
    max_pages=25,              # Maximum number of pages to crawl (optional)
)



async def main():
    # https://docs.crawl4ai.com/api/parameters/#1-browserconfig-controlling-the-browser
    browser_config = BrowserConfig(verbose=False,
                                   headless=True,  # Headless means no visible UI. False is handy for debugging.
                                   viewport_width=3024,  # Width of the browser window. Default is 1280.
                                   viewport_height=1964,  # Height of the browser window. Default is 800.
                                   browser_type="chromium",  # Which browser engine to use. "chromium" is typical for many sites, "firefox" or "webkit" for specialized tests.
                                   use_persistent_context=False,  # If True, uses a persistent browser context (keep cookies, sessions across runs). Also sets use_managed_browser=True.
                                   user_data_dir=None,  # Directory to store user data (profiles, cookies). Must be set if you want permanent sessions.
                                   ignore_https_errors=True,  # If True, continues despite invalid certificates (common in dev/staging).
                                   java_script_enabled=True,  # Disable if you want no JS overhead, or if only static content is needed.
                                   cookies=[],  # Pre-set cookies, each a dict like {"name": "session", "value": "...", "url": "..."}.
                                   headers={},  # Extra HTTP headers for every request, e.g. {"Accept-Language": "en-US"}.
                                   user_agent='random',  # CYour custom or random user agent. user_agent_mode="random" can shuffle it.
                                   light_mode=True,  # Use light mode for faster crawling
                                   text_mode=True,  # If True, tries to disable images/other heavy content for speed.
                                   use_managed_browser=False,  # For advanced “managed” interactions (debugging, CDP usage). Typically set automatically if persistent context is on
                                   extra_args=[],  # Additional flags for the underlying browser process, e.g. ["--disable-extensions"].

    ) 
    # https://docs.crawl4ai.com/api/parameters/#2-crawlerrunconfig-controlling-each-crawl
    run_config = CrawlerRunConfig(
            stream=True,  # Enable streaming
            word_count_threshold=200,        # Skips text blocks below X words. Helps ignore trivial sections.
            deep_crawl_strategy=DFSstrategy,
            extraction_strategy=None,       # If set, extracts structured data (CSS-based, LLM-based, etc.).
            markdown_generator=None,        # If you want specialized markdown output (citations, filtering, chunking, etc.).
            exclude_external_links=False,    # Remove external links
            remove_overlay_elements=False,   # Remove popups/modals
            process_iframes=True,           # Process iframe content
            cache_mode=CacheMode.BYPASS,  # Cache mode
            wait_until="domcontentloaded",  # Condition for navigation to “complete”. Often "networkidle" or "domcontentloaded".
    )   

    async with AsyncWebCrawler(config=browser_config) as crawler:
        results = await crawler.arun(
            # url="https://www.google.com/maps/search/{{query}}",
            url="https://www.google.com/maps/search/Small+bakeries+west+village+New+york",
            config=run_config,
        )

        for result in results:

            if result.success:
                # Print clean content
                # print("Content:", result.markdown[:500])  # First 500 chars

                # Process images
                # for image in result.media["images"]:
                #     print(f"Found image: {image['src']}")

                # Process links
                internal_links = result.links.get("internal", [])
                external_links = result.links.get("external", [])
                print(f"Found {len(internal_links)} internal links.")
                print(f"Found {len(external_links)} external links.")
                print(f"Found {len(result.media)} media items.")
                # Print internal links
                # for link in internal_links:
                #     print(f"Internal link: {link['href']}")
                # Print external links
                for link in external_links:
                    # print(f"External link: {link['href']}")
                    print(f"External link: {link}")


            else:
                print(f"Crawl failed: {result.error_message}")


if __name__ == "__main__":
    asyncio.run(main())