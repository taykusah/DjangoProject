# core/news_utils.py
import requests
from django.conf import settings
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

def get_news_data(category='technology', page_size=5):
    """
    Fetch news from NewsAPI
    """
    api_key = settings.NEWSAPI_KEY
    base_url = "https://newsapi.org/v2/top-headlines"
    
    try:
        response = requests.get(
            base_url,
            params={
                'category': category,
                'language': 'en',
                'pageSize': page_size,
                'apiKey': api_key,
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        articles = []
        for article in data.get('articles', []):
            # Format the date
            published_at = datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
            
            articles.append({
                'title': article['title'],
                'description': article['description'],
                'url': article['url'],
                'image_url': article['urlToImage'],
                'source': article['source']['name'],
                'published_at': published_at.strftime('%B %d, %Y'),
            })
        
        return articles
    
    except requests.RequestException as e:
        logger.error(f"Error fetching news data: {str(e)}")
        return None