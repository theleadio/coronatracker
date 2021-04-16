from abc import ABCMeta, abstractmethod
#Builder Interface
class IBuilder(metaclass=ABCMeta):
    "The Builder Interface"

     @abstractstaticmethod
    def set_title():
        pass

    @abstractstaticmethod
    def set_description():
        pass 

     @abstractstaticmethod
    def set_author():
        pass

    @abstractstaticmethod
    def set_url():
        pass

     @abstractstaticmethod
    def set_content():
        pass

     @abstractstaticmethod
    def set_urlToImage():
        pass

     @abstractstaticmethod
    def set_publishedAt():
        pass

     @abstractstaticmethod
    def set_addedOn():
        pass

    @abstractstaticmethod
    def set_language():
        pass

     @abstractstaticmethod
    def set_countryCode():
        pass

      @abstractstaticmethod
    def get_info():
        pass

    class Builder(IBuilder):
        """ the concrete builder."""

        def __init__(self):
            self.info = Info()

        def set_title(self, title):
            self.info.title = title
            return self

        def set_description(self, description):
            self.info.description = description
            return self

        def set_author(self, author):
            self.info.author = author
            return self

        def set_url(self, url):
            self.info.url = url
            return self

        def set_content(self, content):
            self.info.content = content
            return self

        def set_urlToImage(self, urlToImage):
            self.info.urlToImage = urlToImage
            return self

        def set_publishedAt(self, publishedAt):
            self.info.publishedAt = publishedAt
            return self

        def set_addedOn(self, addedOn):
            self.info.addedOn = addedOn
            return self

        def set_siteName(self, siteName):
            self.info.siteName = siteName
            return self

        def set_language(self, language):
            self.info.language = language
            return self

        def set_countryCode(self, countryCode):
            self.info.countryCode = countryCode
            return self

        def get_info(self):
            return self.Info


    class Product():
    """The Product"""

    def __init__(self):
        self.info = []


    class Director:
        @staticmethod
        def construct()
            return Builder()\
                .set_title()\
                .set_description()\
                .set_author()\
                .set_url()\
                .set_content()\
                .set_urlToImage()\
                .set_publishedAt()\
                .set_addedOn()\
                .set_siteName()\
                .set_language()\
                .set_countryCode()\
                .get_info()
    
    