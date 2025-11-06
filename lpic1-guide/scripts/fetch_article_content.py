#!/usr/bin/env python3
"""
Fetch full content for each article from linux1st_articles.json
Extracts readable text (ignoring navigation, ads, etc.)
Saves results to linux1st_full.json
"""

import requests
from bs4 import BeautifulSoup
import json
import sys
import time
from pathlib import Path


def extract_article_content(url):
    """
    Fetch and extract readable article content from a URL.
    Removes navigation, ads, sidebars, comments, etc.
    """
    print(f"  Fetching: {url}")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove unwanted elements
        for element in soup.find_all(['script', 'style', 'nav', 'header', 'footer', 
                                       'aside', 'iframe', 'noscript']):
            element.decompose()
        
        # Remove common ad/social containers
        for element in soup.find_all(class_=lambda x: x and any(
            term in x.lower() for term in ['ad', 'banner', 'social', 'share', 
                                           'comment', 'sidebar', 'widget', 
                                           'popup', 'modal', 'newsletter'])):
            element.decompose()
        
        # Try to find the main article content
        # Strategy 1: Look for article tag
        article = soup.find('article')
        
        # Strategy 2: Look for main content containers
        if not article:
            article = soup.find(['div', 'section'], class_=lambda x: x and any(
                term in x.lower() for term in ['content', 'post', 'article', 'entry']))
        
        # Strategy 3: Look for main tag
        if not article:
            article = soup.find('main')
        
        # Strategy 4: Fall back to body
        if not article:
            article = soup.find('body')
        
        if not article:
            return "Unable to extract content"
        
        # Extract text
        content_text = article.get_text(separator='\n', strip=True)
        
        # Clean up excessive whitespace
        lines = [line.strip() for line in content_text.split('\n') if line.strip()]
        content_text = '\n'.join(lines)
        
        # Extract title if available
        title_tag = soup.find('h1')
        title = title_tag.get_text(strip=True) if title_tag else ""
        
        return {
            'title': title,
            'content': content_text
        }
        
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return {
            'title': "",
            'content': f"Error fetching content: {str(e)}"
        }


def main():
    """Main function to process all articles."""
    # Load article list
    script_dir = Path(__file__).parent
    input_file = script_dir / 'linux1st_articles.json'
    output_file = script_dir / 'linux1st_full.json'
    
    if not input_file.exists():
        print(f"✗ Error: {input_file.name} not found!")
        print("  Please run fetch_articles.py first.")
        sys.exit(1)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    print(f"{'='*60}")
    print(f"Processing {len(articles)} articles")
    print(f"{'='*60}\n")
    
    # Process each article
    full_articles = []
    
    for i, article in enumerate(articles, 1):
        print(f"[{i}/{len(articles)}] {article['title']}")
        
        # Extract content
        extracted = extract_article_content(article['url'])
        
        # Combine with original data
        full_article = {
            'title': article['title'],
            'url': article['url'],
            'extracted_title': extracted.get('title', ''),
            'content': extracted.get('content', '')
        }
        
        full_articles.append(full_article)
        
        # Progress indicator
        content_length = len(full_article['content'])
        print(f"  ✓ Extracted {content_length} characters\n")
        
        # Be polite - small delay between requests
        if i < len(articles):
            time.sleep(1)
    
    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(full_articles, f, ensure_ascii=False, indent=2)
    
    print(f"{'='*60}")
    print(f"✓ Saved {len(full_articles)} articles to: {output_file.name}")
    print(f"{'='*60}")
    
    # Statistics
    total_chars = sum(len(a['content']) for a in full_articles)
    avg_chars = total_chars // len(full_articles) if full_articles else 0
    
    print(f"\nStatistics:")
    print(f"  Total content: {total_chars:,} characters")
    print(f"  Average per article: {avg_chars:,} characters")


if __name__ == '__main__':
    main()