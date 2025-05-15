from fhirclient.models.meta import Meta
from fhirclient.models.organization import Organization

from miabis_model.util.config import FHIRConfig


class _JuristicPerson:
    """Class representing Juristic Person for Biobank, or Network"""

    def __init__(self, name: str):
        """
        :param name: juristic person's name
        """
        self.name = name
        self._fhir_id = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        if not isinstance(name, str):
            raise TypeError("Juristic person name must be a string!")
        self._name = name

    @property
    def fhir_id(self):
        return self._fhir_id

    def to_fhir(self) -> Organization:
        organization = Organization()
        organization.meta = Meta()
        organization.meta.profile = [FHIRConfig.get_meta_profile_url("juristic_person")]
        organization.name = self._name
        return organization
