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

        # Creating an aggregate to access details about the news article through the class NewsArticleDetails. This allows the class NewsContent
        #to act as the root of the aggregate, and the class NewsArticleDetails acts as an entity.
        def article_details(self):
            access_to_newsarticledetails = NewsArticleDetails(self.title, self.author, self.description, self.published_at, self.seed_source)

class NewsArticleDetails:
    def __intit__(
            self,
            title="",
            author="",
            description="",
            published_at=None,
            seed_source=None,
    ):
        self.title = title
        self.author = author
        self.description = description
        self.published_at = published_at
        self.seed_source = seed_source