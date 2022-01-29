from django.forms.widgets import TextInput
from django.utils.dateparse import parse_duration


class LabDurationInput(TextInput):
    def _format_value(self, value):
        duration = parse_duration(value)

        days = duration.days

        return "{:02d}".format(days)
