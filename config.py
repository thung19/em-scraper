HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

REGEX_PATTERNS = [
    r"^/[\d]{4}/[\d]{2}/[\d]{2}/[a-z0-9-]+(/[a-z0-9-]+)*$",
    r"^/[\d]{4}/[\d]{2}/[\d]{2}/[a-z0-9/-]+$",
    r"^/[\d]{4}/[\d]{2}/[\d]{2}/[a-z]+(?:/[a-z]+)*/[a-z0-9-]+$",
    r"/\d{4}/\d{2}/\d{2}/",
    r"\b\d{8}\b"
]

HOME_KEYWORDS = ["news", "article", "articles", "stories", "story", "press", "releases" ]

EM_KEYWORDS = [
    "FEMA", "NJEMA", "earthquake", "storm", "flood",
    "shooting", "bomb", "hospital", "disaster",
    "Federal Emergency Management Agency", "CDC", "Centers for Disease Control and Prevention"
]

POSSIBLE_CLASSES = [
    "articleBody", "ArticleBody", "article-body", "article-content",
    "article__content", "story-body", "entry-content", "field--name-body", "post-content"
]

DATE_ATTRS = [{"property": "article:published_time"},
    {"name": "pubdate"},
    {"name": "publishdate"},
    {"name": "timestamp"},
    {"name": "DC.date.issued"},
    {"name": "date"},
    {"itemprop": "datePublished"},
    {"name": "sailthru.date"},
    {"name": "article.published"},
    {"property": "og:published_time"},
    {"name": "dc.date"},
    {"property": "article:published_time"},
    {"property": "lastPublishedDate",
     "property": "og:updated_time"}
]

BS4_URLS = ["https://www.cnn.com", 
            "https://www.bbc.com", 
            "https://apnews.com/us-news", 
            "https://www.nbcnews.com/us-news",
            "https://abcnews.go.com/",
            "https://www.nj.com/healthfit/",
            "https://www.nj.com/"]

NATIONAL_URLS = ["https://www.cnn.com", 
            "https://www.bbc.com", 
            "https://apnews.com/us-news", 
            "https://www.nbcnews.com/us-news",
            "https://abcnews.go.com/",
            "https://www.nbcnews.com/us-news",]

NJ_URLS = ["https://www.nj.com/healthfit/",
            "https://www.nj.com/",
            "https://www.northjersey.com/news/"]

GOV_URLS = ["https://www.fema.gov/about/news-multimedia/press-releases"

]

ALL_URLS = ["https://www.cnn.com", 
            "https://www.bbc.com", 
            "https://apnews.com/us-news", 
            "https://www.fema.gov/about/news-multimedia/press-releases", 
            "https://www.nbcnews.com/us-news",
            "https://abcnews.go.com/",
            "https://www.nj.com/healthfit/",
            "https://www.nj.com/",
            "https://www.northjersey.com/news/"]