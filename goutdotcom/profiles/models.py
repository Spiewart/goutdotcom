import datetime

from django.conf import settings
from django.db import models
from django.db.models.fields import BooleanField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django_extensions.db.models import TimeStampedModel

from goutdotcom.history.models import (
    CHF,
    CKD,
    Alcohol,
    Bleed,
    Diabetes,
    Erosions,
    Fructose,
    Gout,
    HeartAttack,
    Hypertension,
    Hyperuricemia,
    OrganTransplant,
    Shellfish,
    Stroke,
    Tophi,
    UrateKidneyStones,
)
from goutdotcom.profiles.choices import BOOL_CHOICES, races, sexes
from goutdotcom.users.models import models
from goutdotcom.vitals.models import Height, Weight


# Create your models here.
class ContraindicationsProfile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    contraindication = BooleanField(
        choices=BOOL_CHOICES,
        help_text="Have you ever had a stroke, heart attack, or major bleeding event?",
        null=True,
        blank=True,
    )
    stroke = models.OneToOneField(
        Stroke,
        on_delete=models.CASCADE,
        help_text="Have you had a stroke?",
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
    bleed = models.OneToOneField(
        Bleed,
        on_delete=models.CASCADE,
        help_text="Have you had a major bleeding event?",
        null=True,
        blank=True,
    )

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.user_username})

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_contraindications_profile(sender, instance, created, **kwargs):
        if created:
            new_profile = ContraindicationsProfile.objects.create(user=instance)
            new_profile.stroke = Stroke.objects.create(user=instance)
            new_profile.heartattack = HeartAttack.objects.create(user=instance)
            new_profile.bleed = Bleed.objects.create(user=instance)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_contraindications_profile(sender, instance, **kwargs):
        instance.contraindicationsprofile.save()


class FamilyProfile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    gout = models.OneToOneField(
        Gout, on_delete=models.CASCADE, help_text="Do you have a family history of gout?", null=True, blank=True
    )

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.user_username})

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_family_profile(sender, instance, created, **kwargs):
        if created:
            new_profile = FamilyProfile.objects.create(user=instance)
            new_profile.gout = Gout.objects.create(user=instance)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_family_profile(sender, instance, **kwargs):
        instance.familyprofile.save()


class PatientProfile(TimeStampedModel):
    # Default User profile
    # If you do this you need to either have a post_save signal or redirect to a profile_edit view on initial login
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    picture = models.ImageField(
        default="default_thumbnail.png", null=True, blank=True, help_text="Upload a picture for your profile"
    )
    bio = models.CharField(max_length=500, help_text="500 character bio", null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=20, choices=sexes, help_text="Enter gender", null=True, blank=True, default="male"
    )
    race = models.CharField(
        max_length=40, choices=races, help_text="Enter race", null=True, blank=True, default="white"
    )
    weight = models.OneToOneField(
        Weight, on_delete=models.CASCADE, help_text="How much do you weight in pounds?", null=True, blank=True
    )
    height = models.OneToOneField(
        Height, on_delete=models.CASCADE, help_text="How tall are you in feet/inches?", null=True, blank=True
    )

    def get_age(self):
        if self.date_of_birth:
            age = datetime.date.today().year - self.date_of_birth.year
            return age
        else:
            return "No date of birth recorded"

    def BMI_calculator(self):
        def weight_kgs_calc(self):
            if self.weight:
                if self.weight.value:
                    return self.weight.value / 2.205
                else:
                    return "Enter a weight in pounds"
            else:
                return "Enter a weight in pounds"

        def height_meters_calc(self):
            if self.height:
                if self.height.value:
                    return self.height.value / 39.37
                else:
                    return "Enter a height in inches"
            else:
                return "Enter a height in inches"

        if self.weight and self.height:
            if self.weight.value and self.height.value:
                BMI = weight_kgs_calc(self) / (height_meters_calc(self) ** 2)
                return BMI
        elif self.weight is None:
            if self.height is None:
                return "Enter a valid height and weight"
            else:
                return weight_kgs_calc(self)
        elif self.height is None:
            if self.weight is None:
                return "Enter a valid height and weight"
            else:
                return height_meters_calc(self)

    def __str__(self):
        return str(self.user.username + "'s profile")

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.user_username})

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_patient_profile(sender, instance, created, **kwargs):
        if created:
            new_profile = PatientProfile.objects.create(user=instance)
            new_profile.weight = Weight.objects.create(user=instance)
            new_profile.height = Height.objects.create(user=instance)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_patient_profile(sender, instance, **kwargs):
        instance.patientprofile.save()


class MedicalProfile(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    CKD = models.OneToOneField(
        CKD,
        on_delete=models.CASCADE,
        help_text="Do you have chronic kidney disease (CKD)?",
        verbose_name="CKD",
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
    CHF = models.OneToOneField(
        CHF, on_delete=models.CASCADE, help_text="Do you have congestive heart failure (CHF)?", null=True, blank=True
    )
    diabetes = models.OneToOneField(
        Diabetes, on_delete=models.CASCADE, help_text="Do you have diabetes?", null=True, blank=True
    )
    erosions = models.OneToOneField(
        Erosions, on_delete=models.CASCADE, help_text="Do you have gouty erosions?", null=True, blank=True
    )
    organ_transplant = models.OneToOneField(
        OrganTransplant, on_delete=models.CASCADE, help_text="Have you had an organ transplant?", null=True, blank=True
    )
    urate_kidney_stones = models.OneToOneField(
        UrateKidneyStones,
        on_delete=models.CASCADE,
        help_text="Have you had urate kidney stones?",
        null=True,
        blank=True,
    )
    tophi = models.OneToOneField(
        Tophi, on_delete=models.CASCADE, help_text="Do you have gouty tophi?", null=True, blank=True
    )

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.user_username})

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_medical_profile(sender, instance, created, **kwargs):
        if created:
            new_profile = MedicalProfile.objects.create(user=instance)
            new_profile.CKD = CKD.objects.create(user=instance)
            new_profile.hypertension = Hypertension.objects.create(user=instance)
            new_profile.hyperuricemia = Hyperuricemia.objects.create(user=instance)
            new_profile.CHF = CHF.objects.create(user=instance)
            new_profile.diabetes = Diabetes.objects.create(user=instance)
            new_profile.erosions = Erosions.objects.create(user=instance)
            new_profile.organ_transplant = OrganTransplant.objects.create(user=instance)
            new_profile.urate_kidney_stones = UrateKidneyStones.objects.create(user=instance)
            new_profile.tophi = Tophi.objects.create(user=instance)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_medical_profile(sender, instance, **kwargs):
        instance.medicalprofile.save()


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

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_social_profile(sender, instance, created, **kwargs):
        if created:
            new_profile = SocialProfile.objects.create(user=instance)
            new_profile.alcohol = Alcohol.objects.create(user=instance)
            new_profile.fructose = Fructose.objects.create(user=instance)
            new_profile.shellfish = Shellfish.objects.create(user=instance)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_social_profile(sender, instance, **kwargs):
        instance.socialprofile.save()

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.user_username})
