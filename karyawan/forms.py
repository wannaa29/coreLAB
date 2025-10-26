from django import forms
from django.forms import fields, widgets
from .models import Karyawan


class KaryawanForm(forms.ModelForm):
    class Meta:
        model = Karyawan
        fields = ["nama", "email", "nomor_telepon", "posisi", "jenis_kelamin"]
        widgets = {
            "tanggal_bergabung": forms.DateInput(attrs={"type": "date"}),
        }
