DEFINITION_BASE_URL = "https://fhir.bbmri-eric.eu/fhir"

DETAILED_MATERIAL_TYPE_CODES = ["AmnioticFluid", "AscitesFluid", "Bile", "BodyCavityFluid", "Bone",
                                "BoneMarrowAspirate", "BoneMarrowPlasma", "BoneMarrowWhole", "BreastMilk",
                                "BronchLavage", "BuffyCoat", "CancerCellLine", "CerebrospinalFluid", "CordBlood",
                                "DentalPulp", "DNA", "Embryo", "EntireOrgan", "Faeces", "FetalTissue", "Fibroblast",
                                "FoodSpecimen", "Gas", "GastricFluid", "Hair", "ImmortalizedCellLine",
                                "IsolatedMicrobe", "IsolatedExosome", "IsolatedTumorCell", "LiquidBiopsy",
                                "MenstrualBlood", "Nail", "NasalWashing", "Organoid", "Other", "PericardialFluid",
                                "PBMC", "Placenta", "Plasma", "PleuralFluid", "PostMortemTissue", "PrimaryCells",
                                "Protein", "RedBloodCells", "RNA", "Saliva", "Semen", "Serum", "SpecimenEnvironment",
                                "Sputum", "StemCells", "Swab", "Sweat", "SynovialFluid", "Tears", "Teeth",
                                "TissueFixed", "TissueFreshFrozen", "UmbilicalCord", "Urine", "UrineSediment",
                                "VitreousFluid", "WholeBlood", "WholeBloodDried"]

DETAILED_MATERIAL_TYPE_TO_COLLECTION_MATERIAL_TYPE_MAP = {"AmnioticFluid": "OtherBodyFluid",
                                                          "AscitesFluid": "OtherBodyFluid", "Bile": "OtherBodyFluid",
                                                          "BodyCavityFluid": "OtherBodyFluid", "Bone": "TissueFrozen",
                                                          "BoneMarrowAspirate": "OtherBodyFluid",
                                                          "BoneMarrowPlasma": "OtherBodyFluid",
                                                          "BoneMarrowWhole": "OtherBodyFluid",
                                                          "BreastMilk": "OtherBodyFluid",
                                                          "BronchLavage": "OtherBodyFluid", "BuffyCoat": "BuffyCoat",
                                                          "CancerCellLine": "CancerCellLine",
                                                          "CerebrospinalFluid": "OtherBodyFluid",
                                                          "CordBlood": "OtherBodyFluid", "DentalPulp": "OtherBodyFluid",
                                                          "DNA": "DNA", "Embryo": "EmbryoFetal",
                                                          "EntireOrgan": "EntireOrgan", "Faeces": "Faeces",
                                                          "FetalTissue": "EmbryoFetal", "Fibroblast": "PrimaryCells",
                                                          "FoodSpecimen": "SpecimenEnvironment", "Gas": "Other",
                                                          "GastricFluid": "OtherBodyFluid", "Hair": "Other",
                                                          "ImmortalizedCellLine": "ImmortalizedCellLine",
                                                          "IsolatedMicrobe": "IsolatedMicrobe",
                                                          "IsolatedExosome": "Other",
                                                          "IsolatedTumorCell": "PrimaryCells", "LiquidBiopsy": "Blood",
                                                          "MenstrualBlood": "OtherBodyFluid", "Nail": "Other",
                                                          "NasalWashing": "OtherBodyFluid", "Organoid": "Other",
                                                          "Other": "Other", "PericardialFluid": "OtherBodyFluid",
                                                          "PBMC": "PrimaryCells", "Placenta": "EntireOrgan",
                                                          "Plasma": "Plasma", "PleuralFluid": "OtherBodyFluid",
                                                          "PostMortemTissue": "PostMortemTissue",
                                                          "PrimaryCells": "PrimaryCells", "Protein": "Other",
                                                          "RedBloodCells": "PrimaryCells", "RNA": "RNA",
                                                          "Saliva": "Saliva", "Semen": "OtherBodyFluid",
                                                          "Serum": "Serum",
                                                          "SpecimenEnvironment": "SpecimenEnvironment",
                                                          "Sputum": "OtherBodyFluid",
                                                          "StemCells": "ImmortalizedCellLine", "Swab": "Swab",
                                                          "Sweat": "OtherBodyFluid", "SynovialFluid": "OtherBodyFluid",
                                                          "Tears": "OtherBodyFluid", "Teeth": "EntireOrgan",
                                                          "TissueFixed": "TissueFrozen",
                                                          "TissueFreshFrozen": "TissueFrozen",
                                                          "UmbilicalCord": "TissueFrozen", "Urine": "Urine",
                                                          "UrineSediment": "Urine", "VitreousFluid": "OtherBodyFluid",
                                                          "WholeBlood": "Blood", "WholeBloodDried": "Blood"}

COLLECTION_MATERIAL_TYPE_CODES = ["Blood", "BuffyCoat", "CancerCellLine", "DNA", "EntireOrgan", "Faeces", "EmbryoFetal",
                                  "ImmortalizedCellLine", "IsolatedMicrobe", "OtherBodyFluid", "Plasma", "PrimaryCells",
                                  "PostMortemTissue", "RNA", "Saliva", "Serum", "SpecimenEnvironment", "Swab",
                                  "TissueFrozen", "TissueFFPE", "Urine", "Other"]

STORAGE_TEMPERATURE_CODES = []

DONOR_DATASET_TYPE = ["Lifestyle", "BiologicalSamples", "SurveyData", "ImagingData", "MedicalRecords",
                      "NatinoalRegistries", "GenealogicalRecords", "PhysioBiochemicalData", "Other"]

BIOBANK_INFRASTRUCTURAL_CAPABILITIES = ["SampleStorage", "DataStorage", "Biosafety"]

BIOBANK_ORGANISATIONAL_CAPABILITIES = ["RecontactDonors", "ClinicalTrials", "ProspectiveCollections", "OmicsData",
                                       "LabAnalysisData", "ClinicalData", "PathologyArchive", "RadiologyArchive",
                                       "MedicalRegistries", "Other"]

BIOBANK_BIOPROCESSING_AND_ANALYTICAL_CAPABILITIES = ["BioChemAnalyses", "Genomics", "NucleicAcidExtraction",
                                                     "Proteomics",
                                                     "Metabolomics", "Histology", "CellLinesProcessing", "Virology",
                                                     "SampleProcessing", "SampleShipping",
                                                     "SampleQualityControlServices",
                                                     "Other"]

COLLECTION_DATASET_TYPE = ["LifeStyle", "Environmental", "Physiological", "Biochemical", "Clinical", "Psychological",
                           "Genomic", "Proteomic", "Metabolomic", "BodyImage", "WholeSlideImage", "PhotoImage",
                           "GenealogicalRecords", "Other"]

COLLECTION_SAMPLE_SOURCE = ["Human", "Animal", "Environment"]

COLLECTION_SAMPLE_COLLECTION_SETTING = ["RoutineHealthCare", "ClinicalTrial", "ResearchStudy", "Public", "Museum",
                                        "Environment", "Unknown", "Other"]

COLLECTION_DESIGN = ["CaseControl", "CrossSectional", "LongitudinalCohort", "TwinStudy", "QualityControl",
                     "PopulationBasedCohort",
                     "DiseaseSpecificCohort", "BirthCohort", "MicrobialCollection", "ReferenceCollection",
                     "RareDiseaseCollection", "Other"]

COLLECTION_USE_AND_ACCESS_CONDITIONS = ["CommercialUse", "Collaboration", "SpecificResearchUse", "GeneticDataUse",
                                        "OutsideEUAccess", "Xenograft", "OtherAnimalWork", "Other"]

COLLECTION_INCLUSION_CRITERIA = ["HealthStatus", "HospitalPatient", "UseOfMedication", "Gravidity", "AgeGroup",
                                 "FamilialStatus", "Sex", "CountryOfResidence", "EthnicOrigin",
                                 "PopulationRepresentative", "Lifestyle", "Other"]

NETWORK_COMMON_COLLAB_TOPICS = ["Charter", "SOP", "DataAccessPolicy", "SampleAccessPolicy", "MTA", "ImageAccessPolicy",
                                "ImageMTA", "Representation", "URL", "Other"]
