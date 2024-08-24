import requests
import json
from urllib.parse import urljoin

def fetch_wordpress_posts(base_url, post_type='posts'):
    api_url = urljoin(base_url, f'/wp-json/wp/v2/{post_type}')
    posts = []
    page = 1
    per_page = 100  # Maximum allowed by WordPress API

    while True:
        response = requests.get(api_url, params={'page': page, 'per_page': per_page})
        if response.status_code != 200:
            break

        page_posts = response.json()
        if not page_posts:
            break

        posts.extend(page_posts)
        page += 1

    return posts

def save_posts_to_file(posts, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    base_url = "https://sonofcauverybook.in"  # Replace with your WordPress site URL
    posts = fetch_wordpress_posts(base_url)
    print(f"Fetched {len(posts)} posts")
    
    save_posts_to_file(posts, 'wordpress_posts.json')
    print(f"Saved posts to wordpress_posts.json")