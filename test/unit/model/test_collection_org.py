import unittest

from MIABIS_on_FHIR.MoF_collection_organization import CollectionOrganization


class TestCollectionOrganization(unittest.TestCase):
    coll_org_json = {'meta': {'versionId': '7', 'lastUpdated': '2024-09-16T07:19:31.673Z',
                              'profile': ['http://example.com/StructureDefinition/Collection']},
                     'name': 'collectionName',
                     'type': [{'coding': [{'system': 'http://example.com/organizationTypeCS', 'code': 'Collection'}]}],
                     'resourceType': 'Organization', 'extension': [
            {'url': 'http://example.com/StructureDefinition/dataset-type-extension',
             'valueCodeableConcept': {'coding': [{'system': 'http://example.com/datasetTypeCS', 'code': 'Other'}]}},
            {'url': 'http://example.com/StructureDefinition/sample-source-extension',
             'valueCodeableConcept': {'coding': [{'system': 'http://example.com/sampleSourceCS', 'code': 'Human'}]}},
            {'url': 'http://example.com/StructureDefinition/sample-collection-setting-extension',
             'valueCodeableConcept': {
                 'coding': [{'system': 'http://example.com/sampleCollectionSettingCS', 'code': 'Other'}]}},
            {'url': 'http://example.com/StructureDefinition/collection-design-extension', 'valueCodeableConcept': {
                'coding': [{'system': 'http://example.com/collectionDesignCS', 'code': 'Other'}]}},
            {'url': 'http://example.com/StructureDefinition/use-and-access-conditions-extension',
             'valueCodeableConcept': {
                 'coding': [{'system': 'http://example.com/useAndAccessConditionsCS', 'code': 'CommercialUse'}]}},
            {'url': 'http://example.com/StructureDefinition/publication-extension', 'valueString': 'publication'},
            {'url': 'http://example.com/StructureDefinition/description-extension', 'valueString': 'description'}],
                     'alias': ['collectionAlias'], 'active': True, 'id': 'DEPZWNXFPHMA5NLM',
                     'identifier': [{'value': 'collectionId'}], 'telecom': [{'system': 'url', 'value': 'url'}],
                     'partOf': {'reference': 'Organization/DEPZWNPN6CSOKEOC'}, 'contact': [
            {'address': {'country': 'cz'}, 'name': {'family': 'Mrkva', 'given': ['Jozef']},
             'telecom': [{'system': 'email', 'value': 'jozefmrkva@email.com'}]}]}

    def test_collection_org_init_required_params(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz")
        self.assertIsInstance(collection_org, CollectionOrganization)
        self.assertEqual("collectionOrgId", collection_org.identifier)
        self.assertEqual("collectionOrgName", collection_org.name)
        self.assertEqual("biobankId", collection_org.managing_biobank_id)
        self.assertEqual("contactName", collection_org.contact_name)
        self.assertEqual("contactSurname", collection_org.contact_surname)
        self.assertEqual("contactEmail", collection_org.contact_email)
        self.assertEqual("cz", collection_org.country)

    def test_collection_org_init_optional_params(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz", "alias", "url",
                                                   "description",
                                                   "LifeStyle", "Human", "Environment", ["CaseControl"],
                                                ["CommercialUse"], ["publication"])
        self.assertIsInstance(collection_org, CollectionOrganization)
        self.assertEqual("collectionOrgId", collection_org.identifier)
        self.assertEqual("collectionOrgName", collection_org.name)
        self.assertEqual("biobankId", collection_org.managing_biobank_id)
        self.assertEqual("contactName", collection_org.contact_name)
        self.assertEqual("contactSurname", collection_org.contact_surname)
        self.assertEqual("contactEmail", collection_org.contact_email)
        self.assertEqual("cz", collection_org.country)
        self.assertEqual("alias", collection_org.alias)
        self.assertEqual("url", collection_org.url)
        self.assertEqual("description", collection_org.description)
        self.assertEqual("LifeStyle", collection_org.dataset_type)
        self.assertEqual("Human", collection_org.sample_source)
        self.assertEqual("Environment", collection_org.sample_collection_setting)
        self.assertEqual(["CaseControl"], collection_org.collection_design)
        self.assertEqual(["CommercialUse"], collection_org.use_and_access_conditions)
        self.assertEqual(["publication"], collection_org.publications)

    def test_collection_org_invalid_identifier_type_innit(self):
        with self.assertRaises(TypeError):
            collection_org = CollectionOrganization(37, "collectionOrgName", "biobankId", "contactName",
                                                       "contactSurname", "contactEmail", "cz")

    def test_collection_org_invalid_name_type_innit(self):
        with self.assertRaises(TypeError):
            collection_org = CollectionOrganization("collectionOrgId", 22, "biobankId", "contactName",
                                                       "contactSurname", "contactEmail", "cz")

    def test_collection_org_invalid_managing_biobank_id_type_innit(self):
        with self.assertRaises(TypeError):
            collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", 22, "contactName",
                                                       "contactSurname", "contactEmail", "cz")

    def test_collection_org_invalid_contact_name_type_innit(self):
        with self.assertRaises(TypeError):
            collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", 22,
                                                       "contactSurname", "contactEmail", "cz")

    def test_collection_org_invalid_contact_surname_type_innit(self):
        with self.assertRaises(TypeError):
            collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId",
                                                       "contactName",
                                                    22, "contactEmail", "cz")

    def test_collection_org_invalid_contact_email_type_innit(self):
        with self.assertRaises(TypeError):
            collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId",
                                                       "contactName",
                                                       "contactSurname", 22, "cz")

    def test_collection_org_invalid_country_type_innit(self):
        with self.assertRaises(TypeError):
            collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId",
                                                       "contactName",
                                                       "contactSurname", "contactEmail", 22)

    def test_collection_org_invalid_alias_type_innit(self):
        with self.assertRaises(TypeError):
            collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId",
                                                       "contactName",
                                                       "contactSurname", "contactEmail", "cz", 22)

    def test_collection_org_invalid_url_type_innit(self):
        with self.assertRaises(TypeError):
            collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId",
                                                       "contactName",
                                                       "contactSurname", "contactEmail", "cz", url=22)

    def test_collection_org_invalid_description_type_innit(self):
        with self.assertRaises(TypeError):
            collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId",
                                                       "contactName",
                                                       "contactSurname", "contactEmail", "cz", description=22)

    def test_collection_org_invalid_dataset_type_type_innit(self):
        with self.assertRaises(ValueError):
            collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId",
                                                       "contactName",
                                                       "contactSurname", "contactEmail", "cz", dataset_type=22)

    def test_collection_org_invalid_sample_source_type_innit(self):
        with self.assertRaises(ValueError):
            collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId",
                                                       "contactName",
                                                       "contactSurname", "contactEmail", "cz", sample_source=22)

    def test_collection_org_invalid_sample_collection_setting_type_innit(self):
        with self.assertRaises(ValueError):
            collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId",
                                                       "contactName",
                                                       "contactSurname", "contactEmail", "cz",
                                                    sample_collection_setting=22)

    def test_collection_org_invalid_collection_design_type_innit(self):
        with self.assertRaises(TypeError):
            collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId",
                                                       "contactName",
                                                       "contactSurname", "contactEmail", "cz", collection_design=22)

    def test_collection_org_invalid_use_and_access_conditions_type_innit(self):
        with self.assertRaises(TypeError):
            collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId",
                                                       "contactName",
                                                       "contactSurname", "contactEmail", "cz",
                                                    use_and_access_conditions=22)

    def test_collection_org_invalid_publications_type_innit(self):
        with self.assertRaises(TypeError):
            collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId",
                                                       "contactName",
                                                       "contactSurname", "contactEmail", "cz", publications=22)

    def test_collection_org_set_identifier_ok(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz")
        collection_org.identifier = "newId"
        self.assertEqual("newId", collection_org.identifier)

    def test_collection_org_set_identifier_invalid(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz")
        with self.assertRaises(TypeError):
            collection_org.identifier = 37

    def test_collection_org_set_name_ok(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz")
        collection_org.name = "newName"
        self.assertEqual("newName", collection_org.name)

    def test_collection_org_set_name_invalid(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz")
        with self.assertRaises(TypeError):
            collection_org.name = 37

    def test_collection_org_set_managing_biobank_id_ok(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz")
        collection_org.managing_biobank_id = "newId"
        self.assertEqual("newId", collection_org.managing_biobank_id)

    def test_collection_org_set_managing_biobank_id_invalid(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz")
        with self.assertRaises(TypeError):
            collection_org.managing_biobank_id = 37

    def test_collection_org_set_contact_name_ok(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz")
        collection_org.contact_name = "newName"
        self.assertEqual("newName", collection_org.contact_name)

    def test_collection_org_set_contact_name_invalid(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz")
        with self.assertRaises(TypeError):
            collection_org.contact_name = 37

    def test_collection_org_set_contact_surname_ok(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz")
        collection_org.contact_surname = "newName"
        self.assertEqual("newName", collection_org.contact_surname)

    def test_collection_org_set_contact_surname_invalid(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz")
        with self.assertRaises(TypeError):
            collection_org.contact_surname = 37

    def test_collection_org_set_contact_email_ok(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz")
        collection_org.contact_email = "newName"
        self.assertEqual("newName", collection_org.contact_email)

    def test_collection_org_set_contact_email_invalid(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz")
        with self.assertRaises(TypeError):
            collection_org.contact_email = 37

    def test_collection_org_set_country_ok(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz")
        collection_org.country = "newName"
        self.assertEqual("newName", collection_org.country)

    def test_collection_org_set_country_invalid(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz")
        with self.assertRaises(TypeError):
            collection_org.country = 37

    def test_collection_org_set_alias_ok(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz", "alias")
        collection_org.alias = "newName"
        self.assertEqual("newName", collection_org.alias)

    def test_collection_org_set_alias_invalid(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz", "alias")
        with self.assertRaises(TypeError):
            collection_org.alias = 37

    def test_collection_org_set_url_ok(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz", url="url")
        collection_org.url = "newName"
        self.assertEqual("newName", collection_org.url)

    def test_collection_org_set_url_invalid(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz", url="url")
        with self.assertRaises(TypeError):
            collection_org.url = 37

    def test_collection_org_set_description_ok(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz", description="description")
        collection_org.description = "newName"
        self.assertEqual("newName", collection_org.description)

    def test_collection_org_set_description_invalid(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz", description="description")
        with self.assertRaises(TypeError):
            collection_org.description = 37

    def test_collection_org_set_dataset_type_ok(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz", dataset_type="LifeStyle")
        collection_org.dataset_type = "Environmental"
        self.assertEqual("Environmental", collection_org.dataset_type)

    def test_collection_org_set_dataset_type_invalid(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz", dataset_type="LifeStyle")
        with self.assertRaises(ValueError):
            collection_org.dataset_type = 37

    def test_collection_org_set_sample_source_ok(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz", sample_source="Human")
        collection_org.sample_source = "Environment"
        self.assertEqual("Environment", collection_org.sample_source)

    def test_collection_org_set_sample_source_invalid(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz", sample_source="Human")
        with self.assertRaises(ValueError):
            collection_org.sample_source = "Invalid"

    def test_collection_org_set_sample_collection_setting_ok(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz",
                                                sample_collection_setting="Environment")
        collection_org.sample_collection_setting = "Unknown"
        self.assertEqual("Unknown", collection_org.sample_collection_setting)

    def test_collection_org_set_sample_collection_setting_invalid(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz",
                                                sample_collection_setting="Environment")
        with self.assertRaises(ValueError):
            collection_org.sample_collection_setting = "Invalid"

    def test_collection_org_set_collection_design_ok(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz",
                                                collection_design=["CaseControl"])
        collection_org.collection_design = ["CrossSectional"]
        self.assertEqual(["CrossSectional"], collection_org.collection_design)

    def test_collection_org_set_collection_design_invalid(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz",
                                                collection_design=["CaseControl"])
        with self.assertRaises(ValueError):
            collection_org.collection_design = ["Invalid"]

    def test_collection_org_set_use_and_access_conditions_ok(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz",
                                                use_and_access_conditions=["CommercialUse"])
        collection_org.use_and_access_conditions = ["Xenograft"]
        self.assertEqual(["Xenograft"], collection_org.use_and_access_conditions)

    def test_collection_org_set_use_and_access_conditions_invalid(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz",
                                                use_and_access_conditions=["CommercialUse"])
        with self.assertRaises(ValueError):
            collection_org.use_and_access_conditions = ["Invalid"]

    def test_collection_org_set_publications_ok(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz", publications=["publication"])
        collection_org.publications = ["publication2"]
        self.assertEqual(["publication2"], collection_org.publications)

    def test_collection_org_set_publications_invalid(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz", publications=["publication"])
        with self.assertRaises(TypeError):
            collection_org.publications = 37

    def test_collection_org_to_fhir_required_params_ok(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz")
        collection_org_fhir = collection_org.to_fhir("biobankFhirId")
        self.assertEqual("collectionOrgId", collection_org_fhir.identifier[0].value)
        self.assertEqual("collectionOrgName", collection_org_fhir.name)
        self.assertEqual("Organization/biobankFhirId", collection_org_fhir.partOf.reference)
        self.assertEqual("Organization", collection_org_fhir.resource_type)
        self.assertEqual(True, collection_org_fhir.active)
        self.assertEqual("contactName", collection_org_fhir.contact[0].name.given[0])
        self.assertEqual("contactSurname", collection_org_fhir.contact[0].name.family)
        self.assertEqual("contactEmail", collection_org_fhir.contact[0].telecom[0].value)
        self.assertEqual("cz", collection_org_fhir.contact[0].address.country)

    def test_collection_org_to_fhir_optional_params_ok(self):
        collection_org = CollectionOrganization("collectionOrgId", "collectionOrgName", "biobankId", "contactName",
                                                   "contactSurname", "contactEmail", "cz", "alias", "url",
                                                   "description",
                                                   "LifeStyle", "Human", "Environment", ["CaseControl"],
                                                ["CommercialUse"], ["publication"])
        collection_org_fhir = collection_org.to_fhir("biobankFhirId")
        self.assertEqual("alias", collection_org_fhir.alias[0])
        self.assertEqual("url", collection_org_fhir.telecom[0].value)
        self.assertEqual("LifeStyle", collection_org_fhir.extension[0].valueCodeableConcept.coding[0].code)
        self.assertEqual("Human", collection_org_fhir.extension[1].valueCodeableConcept.coding[0].code)
        self.assertEqual("Environment", collection_org_fhir.extension[2].valueCodeableConcept.coding[0].code)
        self.assertEqual("CaseControl", collection_org_fhir.extension[3].valueCodeableConcept.coding[0].code)
        self.assertEqual("CommercialUse", collection_org_fhir.extension[4].valueCodeableConcept.coding[0].code)
        self.assertEqual("publication", collection_org_fhir.extension[5].valueString)
        self.assertEqual("description", collection_org_fhir.extension[6].valueString)

    def test_collection_org_from_json(self):
        collection_org = CollectionOrganization.from_json(self.coll_org_json, "biobankId")
        self.assertEqual("collectionId", collection_org.identifier)
        self.assertEqual("collectionName", collection_org.name)
        self.assertEqual("biobankId", collection_org.managing_biobank_id)
        self.assertEqual("Jozef", collection_org.contact_name)
        self.assertEqual("Mrkva", collection_org.contact_surname)
        self.assertEqual("jozefmrkva@email.com", collection_org.contact_email)
        self.assertEqual("cz", collection_org.country)
        self.assertEqual("collectionAlias", collection_org.alias)
        self.assertEqual("url", collection_org.url)
        self.assertEqual("description", collection_org.description)
        self.assertEqual("Other", collection_org.dataset_type)
        self.assertEqual("Human", collection_org.sample_source)
        self.assertEqual("Other", collection_org.sample_collection_setting)
        self.assertEqual(["Other"], collection_org.collection_design)
        self.assertEqual(["CommercialUse"], collection_org.use_and_access_conditions)
        self.assertEqual(["publication"], collection_org.publications)
        self.assertEqual("description", collection_org.description)

