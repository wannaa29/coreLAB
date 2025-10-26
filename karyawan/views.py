import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import KaryawanForm

API_URL = settings.API_BASE_URL


def list_karyawans(request):
    response = requests.get(f"{API_URL}/karyawans/")
    karyawans = response.json()
    return render(
        request, "karyawan_client/karyawan_list.html", {"karyawans": karyawans}
    )


def add_karyawan(request):
    if request.method == "POST":
        form = KaryawanForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Konversi objek date ke string format YYYY-MM-DD
            if data["tanggal_lahir"]:
                data["tanggal_lahir"] = data["tanggal_lahir"].isoformat()
            if data["tanggal_bergabung"]:
                data["tanggal_bergabung"] = data["tanggal_bergabung"].isoformat()

            requests.post(f"{API_URL}/karyawans/", json=data)
            return redirect("list_karyawans")
    else:
        form = KaryawanForm()
    return render(request, "karyawan_client/karyawan_form.html", {"form": form})


def edit_karyawan(request, karyawan_id):
    # Ambil data karyawan dari API untuk mengisi form
    response = requests.get(f"{API_URL}/karyawans/{karyawan_id}/")
    karyawan_data = response.json()

    if request.method == "POST":
        form = KaryawanForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data["tanggal_lahir"]:
                data["tanggal_lahir"] = data["tanggal_lahir"].isoformat()
            if data["tanggal_bergabung"]:
                data["tanggal_bergabung"] = data["tanggal_bergabung"].isoformat()

            requests.put(f"{API_URL}/karyawans/{karyawan_id}/", json=data)
            return redirect("list_karyawans")
    else:
        # Pre-populate form dengan data dari API
        form = KaryawanForm(initial=karyawan_data)

    return render(
        request, "karyawan_client/karyawan_form.html", {"form": form, "edit_mode": True}
    )


def delete_karyawan(request, karyawan_id):
    requests.delete(f"{API_URL}/karyawans/{karyawan_id}/")
    return redirect("list_karyawans")
