from django import forms
#from pagedown.widgets import PagedownWidget
from apps.saas.models import Offer

class OfferForm(forms.ModelForm):

	#content= forms.CharField(widget=PagedownWidget(show_preview=False))
	#publish= forms.DateField(widget=forms.SelectDateWidget)

	class Meta:
		model = Offer
		fields= [
			"tipo_venta",
			"financing",
			"hardware",
			"empleados",
			"modulos",
		]