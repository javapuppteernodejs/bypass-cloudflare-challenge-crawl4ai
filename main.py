import asyncio
import time

import capsolver
from crawl4ai import *

# TODO: set your config
api_key = "CAP-XXX"  # your api key of capsolver
site_url = "https://www.tempo.co/hukum/polisi-diduga-salah-tangkap-pelajar-di-magelang-yang-dituduh-perusuh-demo-2070572"  # page url of your target site
captcha_type = "AntiCloudflareTask"  # type of your target captcha
api_proxy = "http://127.0.0.1:13120" # If you need a proxy for CapSolver, configure it here
capsolver.api_key = api_key

user_data_dir = "./crawl4ai_/browser-profile/Default1493" # Persistent browser profile directory
# or
# cdp_url = "ws://localhost:xxxx" # If connecting to an existing CDP session

async def main():
    print("solver token start")
    start_time = time.time()
    # get cloudflare token using capsolver sdk
    solution = capsolver.solve({
        "type": captcha_type,
        "websiteURL": site_url,
        "proxy": api_proxy,
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36" # Important: Use a User-Agent that CapSolver supports and matches your intended browser
    })
    token_time = time.time()
    print(f"solver token: {token_time - start_time:.2f} s")

    # CapSolver may return cookies as a dict or list, normalize to list of dicts for Crawl4AI
    cookies = solution.get("cookies", [])
    if isinstance(cookies, dict):
        cookies_array = []
        for name, value in cookies.items():
            cookies_array.append({
                "name": name,
                "value": value,
                "url": site_url,
            })
        cookies = cookies_array
    elif not isinstance(cookies, list):
        cookies = []
    token = solution["token"]
    print("challenge token:", token)

    # Configure Crawl4AI browser with the solution from CapSolver
    browser_config = BrowserConfig(
        verbose=True, # Enable verbose logging for debugging
        headless=False, # Set to True for production scraping without a visible browser UI
        use_persistent_context=True, # Use a persistent browser context
        user_data_dir=user_data_dir, # Specify user data directory for profile persistence
        # cdp_url=cdp_url, # Uncomment if using an existing CDP session
        user_agent=solution["userAgent"], # Use the User-Agent recommended by CapSolver
        cookies=cookies, # Inject cookies provided by CapSolver
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url=site_url,
            cache_mode=CacheMode.BYPASS, # Bypass cache to ensure fresh content
            session_id="session_captcha_test" # Unique session ID for this crawl
        )
        print(result.markdown[:500]) # Print first 500 characters of the scraped markdown content


if __name__ == "__main__":
    asyncio.run(main())

