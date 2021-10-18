from pathlib import Path

import rootpath


class Paths:
    """
    Class for easy access to necessary directories of current repositories.
    """

    @staticmethod
    def root():
        return Paths._ensure_exists(Path(rootpath.detect()))

    @staticmethod
    def backgrounds():
        return Paths.root() / 'background'

    @staticmethod
    def fonts():
        return Paths.root() / 'fonts'

    @staticmethod
    def data_passport():
        return Paths.root() / 'dataPassport'

    @staticmethod
    def file_dataset(key):
        return str(Paths.data_passport() / str(key + '.txt'))

    @staticmethod
    def photo_male():
        return Paths.root() / 'photo' / 'male'

    @staticmethod
    def photo_female():
        return Paths.root() / 'photo' / 'female'

    @staticmethod
    def signs():
        return Paths.root() / 'signs'

    @staticmethod
    def crumpled():
        return Paths.root() / 'crumpled paper/'

    @staticmethod
    def glares():
        return Paths.root() / 'glares'

    @staticmethod
    def dirty():
        return Paths.root() / 'dirty'

    @staticmethod
    def numbers_font():
        return str(Paths.fonts() / 'a_SeriferNr_Bold.ttf')

    @staticmethod
    def outputs(save_path='output'):
        return Paths.root() / save_path

    @staticmethod
    def _ensure_exists(path: Path) -> Path:
        path.mkdir(exist_ok=True, parents=True)
        return path
