from datetime import datetime, timedelta
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django_extensions.db.models import TimeStampedModel
from simple_history.models import HistoricalRecords

from ..history.models import (
    CHF,
    CKD,
    IBD,
    PVD,
    Alcohol,
    AllopurinolHypersensitivity,
    Anemia,
    Angina,
    Anticoagulation,
    Bleed,
    ColchicineInteractions,
    Diabetes,
    Erosions,
    FebuxostatHypersensitivity,
    Fructose,
    Gout,
    HeartAttack,
    Hypertension,
    Hyperuricemia,
    Leukocytosis,
    Leukopenia,
    OrganTransplant,
    Osteoporosis,
    Polycythemia,
    Shellfish,
    Stroke,
    Thrombocytopenia,
    Thrombocytosis,
    Tophi,
    Transaminitis,
    UrateKidneyStones,
    XOIInteractions,
)
from ..users.models import models
from ..vitals.models import Height, Weight
from .choices import races, sexes


# Create your models here.
class FamilyProfile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    gout = models.OneToOneField(
        Gout, on_delete=models.CASCADE, help_text="Do you have a family history of gout?", null=True, blank=True
    )
    slug = models.SlugField(max_length=200)
    history = HistoricalRecords()

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            # If no id, it is a newly created object and needs slug set
            self.slug = slugify(self.user.username)
        super(FamilyProfile, self).save(*args, **kwargs)

    # post_save() signal to create FamilyProfile if User selected role="Patient" at signup
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_family_profile(sender, instance, **kwargs):
        # Check if User instance Role is Patient
        if instance.role == "PATIENT":
            # Check if Patient has FamilyrProfile, save() if so, otherwise create() and assign User to Patient
            try:
                familyprofile = instance.familyprofile
            except:
                familyprofile = None
            if familyprofile:
                familyprofile.save()
            else:
                familyprofile = FamilyProfile.objects.create(user=instance)
                familyprofile.gout = Gout.objects.create(user=instance)
                familyprofile.save()


class PatientProfile(TimeStampedModel):
    # Default User profile
    # If you do this you need to either have a post_save signal or redirect to a profile_edit view on initial login

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="provider",
        null=True,
        blank=True,
        default=None,
    )
    patient_id = models.IntegerField(
        help_text="Does the Patient have an ID for you to reference?", null=True, blank=True
    )
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=20, choices=sexes, help_text="Enter gender", null=True, blank=True, default=None
    )
    race = models.CharField(max_length=40, choices=races, help_text="Enter race", null=True, blank=True, default=None)
    weight = models.OneToOneField(
        Weight, on_delete=models.CASCADE, help_text="How much do you weight in pounds?", null=True, blank=True
    )
    height = models.OneToOneField(
        Height, on_delete=models.CASCADE, help_text="How tall are you in feet/inches?", null=True, blank=True
    )
    slug = models.SlugField(max_length=200)
    history = HistoricalRecords()

    # Fields for processing high lab values
    #LFTs
    lft_trivial = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(1.00), help_text="Percentage for trivial LFT abnormality calculation", null=False, blank=False)
    lft_nonurgent = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(2.00), help_text="Percentage for nonurgent LFT abnormality calculation", null=False, blank=False)
    lft_urgent = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(3.00), help_text="Percentage for urgent LFT abnormality calculation", null=False, blank=False)
    lft_emergency = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(5.00), help_text="Percentage for emergency LFT abnormality calculation", null=False, blank=False)
    #Creatinine
    creatinine_trivial = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(1.00), help_text="Percentage for trivial creatinine abnormality calculation", null=False, blank=False)
    creatinine_nonurgent = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(2.00), help_text="Percentage for trivial creatinine abnormality calculation", null=False, blank=False)
    creatinine_urgent = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(3.00), help_text="Percentage for trivial creatinine abnormality calculation", null=False, blank=False)
    creatinine_emergency = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(5.00), help_text="Percentage for trivial creatinine abnormality calculation", null=False, blank=False)
    #Platelet
    # High Platelet will never trigger anything other than a "trivial" response from process_high(), thus other non/urgent and emergency criteria not required
    platelet_high_trivial = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(1.00), help_text="Percentage for trivial high platelet abnormality calculation", null=False, blank=False)
    platelet_high_nonurgent = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(1.5), help_text="Percentage for trivial high platelet abnormality calculation", null=False, blank=False)
    platelet_high_urgent = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(1.75), help_text="Percentage for trivial high platelet abnormality calculation", null=False, blank=False)
    platelet_high_emergency = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(2.00), help_text="Percentage for trivial high platelet abnormality calculation", null=False, blank=False)
    platelet_low_trivial = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(1.00), help_text="Percentage for trivial low platelet abnormality calculation", null=False, blank=False)
    platelet_low_nonurgent = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(0.75), help_text="Percentage for trivial low platelet abnormality calculation", null=False, blank=False)
    platelet_low_urgent = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(0.5), help_text="Percentage for trivial low platelet abnormality calculation", null=False, blank=False)
    platelet_low_emergency = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(0.25), help_text="Percentage for trivial low platelet abnormality calculation", null=False, blank=False)
    #WBC
    wbc_high_trivial = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(1.00), help_text="Percentage for trivial high WBC abnormality calculation", null=False, blank=False)
    wbc_high_nonurgent = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(1.00), help_text="Percentage for trivial high WBC abnormality calculation", null=False, blank=False)
    wbc_high_urgent = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(1.00), help_text="Percentage for trivial high WBC abnormality calculation", null=False, blank=False)
    wbc_high_emergency = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(1.00), help_text="Percentage for trivial high WBC abnormality calculation", null=False, blank=False)
    wbc_low_trivial = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(1.00), help_text="Percentage for trivial low WBC abnormality calculation", null=False, blank=False)
    wbc_low_nonurgent = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(1.00), help_text="Percentage for trivial low WBC abnormality calculation", null=False, blank=False)
    wbc_low_urgent = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(1.00), help_text="Percentage for trivial low WBC abnormality calculation", null=False, blank=False)
    wbc_low_emergency = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(1.00), help_text="Percentage for trivial low WBC abnormality calculation", null=False, blank=False)
    #Hemoglobin
    hemoglobin_high_trivial = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(1.00), help_text="Percentage for trivial high hemoglobin abnormality calculation", null=False, blank=False)
    hemoglobin_high_nonurgent = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(1.00), help_text="Percentage for trivial high hemoglobin abnormality calculation", null=False, blank=False)
    hemoglobin_high_urgent = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(1.00), help_text="Percentage for trivial high hemoglobin abnormality calculation", null=False, blank=False)
    hemoglobin_high_emergency = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(1.00), help_text="Percentage for trivial high hemoglobin abnormality calculation", null=False, blank=False)
    hemoglobin_low_trivial = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(1.00), help_text="Percentage for trivial low hemoglobin abnormality calculation", null=False, blank=False)
    hemoglobin_low_nonurgent = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(1.00), help_text="Percentage for trivial low hemoglobin abnormality calculation", null=False, blank=False)
    hemoglobin_low_urgent = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(1.00), help_text="Percentage for trivial low hemoglobin abnormality calculation", null=False, blank=False)
    hemoglobin_low_emergency = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal(1.00), help_text="Percentage for trivial low hemoglobin abnormality calculation", null=False, blank=False)

    @property
    def age(self):
        if self.date_of_birth:
            age = datetime.today().year - self.date_of_birth.year
            return age
        else:
            return None

    @property
    def BMI(self):
        """BMI calculator and model property.
        Requires Height and Weight Values.
        Returns: BMI float or str telling User what is needed to calculate BMI."""
        valid_inputs = "Enter a valid "
        if self.weight and self.height:
            if self.height.value is None and self.weight.value is None:
                valid_inputs + "height and weight"
            elif self.height.value is None:
                valid_inputs + "height"
            elif self.weight.value is None:
                valid_inputs + "weight"
            elif self.weight.value and self.height.value:
                BMI = self.weight.weight_in_kgs / (self.height.height_in_meters ** 2)
                return BMI
        elif self.weight is None and self.height is None:
            valid_inputs + "height and weight"
        elif self.height is None:
            valid_inputs + "height"
        elif self.weight is None:
            valid_inputs + "weight"
        return valid_inputs

    def __str__(self):
        return str(self.user.username + "'s profile")

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.user_username})

    def save(self, *args, **kwargs):
        if not self.id:
            # If no id, it is a newly created object and needs slug set
            self.slug = slugify(self.user.username)
        super(PatientProfile, self).save(*args, **kwargs)

    # post_save() signal to create PatientProfile if User selected role="Patient" at signup
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_patient_profile(sender, instance, **kwargs):
        # Check if User instance Role is Patient
        if instance.role == "PATIENT":
            # Check if Patient has PatientProfile, save() if so, otherwise create() and assign User to Patient
            try:
                patientprofile = instance.patientprofile
            except:
                patientprofile = None
            if patientprofile:
                patientprofile.save()
            else:
                patientprofile = PatientProfile.objects.create(user=instance)
                patientprofile.height = Height.objects.create(user=instance)
                patientprofile.weight = Weight.objects.create(user=instance)
                patientprofile.save()


class ProviderProfile(TimeStampedModel):
    """Provider User Profile.
    post_save() signal to check if User selected Provider Role on SignUp.
    Creates ProviderProfile if so.
    post_save() signal to save ProviderProfile on User save() if User Role is Provider.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    organization = models.CharField(max_length=200, help_text="Organization", null=True, blank=True)
    titration_lab_interval = models.DurationField(
        help_text="How frequently are labs required to be checked duration ULT titration?",
        verbose_name="Titration Lab Check Interval",
        default=timedelta(days=42),
    )
    monitoring_lab_interval = models.DurationField(
        help_text="How frequently are labs required to be checked during routine monitoring?",
        verbose_name="Monitoring Lab Check Interval",
        default=timedelta(days=180),
    )
    urgent_lab_interval = models.DurationField(
        help_text="How frequently do you recheck urgent labs?",
        verbose_name="Urgent Lab Check Interval",
        default=timedelta(days=14),
    )
    delinquent_lab_interval = models.DurationField(
        help_text="How frequently do you recheck urgent labs?",
        verbose_name="Urgent Lab Check Interval",
        default=timedelta(days=21),
    )
    slug = models.SlugField(max_length=200)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if not self.id:
            # If no id, it is a newly created object and needs slug set
            self.slug = slugify(self.user.username)
        super(ProviderProfile, self).save(*args, **kwargs)

    # post_save() signal to create ProviderProfile if User selected role="Provider" at signup
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_provider_profile(sender, instance, **kwargs):
        # Check if User instance Role is Provider
        if instance.role == "PROVIDER":
            # Check if Provider has ProviderProfile, save() if so, otherwise create() and assign User to Provider
            try:
                providerprofile = instance.providerprofile
            except:
                providerprofile = None
            if providerprofile:
                providerprofile.save()
            else:
                ProviderProfile.objects.create(user=instance)


class MedicalProfile(TimeStampedModel):
    """MedicalProfile OneToOne related to User containing OneToOne relations with history model instances of medical problems.
    These are meant to be changed in the MedicalProfile page AS WELL AS all over the site when processing Aid forms."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    slug = models.SlugField(max_length=200)
    history = HistoricalRecords()
    # Related History models (1to1)
    allopurinol_hypersensitivity = models.OneToOneField(
        AllopurinolHypersensitivity,
        on_delete=models.CASCADE,
        help_text="Have you ever had an adverse reaction to allopurinol?",
        verbose_name="Allopurinol Hypersensitivity",
        null=True,
        blank=True,
    )
    anemia = models.OneToOneField(
        Anemia,
        on_delete=models.CASCADE,
        help_text=mark_safe(
            "Do you have chronic <a href='https://www.hematology.org/education/patients/anemia' target='_blank'>anemia</a> (low hemoglobin)?"
        ),
        verbose_name="Chronic Anemia (low hemoglobin)",
        null=True,
        blank=True,
    )
    angina = models.OneToOneField(
        Angina,
        on_delete=models.CASCADE,
        help_text=mark_safe(
            "Do you get <a href='https://www.heart.org/en/health-topics/heart-attack/angina-chest-pain' target='_blank'>angina</a>?"
        ),
        verbose_name="Angina (Cardiac Chest Pain)",
        null=True,
        blank=True,
    )
    anticoagulation = models.OneToOneField(
        Anticoagulation,
        on_delete=models.CASCADE,
        help_text="Are you on anticoagulation?",
        null=True,
        blank=True,
    )
    bleed = models.OneToOneField(
        Bleed,
        on_delete=models.CASCADE,
        help_text="Have you had a major bleeding event?",
        null=True,
        blank=True,
    )
    colchicine_interactions = models.OneToOneField(
        ColchicineInteractions,
        on_delete=models.CASCADE,
        help_text="Are you on a medication that interacts with colchicine, such as simvastatin, clarithromycin, or diltiazem?",
        null=True,
        blank=True,
    )
    CHF = models.OneToOneField(
        CHF, on_delete=models.CASCADE, help_text="Do you have congestive heart failure (CHF)?", null=True, blank=True
    )
    CKD = models.OneToOneField(
        CKD,
        on_delete=models.CASCADE,
        help_text="Do you have chronic kidney disease (CKD)?",
        verbose_name="CKD",
        null=True,
        blank=True,
    )
    diabetes = models.OneToOneField(
        Diabetes, on_delete=models.CASCADE, help_text="Do you have diabetes?", null=True, blank=True
    )
    erosions = models.OneToOneField(
        Erosions, on_delete=models.CASCADE, help_text="Do you have gouty erosions?", null=True, blank=True
    )
    febuxostat_hypersensitivity = models.OneToOneField(
        FebuxostatHypersensitivity,
        on_delete=models.CASCADE,
        help_text="Have you ever had an adverse reaction to febuxostat?",
        verbose_name="Febuxostat Hypersensitivity",
        null=True,
        blank=True,
    )
    heartattack = models.OneToOneField(
        HeartAttack,
        on_delete=models.CASCADE,
        help_text="Have you had a heart attack?",
        null=True,
        blank=True,
    )
    hypertension = models.OneToOneField(
        Hypertension,
        on_delete=models.CASCADE,
        help_text="Do you have high blood pressure (hypertension)?",
        null=True,
        blank=True,
    )
    hyperuricemia = models.OneToOneField(
        Hyperuricemia,
        on_delete=models.CASCADE,
        help_text="Do you have blood uric acid levels greater than 9.0 mg/dL?",
        null=True,
        blank=True,
    )
    IBD = models.OneToOneField(
        IBD,
        on_delete=models.CASCADE,
        help_text="Do you have IBD (inflammatory bowel disease=Crohn's disease or ulcerative colitis)?",
        null=True,
        blank=True,
    )
    leukocytosis = models.OneToOneField(
        Leukocytosis,
        on_delete=models.CASCADE,
        help_text="Do you have <a href='https://www.ncbi.nlm.nih.gov/books/NBK560882/#:~:text=Leukocytosis%20is%20the%20broad%20term,identified%20by%20their%20reference%20ranges.' target='_blank'>leukocytosis</a> (elevated WBCs)?",
        null=True,
        blank=True,
    )
    leukopenia = models.OneToOneField(
        Leukopenia,
        on_delete=models.CASCADE,
        help_text="Do you have <a href='https://en.wikipedia.org/wiki/Leukopenia' target='_blank'>leukopenia</a> (low WBCs)?",
        null=True,
        blank=True,
    )
    polycythemia = models.OneToOneField(
        Polycythemia,
        on_delete=models.CASCADE,
        help_text=mark_safe(
            "Do you have <a href='https://en.wikipedia.org/wiki/Polycythemia' target='_blank'>polycythemia</a> (high hemoglobin)?"
        ),
        null=True,
        blank=True,
    )
    PVD = models.OneToOneField(
        PVD,
        on_delete=models.CASCADE,
        help_text=mark_safe(
            "Do you have <a href='https://en.wikipedia.org/wiki/Peripheral_artery_disease' target='_blank'>peripheral vascular disease</a>?"
        ),
        null=True,
        blank=True,
    )
    organ_transplant = models.OneToOneField(
        OrganTransplant, on_delete=models.CASCADE, help_text="Have you had an organ transplant?", null=True, blank=True
    )
    osteoporosis = models.OneToOneField(
        Osteoporosis, on_delete=models.CASCADE, help_text="Do you have osteoporosis?", null=True, blank=True
    )
    stroke = models.OneToOneField(
        Stroke,
        on_delete=models.CASCADE,
        help_text="Have you had a stroke?",
        null=True,
        blank=True,
    )
    thrombocytopenia = models.OneToOneField(
        Thrombocytopenia,
        on_delete=models.CASCADE,
        help_text=mark_safe(
            "Do you have <a href='https://www.nhlbi.nih.gov/health-topics/thrombocytopenia' target='_blank'>thrombocytopenia</a> (low platelets)?"
        ),
        null=True,
        blank=True,
    )
    thrombocytosis = models.OneToOneField(
        Thrombocytosis,
        on_delete=models.CASCADE,
        help_text=mark_safe(
            "Do you have <a href='https://www.nhlbi.nih.gov/health-topics/thrombocythemia-and-thrombocytosis' target='_blank'>thrombocytosis</a> (high platelets)?"
        ),
        null=True,
        blank=True,
    )
    tophi = models.OneToOneField(
        Tophi, on_delete=models.CASCADE, help_text="Do you have gouty tophi?", null=True, blank=True
    )
    transaminitis = models.OneToOneField(
        Transaminitis,
        on_delete=models.CASCADE,
        help_text=mark_safe(
            "Do you have <a href='https://en.wikipedia.org/wiki/Elevated_transaminases' target='_blank'>transaminitis</a> (elevated liver function tests)?"
        ),
        null=True,
        blank=True,
    )
    urate_kidney_stones = models.OneToOneField(
        UrateKidneyStones,
        on_delete=models.CASCADE,
        help_text="Have you had urate kidney stones?",
        null=True,
        blank=True,
    )
    XOI_interactions = models.OneToOneField(
        XOIInteractions,
        on_delete=models.CASCADE,
        help_text="Are you on 6-mercaptopurine or azathioprine?",
        null=True,
        blank=True,
    )


    def save(self, *args, **kwargs):
        if not self.id:
            # If no id, it is a newly created object and needs slug set
            self.slug = slugify(self.user.username)
        super(MedicalProfile, self).save(*args, **kwargs)

    # post_save() signal to create MedicalProfile if User selected role="Patient" at signup
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_medical_profile(sender, instance, **kwargs):
        # Check if User instance Role is Patient
        if instance.role == "PATIENT":
            # Check if Patient has MedicalProfile, save() if so, otherwise create() and assign User to Patient
            try:
                medicalprofile = instance.medicalprofile
            except:
                medicalprofile = None
            if medicalprofile:
                medicalprofile.save()
            else:
                medicalprofile = MedicalProfile.objects.create(user=instance)
                medicalprofile.anemia = Anemia.objects.create(user=instance)
                medicalprofile.angina = Angina.objects.create(user=instance)
                medicalprofile.allopurinol_hypersensitivity = AllopurinolHypersensitivity.objects.create(user=instance)
                medicalprofile.anticoagulation = Anticoagulation.objects.create(user=instance)
                medicalprofile.bleed = Bleed.objects.create(user=instance)
                medicalprofile.CKD = CKD.objects.create(user=instance)
                medicalprofile.CHF = CHF.objects.create(user=instance)
                medicalprofile.colchicine_interactions = ColchicineInteractions.objects.create(user=instance)
                medicalprofile.diabetes = Diabetes.objects.create(user=instance)
                medicalprofile.erosions = Erosions.objects.create(user=instance)
                medicalprofile.febuxostat_hypersensitivity = FebuxostatHypersensitivity.objects.create(user=instance)
                medicalprofile.hypertension = Hypertension.objects.create(user=instance)
                medicalprofile.hyperuricemia = Hyperuricemia.objects.create(user=instance)
                medicalprofile.heartattack = HeartAttack.objects.create(user=instance)
                medicalprofile.IBD = IBD.objects.create(user=instance)
                medicalprofile.leukocytosis = Leukocytosis.objects.create(user=instance)
                medicalprofile.leukopenia = Leukopenia.objects.create(user=instance)
                medicalprofile.organ_transplant = OrganTransplant.objects.create(user=instance)
                medicalprofile.osteoporosis = Osteoporosis.objects.create(user=instance)
                medicalprofile.polycythemia = Polycythemia.objects.create(user=instance)
                medicalprofile.stroke = Stroke.objects.create(user=instance)
                medicalprofile.urate_kidney_stones = UrateKidneyStones.objects.create(user=instance)
                medicalprofile.tophi = Tophi.objects.create(user=instance)
                medicalprofile.thrombocytopenia = Thrombocytopenia.objects.create(user=instance)
                medicalprofile.thrombocytosis = Thrombocytosis.objects.create(user=instance)
                medicalprofile.transaminitis = Transaminitis.objects.create(user=instance)
                medicalprofile.XOI_interactions = XOIInteractions.objects.create(user=instance)
                medicalprofile.save()


class SocialProfile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    alcohol = models.OneToOneField(
        Alcohol,
        on_delete=models.CASCADE,
        help_text="How many drinks do you have per week?",
        null=True,
        blank=True,
    )
    fructose = models.OneToOneField(
        Fructose,
        on_delete=models.CASCADE,
        help_text="Do you eat a lot of fructose such as the sugar found in soda/pop, processed candies, or juices?",
        null=True,
        blank=True,
    )
    shellfish = models.OneToOneField(
        Shellfish,
        on_delete=models.CASCADE,
        help_text="Do you eat a lot of shellfish?",
        null=True,
        blank=True,
    )
    slug = models.SlugField(max_length=200)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if not self.id:
            # If no id, it is a newly created object and needs slug set
            self.slug = slugify(self.user.username)
        super(SocialProfile, self).save(*args, **kwargs)

    # post_save() signal to create SocialProfile if User selected role="Patient" at signup
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_family_profile(sender, instance, **kwargs):
        # Check if User instance Role is Patient
        if instance.role == "PATIENT":
            # Check if Patient has SocialProfile, save() if so, otherwise create() and assign User to Patient
            try:
                socialprofile = instance.socialprofile
            except:
                socialprofile = None
            if socialprofile:
                socialprofile.save()
            else:
                socialprofile = SocialProfile.objects.create(user=instance)
                socialprofile.alcohol = Alcohol.objects.create(user=instance)
                socialprofile.fructose = Fructose.objects.create(user=instance)
                socialprofile.shellfish = Shellfish.objects.create(user=instance)
                socialprofile.save()
