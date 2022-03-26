BOOL_CHOICES = ((True, "Yes"), (False, "No"))

CHF_BOOL_CHOICES = ((True, "Systolic"), (False, "Diastolic"))

FLAG_CHOICES = ((0, "normal"),
                (1, "trivial"),
                (2, "nonurgent"),
                (3, "urgent"),
                (4, "emergency"),
                )

FATHER = "Father"
MOTHER = "Mother"
SISTER = "Sister"
BROTHER = "Brother"
UNCLE = "Uncle"
AUNT = "Aunt"
SON = "Son"
DAUGHTER = "Daughter"
GRANDPA = "Grandpa"
GRANDMA = "Grandma"

FAMILY_CHOICES = (
    (FATHER, "Father"),
    (MOTHER, "Mother"),
    (SISTER, "Sister"),
    (BROTHER, "Brother"),
    (UNCLE, "Uncle"),
    (AUNT, "Aunt"),
    (SON, "Son"),
    (DAUGHTER, "Daughter"),
    (GRANDPA, "Grandpa"),
    (GRANDMA, "Grandma"),
)

HEART = "Heart"
KIDNEY = "Kidney"
LIVER = "Liver"
LUNG = "Lung"
PANCREAS = "Pancreas"
FACE = "Face"

ORGAN_CHOICES = (
    (HEART, "Heart"),
    (KIDNEY, "Kidney"),
    (LIVER, "Liver"),
    (LUNG, "Lung"),
    (PANCREAS, "Pancreas"),
    (FACE, "Face"),
)

BEHINDTHESCENES = "Behind the scenes"
FLAREAID = "FlareAid"
FLARE = "Flare"
FAMILYPROFILE = "FamilyProfile"
MEDICALPROFILE = "MedicalProfile"
SOCIALPROFILE = "SocialProfile"
ULT = "ULT"
ULTAID = "ULTAid"

LAST_MODIFIED_CHOICES = (
    (BEHINDTHESCENES, "Behind the scenes"),
    (FLAREAID, "FlareAid"),
    (FLARE, "Flare"),
    (FAMILYPROFILE, "FamilyProfile"),
    (MEDICALPROFILE, "MedicalProfile"),
    (SOCIALPROFILE, "SocialProfile"),
    (ULT, "ULT"),
    (ULTAID, "ULTAid"),
)
