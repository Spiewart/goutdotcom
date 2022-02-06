from django.core.exceptions import PermissionDenied

from ..profiles.models import PatientProfile


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
