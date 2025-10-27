import requests
import pandas as pd
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from .forms import KaryawanForm, ImportForm

API_URL = settings.API_BASE_URL


def list_karyawans(request):
    try:
        response = requests.get(f"{API_URL}/karyawans/")
        response.raise_for_status()  # Akan raise error untuk status 4xx/5xx
        karyawans = response.json()
    except requests.exceptions.RequestException as e:
        karyawans = []
        messages.error(request, f"Gagal mengambil data dari API: {e}")

    return render(
        request, "karyawan_client/karyawan_list.html", {"karyawans": karyawans}
    )


def add_karyawan(request):
    if request.method == "POST":
        form = KaryawanForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data.get("tanggal_lahir"):
                data["tanggal_lahir"] = data["tanggal_lahir"].isoformat()
            if data.get("tanggal_bergabung"):
                data["tanggal_bergabung"] = data["tanggal_bergabung"].isoformat()

            try:
                response = requests.post(f"{API_URL}/karyawans/", json=data)
                response.raise_for_status()
                messages.success(request, "Karyawan berhasil ditambahkan!")
                return redirect("list_karyawans")
            except requests.exceptions.RequestException as e:
                # Tampilkan error dari API jika ada
                error_detail = "Gagal menambahkan karyawan."
                if e.response is not None and e.response.status_code == 400:
                    error_detail += f" Detail: {e.response.json().get('detail', '')}"
                messages.error(request, error_detail)
    else:
        form = KaryawanForm()
    return render(request, "karyawan_client/karyawan_form.html", {"form": form})


def edit_karyawan(request, karyawan_id):
    if request.method == "POST":
        form = KaryawanForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data.get("tanggal_lahir"):
                data["tanggal_lahir"] = data["tanggal_lahir"].isoformat()
            if data.get("tanggal_bergabung"):
                data["tanggal_bergabung"] = data["tanggal_bergabung"].isoformat()

            try:
                response = requests.put(
                    f"{API_URL}/karyawans/{karyawan_id}/", json=data
                )
                response.raise_for_status()
                messages.success(request, "Data karyawan berhasil diperbarui!")
                return redirect("list_karyawans")
            except requests.exceptions.RequestException as e:
                error_detail = "Gagal memperbarui karyawan."
                if e.response is not None and e.response.status_code == 404:
                    error_detail = "Karyawan tidak ditemukan."
                messages.error(request, error_detail)
    else:
        # Ambil data awal untuk form edit
        try:
            response = requests.get(f"{API_URL}/karyawans/{karyawan_id}/")
            response.raise_for_status()
            karyawan_data = response.json()
            form = KaryawanForm(initial=karyawan_data)
        except requests.exceptions.RequestException:
            messages.error(request, "Gagal mengambil data karyawan untuk diedit.")
            return redirect("list_karyawans")

    return render(
        request, "karyawan_client/karyawan_form.html", {"form": form, "edit_mode": True}
    )


def delete_karyawan(request, karyawan_id):
    try:
        response = requests.delete(f"{API_URL}/karyawans/{karyawan_id}/")
        response.raise_for_status()
        messages.success(request, "Karyawan berhasil dihapus.")
    except requests.exceptions.RequestException:
        messages.error(request, "Gagal menghapus karyawan.")
    return redirect("list_karyawans")


def import_karyawan(request):
    if request.method == "POST":
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data["file"]

            # Baca file berdasarkan ekstensinya
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
                    return redirect("import_karyawan")
            except Exception as e:
                messages.error(request, f"Gagal membaca file: {e}")
                return redirect("import_karyawan")

            success_count = 0
            fail_count = 0
            failed_rows = []

            # Iterasi setiap baris di DataFrame
            for index, row in df.iterrows():
                # Siapkan data untuk dikirim ke API
                # Ganti NaN (kosong) dengan None
                data = row.where(pd.notnull(row), None).to_dict()

                # Konversi tipe data jika perlu (khususnya tanggal)
                if pd.notna(data.get("tanggal_lahir")):
                    data["tanggal_lahir"] = (
                        pd.to_datetime(data["tanggal_lahir"]).date().isoformat()
                    )
                if pd.notna(data.get("tanggal_bergabung")):
                    data["tanggal_bergabung"] = (
                        pd.to_datetime(data["tanggal_bergabung"]).date().isoformat()
                    )

                # Kirim data ke API
                try:
                    response = requests.post(f"{API_URL}/karyawans/", json=data)
                    if response.status_code == 201:
                        success_count += 1
                    else:
                        fail_count += 1
                        # Ambil pesan error dari API jika ada
                        error_detail = response.json().get("detail", "Unknown error")
                        failed_rows.append(
                            {"row": index + 2, "data": data, "error": error_detail}
                        )
                except requests.exceptions.RequestException as e:
                    fail_count += 1
                    failed_rows.append(
                        {"row": index + 2, "data": data, "error": str(e)}
                    )

            # Tampilkan pesan hasil
            if success_count > 0:
                messages.success(
                    request, f"Berhasil mengimport {success_count} karyawan."
                )
            if fail_count > 0:
                messages.warning(
                    request,
                    f"Gagal mengimport {fail_count} karyawan. Lihat baris yang gagal di console developer browser untuk detailnya.",
                )
                # Opsional: Anda bisa menyimpan `failed_rows` di session untuk ditampilkan

            return redirect("list_karyawans")
    else:
        form = ImportForm()

    return render(request, "karyawan_client/import_form.html", {"form": form})
