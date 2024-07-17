from fhirclient.models import list as fhir_list
from fhirclient.models.fhirreference import FHIRReference


class MoFSpecimenList:
    """Class representing a list of specimens in a collection."""
    def __init__(self, collection_identifier: str, specimen_identifiers: list[str], name: str = None):
        """
        :param name: Name of the specimen list
        :param collection_identifier: Identifier of the collection
        :param specimens_ids: List of specimen identifiers
        """
        self._name = name
        self._collection_identifier = collection_identifier
        self._specimen_identifiers = specimen_identifiers

    @property
    def name(self) -> str:
        return self._name

    @property
    def collection_id(self) -> str:
        return self._collection_identifier

    @property
    def specimens_ids(self) -> list[str]:
        return self._specimen_identifiers

    def to_fhir(self, collection_id: str, specimen_ids: list[str]):
        """Return specimen list representation in FHIR
        :param collection_id: FHIR Identifier of the collection
        :param specimen_ids: List of FHIR specimen identifiers
        """
        # TODO entry.deleted maybe not always false ? when deleting samples from storage, it could be used as a flag
        specimen_list = fhir_list.List()
        specimen_list.title = self._name
        specimen_list.status = "current"
        specimen_list.mode = "working"
        specimen_list.subject = FHIRReference()
        specimen_list.subject.reference = f"Group/{collection_id}"
        specimen_list.entry = []
        for specimen_id in specimen_ids:
            entry = fhir_list.ListEntry()
            entry.item = FHIRReference()
            entry.deleted = False
            entry.item.reference = f"Specimen/{specimen_id}"
            specimen_list.entry.append(entry)
        return specimen_list