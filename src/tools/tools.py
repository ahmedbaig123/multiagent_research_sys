from langchain.tools import tool
import requests
from dotenv import load_dotenv
import os
from tavily import TavilyClient
from rich import print
from bs4 import BeautifulSoup
from readability import Document
import trafilatura
import re

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def websearch(query:str) -> str:
    results = tavily.search(query=query,max_results=5)

    out = []

    for r in results['results']:
        out.append(
            f"Title: {r['title']} \n URL:{r['url']} \nSnippet: {r['content'][:300]}\n"
        )

    return "\n----\n".join(out)


@tool
def scrape_url(url: str) -> str:
    """Scrape the webpage and extract its readable text content."""

    try:
        # Send HTTP request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        response.raise_for_status()

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove unnecessary elements
        for element in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "noscript"
        ]):
            element.decompose()

        # Extract webpage title
        title = soup.title.get_text(strip=True) if soup.title else "No title"

        # Extract text
        text = soup.get_text(separator=" ", strip=True)

        # Clean extra whitespace
        text = re.sub(r"\s+", " ", text)

        return f"Title: {title}\n\nContent:\n{text[:10000]}"

    except requests.exceptions.RequestException as e:
        return f"Error scraping webpage: {str(e)}"

    except Exception as e:
        return f"Unexpected error: {str(e)}"
