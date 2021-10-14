from pathlib import Path

import rootpath


class Paths:
    """
    Class for easy access to necessary directories of current repositories
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
    def datapassport():
        return Paths.root() / 'dataPassport'

    @staticmethod
    def outputs():
        return Paths.root() / 'output'

    @staticmethod
    def _ensure_exists(path: Path) -> Path:
        path.mkdir(exist_ok=True, parents=True)
        return path
