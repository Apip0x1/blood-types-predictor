import os
import re

# ============================
# MENU
# ============================
os.system("clear")
print("======================")
print("BLOOD TYPE'S PREDICTOR")
print("======================")

def menu():
    print("\n===================================")
    print("Masukkan angka untuk memilih menu\n")
    print("1. Prediksi dari fenotipe (A, B, O, AB)")
    print("2. Prediksi dari genotipe (IAIA, IAi, IBi, ii, dst)")
    print("===================================")
    return input("Masukkan Angka ~: ").strip()

# ============================
# INPUT FENOTIPE
# ============================
def baca_tipe_orangtua():
    goldar = {"A", "B", "AB", "O"}
    ayah = input("Golongan darah Ayah (A/B/AB/O): ").strip().upper()
    ibu  = input("Golongan darah Ibu  (A/B/AB/O): ").strip().upper()
    
    if ayah not in goldar or ibu not in goldar:
        print("Input harus salah satu dari: A, B, AB, O")
        exit()
    return ayah, ibu

# ============================
# HITUNG FENOTIPE
# ============================
def hitung_probabilitas(ayah, ibu):
    tabel = {
        ("A", "A"): {"A": 75, "O": 25},
        ("A", "B"): {"A": 25, "B": 25, "AB": 25, "O": 25},
        ("A", "AB"): {"A": 50, "B": 25, "AB": 25},
        ("A", "O"): {"A": 50, "O": 50},

        ("B", "B"): {"B": 75, "O": 25},
        ("B", "AB"): {"A": 25, "B": 50, "AB": 25},
        ("B", "O"): {"B": 50, "O": 50},

        ("AB", "AB"): {"A": 25, "B": 25, "AB": 50},
        ("AB", "O"): {"A": 50, "B": 50},

        ("O", "O"): {"O": 100},
    }
    return tabel.get((ayah, ibu)) or tabel.get((ibu, ayah), {"Tidak diketahui": 0})

# ============================
# PREDIKSI GENOTIPE (FENOTIPE)
# ============================
def prediksi_genotipe(ayah, ibu):
    tabel = {
        ("A", "A"): ["IAIA", "IAi", "IAi", "ii"],
        ("A", "B"): ["IAIB", "IAi", "IBi", "ii"],
        ("A", "AB"): ["IAIA", "IAIB", "IAi", "IBi"],
        ("A", "O"): ["IAi", "IAi", "ii", "ii"],

        ("B", "B"): ["IBIB", "IBi", "IBi", "ii"],
        ("B", "AB"): ["IBIB", "IAIB", "IAi", "IBi"],
        ("B", "O"): ["IBi", "IBi", "ii", "ii"],

        ("AB", "AB"): ["IAIA", "IAIB", "IBIB", "IAIB"],
        ("AB", "O"): ["IAi", "IBi", "IAi", "IBi"],

        ("O", "O"): ["ii", "ii", "ii", "ii"]
    }

    data = tabel.get((ayah, ibu)) or tabel.get((ibu, ayah))
    hasil = {}
    for g in data:
        hasil[g] = hasil.get(g, 0) + 25
    return hasil

def parse_gen(g):
    g = g.strip().upper()

    # Cari pola IA, IB, atau i
    alleles = re.findall(r'IA|IB|I', g)

    # Ubah alel tunggal "I" menjadi "i"
    alleles = ["i" if a == "I" else a for a in alleles]

    # Validasi jumlah alel
    if len(alleles) != 2:
        print("Genotipe tidak valid. Harus 2 alel (contoh: IAIA, IAi, IBi, ii)")
        exit()

    return alleles


# ============================
# KOMBINASI GENOTIPE ANAK
# ============================
def prediksi_dari_genotipe(gen_ayah, gen_ibu):
    ayah = parse_gen(gen_ayah)
    ibu  = parse_gen(gen_ibu)

    kombinasi = []
    for a in ayah:
        for b in ibu:
            anak = "".join(sorted([a, b]))  # sort biar konsisten
            kombinasi.append(anak)

    total = len(kombinasi)
    hasil = {}
    for k in kombinasi:
        hasil[k] = hasil.get(k, 0) + (100 / total)

    return hasil

# ============================
# GENOTIPE → FENOTIPE
# ============================
def genotipe_ke_fenotipe(gen):
    alel = parse_gen(gen)          # gunakan parser yang benar
    alel = sorted(alel)            # normalisasi

    if alel == ["IA", "IA"] or alel == ["IA", "i"]:
        return "A"
    if alel == ["IB", "IB"] or alel == ["IB", "i"]:
        return "B"
    if alel == ["IA", "IB"]:
        return "AB"
    if alel == ["i", "i"]:
        return "O"

    return "?"

# ============================
# MAIN
# ============================
if __name__ == "__main__":
    pilihan = menu()

    # MENU 1 — FENOTIPE
    if pilihan == "1":
        ayah, ibu = baca_tipe_orangtua()
        hasil = hitung_probabilitas(ayah, ibu)

        print("\nProbabilitas golongan darah anak:")
        for gol, p in hasil.items():
            print(f"{gol}: {p}%")

        print("\nPrediksi Genotipe Anak:")
        for g, p in prediksi_genotipe(ayah, ibu).items():
            print(f"{g}: {p}%")
        exit()


    # MENU 2 — GENOTIPE → GENOTIPE + FENOTIPE
    if pilihan == "2":
        print("Contoh input genotipe: IAIA, IAi, IBi, ii")
        gen_ayah = input("Genotipe Ayah: ").strip()
        gen_ibu  = input("Genotipe Ibu : ").strip()

        hasil = prediksi_dari_genotipe(gen_ayah, gen_ibu)

        print("\nPrediksi Genotipe Anak:")
        for g, p in hasil.items():
            print(f"{g}: {p:.0f}%")

        print("\nPrediksi Golongan Darah Anak (fenotipe):")
        feno = {}
        for g, p in hasil.items():
            tipe = genotipe_ke_fenotipe(g)
            feno[tipe] = feno.get(tipe, 0) + p

        for f, p in feno.items():
            print(f"{f}: {p:.0f}%")
        exit()

    print("Masukkan input yang benar.")
