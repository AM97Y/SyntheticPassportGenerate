from enum import Enum


class Sex(Enum):
    MALE = 'МУЖ.'
    FEMALE = 'ЖЕН.'

    def __str__(self):
        return str(self.value)
