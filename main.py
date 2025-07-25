from bs4 import BeautifulSoup
import requests

url = "https://www.cnn.com/2025/07/21/politics/fema-search-and-rescue-chief-resigns"

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")
print(doc.prettify())
