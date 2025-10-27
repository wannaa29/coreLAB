from django import forms

CHOICES_JK = (
    ("Laki-laki", "Laki-laki"),
    ("Perempuan", "Perempuan"),
)

CHOICES_STATUS = (
    ("kontrak", "Kontrak"),
    ("training", "Training"),
    ("tetap", "Tetap"),
)


class KaryawanForm(forms.Form):
    nama = forms.CharField(max_length=100, label="Nama")
    tempat_lahir = forms.CharField(max_length=100, required=False, label="Tempat Lahir")
    tanggal_lahir = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        required=False,
        label="Tanggal Lahir",
    )
    posisi = forms.CharField(max_length=100, required=False, label="Posisi")
    email = forms.EmailField(label="Email")
    jenis_kelamin = forms.ChoiceField(
        choices=CHOICES_JK,
        widget=forms.RadioSelect,
        required=False,
        label="Jenis Kelamin",
    )
    tanggal_bergabung = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        required=False,
        label="Tanggal Bergabung",
    )
    status = forms.ChoiceField(choices=CHOICES_STATUS, required=False, label="Status")


class ImportForm(forms.Form):
    file = forms.FileField(
        label="Pilih File CSV atau Excel",
        help_text="Pastikan file memiliki kolom: nama, email, posisi, tempat_lahir, tanggal_lahir, jenis_kelamin, tanggal_bergabung, status.",
    )
