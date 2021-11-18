from pymorphy2 import MorphAnalyzer
import pandas as pd

from utils.path_utils import Paths


def load_names(sex: str) -> list:
    """
    This function returns names by sex.

    :param sex: Sex of person.
    :return: List of names.
    """
    if sex:
        df = pd.read_csv(Paths.data_passport() / 'male_names.csv', ';')
    else:
        df = pd.read_csv(Paths.data_passport() / 'female_names.csv', ';')
    return df[df.PeoplesCount > 1000]['Name'].tolist()


def get_sex(name: str) -> str:
    """
    This function returns gender by name.

    :param name:
    :return: Sex of person.
    """
    df = pd.read_csv(Paths.data_passport() / 'male_names.csv', ';')
    if df.loc[df.Name == name].count()['Name'] > 0:
        sex = "МУЖ."
    else:
        sex = "ЖЕН."
    return sex


def gender_format(text: str, sex: str) -> str:
    parsed = MorphAnalyzer().parse(text)
    if sex == "ЖЕН.":
        gender = 'femn'
    else:
        gender = 'masc'
    return (parsed[0].inflect({gender, 'nomn'}) or parsed[0]).word.title()
