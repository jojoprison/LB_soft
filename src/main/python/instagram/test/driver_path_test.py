from selenium import webdriver

from utility.paths import get_resources_path
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


if __name__ == '__main__':
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    # driver = webdriver.Firefox(executable_path=GeckoDriverManager(cache_valid_range=7).install())
    # driver = webdriver.Firefox(executable_path=f'{get_resources_path()}\\drivers\\geckodriver.exe')
    # path = f'{get_resources_path()}\\drivers\\chromedriver.exe'
    # print(path)

    # driver.get('https://www.instagram.com/qb_pchelovod/')
