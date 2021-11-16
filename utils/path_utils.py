import os
from pathlib import Path

import rootpath


class Paths:
    """
    Class for easy access to necessary directories of current repository.
    """

    @staticmethod
    def root():
        return Paths._ensure_exists(Path(rootpath.detect()))

    @staticmethod
    def outputs(save_path='output'):
        return Paths._ensure_exists(Paths.root() / save_path)

    @staticmethod
    def _ensure_exists(path: Path) -> Path:
        path.mkdir(exist_ok=True, parents=True)
        return path

    @staticmethod
    def photo():
        return Paths.root() / 'photo'

    @staticmethod
    def data_passport():
        return Paths.root() / 'dataPassport'

    @staticmethod
    def backgrounds():
        return Paths.root() / 'background'

    @staticmethod
    def fonts():
        return Paths.root() / 'fonts'


class Resources:
    """
    Class for .
    """

    @staticmethod
    def fonts():
        fonts_path = Paths.root() / 'fonts'
        return [str(fonts_path / img) for img in os.listdir(fonts_path)]

    @staticmethod
    def file_dataset(key):
        return str(Paths.data_passport() / str(key + '.txt'))

    @staticmethod
    def photo_male():
        male_path = Paths.photo() / 'male'
        return [str(male_path / img) for img in os.listdir(male_path)]

    @staticmethod
    def photo_female():
        female_path = Paths.photo() / 'female'
        return [str(female_path / img) for img in os.listdir(female_path)]

    @staticmethod
    def signs():
        signs_path = Paths.root() / 'signs'
        return [str(signs_path / img) for img in os.listdir(signs_path)]

    @staticmethod
    def crumpled():
        crumpled_paper_path = Paths.root() / 'crumpled paper'
        return [str(crumpled_paper_path / img) for img in os.listdir(crumpled_paper_path)]

    @staticmethod
    def dataset(key):
        return str(Paths.data_passport() / str(key + '.txt'))

    @staticmethod
    def dirty():
        dirty_path = Paths.root() / 'dirty'
        return [str(dirty_path / img) for img in os.listdir(dirty_path)]

    @staticmethod
    def numbers_font():
        return str(Paths.fonts() / 'a_SeriferNr_Bold.ttf')
