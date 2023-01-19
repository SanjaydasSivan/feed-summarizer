import requests
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

def summarize_html(url: str, sentences_count: int, language: str = 'english') -> str:
    """
    Summarizes text from URL
    """
    parser = HtmlParser.from_url(url, Tokenizer(language))
    stemmer = Stemmer(language)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(language)

    summary = ''
    for sentence in summarizer(parser.document, sentences_count):
        if not summary:
            summary += str(sentence)
        else:
            summary += ' ' + str(sentence)

    return summary


def news_api_request(url: str, **kwargs) -> list:
    """
    Sends GET request to News API endpoint
    """
    params = kwargs
    res = requests.get(url, params=params)
    articles = res.json().get('articles')
    return articles


def summarize_news_api(articles: list, sentences_count: int) -> list:
    """
    Summarizes text at each URL in articles
    """
    for article in articles:
        summary = summarize_html(article.get('url'), sentences_count)
        article.update({'summary': summary})

    return articles


def get_headlines(sentences_count: int, **kwargs) -> list:
    """
    Sends GET request to News API /v2/top-headlines endpoint,
    """
    url = 'https://newsapi.org/v2/top-headlines/'
    articles = news_api_request(url, **kwargs)
    return summarize_news_api(articles, sentences_count)
