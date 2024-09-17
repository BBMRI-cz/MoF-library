from typing import Self

from fhirclient.models.extension import Extension
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.group import Group
from fhirclient.models.meta import Meta

from MIABIS_on_FHIR._constants import DEFINITION_BASE_URL
from MIABIS_on_FHIR._util import create_fhir_identifier
from MIABIS_on_FHIR.incorrect_json_format import IncorrectJsonFormatException


class Network:
    """Class representing a group of interconnected biobanks or collections with defined common governance"""

    def __init__(self, identifier: str, name: str, network_org_id: str, members_collections_ids: list[str] = None,
                 members_biobanks_ids: list[str] = None):
        """
        :param identifier: network organizational identifier
        :param name: name of the network
        :param network_org_id: biobank which is managing this Network
        ( for the purposes of having a contact person for this network)
        :param members_collections_ids: ids of all the collections (given by the organization) that are part of this network
        :param members_biobanks_ids: ids of all the biobanks (given by the organization) that are part of this network
        """
        if not isinstance(identifier, str):
            raise TypeError("Identifier must be string")
        if not isinstance(name, str):
            raise TypeError("Name must be string")
        if not isinstance(network_org_id, str):
            raise TypeError("Managing biobank id must be string")
        if members_collections_ids is not None:
            if not isinstance(members_collections_ids, list):
                raise TypeError("Members collections ids must be a list")
            for member in members_collections_ids:
                if not isinstance(member, str):
                    raise TypeError("Members collections ids must be a list of strings")
        if members_biobanks_ids is not None:
            if not isinstance(members_biobanks_ids, list):
                raise TypeError("Members biobanks ids must be a list")
            for member in members_biobanks_ids:
                if not isinstance(member, str):
                    raise TypeError("Members biobanks ids must be a list of strings")
        self._identifier = identifier
        self._name = name
        self._managing_biobank_id = network_org_id
        self._members_collections_ids = members_collections_ids
        self._members_biobanks_ids = members_biobanks_ids

    @property
    def identifier(self) -> str:
        return self._identifier

    @identifier.setter
    def identifier(self, identifier: str):
        if not isinstance(identifier, str):
            raise TypeError("Identifier must be string")
        self._identifier = identifier

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str):
            raise TypeError("Name must be string")
        self._name = name

    @property
    def managing_biobank_id(self) -> str:
        return self._managing_biobank_id

    @managing_biobank_id.setter
    def managing_biobank_id(self, managing_biobank_id: str):
        if not isinstance(managing_biobank_id, str):
            raise TypeError("Managing biobank id must be string")
        self._managing_biobank_id = managing_biobank_id

    @property
    def members_collections_ids(self) -> list[str]:
        return self._members_collections_ids

    @members_collections_ids.setter
    def members_collections_ids(self, members_collections_ids: list[str]):
        if not isinstance(members_collections_ids, list):
            raise TypeError("Members collections ids must be a list")
        for member in members_collections_ids:
            if not isinstance(member, str):
                raise TypeError("Members collections ids must be a list of strings")
        self._members_collections_ids = members_collections_ids

    @property
    def members_biobanks_ids(self) -> list[str]:
        return self._members_biobanks_ids

    @members_biobanks_ids.setter
    def members_biobanks_ids(self, members_biobanks_ids: list[str]):
        if not isinstance(members_biobanks_ids, list):
            raise TypeError("Members biobanks ids must be a list")
        for member in members_biobanks_ids:
            if not isinstance(member, str):
                raise TypeError("Members biobanks ids must be a list of strings")
        self._members_biobanks_ids = members_biobanks_ids

    @classmethod
    def from_json(cls, network_json: dict, managing_biobank_id: str) -> Self:
        try:
            identifier = network_json["identifier"][0]["value"]
            name = network_json["name"]
            if "extension" in network_json:
                common_collaboration_topics = []
            return cls(identifier, name, managing_biobank_id)
        except KeyError:
            raise IncorrectJsonFormatException("Error occured when parsing json into the MoFNetwork")

    def to_fhir(self, network_organization_fhir_id: str, member_collection_fhir_ids, member_biobank_fhir_ids) -> Group:
        network = Group()
        network.meta = Meta()
        network.meta.profile = [DEFINITION_BASE_URL + "/StructureDefinition/Network"]
        network.identifier = [create_fhir_identifier(self.identifier)]
        network.name = self._name
        network.active = True
        network.actual = True
        network.type = "person"
        network.managingEntity = FHIRReference()
        network.managingEntity.reference = f"Organization/{network_organization_fhir_id}"
        network.extension = []
        for member_collection_fhir_id in member_collection_fhir_ids:
            network.extension.append(self.__create_member_extension("Group", member_collection_fhir_id))
        for member_biobank_fhir_id in member_biobank_fhir_ids:
            network.extension.append(self.__create_member_extension("Organization", member_biobank_fhir_id))
        return network

    @staticmethod
    def __create_member_extension(member_type: str, member_fhir_id: str):
        extension = Extension()
        extension.url = "http://hl7.org/fhir/5.0/StructureDefinition/extension-Group.member.entity"
        extension.valueReference = FHIRReference()
        extension.valueReference.reference = f"{member_type}/{member_fhir_id}"
        return extension
