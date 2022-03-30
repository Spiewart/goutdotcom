from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.utils.functional import cached_property
from django.views.generic.base import ContextMixin, View

from ..profiles.models import MedicalProfile, PatientProfile

User = get_user_model()


class TreatmentModelMixin(ContextMixin, View):
    """Mixin that checks for a treatment kwarg and tries to fetch the Treatment model with it.
    Adds the model to object instance to be called as a property.
    Avoids multiple queries.

    Returns:
        [model or 404]: [Returns a model class or 404]
    """

    @cached_property
    def model(self):
        self.treatment = None
        self.model = None
        # Check for treatment kwarg, mark None if not
        try:
            self.treatment = self.kwargs.get("treatment", None)
        except ObjectDoesNotExist:
            self.treatment = None
        # Find treatment via kwarg, 404 if treatment isn't a treatment
        if self.treatment:
            try:
                self.model = apps.get_model("treatment", model_name=self.treatment)
            except LookupError:
                raise Http404("That's not a valid treatment to create")
        if self.model:
            return self.model
        # 404 if no model returned
        else:
            raise Http404("Treatment not found")


class PatientProviderMixin:
    """Mixin that checks whether a User is a Provider or a Patient and restricts access to User-related objects.
    Limits providers to patients for whom he/she is the provider (field).
    Limits patients to their own objects.
    """

    def get(self, request, *args, **kwargs):
        # Fetch object
        self.object = self.get_object()
        # Check if User has object, need permissions if so
        if self.object.user:
            # Check if requesting User is a Provider
            if self.request.user.role == "PROVIDER":
                # Check if object is a PatientProfile
                if type(self.object) == PatientProfile:
                    # Check if PatientProfile provider is the requesting User
                    if self.object.provider and self.object.provider == self.request.user:
                        # Return super().get() if so
                        return super().get(request, *args, **kwargs)
                    else:
                        raise PermissionDenied
                else:
                    if (
                        self.object.user.patientprofile.provider
                        and self.object.user.patientprofile.provider == self.request.user
                    ):
                        # Return super().get() if so
                        return super().get(request, *args, **kwargs)
                    else:
                        raise PermissionDenied
            # Check if requesting User is a Patient
            elif self.request.user.role == "PATIENT":
                # Check if the object's User is the requesting User
                if self.object.user == self.request.user:
                    # Return super().get() if so
                    return super().get(request, *args, **kwargs)
                # Else raise 404
                else:
                    raise PermissionDenied
            else:
                # Else raise 404
                raise PermissionDenied
        else:
            if self.object.creator:
                if self.object.creator == self.request.user:
                    return super().get(request, *args, **kwargs)
                else:
                    raise PermissionDenied
            else:
                return super().get(request, *args, **kwargs)


class PatientProviderUserMixin:
    """Mixin that checks whether a User is a Provider or a Patient and restricts access to User objects.
    Limits providers to patients for whom he/she is the provider (field).
    Limits patients to their own User objects.
    """

    def get(self, request, *args, **kwargs):
        # Fetch object (Profile)
        self.object = self.get_object()
        # Check if requesting User is a Provider
        if self.request.user.role == "PROVIDER":
            # Check if the object is the Provider's User object
            if self.object == self.request.user:
                return super().get(request, *args, **kwargs)
            # Check if the Profile User's provider is the requesting User
            elif self.object.patientprofile.provider and self.object.patientprofile.provider == self.request.user:
                # Return super().get() if so
                return super().get(request, *args, **kwargs)
                # Else raise 404
            else:
                raise PermissionDenied
        # Check if requesting User is a Patient
        elif self.request.user.role == "PATIENT":
            # Check if the object is the requesting User
            if self.object == self.request.user:
                # Return super().get() if so
                return super().get(request, *args, **kwargs)
            # Else raise 404
            else:
                raise PermissionDenied
        else:
            # Else raise 404
            raise PermissionDenied


class PatientProviderCreateMixin:
    """Mixin that checks whether a User is a Provider or a Patient and restricts access to CreateViews.
    Limits providers to creating objects belonging to patients for whom he/she is the provider (field).
    Limits patients to creating their own objects.
    ***REQUIRES UserMixin and ProfileMixin***
    """

    def get(self, request, *args, **kwargs):
        # Check if requesting User is a Provider
        if self.request.user.is_authenticated:
            if self.request.user.role == "PROVIDER":
                # Check if there is User with a PatientProfile
                if self.patientprofile:
                    # Check if the User with the username provided in kwargs is a patient of Provider
                    if self.patientprofile.provider == self.request.user:
                        return super().get(request, *args, **kwargs)
                    # Else raise 404
                    else:
                        raise PermissionDenied
                # If no Patient, the CreateView is for an anonymous object
                return super().get(request, *args, **kwargs)
            # Check if requesting User is a Patient
            elif self.request.user.role == "PATIENT":
                # Check if there is a username kwarg provided
                if self.user:
                    if self.user == self.request.user:
                        # Return super().get() if so
                        return super().get(request, *args, **kwargs)
                    # Else raise 404
                    else:
                        raise PermissionDenied
                # If no User
                return super().get(request, *args, **kwargs)
            else:
                # Else raise 404
                raise PermissionDenied
        # If User is not logged in, restrict access to any username-based CreateViews
        else:
            if self.kwargs.get("username"):
                raise PermissionDenied
            return super().get(request, *args, **kwargs)


class PatientProviderListMixin:
    """Mixin that checks whether a User is a Provider or a Patient and restricts access to ListViews.
    Limits providers to lists of objects belonging to patients for whom he/she is the provider (field).
    Limits patients their own lists.
    ***REQUIRES UserMixin and ProfileMixin***
    """

    def get(self, request, *args, **kwargs):
        # Check if requesting User is a Provider
        if self.request.user.is_authenticated:
            if self.request.user.role == "PROVIDER":
                # Check if the User with the username provided in kwargs is a patient of Provider
                if self.patientprofile:
                    if self.patientprofile.provider == self.request.user:
                        return super().get(request, *args, **kwargs)
                else:
                    return PermissionDenied
            # Check if requesting User is a Patient
            elif self.request.user.role == "PATIENT":
                # Check if there is a username kwarg provided
                if self.kwargs.get("username"):
                    # Check if User's username is the same as that in the kwarg
                    if self.kwargs.get("username") == self.request.user.username:
                        # Return super().get() if so
                        return super().get(request, *args, **kwargs)
                    # Else raise 404
                    else:
                        raise PermissionDenied
            else:
                # Else raise 404
                raise PermissionDenied
        # If User is not logged in, restrict access to any username-based CreateViews
        else:
            raise PermissionDenied


class UserMixin(ContextMixin, View):
    """Mixin that checks for a username kwarg and tries to fetch a User with it.
    Adds the User to object instance to be called as a property.
    Avoids multiple queries to DB.
    Adds User object to context

    Returns:
        [User or None]: [Returns a User object or None]
    """

    @cached_property
    def user(self):
        self.username = None
        self.user = None
        try:
            self.username = self.kwargs.get("username", None)
        except ObjectDoesNotExist:
            self.username = None
        if self.username:
            try:
                self.user = User.objects.get(username=self.username)
            except User.DoesNotExist:
                raise Http404("No Patient with that username")
        return self.user

    def get_context_data(self, **kwargs):
        context = super(UserMixin, self).get_context_data(**kwargs)
        context["user"] = self.user
        return context


class UserSlugMixin(ContextMixin, View):
    """Mixin that finds an object's User without a username kwarg.
    For UpdateViews (LabCheck).
    Adds the User to object instance to be called as a property.
    Avoids multiple queries to DB.
    Adds User object to context.

    Returns:
        [User or None]: [Returns a User object or None]
    """

    @cached_property
    def user(self):
        self.object = self.get_object()
        self.user = get_object_or_404(User, username=self.object.user.username)
        return self.user

    def get_context_data(self, **kwargs):
        context = super(UserSlugMixin, self).get_context_data(**kwargs)
        context["user"] = self.user
        return context


class ProfileMixin(ContextMixin, View):
    """Mixin that checks for a MedicalProfile and PatientProfile based on User.
    Adds the MedicalProfile and PatientProfile to object instance to be called as properties.
    Avoids multiple queries to DB.
    Adds MedcicalProfile and PatientProfile objects to context

    Returns:
        [User or None]: [Returns a MedcicalProfile and PatientProfile objects or None]
    """

    @cached_property
    def medicalprofile(self):
        if self.user:
            self.medicalprofile = None
            try:
                self.medicalprofile = MedicalProfile.objects.get(user=self.user)
            except ObjectDoesNotExist:
                self.medicalprofile = None
            return self.medicalprofile
        else:
            return None

    @cached_property
    def patientprofile(self):
        if self.user:
            self.patientprofile = None
            try:
                self.patientprofile = PatientProfile.objects.get(user=self.user)
            except ObjectDoesNotExist:
                self.patientprofile = None
            return self.patientprofile
        else:
            return None

    def get_context_data(self, **kwargs):
        context = super(ProfileMixin, self).get_context_data(**kwargs)
        context["medicalprofile"] = self.medicalprofile
        context["patientprofile"] = self.patientprofile
        return context
