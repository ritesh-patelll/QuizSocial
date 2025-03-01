from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3

class Recaptcha(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV3)