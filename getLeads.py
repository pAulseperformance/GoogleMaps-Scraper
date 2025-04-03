import asyncio
from googleMapBusinessCrawl import main as crawl_google_maps
from websiteEmailCrawl import main as crawl_emails

async def get_business_urls(search_query):
    print(f"Fetching business URLs for query: {search_query}")
    business_urls = await crawl_google_maps(search_query)
    return business_urls

async def get_emails_from_urls(business_urls):
    print(f"Found {len(business_urls)} business URLs. Extracting emails...")
    results = await crawl_emails(business_urls)
    return results


async def main(search_query):
    # Run the first script to get business URLs
    business_urls = await get_business_urls(search_query)

    if not business_urls:
        print("No business URLs found.")
        return

    # Run the second script to extract emails
    results = await get_emails_from_urls(business_urls)

    print("\nLead Generation Complete!")
    print(f"Extracted {len(results)} leads.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python getLeads.py <search_query>")
    else:
        search_query = sys.argv[1]
        asyncio.run(main(search_query))
