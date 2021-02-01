
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

URL_BASE = 'https://www.speedrun.com/mk8dx'
URL_CAT = '48_Tracks'

(DRV, OUT) = ('./driver/chromedriver', './data/')
(TRK, SPD, ITM) = ('Nitro', '200cc', 'NoItems')
# Load driver and mainpage ----------------------------------------------------
print('* Loading selenium scraper...')
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(DRV, options=chrome_options)
driver.get(URL_BASE)
# Select category -------------------------------------------------------------

# Parse table -----------------------------------------------------------------
table = driver.find_elements_by_tag_name('tr')

i = 1
row = table[i]
entry = row.find_elements_by_tag_name('td')
(rank, name, time, _, version, dateDiff, _) = [j.text for j in entry]
