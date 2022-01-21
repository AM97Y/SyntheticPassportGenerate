from datetime import datetime
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from utils.name_utils import get_sex

URL: str = 'https://www.random1.ru/generator-pasportnyh-dannyh'
NAMES: dict = {
    'LastName': 'second_name',
    'FirstName': 'first_name',
    'FatherName': 'patronymic_name',
    'DateOfBirth': 'date_birth',
    'PasportNum': ['series_passport', 'number_passport'],
    'PasportCode': 'department_code',
    'PasportOtd': 'department',
    'PasportDate': 'date_issue',
    'Address': 'address',
}


def upload_online_passport_data(data: dict, browser: str, path_driver: str) -> dict:
    """
    This function returns downloaded passport content from request

    :param data: passport content.p
    :param browser: browser type (Chrome or Firefox)
    :param path_driver: path to browser driver
    :return: downloaded passport content
    """

    if browser == 'Firefox':
        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(executable_path=path_driver, firefox_options=options)
    elif browser == 'Chrome':
        options = ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(executable_path=path_driver, chrome_options=options)
    else:
        raise ValueError('use browser Chrome or Firefox')

    driver.get(URL)
    driver.set_page_load_timeout(30)
    time.sleep(5)
    # Extract passport data generated on the web page
    for name in NAMES:
        value = driver.find_element_by_xpath(f'//input[@id="{name}"]').get_attribute('value')
        if name == 'Address':
            # Information about accommodation is divided into the city and the address itself.
            city = value.split(",")[1]
            data.update({'address': city})
        elif name == 'PasportNum':
            series_passport, number_passport = value.split(' ')
            data.update({'series_passport': int(series_passport)})
            data.update({'number_passport': int(number_passport)})
        elif name == "PasportDate" or name == "DateOfBirth":
            data.update({NAMES[name]: datetime.strptime(str(value), "%d.%m.%Y")})
        elif name == 'PasportCode':
            data.update({NAMES[name]: list(map(int, value.split('-')))})
        else:
            data.update({NAMES[name]: value})
    data.update({'sex': get_sex(data['first_name'])})

    del driver
    return data


