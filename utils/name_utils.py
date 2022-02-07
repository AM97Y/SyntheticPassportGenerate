import pandas as pd

from utils.path_utils import Paths


def load_names(sex: str) -> list:
    """
    This function returns names by sex

    :param sex: sex of person
    :return: list of corresponding names
    """
    names_file = 'male_names.csv' if sex == 'МУЖ.' else 'female_names.csv'
    df = pd.read_csv(Paths.data_passport() / names_file, ';')
    return df[df.Popularity > -110]['Name'].tolist()


def load_surnames(sex: str) -> list:
    """
    This function returns surnames by sex

    :param sex: sex of person
    :return: list of corresponding surnames
    """
    surnames_file = 'male_surnames.txt' if sex == 'МУЖ.' else 'female_surnames.txt'
    with open(Paths.data_passport() / surnames_file, 'r', encoding='utf-8') as f:
        data = f.readlines()
    return data


def load_patronymics(sex: str) -> list:
    """
    This function returns patronymics by sex

    :param sex: sex of person
    :return: list of corresponding patronymics
    """
    patronymics_file = 'male_patronymics.txt' if sex == 'МУЖ.' else 'female_patronymics.txt'
    with open(Paths.data_passport() / patronymics_file, 'r', encoding='utf-8') as f:
        data = f.readlines()
    return data


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
