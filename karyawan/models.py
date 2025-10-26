from enum import unique
from inspect import modulesbyfile
from django.db import models
from django.utils import choices


class Karyawan(models.Model):
    JENIS_KELAMIN_CHOICE = (
        ("P", "Pria"),
        ("W", "Wanita"),
    )

    nama = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    nomor_telepon = models.CharField(max_length=15, blank=True, null=True)
    posisi = models.CharField(max_length=100)
    tanggal_bergabung = models.DateTimeField(auto_now=True)
    jenis_kelamin = models.CharField(max_length=1, choices=JENIS_KELAMIN_CHOICE)

    def __str__(self):
        # Fungsi ini untuk menampilkan nama karyawan di admin panel
        return self.nama
