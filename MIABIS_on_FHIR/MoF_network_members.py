from datetime import datetime

from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.list import List, ListEntry
from fhirclient.models.meta import Meta

from _constants import DEFINITION_BASE_URL


class MoFNetworkMembers():
    """Class representing actual members of a network."""

    def __init__(self, network_id: str, title: str, members: list[str]):
        """
        :param title: name of network this members belongs to
        :param network_id: network id this members belongs to
        :param members: ids of all the members that are part of this network
        """
        if not isinstance(title, str):
            raise TypeError("Title must be string")
        if not isinstance(network_id, str):
            raise TypeError("Network id must be string")
        if not isinstance(members, list):
            raise TypeError("Members must be a list")
        for member in members:
            if not isinstance(member, str):
                raise TypeError("Members must be a list of strings")

        self._title = title
        self._network_id = network_id
        self._members = members

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, title: str):
        if not isinstance(title, str):
            raise TypeError("Title must be string")
        self._title = title

    @property
    def network_id(self) -> str:
        return self._network_id

    @network_id.setter
    def network_id(self, network_id: str):
        if not isinstance(network_id, str):
            raise TypeError("Network id must be string")
        self._network_id = network_id

    @property
    def members(self) -> list[str]:
        return self._members

    @members.setter
    def members(self, members: list[str]):
        if not isinstance(members, list):
            raise TypeError("Members must be a list")
        for member in members:
            if not isinstance(member, str):
                raise TypeError("Members must be a list of strings")
        self._members = members

    def to_fhir(self, network_fhir_id: str, member_collection_fhir_ids: list[str],
                member_biobanks_fhir_ids: list[str]) -> List:
        """
        :param network_fhir_id: FHIR id of the network this members belongs to
        :param member_collection_fhir_ids: FHIR ids of all the collections that are part of this network
        :param member_biobanks_fhir_ids: FHIR ids of all the biobanks that are part of this network
        :return: List object representing the members of the network
        """
        network_members = List()
        network_members.meta = Meta()
        network_members.meta.profile = [DEFINITION_BASE_URL + "/StructureDefinition/NetworkMembers"]
        network_members.title = self._title
        network_members.status = "current"
        network_members.mode = "working"
        network_members.subject = FHIRReference()
        network_members.subject.reference = f"Group/{network_fhir_id}"
        network_members.entry = []
        for member_collection_fhir_id in member_collection_fhir_ids:
            network_members.entry.append(self.__create_entry("Group", member_collection_fhir_id))
        for member_biobank_fhir_id in member_biobanks_fhir_ids:
            network_members.entry.append(self.__create_entry("Organization", member_biobank_fhir_id))
        return network_members

    def __create_entry(self, member_type: str, member_fhir_id: str):
        entry = ListEntry()
        entry.item = FHIRReference()
        entry.item.reference = f"{member_type}/{member_fhir_id}"
        entry.deleted = False
        entry.date = FHIRDate()
        entry.date.date = datetime.now().date()
        return entry
