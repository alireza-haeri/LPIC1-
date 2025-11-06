#!/usr/bin/env python3
"""
Fetch article list from linux1st.com/archives.html
Extracts article titles and URLs, saves to linux1st_articles.json
"""

import requests
from bs4 import BeautifulSoup
import json
import sys
from pathlib import Path


def fetch_archives():
    """Fetch and parse the archives page to extract article links."""
    url = "https://linux1st.com/archives.html"
    
    print(f"Fetching: {url}")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        print(f"✓ Successfully fetched archives page ({len(response.content)} bytes)")
        
    except Exception as e:
        print(f"✗ Error fetching archives: {e}")
        sys.exit(1)
    
    # Parse HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all article links
    # Looking for common patterns in archive pages
    articles = []
    
    # Try to find article links - adjust selectors based on actual page structure
    # Common patterns: links within article containers, post listings, etc.
    
    # Strategy 1: Find links in article/post containers
    for container in soup.find_all(['article', 'div'], class_=lambda x: x and ('post' in x.lower() or 'article' in x.lower())):
        link = container.find('a', href=True)
        if link:
            title = link.get_text(strip=True)
            href = link.get('href')
            if title and href and len(title) > 10:
                articles.append({
                    'title': title,
                    'url': href if href.startswith('http') else f"https://linux1st.com{href}"
                })
    
    # Strategy 2: Find all links that look like article links
    if not articles:
        for link in soup.find_all('a', href=True):
            href = link.get('href')
            title = link.get_text(strip=True)
            
            # Filter for article-like links
            if (href and title and len(title) > 15 and
                not any(skip in href.lower() for skip in 
                       ['#', 'javascript:', 'mailto:', 'tel:', 'about', 'contact', 
                        'privacy', 'terms', 'login', 'register', 'search', 
                        'category', 'tag', 'author', 'page', 'comment'])):
                
                full_url = href if href.startswith('http') else f"https://linux1st.com{href}"
                
                # Avoid duplicates
                if not any(a['url'] == full_url for a in articles):
                    articles.append({
                        'title': title,
                        'url': full_url
                    })
    
    # Remove duplicates while preserving order
    seen = set()
    unique_articles = []
    for article in articles:
        url_key = article['url']
        if url_key not in seen:
            seen.add(url_key)
            unique_articles.append(article)
    
    return unique_articles


def main():
    """Main function to fetch articles and save to JSON."""
    articles = fetch_archives()
    
    print(f"\n{'='*60}")
    print(f"Found {len(articles)} articles")
    print(f"{'='*60}\n")
    
    # Display first 5 articles as preview
    for i, article in enumerate(articles[:5], 1):
        print(f"{i}. {article['title']}")
        print(f"   {article['url']}\n")
    
    if len(articles) > 5:
        print(f"... and {len(articles) - 5} more articles\n")
    
    # Save to JSON file
    output_file = Path(__file__).parent / 'linux1st_articles.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    print(f"{'='*60}")
    print(f"✓ Saved {len(articles)} articles to: {output_file.name}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()