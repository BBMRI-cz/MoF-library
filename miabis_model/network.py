from typing import Self

from fhirclient.models.extension import Extension
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.group import Group
from fhirclient.models.meta import Meta

from miabis_model.incorrect_json_format import IncorrectJsonFormatException
from miabis_model.util.config import FHIRConfig
from miabis_model.util.parsing_util import get_nested_value, parse_reference_id
from miabis_model.util.util import create_fhir_identifier


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
        self.identifier = identifier
        self.name = name
        self.managing_network_org_id = network_org_id
        self.members_collections_ids = members_collections_ids
        self.members_biobanks_ids = members_biobanks_ids
        self._network_fhir_id = None
        self._managing_network_org_fhir_id = None
        self._members_biobanks_fhir_ids = None
        self._members_collections_fhir_ids = None

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
    def managing_network_org_id(self) -> str:
        return self._managing_biobank_id

    @managing_network_org_id.setter
    def managing_network_org_id(self, managing_biobank_id: str):
        if not isinstance(managing_biobank_id, str):
            raise TypeError("Managing biobank id must be string")
        self._managing_biobank_id = managing_biobank_id

    @property
    def members_collections_ids(self) -> list[str]:
        return self._members_collections_ids

    @members_collections_ids.setter
    def members_collections_ids(self, members_collections_ids: list[str]):
        if members_collections_ids is not None and not isinstance(members_collections_ids, list):
            raise TypeError("Members collections ids must be a list")
        for member in members_collections_ids if members_collections_ids is not None else []:
            if not isinstance(member, str):
                raise TypeError("Members collections ids must be a list of strings")
        self._members_collections_ids = members_collections_ids

    @property
    def members_biobanks_ids(self) -> list[str]:
        return self._members_biobanks_ids

    @members_biobanks_ids.setter
    def members_biobanks_ids(self, members_biobanks_ids: list[str]):
        if members_biobanks_ids is not None and not isinstance(members_biobanks_ids, list):
            raise TypeError("Members biobanks ids must be a list")
        for member in members_biobanks_ids if members_biobanks_ids is not None else []:
            if not isinstance(member, str):
                raise TypeError("Members biobanks ids must be a list of strings")
        self._members_biobanks_ids = members_biobanks_ids

    @property
    def network_fhir_id(self) -> str:
        return self._network_fhir_id

    @property
    def managing_network_org_fhir_id(self) -> str:
        return self._managing_network_org_fhir_id

    @property
    def members_collections_fhir_ids(self) -> list[str]:
        return self._members_collections_fhir_ids

    @property
    def members_biobanks_fhir_ids(self) -> list[str]:
        return self._members_biobanks_fhir_ids

    @classmethod
    def from_json(cls, network_json: dict, managing_network_org_id: str, member_collection_ids: list[str],
                  member_biobank_ids: list[str]) -> Self:
        try:
            identifier = get_nested_value(network_json, ["identifier", 0, "value"])
            name = network_json["name"]
            network_fhir_id = get_nested_value(network_json, ["id"])
            managing_biobank_fhir_id = parse_reference_id(
                get_nested_value(network_json, ["managingEntity", "reference"]))
            extensions = cls._parse_extensions(network_json.get("extension", []))
            instance = cls(identifier, name, managing_network_org_id, member_collection_ids, member_biobank_ids)
            instance._network_fhir_id = network_fhir_id
            instance._managing_network_org_fhir_id = managing_biobank_fhir_id
            instance._members_collections_fhir_ids = extensions["member_collection_fhir_ids"]
            instance._members_biobanks_fhir_ids = extensions["member_biobank_fhir_ids"]
            return instance
        except KeyError:
            raise IncorrectJsonFormatException("Error occured when parsing json into the MoFNetwork")

    @staticmethod
    def _parse_extensions(extensions: list[dict]) -> dict:
        parsed_extensions = {"member_collection_fhir_ids": [], "member_biobank_fhir_ids": []}
        for extension in extensions:
            if extension["url"] == FHIRConfig.MEMBER_V5_EXTENSION:
                ref_type, reference = get_nested_value(extension, ["valueReference", "reference"]).split("/")
                if ref_type == "Group":
                    parsed_extensions["member_collection_fhir_ids"].append(reference)
                else:
                    parsed_extensions["member_biobank_fhir_ids"].append(reference)
        return parsed_extensions

    def to_fhir(self, network_organization_fhir_id: str = None, member_collection_fhir_ids: list[str] = None,
                member_biobank_fhir_ids: list[str] = None) -> Group:
        network_organization_fhir_id = network_organization_fhir_id or self.managing_network_org_id
        if network_organization_fhir_id is None:
            raise ValueError("Managing biobank FHIR id must be provided either as an argument or as a property.")
        member_collection_fhir_ids = member_collection_fhir_ids or self.members_collections_fhir_ids
        member_biobank_fhir_ids = member_biobank_fhir_ids or self.members_biobanks_fhir_ids
        network = Group()
        network.meta = Meta()
        network.meta.profile = [FHIRConfig.get_meta_profile_url("network")]
        network.identifier = [create_fhir_identifier(self.identifier)]
        network.name = self._name
        network.active = True
        network.actual = True
        network.type = "person"
        network.managingEntity = FHIRReference()
        network.managingEntity.reference = f"Organization/{network_organization_fhir_id}"
        network.extension = []
        for member_collection_fhir_id in member_collection_fhir_ids if member_collection_fhir_ids is not None else []:
            network.extension.append(self.__create_member_extension("Group", member_collection_fhir_id))
        for member_biobank_fhir_id in member_biobank_fhir_ids if member_biobank_fhir_ids is not None else []:
            network.extension.append(self.__create_member_extension("Organization", member_biobank_fhir_id))
        return network

    @staticmethod
    def __create_member_extension(member_type: str, member_fhir_id: str):
        extension = Extension()
        extension.url = FHIRConfig.MEMBER_V5_EXTENSION
        extension.valueReference = FHIRReference()
        extension.valueReference.reference = f"{member_type}/{member_fhir_id}"
        return extension

    def add_fhir_id_to_network(self, network: Group) -> Group:
        """Add FHIR id to the FHIR representation of the Network. FHIR ID is necessary for updating the
                resource on the server.This method should only be called if the Network object was created by the
                from_json method. Otherwise,the network_fhir_id attribute is None,
                as the FHIR ID is generated by the server and is not known in advance."""
        network.id = self._network_fhir_id
        return network
