from django import forms

# Nilai-nilai ini HARUS sama dengan di api_karyawan/schemas.py
KONDISI_CHOICES = [
    ("baik", "Baik"),
    ("rusak ringan", "Rusak Ringan"),
    ("rusak berat", "Rusak Berat"),
    ("dalam perbaikan", "Dalam Perbaikan"),
]

STATUS_CHOICES = [
    ("tersedia", "Tersedia"),
    ("digunakan", "Digunakan"),
    ("dihapuskan", "Dihapuskan"),
]


class InventarisForm(forms.Form):
    nama_alat = forms.CharField(max_length=200, label="Nama Alat")
    kategori = forms.CharField(max_length=100, label="Kategori")
    merk = forms.CharField(max_length=100, required=False, label="Merk")
    model = forms.CharField(max_length=100, required=False, label="Model")
    nomor_seri = forms.CharField(max_length=100, required=False, label="Nomor Seri")
    karyawan_id = forms.IntegerField(
        required=False,
        label="ID Pemegang (Kosongkan jika tersedia)",
        help_text="Masukkan ID angka dari karyawan yang bersangkutan.",
    )
    tanggal_pembelian = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        required=False,
        label="Tanggal Pembelian",
    )
    kondisi = forms.ChoiceField(
        choices=KONDISI_CHOICES, required=False, label="Kondisi"
    )
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label="Status")
