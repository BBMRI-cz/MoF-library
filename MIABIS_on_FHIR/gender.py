"""This module contains a class for patient's gender"""
from enum import Enum


class MoFGender(Enum):
    """Enum for expressing patient's gender"""
    MALE = 1
    FEMALE = 2
    OTHER = 3
    UNKNOWN = 4

    @classmethod
    def list(cls):
        """List all possible gender values"""
        return list(map(lambda c: c.name, cls))

    @classmethod
    def from_string(cls, value: str):
        try:
            return cls[value.upper()]
        except KeyError:
            raise ValueError(f"'{value}' is not a valid gender")


def get_gender_from_abbreviation(gender: str) -> MoFGender:
    match gender.upper():
        case "F":
            return MoFGender.FEMALE
        case "M":
            return MoFGender.MALE
        case "O":
            return MoFGender.OTHER
        case _:
            return MoFGender.UNKNOWN
