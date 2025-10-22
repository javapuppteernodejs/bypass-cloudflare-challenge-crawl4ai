# 🚀 Bypassing Cloudflare Challenge: Deep Integration of Crawl4AI and CapSolver

## 🌟 Project Introduction

This project aims to provide a practical solution for developers to effectively bypass Cloudflare Challenge using the powerful crawling capabilities of **[Crawl4AI](https://docs.crawl4ai.com/)** and the advanced CAPTCHA and anti-bot services of **[CapSolver](https://dashboard.capsolver.com/passport/login/?utm_source=github&utm_medium=partnership&utm_campaign=how-to-solve-cloudflare-challenge-in-crawl4ai-capsolver)**. When performing web data scraping, anti-bot mechanisms like Cloudflare often become obstacles. This solution utilizes API-level integration to simulate real browser behavior, ensuring the smooth execution of crawling tasks.

As an developer, I deeply understand the various challenges encountered during data scraping. Cloudflare Challenge is particularly complex, combining techniques such as browser fingerprinting, User-Agent validation, and JavaScript execution to identify and block automated traffic. This project is my exploration and practice of an efficient strategy to address this pain point.

## ✨ Core Features

-   **CapSolver `AntiCloudflareTask` Integration**: Leverage CapSolver's specialized anti-Cloudflare task type to obtain challenge solutions (token, cookies, User-Agent).
-   **Crawl4AI Browser Configuration**: Precisely configure Crawl4AI's browser environment based on the solution returned by CapSolver, ensuring consistency with the environment where the challenge was solved.
-   **Seamless Cloudflare Bypass**: Enable Crawl4AI to access Cloudflare-protected websites like a real user.
-   **Python Implementation**: Provide clear, executable Python code examples.

## ⚙️ How It Works

1.  **Request CapSolver Solution**: Before launching Crawl4AI, call the CapSolver API using the `AntiCloudflareTask` type, providing the target website URL, proxy (if needed), and a User-Agent that matches the one CapSolver uses internally.
2.  **Obtain Challenge Credentials**: CapSolver processes the challenge and returns a `solution` object containing a `token`, `cookies`, and the recommended `userAgent`.
3.  **Configure Crawl4AI Browser**: Use the `token`, `cookies`, and `userAgent` obtained from CapSolver to configure Crawl4AI's `BrowserConfig`, ensuring Crawl4AI's browser instance perfectly matches the environment in which the challenge was solved.
4.  **Execute Crawling Task**: Crawl4AI then executes its `arun` method with this specially configured browser, successfully accessing the target URL without triggering the Cloudflare Challenge again.

## 🚀 Getting Started

### 🛠️ Environment Setup

Before running the code, please ensure you have installed the following libraries:

```bash
pip install capsolver crawl4ai
```

### 🔑 Configure Your API Key

Please replace `api_key` with your CapSolver API key. You can obtain it from the [CapSolver Dashboard](https://dashboard.capsolver.com/).

```python
# TODO: set your config
api_key = "CAP-XXX"  # your api key of capsolver
```

### 💻 Example Code

The following Python code demonstrates how to integrate CapSolver's API with Crawl4AI to solve Cloudflare Challenge. This example targets a news article page protected by Cloudflare.

```python
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
```

### 💡 Code Analysis

1.  **CapSolver SDK Call**: The `capsolver.solve` method is central here, using the `AntiCloudflareTask` type. It requires `websiteURL`, `proxy` (optional), and a specific `userAgent`. CapSolver processes the challenge and returns a `solution` object containing a `token`, `cookies`, and the `userAgent` that was used to solve the challenge.
2.  **Crawl4AI Browser Configuration**: The `BrowserConfig` for Crawl4AI is meticulously set up using the information from CapSolver's solution. This includes `user_agent` and `cookies` to ensure the Crawl4AI browser instance perfectly matches the conditions under which the Cloudflare Challenge was solved. The `user_data_dir` is also specified to maintain a consistent browser profile.
3.  **Crawler Execution**: Crawl4AI then executes its `arun` method with this carefully configured `browser_config`, allowing it to successfully access the target URL without triggering the Cloudflare Challenge again.

## 🤝 Contributing

Contributions of any kind are welcome! If you have better methods or find bugs, please feel free to submit an Issue or Pull Request.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 🔗 References

-   [Crawl4AI Official Documentation](https://docs.crawl4ai.com/)
-   [CapSolver Official Documentation](https://docs.capsolver.com/)
-   [CapSolver: Cloudflare Challenge Documentation](https://docs.capsolver.com/guide/captcha/cloudflare_challenge/)
-   [Overall Crawl4AI CapSolver Integration Blog Post](https://www.capsolver.com/blog/Partners/crawl4ai-capsolver)

