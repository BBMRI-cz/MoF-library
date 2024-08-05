from typing import Self

from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding
from fhirclient.models.extension import Extension
from fhirclient.models.group import Group
from fhirclient.models.identifier import Identifier
from fhirclient.models.meta import Meta

from MIABIS_on_FHIR.incorrect_json_format import IncorrectJsonFormatException
from _constants import NETWORK_COMMON_COLLAB_TOPICS, DEFINITION_BASE_URL


class MoFNetwork():
    """Class representing a group of interconnected biobanks or collections with defined common governance"""

    def __init__(self, identifier: str, name: str, common_collaboration_topics: list[str] = None):
        if not isinstance(identifier, str):
            raise TypeError("Identifier must be string")
        if not isinstance(name, str):
            raise TypeError("Name must be string")
        self._identifier = identifier
        self._name = name
        if common_collaboration_topics is not None:
            if not isinstance(common_collaboration_topics, list):
                raise TypeError("Common collaboration topics must be a list")
            for topic in common_collaboration_topics:
                if topic not in NETWORK_COMMON_COLLAB_TOPICS:
                    raise ValueError(f"{topic} is not a valid code for common collaboration topics")
        self._common_collaboration_topics = common_collaboration_topics

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
    def common_collaboration_topics(self) ->list[str]:
        return self._common_collaboration_topics

    @common_collaboration_topics.setter
    def common_collaboration_topics(self, common_collaboration_topics: list[str]):
        if not isinstance(common_collaboration_topics, list):
            raise TypeError("Common collaboration topics must be a list")
        for topic in common_collaboration_topics:
            if topic not in NETWORK_COMMON_COLLAB_TOPICS:
                raise ValueError(f"{topic} is not a valid code for common collaboration")
        self._common_collaboration_topics = common_collaboration_topics


    @classmethod
    def from_json(cls, network_json: dict) -> Self:
        try:
            identifier = network_json["identifier"][0]["value"]
            name = network_json["name"]
            common_collaboration_topics = None
            if "extension" in network_json:
                common_collaboration_topics = []
                for extension in network_json["extension"]:
                    if extension["url"] == DEFINITION_BASE_URL + "/common-collaboration-topics":
                        common_collaboration_topics.append(extension["valueCodeableConcept"]["coding"][0]["code"])
            return cls(identifier, name, common_collaboration_topics)
        except KeyError:
            raise IncorrectJsonFormatException("Error occured when parsing json into the MoFNetwork")



    def to_fhir(self) -> Group:
        network = Group()
        network.meta = Meta()
        network.meta.profile = [DEFINITION_BASE_URL + "/StructureDefinition/Network"]
        network.identifier = [self.__create_identifier()]
        network.name = self._name
        network.active = True
        network.actual = True
        network.type = "person"
        if self._common_collaboration_topics is not None:
            extensions = []
            for topic in self._common_collaboration_topics:
                extensions.append(self.__create_extension(DEFINITION_BASE_URL + "/common-collaboration-topics", topic))
            network.extension = extensions
        return network

    def __create_identifier(self):
        identifier = Identifier()
        identifier.system = DEFINITION_BASE_URL + "/network"
        identifier.value = self._identifier
        return identifier

    def __create_extension(self, url: str, value: str):
        extension = Extension()
        extension.url = url
        extension.valueCodeableConcept = CodeableConcept()
        extension.valueCodeableConcept.coding = [Coding()]
        extension.valueCodeableConcept.coding[0].code = value
        extension.valueCodeableConcept.coding[0].system = DEFINITION_BASE_URL + "/common-collaboration-topics-vs"
        return extension
