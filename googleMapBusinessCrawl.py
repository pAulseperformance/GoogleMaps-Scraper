
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

from helpers import saveMockData


MAXPAGES = 10
MAXDEPTH = 2
DEEPCRAWLSTRATEGY = "DFS"  # DFS, BFS, BFC
USEMOCKDATA = False  # True, False

# Create a chain of filters
filter_chain = FilterChain([
    # Only follow URLs with specific patterns Matches URL patterns using wildcard syntax
    # URLPatternFilter(patterns=["*url?*", "*place*"]), 
    URLPatternFilter(patterns=["*place*"]), 

    # Controls which domains to include or exclude
    DomainFilter(
        allowed_domains=["google.com"],
        blocked_domains=["maps.gstatic.com", "support.google.com", "googleusercontent.com", "streetviewpixels-pa.googleapis.com", "googleusercontent.com", "wixpress.com", "wix.com", "wixstatic.com", "wixmp.com"]
    ),

    # Filters based on HTTP Content-Type
    # ContentTypeFilter(allowed_types=["text/html"]),

    # Uses similarity to a text query
    # ContentRelevanceFilter(
    #     query="Web crawling and data extraction with Python",
    #     threshold=0.7  # Minimum similarity score (0.0 to 1.0)
    # )

    # Evaluates SEO elements (meta tags, headers, etc.)
    # SEOFilter(
    #     threshold=0.5,  # Minimum score (0.0 to 1.0)
    #     keywords=["tutorial", "guide", "documentation"]
    # )
])



# Create a scorer
scorer = KeywordRelevanceScorer(
    keywords=["place"],
    # keywords=["places", "restaurants", "food", "bakeries", "coffee", "cafe", "bars"],
    weight=0.7
)


# The DFSDeepCrawlStrategy uses a depth-first approach, explores as far down a branch as possible before backtracking.
DFSstrategy = DFSDeepCrawlStrategy(
    max_depth=MAXDEPTH,               # Crawl initial page + 2 levels deep
    filter_chain=filter_chain,  # Only follow URLs in filter patterns
    include_external=True,    # Stay within the same domain
    url_scorer=scorer,  # Use the scorer to prioritize URLs
    max_pages=MAXPAGES,              # Maximum number of pages to crawl (optional)
    # score_threshold=0.5,       # Minimum score for URLs to be crawled (optional)
)
# The BFSDeepCrawlStrategy uses a breadth-first approach, exploring all links at one depth before moving deeper:
BFSstrategy = BFSDeepCrawlStrategy(
            max_depth=MAXDEPTH, # Crawl initial page + 2 levels deep
            filter_chain=filter_chain,  # Only follow URLs in filter patterns
            url_scorer=scorer,  # Use the scorer to prioritize URLs
            include_external=True,   # Stay within the same domain Or not
            max_pages=MAXPAGES,              # Maximum number of pages to crawl (optional)
            score_threshold=0.3,       # Minimum score for URLs to be crawled (optional)

        )

# For more intelligent crawling, use BestFirstCrawlingStrategy with scorers to prioritize the most relevant pages:
# Configure the strategy
BFCstrategy = BestFirstCrawlingStrategy(
    max_depth=MAXDEPTH,
    filter_chain=filter_chain,  # Only follow URLs in filter patterns
    url_scorer=scorer,  # Use the scorer to prioritize URLs
    include_external=False,
    max_pages=MAXPAGES,              # Maximum number of pages to crawl (optional)
)





def printCrawlStats(results):
    print(f"Google Crawl for completed with {len(results)} results.")
    
    # print("Crawl statistics:")
    # for result in results:
        # if result.success:
            # print(f"URL: {result.url} - Status: Success")
            # print(f"Title: {result.title}")
            # print(f"Word Count: {result.word_count}")
            # print(f"Content Length: {len(result.cleaned_html)} characters")

    
            # Print clean content
            # print("Content:", result.markdown[:500])  # First 500 chars
            # print(result.cleaned_html) # Cleaned HTML

            # Assuming `result.cleaned_html` contains the HTML content
            # html_content = result.cleaned_html

            # Perform regex to find all links
            # links = re.findall(r'https?:\/\/[^\/]+', html_content)

            # Print the found links
            # print(f"Found {len(links)} links:")
            # for link in links:
                # print(link)


            # Process images
            # for image in result.media["images"]:
            #     print(f"Found image: {image['src']}")

            # Process links
            # internal_links = result.links.get("internal", [])
            # external_links = result.links.get("external", [])
            # print(f"Found {len(internal_links)} internal links.")
            # print(f"Found {len(external_links)} external links.")
            # print(f"Found {len(result.media)} media items.")
            # Print internal links
            # for link in internal_links:
            #     print(f"Internal link: {link['href']}")
            # Print external links
            # for link in external_links:
            #     # print(f"External link: {link['href']}")
            #     print(f"External link: {link}")
        # else:
            # print(f"URL: {result.url} - Status: Failed - Error: {result.error_message}")


def filter_urls(results):
    unique_urls = set()

    for result in results:
        if result.success:
            html_content = result.cleaned_html

            links = re.findall(r'https?:\/\/[^\/]+', html_content)

            for link in links:
                # Normalize the URL by removing the protocol and "www."
                normalized_link = re.sub(r'^https?:\/\/(www\.)?', '', link)

                # Exclude links that match the provided regex
                if not re.search(r'(google|gstatic|ggpht|schema\.org|example\.com|sentry-next\.wixpress\.com|imli\.com|sentry\.wixpress\.com|ingest\.sentry\.io|opentable\.com|tapmango|toasttab)', normalized_link):
                    unique_urls.add(f"http://{normalized_link}")
        else:
            print(f"Crawl failed: {result.error_message}")
        

    return list(unique_urls)  # Return the filtered unique URLs

async def main(search_query):
    # https://docs.crawl4ai.com/api/parameters/#1-browserconfig-controlling-the-browser
    browser_config = BrowserConfig(verbose=True,
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
            stream=False,  # Process results immediately as they're discovered - Start working with early results while crawling continues - Better for real-time applications or progressive display - Reduces memory pressure when handling many pages
            word_count_threshold=200,        # Skips text blocks below X words. Helps ignore trivial sections.
            excluded_tags=['form', 'header', 'footer'],  # Tags to exclude from the content
            deep_crawl_strategy = (
                                        DFSstrategy if DEEPCRAWLSTRATEGY == "DFS" 
                                        else BFSstrategy if DEEPCRAWLSTRATEGY == "BFS" 
                                        else BFCstrategy
                                ),  # The strategy to use for deep crawling.
            extraction_strategy=None,       # If set, extracts structured data (CSS-based, LLM-based, etc.).
            markdown_generator=None,        # If you want specialized markdown output (citations, filtering, chunking, etc.).
            exclude_external_links=False,    # Remove external links
            remove_overlay_elements=True,   # Remove popups/modals
            process_iframes=True,           # Process iframe content
            cache_mode=CacheMode.BYPASS,  # Cache mode
            wait_until="domcontentloaded",  # Condition for navigation to “complete”. Often "networkidle" or "domcontentloaded".
    )   

    async with AsyncWebCrawler(config=browser_config) as crawler:
        results = await crawler.arun(
            url=f"https://www.google.com/maps/search/{search_query}",
            config=run_config,
        )


        printCrawlStats(results)
        # saveMockData(results)
        filtered_urls = filter_urls(results)
        print(f"Filtered URLs: {filtered_urls}")
        await crawler.close()

        return filtered_urls






if __name__ == "__main__":
        # searchQuery = "Small+bakeries+west+village+New+york"

    import sys
    if len(sys.argv) < 2:
        print("Usage: python googleMapBusinessCrawl.py <search_query>")
    else:
        search_query = sys.argv[1]
        asyncio.run(main(search_query))

    # asyncio.run(main(searchQuery))

