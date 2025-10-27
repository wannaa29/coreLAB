import requests
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .forms import InventarisForm

API_URL = settings.API_BASE_URL


def list_inventaris(request):
    try:
        response = requests.get(f"{API_URL}/inventaris/")
        response.raise_for_status()
        inventariss = response.json()
    except requests.exceptions.RequestException as e:
        inventariss = []
        messages.error(request, f"Gagal mengambil data inventaris dari API: {e}")

    return render(
        request, "inventaris/inventaris_list.html", {"inventariss": inventariss}
    )


def add_inventaris(request):
    if request.method == "POST":
        form = InventarisForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Konversi date ke string ISO format
            if data.get("tanggal_pembelian"):
                data["tanggal_pembelian"] = data["tanggal_pembelian"].isoformat()

            try:
                response = requests.post(f"{API_URL}/inventaris/", json=data)
                response.raise_for_status()
                messages.success(request, "Inventaris berhasil ditambahkan!")
                return redirect("list_inventaris")
            except requests.exceptions.RequestException as e:
                error_detail = "Gagal menambahkan inventaris."
                if e.response is not None and e.response.status_code == 400:
                    error_detail += f" Detail: {e.response.json().get('detail', '')}"
                messages.error(request, error_detail)
    else:
        form = InventarisForm()
    return render(request, "inventaris/inventaris_form.html", {"form": form})


def edit_inventaris(request, inventaris_id):
    if request.method == "POST":
        form = InventarisForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data.get("tanggal_pembelian"):
                data["tanggal_pembelian"] = data["tanggal_pembelian"].isoformat()

            try:
                response = requests.put(
                    f"{API_URL}/inventaris/{inventaris_id}/", json=data
                )
                response.raise_for_status()
                messages.success(request, "Data inventaris berhasil diperbarui!")
                return redirect("list_inventaris")
            except requests.exceptions.RequestException as e:
                error_detail = "Gagal memperbarui inventaris."
                if e.response is not None and e.response.status_code == 404:
                    error_detail = "Inventaris tidak ditemukan."
                messages.error(request, error_detail)
    else:
        try:
            response = requests.get(f"{API_URL}/inventaris/{inventaris_id}/")
            response.raise_for_status()
            inventaris_data = response.json()
            form = InventarisForm(initial=inventaris_data)
        except requests.exceptions.RequestException:
            messages.error(request, "Gagal mengambil data inventaris untuk diedit.")
            return redirect("list_inventaris")

    return render(
        request, "inventaris/inventaris_form.html", {"form": form, "edit_mode": True}
    )


def delete_inventaris(request, inventaris_id):
    try:
        response = requests.delete(f"{API_URL}/inventaris/{inventaris_id}/")
        response.raise_for_status()
        messages.success(request, "Inventaris berhasil dihapus.")
    except requests.exceptions.RequestException:
        messages.error(request, "Gagal menghapus inventaris.")
    return redirect("list_inventaris")


# Create your views here.
