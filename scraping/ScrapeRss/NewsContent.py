
class NewsContent:
    def __init__(
        self,
        news_url="",
        title="",
        author="",
        description="",
        published_at=None,
        seed_source=None,
    ):
        self.news_url = news_url
        self.title = title
        self.author = author
        self.description = description
        self.published_at = published_at
        self.seed_source = seed_source
