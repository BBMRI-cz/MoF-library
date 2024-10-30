from enum import Enum


class StorageTemperature(Enum):
    """Enum for expressing storage temperature of a sample:
    2 to 10 degrees Celsius
    -18 to -35 degrees Celsius
    -60 to -85 degrees Celsius
    Gaseous Nitrogen
    Liquid Nitrogen
    Room temperature
    Other storage temperature"""
    TEMPERATURE_2_TO_10 = "2to10"
    TEMPERATURE_MINUS_18_TO_MINUS_35 = "-18to-35"
    TEMPERATURE_MINUS_60_TO_MINUS_85 = "-60to-85"
    TEMPERATURE_LN = "LN"
    TEMPERATURE_ROOM = "RT"
    TEMPERATURE_OTHER = "Other"

    @classmethod
    def list(cls):
        """List all possible storage temperature values"""
        return list(map(lambda c: c.name, cls))


def parse_storage_temp_from_code(storage_temp_map: dict, code: str) -> StorageTemperature | None:
    if code not in storage_temp_map:
        return None
    storage_temp = storage_temp_map.get(code)
    if storage_temp not in StorageTemperature.list():
        return None
    return StorageTemperature[storage_temp]
