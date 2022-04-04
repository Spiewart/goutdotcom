import rules


@rules.predicate
def is_patient(user, flare):
    return flare.user == user

@rules.predicate
def is_provider(user, flare):
    return flare.provider == user

@rules.predicate
def is_patient_or_provider(flare):
    return flare.user
