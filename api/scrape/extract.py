
from bs4 import BeautifulSoup
import json


# Function to extract main content with structure
def extract_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    content = []

    for element in soup.find_all(["h1", "h2", "h3", "p", "img", "a"]):
        if element.name in ["h1", "h2", "h3"]:
            content.append({
                "type": "heading",
                "level": element.name,
                "text": element.get_text(strip=True)
            })
        elif element.name == "p":
            content.append({
                "type": "paragraph",
                "text": element.get_text(strip=True)
            })
        elif element.name == "img":
            content.append({
                "type": "image",
                "src": element.get("src"),
                "alt": element.get("alt", "")
            })
        elif element.name == "a":
            content.append({
                "type": "link",
                "href": element.get("href"),
                "text": element.get_text(strip=True)
            })

    structured_content = str(json.dumps(content, indent=0))
    return structured_content
