import csv
import os

PESERTA_FILE = "peserta.csv"
KATEGORI_FILE = "kategori.csv"

class HashMapNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashMap:
    def __init__(self, capacity=101):
        self.capacity = capacity
        self.buckets = [None] * self.capacity
        self.jumlah_data = 0

    def _hash(self, key):
        return hash(str(key)) % self.capacity

    def put(self, key, value):
        index = self._hash(key)
        node = self.buckets[index]
        while node:
            if node.key == key:
                node.value = value
                return
            node = node.next
        node_baru = HashMapNode(key, value)
        node_baru.next = self.buckets[index]
        self.buckets[index] = node_baru
        self.jumlah_data += 1

    def get(self, key):
        index = self._hash(key)
        node = self.buckets[index]
        while node:
            if node.key == key:
                return node.value
            node = node.next
        return None

    def remove(self, key):
        index = self._hash(key)
        node = self.buckets[index]
        prev = None
        while node:
            if node.key == key:
                if prev:
                    prev.next = node.next
                else:
                    self.buckets[index] = node.next
                self.jumlah_data -= 1
                return True
            prev = node
            node = node.next
        return False

    def contains(self, key):
        return self.get(key) is not None

    def semua_value(self):
        hasil = []
        for node in self.buckets:
            while node:
                hasil.append(node.value)
                node = node.next
        return hasil

class QueueNode:
    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    """
    Queue FIFO custom berbasis linked list.
    Dipakai sebagai waiting list peserta saat kuota kategori penuh.
    enqueue & dequeue O(1).
    """

    def __init__(self):
        self.depan = None
        self.belakang = None
        self.ukuran = 0

    def is_empty(self):
        return self.ukuran == 0

    def enqueue(self, data):
        node = QueueNode(data)
        if self.belakang is None:
            self.depan = node
            self.belakang = node
        else:
            self.belakang.next = node
            self.belakang = node
        self.ukuran += 1

    def dequeue(self):
        if self.is_empty():
            return None
        node = self.depan
        self.depan = node.next
        if self.depan is None:
            self.belakang = None
        self.ukuran -= 1
        return node.data

    def ke_list(self):
        hasil = []
        node = self.depan
        while node:
            hasil.append(node.data)
            node = node.next
        return hasil

def merge_sort(data, key_func):
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    kiri = merge_sort(data[:mid], key_func)
    kanan = merge_sort(data[mid:], key_func)
    return _merge(kiri, kanan, key_func)


def _merge(kiri, kanan, key_func):
    hasil = []
    i = j = 0
    while i < len(kiri) and j < len(kanan):
        if key_func(kiri[i]) <= key_func(kanan[j]):
            hasil.append(kiri[i])
            i += 1
        else:
            hasil.append(kanan[j])
            j += 1
    hasil.extend(kiri[i:])
    hasil.extend(kanan[j:])
    return hasil


def binary_search_bib(data_terurut, target_bib):
    kiri, kanan = 0, len(data_terurut) - 1
    while kiri <= kanan:
        tengah = (kiri + kanan) // 2
        bib_tengah = int(data_terurut[tengah]["bib"])
        if bib_tengah == target_bib:
            return data_terurut[tengah]
        elif bib_tengah < target_bib:
            kiri = tengah + 1
        else:
            kanan = tengah - 1
    return None


def linear_search_nama(data, keyword):
    keyword = keyword.lower()
    return [p for p in data if keyword in p["nama"].lower()]

def format_waktu(detik_str):
    detik = int(detik_str)
    jam = detik // 3600
    menit = (detik % 3600) // 60
    sisa_detik = detik % 60
    if jam > 0:
        return f"{jam}j {menit}m {sisa_detik}d"
    return f"{menit}m {sisa_detik}d"


def parse_waktu(teks):
    bagian = [int(b) for b in teks.split(":")]
    if len(bagian) == 2:
        menit, detik = bagian
        return menit * 60 + detik
    elif len(bagian) == 3:
        jam, menit, detik = bagian
        return jam * 3600 + menit * 60 + detik
    raise ValueError("Format waktu tidak valid")


def tampilkan_detail_peserta(p):
    waktu = format_waktu(p["waktu_finish_detik"]) if p["waktu_finish_detik"] else "-"
    print(f"BIB: {p['bib']} | Nama: {p['nama']} | Usia: {p['usia']} | Gender: {p['gender']}")
    print(f"No HP: {p['no_hp']} | Kategori: {p['kategori_id']} | Status: {p['status']} | Waktu: {waktu}")

def buat_file_default():
    if not os.path.exists(KATEGORI_FILE):
        with open(KATEGORI_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["kategori_id", "nama_kategori", "jarak_km", "kuota_maks", "terisi"])
            writer.writerow(["K1", "5K Fun Run", "5", "3", "0"])
            writer.writerow(["K2", "10K Road Race", "10", "3", "0"])
            writer.writerow(["K3", "Half Marathon Trail", "21", "2", "0"])

    if not os.path.exists(PESERTA_FILE):
        with open(PESERTA_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["bib", "nama", "usia", "gender", "no_hp", "kategori_id", "status", "waktu_finish_detik", "urutan"])


def load_peserta():
    peserta_map = HashMap()
    if os.path.exists(PESERTA_FILE):
        with open(PESERTA_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                peserta_map.put(row["bib"], row)
    return peserta_map


def simpan_peserta(peserta_map):
    fieldnames = ["bib", "nama", "usia", "gender", "no_hp", "kategori_id", "status", "waktu_finish_detik", "urutan"]
    with open(PESERTA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for data in peserta_map.semua_value():
            writer.writerow(data)


def load_kategori():
    kategori_list = []
    if os.path.exists(KATEGORI_FILE):
        with open(KATEGORI_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                kategori_list.append(row)
    return kategori_list


def simpan_kategori(kategori_list):
    fieldnames = ["kategori_id", "nama_kategori", "jarak_km", "kuota_maks", "terisi"]
    with open(KATEGORI_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for k in kategori_list:
            writer.writerow(k)


def cari_kategori(kategori_list, kategori_id):
    for k in kategori_list:
        if k["kategori_id"] == kategori_id:
            return k
    return None


def get_next_urutan(peserta_map):
    semua = peserta_map.semua_value()
    if not semua:
        return 1
    return max(int(p.get("urutan", 0) or 0) for p in semua) + 1


def bangun_antrian_tunggu():
    daftar_tunggu = []
    if os.path.exists(PESERTA_FILE):
        with open(PESERTA_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["status"] == "Waiting List":
                    daftar_tunggu.append(row)

    daftar_tunggu.sort(key=lambda r: int(r["urutan"]))

    antrian = {}
    for row in daftar_tunggu:
        kid = row["kategori_id"]
        if kid not in antrian:
            antrian[kid] = Queue()
        antrian[kid].enqueue(row["bib"])
    return antrian


def tambah_peserta(peserta_map, kategori_list, antrian_tunggu):
    print("\n=== TAMBAH PESERTA BARU ===")
    bib = input("Nomor BIB (unik): ").strip()
    if not bib:
        print("BIB tidak boleh kosong.")
        return
    if peserta_map.contains(bib):
        print("BIB sudah dipakai peserta lain. Gagal menambah.")
        return

    print("Kategori tersedia:")
    for k in kategori_list:
        print(f"  {k['kategori_id']} - {k['nama_kategori']} ({k['jarak_km']} km) | terisi {k['terisi']}/{k['kuota_maks']}")

    kategori_id = input("Pilih kategori_id: ").strip()
    kategori = cari_kategori(kategori_list, kategori_id)
    if kategori is None:
        print("Kategori tidak ditemukan.")
        return

    nama = input("Nama: ").strip()
    usia = input("Usia: ").strip()
    gender = input("Gender (L/P): ").strip()
    no_hp = input("No HP: ").strip()

    terisi = int(kategori["terisi"])
    kuota = int(kategori["kuota_maks"])

    if terisi < kuota:
        status = "Terdaftar"
        kategori["terisi"] = str(terisi + 1)
        print(f"Pendaftaran berhasil. Status: {status}")
    else:
        status = "Waiting List"
        if kategori_id not in antrian_tunggu:
            antrian_tunggu[kategori_id] = Queue()
        antrian_tunggu[kategori_id].enqueue(bib)
        print(f"Kuota kategori penuh. {nama} masuk Waiting List (posisi ke-{antrian_tunggu[kategori_id].ukuran}).")

    data_peserta = {
        "bib": bib, "nama": nama, "usia": usia, "gender": gender,
        "no_hp": no_hp, "kategori_id": kategori_id, "status": status,
        "waktu_finish_detik": "", "urutan": str(get_next_urutan(peserta_map))
    }
    peserta_map.put(bib, data_peserta)
    simpan_peserta(peserta_map)
    simpan_kategori(kategori_list)


def lihat_semua_peserta(peserta_map):
    data = peserta_map.semua_value()
    if not data:
        print("Belum ada peserta terdaftar.")
        return
    print(f"\n{'BIB':<6}{'Nama':<20}{'Kategori':<10}{'Status':<14}{'Waktu Finish'}")
    print("-" * 65)
    for p in data:
        waktu = format_waktu(p["waktu_finish_detik"]) if p["waktu_finish_detik"] else "-"
        print(f"{p['bib']:<6}{p['nama']:<20}{p['kategori_id']:<10}{p['status']:<14}{waktu}")


def cari_peserta_menu(peserta_map):
    data = peserta_map.semua_value()
    if not data:
        print("Belum ada data peserta.")
        return
    print("\n1. Cari berdasarkan BIB (Binary Search)")
    print("2. Cari berdasarkan Nama (Linear Search)")
    pilihan = input("Pilih: ").strip()

    if pilihan == "1":
        try:
            target = int(input("Masukkan BIB: ").strip())
        except ValueError:
            print("BIB harus berupa angka.")
            return
        data_terurut = merge_sort(data, lambda p: int(p["bib"]))
        hasil = binary_search_bib(data_terurut, target)
        if hasil:
            tampilkan_detail_peserta(hasil)
        else:
            print("Peserta dengan BIB tersebut tidak ditemukan.")
    elif pilihan == "2":
        keyword = input("Masukkan nama (atau sebagian): ").strip()
        hasil = linear_search_nama(data, keyword)
        if hasil:
            for p in hasil:
                tampilkan_detail_peserta(p)
        else:
            print("Tidak ada peserta dengan nama tersebut.")
    else:
        print("Pilihan tidak valid.")


def update_peserta(peserta_map):
    bib = input("Masukkan BIB peserta yang ingin diupdate: ").strip()
    data = peserta_map.get(bib)
    if data is None:
        print("Peserta tidak ditemukan.")
        return

    print("Data saat ini:")
    tampilkan_detail_peserta(data)
    print("\nKosongkan input jika tidak ingin mengubah field tersebut.")

    nama_baru = input(f"Nama baru [{data['nama']}]: ").strip()
    if nama_baru:
        data["nama"] = nama_baru

    no_hp_baru = input(f"No HP baru [{data['no_hp']}]: ").strip()
    if no_hp_baru:
        data["no_hp"] = no_hp_baru

    status_baru = input(f"Status baru (Terdaftar/Selesai/DNF) [{data['status']}]: ").strip()
    if status_baru:
        data["status"] = status_baru

    if data["status"] == "Selesai":
        waktu = input("Waktu finish (format menit:detik, contoh 24:30): ").strip()
        if waktu:
            try:
                data["waktu_finish_detik"] = str(parse_waktu(waktu))
            except ValueError:
                print("Format waktu tidak valid, waktu finish tidak diubah.")

    peserta_map.put(bib, data)
    simpan_peserta(peserta_map)
    print("Data berhasil diperbarui.")


def hapus_peserta(peserta_map, kategori_list, antrian_tunggu):
    bib = input("Masukkan BIB peserta yang ingin dihapus: ").strip()
    data = peserta_map.get(bib)
    if data is None:
        print("Peserta tidak ditemukan.")
        return

    kategori_id = data["kategori_id"]
    status_lama = data["status"]
    peserta_map.remove(bib)

    kategori = cari_kategori(kategori_list, kategori_id)
    if status_lama == "Terdaftar" and kategori:
        kategori["terisi"] = str(max(0, int(kategori["terisi"]) - 1))
        if kategori_id in antrian_tunggu and not antrian_tunggu[kategori_id].is_empty():
            bib_promosi = antrian_tunggu[kategori_id].dequeue()
            peserta_promosi = peserta_map.get(bib_promosi)
            if peserta_promosi:
                peserta_promosi["status"] = "Terdaftar"
                kategori["terisi"] = str(int(kategori["terisi"]) + 1)
                peserta_map.put(bib_promosi, peserta_promosi)
                print(f"{peserta_promosi['nama']} (BIB {bib_promosi}) otomatis naik dari Waiting List ke Terdaftar.")

    simpan_peserta(peserta_map)
    simpan_kategori(kategori_list)
    print("Peserta berhasil dihapus.")


def lihat_antrian_tunggu(antrian_tunggu, peserta_map):
    if not antrian_tunggu or all(q.is_empty() for q in antrian_tunggu.values()):
        print("Tidak ada peserta dalam waiting list.")
        return
    for kategori_id, queue in antrian_tunggu.items():
        if queue.is_empty():
            continue
        print(f"\nWaiting List kategori {kategori_id}:")
        for posisi, bib in enumerate(queue.ke_list(), start=1):
            p = peserta_map.get(bib)
            nama = p["nama"] if p else "?"
            print(f"  {posisi}. BIB {bib} - {nama}")


def tampilkan_leaderboard(peserta_map, kategori_list):
    data = peserta_map.semua_value()
    selesai = [p for p in data if p["status"] == "Selesai" and p["waktu_finish_detik"]]
    if not selesai:
        print("Belum ada peserta yang menyelesaikan race.")
        return

    print("\nPilih kategori untuk leaderboard:")
    for k in kategori_list:
        print(f"  {k['kategori_id']} - {k['nama_kategori']}")
    kategori_id = input("Kategori (kosongkan untuk semua): ").strip()

    if kategori_id:
        selesai = [p for p in selesai if p["kategori_id"] == kategori_id]

    if not selesai:
        print("Tidak ada hasil untuk kategori tersebut.")
        return

    terurut = merge_sort(selesai, lambda p: int(p["waktu_finish_detik"]))

    print(f"\n{'Peringkat':<10}{'BIB':<6}{'Nama':<20}{'Waktu'}")
    print("-" * 50)
    for i, p in enumerate(terurut, start=1):
        print(f"{i:<10}{p['bib']:<6}{p['nama']:<20}{format_waktu(p['waktu_finish_detik'])}")


def tampilkan_statistik(peserta_map, kategori_list):
    data = peserta_map.semua_value()
    total = len(data)
    selesai = len([p for p in data if p["status"] == "Selesai"])
    dnf = len([p for p in data if p["status"] == "DNF"])
    waiting = len([p for p in data if p["status"] == "Waiting List"])

    print(f"\nTotal peserta terdaftar : {total}")
    print(f"Menyelesaikan race      : {selesai}")
    print(f"DNF (Did Not Finish)    : {dnf}")
    print(f"Waiting list             : {waiting}")
    print("\nPer kategori:")
    for k in kategori_list:
        print(f"  {k['nama_kategori']} ({k['jarak_km']} km): {k['terisi']}/{k['kuota_maks']} kuota terisi")


def main():
    buat_file_default()
    peserta_map = load_peserta()
    kategori_list = load_kategori()
    antrian_tunggu = bangun_antrian_tunggu()

    while True:
        print("\n" + "=" * 50)
        print("   SiLARI - SISTEM MANAJEMEN EVENT LARI")
        print("=" * 50)
        print("1. Tambah Peserta (Create)")
        print("2. Lihat Semua Peserta (Read)")
        print("3. Cari Peserta (Search)")
        print("4. Update Data Peserta (Update)")
        print("5. Hapus Peserta (Delete)")
        print("6. Lihat Waiting List")
        print("7. Leaderboard Hasil Race (Sorting)")
        print("8. Statistik Event")
        print("0. Keluar")
        pilihan = input("Pilih menu: ").strip()

        if pilihan == "1":
            tambah_peserta(peserta_map, kategori_list, antrian_tunggu)
        elif pilihan == "2":
            lihat_semua_peserta(peserta_map)
        elif pilihan == "3":
            cari_peserta_menu(peserta_map)
        elif pilihan == "4":
            update_peserta(peserta_map)
        elif pilihan == "5":
            hapus_peserta(peserta_map, kategori_list, antrian_tunggu)
        elif pilihan == "6":
            lihat_antrian_tunggu(antrian_tunggu, peserta_map)
        elif pilihan == "7":
            tampilkan_leaderboard(peserta_map, kategori_list)
        elif pilihan == "8":
            tampilkan_statistik(peserta_map, kategori_list)
        elif pilihan == "0":
            print("Data tersimpan. Sampai jumpa di garis finish berikutnya!")
            break
        else:
            print("Pilihan tidak valid, coba lagi.")


if __name__ == "__main__":
    main()

