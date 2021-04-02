import dbFactory.MySQL_Connector



def insert_news_article(self, data_dict, table_name):

        ''' NEWS TABLE_SCHEMA
            ['nid', 'title', 'description', 'author', 'url', 'content', 'urlToImage', 'publishedAt', 'addedOn', 'siteName', 'language', 'countryCode', 'status']
        '''

        query = "INSERT INTO {} (title, description, author, url, content, urlToImage, publishedAt, addedOn, siteName, language, countryCode, status) \
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE title = %s, description = %s, author = %s, content = %s, \
                urlToImage = %s, publishedAt = %s, addedOn = %s, siteName = %s, language = %s, countryCode = %s".format(table_name)

        val = (
            data_dict["title"],
            data_dict["description"],
            data_dict["author"],
            data_dict["url"],
            data_dict["content"],
            data_dict["urlToImage"],
            data_dict["publishedAt"],
            data_dict["addedOn"],
            data_dict["siteName"],
            data_dict["language"],
            data_dict["countryCode"],
            1,  # Status
            data_dict["title"],
            data_dict["description"],
            data_dict["author"],
            data_dict["content"],
            data_dict["urlToImage"],
            data_dict["publishedAt"],
            data_dict["addedOn"],
            data_dict["siteName"],
            data_dict["language"],
            data_dict["countryCode"],
        )

    # worldometers TABLE_SCHEMA
    # country, total_cases, total_deaths, total_recovered, total_tests, new_cases, new_deaths, active_cases, serious_critical_cases, total_cases_per_million_pop, total_tests_per_million_pop, last_updated
def insert_worldometer_stats(self, data_dict, table_name):

        sql = "INSERT INTO {} (country, total_cases, total_deaths, total_recovered, total_tests, new_cases, new_deaths, active_cases, serious_critical_cases, total_cases_per_million_pop, total_deaths_per_million_pop, total_tests_per_million_pop, last_updated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE country = %s, total_cases = %s, total_deaths = %s, total_recovered = %s, total_tests = %s, new_cases = %s, new_deaths = %s, active_cases = %s, serious_critical_cases = %s, total_cases_per_million_pop = %s, total_deaths_per_million_pop = %s, total_tests_per_million_pop = %s".format(
            table_name
        )
        val = (
            data_dict["country"],
            data_dict["total_cases"],
            data_dict["total_deaths"],
            data_dict["total_recovered"],
            data_dict["total_tests"],
            data_dict["new_cases"],
            data_dict["new_deaths"],
            data_dict["active_cases"],
            data_dict["serious_critical_cases"],
            data_dict["total_cases_per_million_pop"],
            data_dict["total_deaths_per_million_pop"],
            data_dict["total_tests_per_million_pop"],
            data_dict["last_updated"],
            data_dict["country"],
            data_dict["total_cases"],
            data_dict["total_deaths"],
            data_dict["total_recovered"],
            data_dict["total_tests"],
            data_dict["new_cases"],
            data_dict["new_deaths"],
            data_dict["active_cases"],
            data_dict["serious_critical_cases"],
            data_dict["total_cases_per_million_pop"],
            data_dict["total_deaths_per_million_pop"],
            data_dict["total_tests_per_million_pop"],
        )

    # worldometers_total_sum TABLE_SCHEMA
    # total_cases, total_deaths, total_recovered, total_tests, new_cases, new_deaths, active_cases, serious_critical_cases, total_cases_per_million_pop, total_deaths_per_million_pop, total_tests_per_million_pop, last_updated
def insert_worldometers_total_sum(self, data_dict, table_name):

        sql = "INSERT INTO {} (total_cases, total_deaths, total_recovered, total_tests, new_cases, new_deaths, active_cases, serious_critical_cases, total_cases_per_million_pop, total_deaths_per_million_pop, total_tests_per_million_pop, last_updated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE total_cases = %s, total_deaths = %s, total_recovered = %s, total_tests = %s, new_cases = %s, new_deaths = %s, active_cases = %s, serious_critical_cases = %s, total_cases_per_million_pop = %s, total_deaths_per_million_pop = %s, total_tests_per_million_pop = %s".format(
            table_name
        )
        val = (
            data_dict["total_cases"],
            data_dict["total_deaths"],
            data_dict["total_recovered"],
            data_dict["total_tests"],
            data_dict["new_cases"],
            data_dict["new_deaths"],
            data_dict["active_cases"],
            data_dict["serious_critical_cases"],
            data_dict["total_cases_per_million_pop"],
            data_dict["total_deaths_per_million_pop"],
            data_dict["total_tests_per_million_pop"],
            data_dict["last_updated"],
            data_dict["total_cases"],
            data_dict["total_deaths"],
            data_dict["total_recovered"],
            data_dict["total_tests"],
            data_dict["new_cases"],
            data_dict["new_deaths"],
            data_dict["active_cases"],
            data_dict["serious_critical_cases"],
            data_dict["total_cases_per_million_pop"],
            data_dict["total_deaths_per_million_pop"],
            data_dict["total_tests_per_million_pop"],
        )