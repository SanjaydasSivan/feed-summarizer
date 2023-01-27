import fastapi
from fastapi.responses import HTMLResponse
from summarizer import getLlatestArticles
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = fastapi.FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

apiKey = '5707e0ccd82c4f92bdfbdbc731f574e8'

@app.get('/', response_class=HTMLResponse)
def index():
    # render index.html
    return """
    <head>
        <link rel="stylesheet" href="/static/styles.css">
    </head>
    <div class="home">
    <h1 style="margin-left:10px">Energy Data Feed</h1>
    <form action="/search" method="get">
        <input type="text" name="query" placeholder="Search">
        <input type="submit" value="Search">
    </form>
    </div>
    """

def format_article(article):
    return f"""
    <head>
        <link rel="stylesheet" href="/static/styles.css">
    </head>
    <div class='article'>
    <h1 class='title'">{article.get('title')}</h1>
    <p>{article.get('description')}</p>
    <p>{article.get('summary')}</p>
    <a href="{article.get('url')}">Read More</a>
    </div>
    """

@app.get('/search')
def search(query):
    if not query:
        return HTMLResponse(index())
    articles = getLlatestArticles(3, q=query, apiKey=apiKey)
    formatted_articles = [format_article(article) for article in articles]
    formatted_articles.reverse()
    html_content = """
    <h1 style="margin-left:10px">Summaries of feeds on the topic of "{}"</h1>""".format(query) + ''.join(formatted_articles)

    return HTMLResponse(content=html_content)
