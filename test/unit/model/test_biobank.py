import unittest

from src.MIABIS_on_FHIR.biobank import Biobank


class TestBiobank(unittest.TestCase):


    def test_biobank_init(self):
        biobank = Biobank("biobankId", "biobankName", "biobankAlias", "CZ", "ContactName", "ContactSurname",
                          "ContactEmail@email.com")
        self.assertIsInstance(biobank, Biobank)
        self.assertEqual("biobankId", biobank.identifier)
        self.assertEqual("biobankName", biobank.name)
        self.assertEqual("biobankAlias", biobank.alias)
        self.assertEqual("CZ", biobank.country)
        self.assertEqual("ContactName", biobank.contact_name)
        self.assertEqual("ContactSurname", biobank.contact_surname)
        self.assertEqual("ContactEmail@email.com", biobank.contact_email)

    def test_biobank_invalid_identifier_type_innit(self):
        with self.assertRaises(TypeError):
            biobank = Biobank(37, "biobankName", "biobankAlias", "CZ", "ContactName", "ContactSurname",
                              "ContactEmail@email.com")

    def test_biobank_invalid_name_type_innit(self):
        with self.assertRaises(TypeError):
            biobank = Biobank("biobankId", 22, "biobankAlias", "CZ", "ContactName", "ContactSurname",
                              "ContactEmail@email.com")

    def test_biobank_invalid_alias_type_innit(self):
        with self.assertRaises(TypeError):
            biobank = Biobank("biobankId", "biobankName", 22, "CZ", "ContactName", "ContactSurname",
                              "email")

    def test_biobank_invalid_country_type_innit(self):
        with self.assertRaises(TypeError):
            biobank = Biobank("biobankId", "biobankName", "biobankAlias", 22, "ContactName", "ContactSurname",
                              "email")

    def test_biobank_invalid_contact_name_type_innit(self):
        with self.assertRaises(TypeError):
            biobank = Biobank("biobankId", "biobankName", "biobankAlias", "CZ", 22, "ContactSurname",
                              "email")

    def test_biobank_invalid_contact_surname_type_innit(self):
        with self.assertRaises(TypeError):
            biobank = Biobank("biobankId", "biobankName", "biobankAlias", "CZ", "ContactName", 22,
                              "email")

    def test_biobank_invalid_contact_email_type_innit(self):
        with self.assertRaises(TypeError):
            biobank = Biobank("biobankId", "biobankName", "biobankAlias", "CZ", "ContactName", "ContactSurname",
                              22)

    def test_biobank_infrastructural_capabilities(self):
        biobank = Biobank("biobankId", "biobankName", "biobankAlias", "CZ", "ContactName", "ContactSurname",
                          "email", infrastructural_capabilities=["SampleStorage"])
        self.assertEqual(["SampleStorage"], biobank.infrastructural_capabilities)

    def test_biobank_infrastructural_capabilities_invalid(self):
        with self.assertRaises(ValueError):
            biobank = Biobank("biobankId", "biobankName", "biobankAlias", "CZ", "ContactName", "ContactSurname",
                              "email", infrastructural_capabilities=["SampleStorage", "Invalid"])

    def test_biobank_org_cap(self):
        biobank = Biobank("biobankId", "biobankName", "biobankAlias", "CZ", "ContactName", "ContactSurname",
                          "email", organisational_capabilities=["RecontactDonors"])
        self.assertEqual(["RecontactDonors"], biobank.organisational_capabilities)

    def test_biobank_org_cap_invalid(self):
        with self.assertRaises(ValueError):
            biobank = Biobank("biobankId", "biobankName", "biobankAlias", "CZ", "ContactName", "ContactSurname",
                              "email", organisational_capabilities=["RecontactDonors", "Invalid"])

    def test_biobank__bioprocessing_capabilities(self):
        biobank = Biobank("biobankId", "biobankName", "biobankAlias", "CZ", "ContactName", "ContactSurname",
                          "email", bioprocessing_and_analysis_capabilities=["Genomics"])
        self.assertEqual(["Genomics"], biobank.bioprocessing_and_analysis_capabilities)

    def test_biobank__bioprocessing_capabilities_invalid(self):
        with self.assertRaises(ValueError):
            biobank = Biobank("biobankId", "biobankName", "biobankAlias", "CZ", "ContactName", "ContactSurname",
                              "email", bioprocessing_and_analysis_capabilities=["Genomics", "Invalid"])

    def test_biobank_juristic_person(self):
        biobank = Biobank("biobankId", "biobankName", "biobankAlias", "CZ", "ContactName", "ContactSurname",
                          "email", juristic_person="JuristicPerson")
        self.assertEqual("JuristicPerson", biobank.juristic_person)

    def test_biobank_juristic_person_invalid(self):
        with self.assertRaises(TypeError):
            bio = Biobank("biobankId", "biobankName", "biobankAlias", "CZ", "ContactName", "ContactSurname",
                          "email", juristic_person=47)

    def test_biobank_to_fhir_no_optional_args(self):
        biobank = Biobank("biobankId", "biobankName", "biobankAlias", "CZ", "ContactName", "ContactSurname",
                          "email")
        biobank_fhir = biobank.to_fhir()
        self.assertEqual("biobankId", biobank_fhir.identifier[0].value)
        self.assertEqual("biobankName", biobank_fhir.name)
        self.assertEqual("biobankAlias", biobank_fhir.alias[0])
        self.assertEqual("CZ", biobank_fhir.address[0].country)
        self.assertEqual("ContactName", biobank_fhir.contact[0].name.given[0])
        self.assertEqual("ContactSurname", biobank_fhir.contact[0].name.family)
        self.assertEqual("email", biobank_fhir.contact[0].telecom[0].value)

    def test_biobank_to_fhir_with_optional_args(self):
        biobank = Biobank("biobankId", "biobankName", "biobankAlias", "CZ", "ContactName", "ContactSurname",
                          "email", infrastructural_capabilities=["SampleStorage"],
                          organisational_capabilities=["RecontactDonors"],
                          bioprocessing_and_analysis_capabilities=["Genomics"])
        biobank_fhir = biobank.to_fhir()
        self.assertEqual("biobankId", biobank_fhir.identifier[0].value)
        self.assertEqual("biobankName", biobank_fhir.name)
        self.assertEqual("biobankAlias", biobank_fhir.alias[0])
        self.assertEqual("CZ", biobank_fhir.address[0].country)
        self.assertEqual("ContactName", biobank_fhir.contact[0].name.given[0])
        self.assertEqual("ContactSurname", biobank_fhir.contact[0].name.family)
        self.assertEqual("email", biobank_fhir.contact[0].telecom[0].value)
        self.assertEqual("SampleStorage", biobank_fhir.extension[0].valueCodeableConcept.coding[0].code)
        self.assertEqual("RecontactDonors", biobank_fhir.extension[1].valueCodeableConcept.coding[0].code)
        self.assertEqual("Genomics", biobank_fhir.extension[2].valueCodeableConcept.coding[0].code)

    def test_biobank_from_json(self):
        example_biobank = Biobank("biobankId", "biobankName", "biobankAlias", "CZ", "ContactName", "ContactSurname",
                                  "email", infrastructural_capabilities=["SampleStorage"],
                                  organisational_capabilities=["RecontactDonors"],
                                  bioprocessing_and_analysis_capabilities=["Genomics"])
        example_biobank_fhir = example_biobank.to_fhir()
        example_biobank_fhir.id = "TestFHIRId"
        biobank_json =example_biobank_fhir.as_json()
        biobank = Biobank.from_json(biobank_json)
        self.assertEqual(example_biobank.identifier, biobank.identifier)
        self.assertEqual(example_biobank.name, biobank.name)
        self.assertEqual(example_biobank.alias, biobank.alias)
        self.assertEqual(example_biobank.country, biobank.country)
        self.assertEqual(example_biobank.contact_name, biobank.contact_name)
        self.assertEqual(example_biobank.contact_surname, biobank.contact_surname)
        self.assertEqual(example_biobank.contact_email, biobank.contact_email)
        self.assertEqual(example_biobank.infrastructural_capabilities, biobank.infrastructural_capabilities)
        self.assertEqual(example_biobank.organisational_capabilities, biobank.organisational_capabilities)
        self.assertEqual(example_biobank.bioprocessing_and_analysis_capabilities,
                         biobank.bioprocessing_and_analysis_capabilities)
        self.assertEqual("TestFHIRId", biobank.biobank_fhir_id)
