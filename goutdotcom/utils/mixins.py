from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

from ..profiles.models import PatientProfile

User = get_user_model()


class PatientProviderMixin:
    """Mixin that checks whether a User is a Provider or a Patient and restricts access to User-related objects.
    Limits providers to patients for whom he/she is the provider (field).
    Limits patients to their own objects.
    """

    def get(self, request, *args, **kwargs):
        # Fetch object (Profile)
        self.object = self.get_object()
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
    """

    def get(self, request, *args, **kwargs):
        # Check if requesting User is a Provider
        if self.request.user.is_authenticated:
            if self.request.user.role == "PROVIDER":
                # Check if the User with the username provided in kwargs is a patient of Provider
                if self.kwargs.get("username"):
                    self.user = User.objects.get(username=self.kwargs.get("username"))
                    if self.user.patientprofile.provider == self.request.user:
                        return super().get(request, *args, **kwargs)
                    # Else raise 404
                    else:
                        return PermissionDenied
                else:
                    return super().get(request, *args, **kwargs)
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
                # Else raise 404
                else:
                    raise PermissionDenied
            else:
                # Else raise 404
                raise PermissionDenied
        # If User is not logged in, restrict access to any username-based CreateViews
        else:
            if self.kwargs.get("username"):
                raise PermissionDenied
            else:
                return super().get(request, *args, **kwargs)
