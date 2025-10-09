import requests
from bs4 import BeautifulSoup

url = "https://nitter.net/naval"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get(url, headers=headers, timeout=10)
soup = BeautifulSoup(response.content, 'html.parser')

# Save full HTML
with open('nitter_page.html', 'w', encoding='utf-8') as f:
    f.write(soup.prettify())

print("✅ Saved HTML to nitter_page.html")

# Try to find tweets
print("\n🔍 Looking for tweet elements...")

# Check all divs with class containing 'tweet'
tweet_divs = soup.find_all('div', class_=lambda x: x and 'tweet' in x.lower())
print(f"Found {len(tweet_divs)} divs with 'tweet' in class")

# Check for timeline items
timeline = soup.find_all('div', class_='timeline-item')
print(f"Found {len(timeline)} timeline items")

# Check for any text content
all_text = soup.get_text()
if 'twitter' in all_text.lower() or 'tweet' in all_text.lower():
    print("✅ Page contains Twitter-related content")
else:
    print("❌ Page doesn't seem to have Twitter content")

# Print first few class names to see structure
print("\n📋 Sample class names found:")
for div in soup.find_all('div')[:20]:
    if div.get('class'):
        print(f"   {div.get('class')}")