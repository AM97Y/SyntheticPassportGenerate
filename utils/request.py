#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from datetime import datetime
import pandas as pd

from utils.path_utils import Paths

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


def get_data(browser: str, path_driver: str) -> dict:
    """
    This function returns a dict with unique downloaded data from requests.
    browser: type browser - Chrome or Firefox.
    path_driver: driver location.
    number_requests: number requests from https://www.random1.ru/generator-pasportnyh-dannyh.
    return: Dict with unique downloaded data from requests.
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

    data = {'first_name': '',
            'second_name': '',
            'patronymic_name': '',
            'address': '',
            'series_passport': 0,
            'number_passport': 0,
            'department_code': [0, 0],
            'department': '',
            'date_birth': '',
            'date_issue': '',
            'sex': '',
            'images': {'photoLabel': '',
                       'officersignLabel': '',
                       'ownersignLabel': '',
                       'background': ['', {}]
                       }
            }
    driver.get(URL)
    # Extract passport data generated on the web page.
    for name in NAMES:
        value = driver.find_element_by_xpath(f'//input[@id="{name}"]').get_attribute('value')
        # Information about accommodation is divided into the city and the address itself
        if name == 'Address':
            city = value.split(",")[1]
            data.update({'address': city})
        elif name == 'PasportNum':
            series_passport, number_passport = value.split(' ')
            data.update({'series_passport': int(series_passport)})
            data.update({'number_passport': int(number_passport)})
        elif name == "PasportDate" or name == "DateOfBirth":
            data.update({NAMES[name]: datetime.strptime(str(value), "%d.%m.%Y")})
        elif name == 'PasportCode':
            data.update({NAMES[name]: value.split('-')})
        else:
            data.update({NAMES[name]: value})
    data.update({'sex': get_sex(data['first_name'])})
    return data


def get_sex(name: str) -> str:
    df = pd.read_csv(Paths.data_passport() / 'male_names.csv', ';')
    if df.loc[df.Name == name].count()['Name'] > 0:
        sex = "МУЖ."
    else:
        sex = "ЖЕН."
    return sex
