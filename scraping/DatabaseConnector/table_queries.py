import json

db_queries = {}

db_queries['bing'] = {
    'environment': {
        'test': 'bing_covid_temp',
        'prod': 'bing_covid'
    },
    'query': '''"INSERT INTO {table_name} (state, country, last_update, lat, lng, confirmed, deaths, recovered, posted_date) VALUES
                ({0}["state"], {0}["country"], {0}["last_update"], {0}["lat"], {0}["lng"], {0}["confirmed"], {0}["deaths"], {0}["recovered"], {0}["posted_date"]) ON DUPLICATE KEY UPDATE 
                state = {0}["state"], country = {0}["country"], confirmed = {0}["confirmed"], deaths = {0}["deaths"], recovered = {0}["recovered"]"''',
}

db_queries['malaysia_states'] = {
    'environment': {
        'test': 'malaysia_states_temp',
        'prod': 'malaysia_states'
    },
    'query': '''"INSERT INTO {table_name} (state, increment_count, total_count, hospital_count, recovered_count, death_count, last_updated) VALUES ({0}["state"], {0}["increment_count"], {0}["total_count"], {0}["hospital_count"], 
                {0}["recovered_count"], {0}["death_count"], {0}["last_updated"]) ON DUPLICATE KEY UPDATE 
                state = {0}["state"], increment_count = {0}["increment_count"], total_count = {0}["total_count"], hospital_count = {0}["hospital_count"], recovered_count = {0}["recovered_count"], death_count = {0}["death_count"]"''',
}

db_queries['malaysia_patient_case'] = {
    'environment': {
        'test': 'malaysia_patient_case_temp',
        'prod': 'malaysia_patient_case'
    },
    'query': '''"INSERT INTO {table_name} (caseId, status, statusDate, confirmedDate, nationality, age, gender, hospital, description) VALUES
                ({0}["case"], {0}["status"], {0}["status_date"], {0}["confirmed_date"], {0}["nationality"], {0}["age"], {0}["gender"], {0}["hospital"], {0}["description"]) ON DUPLICATE KEY UPDATE caseId = {0}["case"], 
                status = {0}["status"], statusDate = {0}["status_date"], confirmedDate = {0}["confirmed_date"], nationality = {0}["nationality"], age = {0}["age"], gender = {0}["gender"], hospital = {0}["hospital"], description = {0}["description"]"''', 
}


db_queries['news'] = {
    'query': '''"INSERT INTO {table_name} (title, description, author, url, content, urlToImage, publishedAt, addedOn, siteName, language, countryCode, status)
                VALUES ({0}["title"], {0}["description"], {0}["author"], {0}["url"], {0}["content"], {0}["urlToImage"], {0}["publishedAt"], {0}["addedOn"], {0}["siteName"], {0}["language"], {0}["countryCode"], 1) ON DUPLICATE KEY 
                UPDATE title = {0}["title"], description = {0}["description"], author = {0}["author"], content = {0}["content"],
                urlToImage = {0}["urlToImage"], publishedAt = {0}["publishedAt"], addedOn = {0}["addedOn"], siteName = {0}["siteName"], language = {0}["language"], countryCode = {0}["countryCode"]"'''
}

db_queries['world_meter'] = {
    'query': '''"INSERT INTO {table_name} (country, total_cases, total_deaths, total_recovered, total_tests, new_cases, new_deaths, active_cases, serious_critical_cases, 
                total_cases_per_million_pop, total_deaths_per_million_pop, total_tests_per_million_pop, last_updated) VALUES ({0}["country"], {0}["total_cases"], {0}["total_deaths"], {0}["total_recovered"], {0}["total_tests"], 
                {0}["new_cases"], {0}["new_deaths"], {0}["active_cases"], {0}["serious_critical_cases"], {0}["total_cases_per_million_pop"], {0}["total_deaths_per_million_pop"], {0}["total_tests_per_million_pop"], 
                {0}["last_updated"]) ON DUPLICATE KEY UPDATE country = {0}["country"], total_cases = {0}["total_cases"], total_deaths = {0}["total_deaths"], total_recovered = {0}["total_recovered"], total_tests = {0}["total_tests"], 
                new_cases = {0}["new_cases"], new_deaths = {0}["new_deaths"], active_cases = {0}["active_cases"], serious_critical_cases = {0}["serious_critical_cases"], total_cases_per_million_pop = {0}["total_cases_per_million_pop"], 
                total_deaths_per_million_pop = {0}["total_deaths_per_million_pop"], total_tests_per_million_pop = {0}["total_tests_per_million_pop"]"'''
}


db_queries['world_meter_total_sum'] = {
    'query': '''"INSERT INTO {table_name} (total_cases, total_deaths, total_recovered, total_tests, new_cases, new_deaths, active_cases, serious_critical_cases, 
                total_cases_per_million_pop, total_deaths_per_million_pop, total_tests_per_million_pop, last_updated) VALUES ({0}["total_cases"], {0}["total_deaths"], {0}["total_recovered"], {0}["total_tests"], 
                {0}["new_cases"], {0}["new_deaths"], {0}["active_cases"], {0}["serious_critical_cases"], {0}["total_cases_per_million_pop"], {0}["total_deaths_per_million_pop"], {0}["total_tests_per_million_pop"], 
                {0}["last_updated"]) ON DUPLICATE KEY UPDATE country = {0}["country"], total_cases = {0}["total_cases"], total_deaths = {0}["total_deaths"], total_recovered = {0}["total_recovered"], total_tests = {0}["total_tests"], 
                new_cases = {0}["new_cases"], new_deaths = {0}["new_deaths"], active_cases = {0}["active_cases"], serious_critical_cases = {0}["serious_critical_cases"], total_cases_per_million_pop = {0}["total_cases_per_million_pop"], 
                total_deaths_per_million_pop = {0}["total_deaths_per_million_pop"], total_tests_per_million_pop = {0}["total_tests_per_million_pop"]"'''
}

db_queries['newsapi'] = {
    'envorinment': {
        'test': 'newsapi_en',
        'prod': 'newsapi_n'
    },
    'query': '''"INSERT INTO {table_name} (title, description, author, url, content, urlToImage, publishedAt, addedOn, siteName, language, countryCode, status) VALUES ({0}["title"], {0}["description"], {0}["author"], 
                {0}["url"], {0}["content"], {0}["urlToImage"], {0}["publishedAt"], {0}["addedOn"], {0}["siteName"], {0}["language"], {0}["countryCode"], 1) ON DUPLICATE KEY UPDATE title = {0}["title"], 
                description = {0}["description"], author = {0}["author"], content = {0}["content"], urlToImage = {0}["urlToImage"], publishedAt = {0}["publishedAt"], addedOn = {0}["addedOn"], 
                siteName = {0}["siteName"], language = {0}["language"], countryCode = {0}["countryCode"]"'''
}
