# karyawan/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Karyawan
from .forms import KaryawanForm  # Akan kita buat selanjutnya


# READ - Menampilkan daftar semua karyawan
def daftar_karyawan(request):
    all_karyawan = Karyawan.objects.all()
    context = {
        "karyawan_list": all_karyawan,
    }
    return render(request, "karyawan/daftar_karyawan.html", context)


# CREATE - Menambahkan karyawan baru
def tambah_karyawan(request):
    if request.method == "POST":
        form = KaryawanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("daftar_karyawan")
    else:
        form = KaryawanForm()

    return render(request, "karyawan/tambah_karyawan.html", {"form": form})


# UPDATE - Mengedit data karyawan
def edit_karyawan(request, pk):
    karyawan = get_object_or_404(Karyawan, pk=pk)
    if request.method == "POST":
        form = KaryawanForm(request.POST, instance=karyawan)
        if form.is_valid():
            form.save()
            return redirect("daftar_karyawan")
    else:
        form = KaryawanForm(instance=karyawan)

    return render(request, "karyawan/edit_karyawan.html", {"form": form})


# DELETE - Menghapus karyawan
def hapus_karyawan(request, pk):
    karyawan = get_object_or_404(Karyawan, pk=pk)
    if request.method == "POST":
        karyawan.delete()
        return redirect("daftar_karyawan")

    return render(request, "karyawan/hapus_karyawan.html", {"karyawan": karyawan})
