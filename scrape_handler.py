import time
import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# chrome_options.add_argument("--headless=new")
# chrome_options.binary_location = '/opt/homebrew/bin/chromedriver'

def scrape(url: str):
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(5)

        driver.get('https://www.similarweb.com/')

        time.sleep(1)

        search = driver.find_element(By.CLASS_NAME, 'hm-hero__search')
        search = search.find_element(By.CLASS_NAME, 'app-search__input')

        time.sleep(1)

        search.send_keys(url)

        time.sleep(1)

        search.submit()

        category = driver.find_element(By.CSS_SELECTOR, 'button.wa-tabs__button:nth-child(1) > small:nth-child(2)').text

        engajamentsRaw = driver.find_elements(By.CLASS_NAME, 'engagement-list__item')
        engajaments = []
        for engagement in engajamentsRaw:
            name = engagement.find_element(By.CLASS_NAME, 'engagement-list__item-name')
            value = engagement.find_element(By.CLASS_NAME, 'engagement-list__item-value')
            
            if (name.text, value.text) not in engajaments:
                engajaments.append((name.text, value.text))

        countries = [i.find_element(By.CLASS_NAME, 'wa-geography__country-name').text for i in driver.find_elements(By.CLASS_NAME, 'wa-geography__country.wa-geography__legend-item')]

        femalePercentage = driver.find_element(By.CLASS_NAME, 'wa-demographics__gender-legend-item.wa-demographics__gender-legend-item--female').find_element(By.CLASS_NAME, 'wa-demographics__gender-legend-item-value').text
        malePercentage = driver.find_element(By.CLASS_NAME, 'wa-demographics__gender-legend-item.wa-demographics__gender-legend-item--male').find_element(By.CLASS_NAME, 'wa-demographics__gender-legend-item-value').text

        ranksRaw = driver.find_elements(By.CLASS_NAME, 'wa-rank-list__value-container')
        ranks = []
        for rank in ranksRaw:
            a = rank.find_element(By.TAG_NAME, 'p')
            b = rank.find_element(By.TAG_NAME, 'span')
            ranks.append((a.text, b.text))

        driver.quit()
        
        return {
            'category' : category,
            'engajaments' : engajaments,
            'countries' : countries,
            'femalePercentage' : femalePercentage,
            'malePercentage' : malePercentage,
            'ranks' : ranks,
            'error' : False
        }
    except:
        return {
            'category' : '',
            'engajaments' : [],
            'countries' : [],
            'femalePercentage' : '',
            'malePercentage' : '',
            'ranks' : [],
            'error' : True
        }
