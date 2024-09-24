from datetime import datetime
from typing import Self

from fhirclient.models.annotation import Annotation
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding
from fhirclient.models.fhirdatetime import FHIRDateTime
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.meta import Meta
from fhirclient.models.specimen import Specimen, SpecimenCollection, SpecimenProcessing

from MIABIS_on_FHIR._constants import MATERIAL_TYPE_CODES, DEFINITION_BASE_URL
from MIABIS_on_FHIR._parsing_util import get_nested_value
from MIABIS_on_FHIR._util import create_fhir_identifier, create_codeable_concept, create_codeable_concept_extension
from MIABIS_on_FHIR.incorrect_json_format import IncorrectJsonFormatException
from MIABIS_on_FHIR.storage_temperature import StorageTemperature


class Sample:
    """Class representing a biological specimen as defined by the MIABIS on FHIR profile."""

    def __init__(self, identifier: str, donor_identifier: str, material_type: str, collected_datetime: datetime = None,
                 body_site: str = None, body_site_system: str = None, storage_temperature: StorageTemperature = None,
                 use_restrictions: str = None):
        """
        :param identifier: Sample organizational identifier
        :param donor_id: Donor organizational identifier
        :param material_type: Sample type. E.g. tissue, plasma...
        :param collected_datetime: Date and time of sample collection
        :param body_site: The anatomical location from which the sample was collected
        :param body_site_system: The system to which the body site belongs
        :param storage_temperature: Temperature at which the sample is stored
        :param use_restrictions: Restrictions on the use of the sample
        """
        if not isinstance(identifier, str):
            raise TypeError("Identifier must be string")
        self._identifier = identifier
        if not isinstance(donor_identifier, str):
            raise TypeError("Identifier must be string")
        self._donor_identifier = donor_identifier
        if material_type not in MATERIAL_TYPE_CODES:
            raise ValueError(f"Material type {material_type} is not valid. Valid values are: {MATERIAL_TYPE_CODES}")
        self._material_type = material_type
        if collected_datetime is not None and not isinstance(collected_datetime, datetime):
            raise TypeError("Collected datetime must be a datetime object")
        self._collected_datetime = collected_datetime
        if body_site is not None and not isinstance(body_site, str):
            raise TypeError("Body site must be a string")
        self._body_site = body_site
        if body_site_system is not None and not isinstance(body_site_system, str):
            raise TypeError("Body site system must be a string")
        self._body_site_system = body_site_system
        if storage_temperature is not None and not isinstance(storage_temperature, StorageTemperature):
            raise TypeError("Storage temperature must be a StorageTemperature object")
        self._storage_temperature = storage_temperature
        if use_restrictions is not None and not isinstance(use_restrictions, str):
            raise TypeError("Use restrictions must be a string")
        self._use_restrictions = use_restrictions

    @property
    def identifier(self) -> str:
        """Institutional identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self, identifier: str):
        if not isinstance(identifier, str):
            raise TypeError("Identifier must be string")
        self._identifier = identifier

    @property
    def donor_identifier(self) -> str:
        """Institutional ID of donor."""
        return self._donor_identifier

    @donor_identifier.setter
    def donor_identifier(self, donor_identifier: str):
        if not isinstance(donor_identifier, str):
            raise TypeError("Identifier must be string")
        self._donor_identifier = donor_identifier

    @property
    def material_type(self) -> str:
        """Sample type. E.g. tissue, plasma..."""
        return self._material_type

    @material_type.setter
    def material_type(self, material_type: str):
        if material_type not in MATERIAL_TYPE_CODES:
            raise ValueError(f"Material type {material_type} is not valid. Valid values are: {MATERIAL_TYPE_CODES}")
        self._material_type = material_type

    @property
    def collected_datetime(self) -> datetime:
        """Date and time of sample collection."""
        return self._collected_datetime

    @collected_datetime.setter
    def collected_datetime(self, collected_datetime: datetime):
        if collected_datetime is not None and not isinstance(collected_datetime, datetime):
            raise TypeError("Collected datetime must be a datetime object")
        self._collected_datetime = collected_datetime

    @property
    def body_site(self) -> str:
        """The anatomical location from which the sample was collected."""
        return self._body_site

    @body_site.setter
    def body_site(self, body_site: str):
        if body_site is not None and not isinstance(body_site, str):
            raise TypeError("Body site must be a string")
        self._body_site = body_site

    @property
    def body_site_system(self) -> str:
        """The system to which the body site belongs."""
        return self._body_site_system

    @body_site_system.setter
    def body_site_system(self, body_site_system: str):
        if body_site_system is not None and not isinstance(body_site_system, str):
            raise TypeError("Body site system must be a string")
        self._body_site_system = body_site_system

    @property
    def storage_temperature(self) -> StorageTemperature:
        """Temperature at which the sample is stored."""
        return self._storage_temperature

    @storage_temperature.setter
    def storage_temperature(self, storage_temperature: StorageTemperature):
        if storage_temperature is not None and not isinstance(storage_temperature, StorageTemperature):
            raise TypeError("Storage temperature must be a StorageTemperature object")
        self._storage_temperature = storage_temperature

    @property
    def use_restrictions(self) -> str:
        """Restrictions on the use of the sample."""
        return self._use_restrictions

    @use_restrictions.setter
    def use_restrictions(self, use_restrictions: str):
        if use_restrictions is not None and not isinstance(use_restrictions, str):
            raise TypeError("Use restrictions must be a string")
        self._use_restrictions = use_restrictions

    @classmethod
    def from_json(cls, sample_json: dict, donor_identifier: str) -> Self:
        """
        Build MoFSample from FHIR json representation
        :param sample_json: json the sample should be build from
        :param donor_identifier: organizational identifier of the donor (not the FHIR id!)
        :return:
        """
        try:
            identifier = get_nested_value(sample_json, ["identifier", 0, "value"])
            material_type = get_nested_value(sample_json, ["type", "coding", 0, "code"])
            collected_datetime = cls._parse_collection_datetime(sample_json)
            body_site = get_nested_value(sample_json, ["collection", "bodySite", "coding", 0, "code"])
            body_site_system = get_nested_value(sample_json, ["collection", "bodySite", "coding", 0, "system"])
            storage_temperature = cls._parse_storage_temperature(sample_json)
            use_restrictions = get_nested_value(sample_json, ["note", 0, "text"])
            return cls(identifier, donor_identifier, material_type, collected_datetime, body_site, body_site_system,
                       storage_temperature, use_restrictions)
        except KeyError:
            raise IncorrectJsonFormatException("Error occurred when parsing json into the MoFSample")

    @staticmethod
    def _parse_collection_datetime(sample_json: dict) -> datetime | None:
        """Parse the collection datetime from the sample JSON."""
        collection_datetime = get_nested_value(sample_json, ["collection", "collectedDateTime"])
        if collection_datetime is not None:
            collection_datetime = datetime.strptime(collection_datetime, "%Y-%m-%d")
        return collection_datetime

    @staticmethod
    def _parse_storage_temperature(sample_json: dict) -> StorageTemperature | None:
        """Parse the storage temperature from the sample JSON."""
        storage_temperature = get_nested_value(sample_json,
                                               ["processing", 0, "extension", 0, "valueCodeableConcept",
                                                "coding", 0, "code"])
        if storage_temperature is not None:
            storage_temperature = StorageTemperature(storage_temperature)
        return storage_temperature

    def to_fhir(self, subject_fhir_id: str):
        """return sample representation in FHIR format
        :param material_type_map: Mapping of material types to FHIR codes
        :param subject_fhir_id: FHIR ID of the subject to which the sample belongs"""

        specimen = Specimen()
        specimen.meta = Meta()
        specimen.meta.profile = [DEFINITION_BASE_URL + "/StructureDefinition/Specimen"]
        specimen.identifier = [create_fhir_identifier(self.identifier)]
        specimen.subject = FHIRReference()
        specimen.subject.reference = f"Patient/{subject_fhir_id}"
        specimen.type = create_codeable_concept(DEFINITION_BASE_URL + "/ValueSet/miabis-material-type-VS",
                                                self.material_type)
        if self.collected_datetime is not None or self.body_site is not None:
            specimen.collection = SpecimenCollection()
            if self.collected_datetime is not None:
                specimen.collection.collectedDateTime = FHIRDateTime()
                specimen.collection.collectedDateTime.date = self.collected_datetime.date()
            if self.body_site is not None:
                specimen.collection.bodySite = self.__create_body_site()
        if self.storage_temperature is not None:
            specimen.processing = [SpecimenProcessing()]
            specimen.processing[0].extension = [
                create_codeable_concept_extension(
                    DEFINITION_BASE_URL + "/StructureDefinition/miabis-sample-storage-temperature-extension",
                    DEFINITION_BASE_URL + "/StorageTemperatureCS", self.storage_temperature.value)]
        if self.use_restrictions is not None:
            specimen.note = [Annotation()]
            specimen.note[0].text = self.use_restrictions
        return specimen

    def __create_body_site(self) -> CodeableConcept:
        """Create body site codeable concept."""
        body_site = CodeableConcept()
        body_site.coding = [Coding()]
        body_site.coding[0].code = self.body_site
        if self.body_site_system is not None:
            body_site.coding[0].system = self.body_site_system
        return body_site
