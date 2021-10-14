from enum import Enum


class Sex(Enum):
    MALE = 'МУЖ.'
    FEMALE = 'ЖЕН.'

    def upper(self):
        return self.value.upper()

    def __str__(self):
        return str(self.value)