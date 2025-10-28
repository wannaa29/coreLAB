import requests
import pandas as pd
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages
from .forms import InventarisForm, ImportForm

API_URL = settings.API_BASE_URL


def list_inventaris(request):
    try:
        response = requests.get(f"{API_URL}/inventaris/")
        response.raise_for_status()
        inventariss_list = response.json()
    except requests.exceptions.RequestException as e:
        inventariss = []
        messages.error(request, f"Gagal mengambil data inventaris dari API: {e}")

    paginator = Paginator(inventariss_list, 3)  # 10 item per halaman
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "inventaris/inventaris_list.html", {"page_obj": page_obj})


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


def import_inventaris(request):
    if request.method == "POST":
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["file"]

            try:
                if file.name.endswith(".csv"):
                    df = pd.read_csv(file)
                elif file.name.endswith((".xls", ".xlsx")):
                    df = pd.read_excel(file)
                else:
                    messages.error(
                        request,
                        "Format file tidak didukung. Harap unggah file CSV atau Excel.",
                    )
                    return redirect("import_inventaris")
            except Exception as e:
                messages.error(request, f"Gagal membaca file: {e}")
                return redirect("import_inventaris")

            success_count = 0
            fail_count = 0
            failed_rows = []

            for index, row in df.iterrows():
                # Siapkan data untuk dikirim ke API
                # Ganti NaN (kosong) dengan None
                data = row.where(pd.notnull(row), None).to_dict()

                # Konversi tipe data jika perlu
                if pd.notna(data.get("tanggal_pembelian")):
                    data["tanggal_pembelian"] = (
                        pd.to_datetime(data["tanggal_pembelian"]).date().isoformat()
                    )

                # Pastikan karyawan_id adalah integer jika tidak kosong
                if pd.notna(data.get("karyawan_id")):
                    data["karyawan_id"] = int(data["karyawan_id"])

                try:
                    response = requests.post(f"{API_URL}/inventaris/", json=data)
                    if response.status_code == 201:
                        success_count += 1
                    else:
                        fail_count += 1
                        error_detail = response.json().get("detail", "Unknown error")
                        failed_rows.append(
                            {"row": index + 2, "data": data, "error": error_detail}
                        )
                except requests.exceptions.RequestException as e:
                    fail_count += 1
                    failed_rows.append(
                        {"row": index + 2, "data": data, "error": str(e)}
                    )

            if success_count > 0:
                messages.success(
                    request, f"Berhasil mengimport {success_count} item inventaris."
                )
            if fail_count > 0:
                messages.warning(
                    request,
                    f"Gagal mengimport {fail_count} item inventaris. Periksa data Anda (misalnya: nomor seri ganda, ID karyawan tidak valid).",
                )

            return redirect("list_inventaris")
    else:
        form = ImportForm()

    return render(request, "inventaris/import_form.html", {"form": form})
