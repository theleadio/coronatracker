
class INewsBuilder():
    # Interface for the news builder method
    # Insted of making abstract I just put pass (null statement) for interface
    def set_title():
        pass
    
    def set_description():
        pass
    
    def set_author():
        pass

    def set_url():
        pass
    
    def set_content():
        pass

    def set_urlToImage():
        pass

    def set_publishedAt():
        pass
    
    def set_addedOn():
        pass
    
    def set_siteName():
        pass
    
    def set_language():
        pass
    
    def set_countryCode():
        pass
    
    def get_news():
        pass
    # def set_title(self, title):

    
    # def set_description(self, description):

       
    # def set_author(self, author):
        

    # def set_url(self, url):
        
    
    # def set_content(self, content):
       

    # def set_urlToImage(self, urlToImage):
        

    # def set_publishedAt(self, publishedAt):
       
    
    # def set_addedOn(self, addedOn):
        
    
    # def set_siteName(self, siteName):
        
    
    # def set_language(self, language):
        
    
    # def set_countryCode(self, countryCode):

    
    # def get_news(self):


class newsBuilder(INewsBuilder):
    # Implement the interface to build the news article object
    
    def __init__(self):
        self.news = News()
    
    def set_title(self, title):
        self.news.title = title
        return self
    
    def set_description(self, description):
        self.news.description = description
        return self
    
    def set_author(self, author):
        self.news.author = author
        return self

    def set_url(self, url):
        self.news.url = url
        return self
    
    def set_content(self, content):
        self.news.content = content
        return self

    def set_urlToImage(self, urlToImage):
        self.news.urlToImage = urlToImage
        return self

    def set_publishedAt(self, publishedAt):
        self.news.publishedAt = publishedAt
        return self
    
    def set_addedOn(self, addedOn):
        self.news.addedOn = addedOn
        return self
    
    def set_siteName(self, siteName):
        self.news.siteName = siteName
        return self
    
    def set_language(self, language):
        self.news.language = language
        return self
    
    def set_countryCode(self, countryCode):
        self.news.countryCode = countryCode
        return self
    
    # Return the news article information 
    def get_news(self):
        return self.news

class News():
    # Initialise the news article as an empty list
    def __init__(self):
        self.news = []
    
    # Return the list of news article parts
    def __str__(self):
        return self.news


class Builder:
    # This builds the news stories that are brought htrough the news scraper
    def construct(title, description, author, url, content, urlToImage, publishedAt, addedOn, siteName, language, countryCode):
        return (newsBuilder().set_title(title).set_description(description).set_author(author).set_url(url).set_content(content).set_urlToImage(urlToImage)
                    .set_publishedAt(publishedAt).set_addedOn(addedOn).set_siteName(siteName).set_language(language).set_countryCode(countryCode).get_news())



# Method for testing the python script
# if __name__ == "__main__":
#     TEST = Builder.construct('News Article', 'this is a test article', 'ye', 'ye', 'ye', 'ye', 'ye', 'ye', 'ye', 'ye', 'ye')
#     print(TEST.title)