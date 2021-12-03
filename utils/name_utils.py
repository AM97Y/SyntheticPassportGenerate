from pymorphy2 import MorphAnalyzer
import pandas as pd

from utils.path_utils import Paths


def load_names(sex: str) -> list:
    """
    This function returns names by sex

    :param sex: sex of person
    :return: list of corresponding names
    """
    names_file = 'male_names.csv' if sex else 'female_names.csv'
    df = pd.read_csv(Paths.data_passport() / names_file, ';')
    return df[df.PeoplesCount > 20000]['Name'].tolist()


def get_sex(name: str) -> str:
    """
    This function returns gender by name

    :param name: person name
    :return: sex of person
    """
    df = pd.read_csv(Paths.data_passport() / 'male_names.csv', ';')
    if df.loc[df.Name == name].count()['Name'] > 0:
        return "МУЖ."
    else:
        return "ЖЕН."


def gender_format(text: str, sex: str) -> str:
    """
    This function returns the first, middle or last name in the correct gender
    
    :param text: first, middle or last name
    :param sex: gender for format
    :return: gender correct word
    """
    parsed = MorphAnalyzer().parse(text)
    gender = 'femn' if sex == "ЖЕН." else 'masc'
    return (parsed[0].inflect({gender, 'nomn'}) or parsed[0]).word.title()
