import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

def fetch_wikipedia_mos_api():
    """
    Fetch Wikipedia Manual of Style using official Wikipedia API
    
    Uses MediaWiki API: https://www.mediawiki.org/wiki/API:Main_page
    Wikipedia content is licensed under CC BY-SA 4.0
    """
    
    # Wikipedia API endpoint
    api_url = "https://en.wikipedia.org/w/api.php"
    
    # API parameters
    params = {
        "action": "parse",
        "page": "Wikipedia:Manual_of_Style",
        "format": "json",
        "prop": "text",
        "formatversion": "2"
    }
    
    # IMPORTANT: Add User-Agent header (Wikipedia requires this)
    headers = {
        "User-Agent": "StyleGuideBot/1.0 (Educational project; <EMAIL>)"
    }
    
    print("Fetching from Wikipedia API...")
    print(f"   Page: {params['page']}")
    
    response = requests.get(api_url, params=params, headers=headers)
    response.raise_for_status()
    
    data = response.json()
    
    # Check if page exists
    if "parse" not in data:
        raise ValueError(f"Page not found or API error: {data}")
    
    html_content = data["parse"]["text"]
    page_title = data["parse"]["title"]
    
    print(f"Retrieved page: {page_title}")
    
    return html_content, page_title

def parse_html_content(html_content):
    """
    Parse HTML content into structured sections
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    sidebars = soup.find_all("table", class_="sidebar")
    for sidebar in sidebars:
        sidebar.decompose()
    
    sections = []
    current_section = {
        "title": "Introduction",
        "content": "",
        "level": 1,
        "shortcuts": []
    }
    
    # Find all headings and content
    for element in soup.find_all(['h2', 'h3', 'h4', 'p', 'ul', 'ol']):
        if element.name in ['h2', 'h3', 'h4']:
            # Save previous section if it has content
            sections.append(current_section)
            
            # Get heading text and clean it
            heading_text = element.get_text()
            # Remove [edit] links and brackets
            heading_text = heading_text.replace('[edit]', '').strip()
            
            # Start new section
            level = int(element.name[1])  # h2 -> 2, h3 -> 3
            current_section = {
                "title": heading_text,
                "content": "",
                "level": level,
                "shortcuts": []
            }
            
        elif element.name in ['p', 'ul', 'ol']:
            if element.name == 'ul':
                if 'plainlist' in element.parent.get('class', []):
                    list_items = element.find_all('li')
                    for item in list_items:
                        shortcut = item.find('a')
                        if shortcut:
                            text = shortcut.get_text().strip()
                            current_section["shortcuts"].append(text)
                    continue

            # Add content to current section
            text = element.get_text().strip()
            
            # Skip very short paragraphs and navigation elements
            if text and len(text) > 10 and not text.startswith('Retrieved from'):
                current_section["content"] += text + "\n\n"
    
    # Add last section
    sections.append(current_section)
    
    return sections

def scrape_wikipedia_mos():
    """
    Main function to scrape and save Wikipedia Manual of Style
    """
    try:
        # Fetch content via API
        html_content, page_title = fetch_wikipedia_mos_api()
        
        # Parse HTML into sections
        print("\n🔍 Parsing content...")
        sections = parse_html_content(html_content)
        
        # Create metadata
        metadata = {
            "source": "Wikipedia Manual of Style",
            "page_title": page_title,
            "url": "https://en.wikipedia.org/wiki/Wikipedia:Manual_of_Style",
            "api_url": "https://en.wikipedia.org/w/api.php",
            "license": "CC BY-SA 4.0",
            "scraped_at": datetime.now().isoformat(),
            "total_sections": len(sections)
        }
        
        # Prepare output data
        output_data = {
            "metadata": metadata,
            "sections": sections
        }
        
        # Save to JSON
        output_dir = "./data"
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, "wikipedia_mos_raw.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        # Print statistics
        total_chars = sum(len(s['content']) for s in sections)
        avg_length = total_chars // len(sections) if sections else 0
        
        print(f"\n✅ Scraped {len(sections)} sections")
        print(f"✅ Saved to {output_file}")
        print(f"\n📊 Stats:")
        print(f"   - Total characters: {total_chars:,}")
        print(f"   - Average section length: {avg_length:,} chars")
        print(f"   - License: {metadata['license']}")
        
        return output_data
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Network error: {e}")
        raise
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise

if __name__ == "__main__":
    try:
        data = scrape_wikipedia_mos()
        
        # Print preview
        if data['sections']:
            print("\n📄 Preview of first section:")
            print(f"   Title: {data['sections'][0]['title']}")
            print(f"   Level: {data['sections'][0]['level']}")
            print(f"   Content: {data['sections'][0]['content'][:200]}...")
        
        print("\n🎉 Scraping complete!")
        print("\n💡 Attribution: Wikipedia contributors, CC BY-SA 4.0")
        
    except Exception as e:
        print(f"\n❌ Failed to scrape: {e}")
        exit(1)