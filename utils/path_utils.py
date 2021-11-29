import os
from pathlib import Path

import rootpath


class Paths:
    """
    Class for easy access to necessary directories of current repository
    """

    @staticmethod
    def root() -> Path:
        return Paths._ensure_exists(Path(rootpath.detect()))

    @staticmethod
    def outputs(save_path='output') -> Path:
        return Paths._ensure_exists(Paths.root() / save_path)

    @staticmethod
    def _ensure_exists(path: Path) -> Path:
        path.mkdir(exist_ok=True, parents=True)
        return path

    @staticmethod
    def photo() -> Path:
        return Paths.root() / 'photo'

    @staticmethod
    def data_passport() -> Path:
        return Paths.root() / 'dataPassport'

    @staticmethod
    def backgrounds() -> Path:
        return Paths.root() / 'background'

    @staticmethod
    def fonts() -> Path:
        return Paths.root() / 'fonts'

    @staticmethod
    def signs() -> Path:
        return Paths.root() / 'signs'


class Resources:
    """
    Class for access to necessary files of current repository
    """

    @staticmethod
    def fonts() -> list:
        fonts_path = Paths.root() / 'fonts'
        return [str(fonts_path / img) for img in os.listdir(fonts_path)]

    @staticmethod
    def file_dataset(key) -> str:
        return str(Paths.data_passport() / str(key + '.txt'))

    @staticmethod
    def photo_male() -> list:
        male_path = Paths.photo() / 'male'
        return [str(male_path / img) for img in os.listdir(male_path)]

    @staticmethod
    def photo_female() -> list:
        female_path = Paths.photo() / 'female'
        return [str(female_path / img) for img in os.listdir(female_path)]

    @staticmethod
    def signs() -> list:
        signs_path = Paths.signs()
        return [str(signs_path / img) for img in os.listdir(signs_path)]

    @staticmethod
    def crumpled() -> list:
        crumpled_paper_path = Paths.root() / 'crumpled paper'
        return [str(crumpled_paper_path / img) for img in os.listdir(crumpled_paper_path)]

    @staticmethod
    def dataset(key) -> str:
        return str(Paths.data_passport() / str(key + '.txt'))

    @staticmethod
    def dirty() -> list:
        dirty_path = Paths.root() / 'dirty'
        return [str(dirty_path / img) for img in os.listdir(dirty_path)]

    @staticmethod
    def numbers_font() -> str:
        return str(Paths.fonts() / 'a_SeriferNr_Bold.ttf')

    @staticmethod
    def background() -> list:
        backgrounds_path = Paths.backgrounds()
        return [str(backgrounds_path / img) for img in os.listdir(backgrounds_path) if img.split('.')[-1] != 'json']

    @staticmethod
    def driver(browser='Firefox') -> str:
        if browser == 'Firefox':
            return str(Paths.root() / 'geckodriver')
        elif browser == 'Chrome':
            return str(Paths.root() / 'chromedriver')
