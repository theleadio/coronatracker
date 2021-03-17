#Aggregate root for GlobalTimes_scraping and date_convertor.py
class date_and_time:

    import GlobalTimes_scraping
    import date_converter
    import pandas as pd


def __init__(self)
    pass

def get_globalTimes(self):
    now = datetime.datetime.now()
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome('chromedriver', options=chrome_options)
    driver.get("https://www.globaltimes.cn/content/1177737.shtml")
    WebDriverWait(driver,100000000).until(EC.presence_of_element_located((By.XPATH,'//*[@id="left"]/div[4]/div')))
    news= driver.find_element_by_css_selector('#left > div:nth-child(4) > div')
    row=0
    col=0
    data=[]
    df=news.text
    data=df.splitlines()
    #delete unrelevant data
    while ("" in data):
        data.remove("")
    del data[0]
    del data[-1]
    del data[-1]
    del data[-1]
    del data[-1]
    df=pd.DataFrame(data)
    df.to_csv('GlobalTimes.csv',index=False,header=False)
    print("done")

def get_date(self):
    str = "Sat, 25 Jan 2020 01:52:22 +2000"
    all = re.findall(r"[\d]{1,2} [ADFJMNOS]\w* [\d]{4} \b(?:[01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9] [\+]{1}[0-9]{4}\b", str)

    datetime_str = all[0] # '09/19/18 13:55:26'

    datetime_object = datetime.strptime(datetime_str, '%d %b %Y %H:%M:%S %z')

    print(type(datetime_object))
    print(datetime_object)  # printed in default format
    print(datetime_object.astimezone(timezone.utc))
