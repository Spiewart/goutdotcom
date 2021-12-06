from django.forms import RadioSelect


class HorizontalRadioSelect(RadioSelect):
    template_name = "widgets/horizontal_radios.html"
    option_template_name = "widgets/horizontal_inputs.html"
