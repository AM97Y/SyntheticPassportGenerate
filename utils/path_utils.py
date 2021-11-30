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
