from dateutil import parser as date_parser
from datetime import date

from miabis_model.util.constants import DETAILED_MATERIAL_TYPE_TO_COLLECTION_MATERIAL_TYPE_MAP


def get_nested_value(data: dict, keys: list):
    for key in keys:
        if isinstance(data, list) and isinstance(key, int):
            data = data[key] if key < len(data) else None
        else:
            data = data.get(key) if data else None
        if data is None:
            return None
    return data


def parse_reference_id(reference: str) -> str:
    """Helper method to parse reference id."""
    return reference.split("/")[-1]


def parse_contact(contact: dict) -> dict:
    """Helper method to parse contact information."""
    return {
        "name": contact.get("name", {}).get("given", [None])[0],
        "surname": contact.get("name", {}).get("family", None),
        "email": contact.get("telecom", [{}])[0].get("value", "")
    }


def parse_date_from_string(date_str: str) -> date:
    """Parse date from string."""
    return date_parser.parse(date_str).date()


def get_material_type_from_detailed_material_type(detailed_material_type: str) -> str:
    return DETAILED_MATERIAL_TYPE_TO_COLLECTION_MATERIAL_TYPE_MAP.get(detailed_material_type, None)
