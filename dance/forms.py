from django.forms import ChoiceField, ModelChoiceField, Form, IntegerField, ModelForm
from django.forms.utils import ErrorList
from .models import StepAppearance, Step, Artist


class AddStepAppearanceErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        return '<div class="errorList">%s</div>' % ''.join(['<p class="small error">%s</p>' % e for e in self])


class AddStepAppearanceForm(Form):
    step = ChoiceField(choices=[])
    minutes = IntegerField()  # default=0, min_value=0)
    seconds = IntegerField()  # default=0, min_value=0, max_value=59)

    def __init__(self, *args, **kwargs):
        super(AddStepAppearanceForm, self).__init__(*args, **kwargs)
        self.fields['step'].choices = [(x.pk, x.name) for x in Step.objects.all().order_by('name')]


class GenericErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        return '<div class="errorList">%s</div>' % ''.join(['<p class="small error">%s</p>' % e for e in self])


class StepForm(ModelForm):
    creator = ModelChoiceField(queryset=Artist.objects.order_by('name'))

    class Meta:
        model = Step
        fields = ['name', 'creator', 'school']


class ArtistForm(ModelForm):
    class Meta:
        model = Artist
        fields = ['name']
