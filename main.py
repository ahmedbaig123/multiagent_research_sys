from src.tools.tools import websearch, scrape_url

result = scrape_url.invoke({
    "url": "https://github.com/"
})

print(result)