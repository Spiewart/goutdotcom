from django.forms import RadioSelect
from django.forms.widgets import TextInput
from django.utils.dateparse import parse_duration


class HorizontalRadioSelect(RadioSelect):
    template_name = "widgets/horizontal_radios.html"
    option_template_name = "widgets/horizontal_inputs.html"


class LabDurationInput(TextInput):
    def _format_value(self, value):
        duration = parse_duration(value)

        days = duration.days

        return "{:02d}".format(days)
