# =====================================================================
# SISTEM PAKAR DIAGNOSA SPESIALIS JIWA
# Metode: Forward Chaining + Depth-First Search (DFS) + Certainty Factor
# =====================================================================

def hitung_cf_kombinasi(cf_list):
    """
    Menghitung nilai kombinasi Certainty Factor (CF) dari kumpulan gejala.
    Rumus: CF_Lama + CF_Baru * (1 - CF_Lama)
    """
    if not cf_list:
        return 0.0
    
    cf_lama = cf_list[0]
    for i in range(1, len(cf_list)):
        cf_baru = cf_list[i]
        cf_lama = cf_lama + cf_baru * (1 - cf_lama)
        
    return cf_lama

# ---------------------------------------------------------------------
# 1. KNOWLEDGE BASE (BASIS PENGETAHUAN)
# ---------------------------------------------------------------------
knowledge_base = {
    "P01": {
        "nama_penyakit": "ANSIETAS",
        "gejala": {
            "G01": {"nama": "Sering napas pendek", "cf_pakar": 0.90},
            "G02": {"nama": "Nadi dan tekanan darah naik", "cf_pakar": 0.95},
            "G03": {"nama": "Mulut kering", "cf_pakar": 0.90},
            "G04": {"nama": "Anoreksia", "cf_pakar": 0.91},
            "G09": {"nama": "Sakit kepala", "cf_pakar": 0.92},
            "G10": {"nama": "Sulit tidur", "cf_pakar": 0.96},
            "G11": {"nama": "Berkeringat", "cf_pakar": 0.98}
        },
        "rekomendasi": "Teknik relaksasi"
    },
    "P02": {
        "nama_penyakit": "KETIDAKBERDAYAAN",
        "gejala": {
            "G12": {"nama": "Mengungkapkan dengan kata-kata bahwa tidak mempunyai kemampuan mengendalikan atau mempengaruhi situasi", "cf_pakar": 0.92},
            "G13": {"nama": "Mengungkapkan tidak dapat menghasilkan sesuatu", "cf_pakar": 0.99},
            "G14": {"nama": "Mengungkapkan ketidakpuasan dan frustasi terhadap ketidakmampuan untuk melakukan tugas atau aktivitas sebelumnya", "cf_pakar": 0.98},
            "G15": {"nama": "Mengungkapkan keragu-raguan terhadap penampilan peran", "cf_pakar": 0.96},
            "G16": {"nama": "Mengatakan ketidakmampuan perawatan diri", "cf_pakar": 0.93},
            "G17": {"nama": "Menunjukan prilaku ketidakmampuan untuk mencari informasi tentang perawatan diri", "cf_pakar": 0.91},
            "G18": {"nama": "Tidak berpartisipasi dalam pengambilan keputusan saat diberikan kesempatan", "cf_pakar": 0.93},
            "G19": {"nama": "Enggan mengungkapkan perasaan sebenarnya", "cf_pakar": 0.99},
            "G20": {"nama": "Ketergantungan terhadap orang lain yang dapat mengakibatkan iritabilitas, ketidaksukaan, marah dan rasa bersalah", "cf_pakar": 0.98},
            "G21": {"nama": "Gagal mempertahakan ide atau pendapat yang berkaitan dengan orang lain ketika mendapat perlawanan", "cf_pakar": 0.98}
        },
        "rekomendasi": "Mengembangkan harapan positif (afirmasi positif)"
    },
    "P03": {
        "nama_penyakit": "GANGGUAN CITRA TUBUH",
        "gejala": {
            "G22": {"nama": "Hilangnya bagian tubuh", "cf_pakar": 1.0},
            "G23": {"nama": "Perubahan anggota tubuh baik bentuk maupun fungsi", "cf_pakar": 1.0},
            "G24": {"nama": "Menyembunyikan atau memamerkan bagian tubuh yang terganggu", "cf_pakar": 0.96},
            "G25": {"nama": "Menolak melihat bagian tubuh", "cf_pakar": 0.99},
            "G26": {"nama": "Menolak menyentuh bagian tubuh", "cf_pakar": 0.98},
            "G27": {"nama": "Aktifitas sosial menurun", "cf_pakar": 0.95},
            "G28": {"nama": "Mengungkapkan rasa malu/bersalah", "cf_pakar": 0.98},
            "G30": {"nama": "Mengungkapkan hal-hal yang negatif tentang diri (misalnya, ketidakberdayaan dan ketidakbergunaan)", "cf_pakar": 1.0},
            "G31": {"nama": "Kesulitan dalam membuat keputusan", "cf_pakar": 0.98}
        },
        "rekomendasi": "Memberikan dukungan psikososial melalui komunikasi terapeutik untuk membantu pasien menerima perubahan tubuhnya secara bertahap"
    },
    "P04": {
        "nama_penyakit": "HARGA DIRI RENDAH SITUASIONAL",
        "gejala": {
            "G32": {"nama": "Mengungkapkan / menjelek jelekan diri", "cf_pakar": 0.98},
            "G33": {"nama": "Mengungkapkan hal hal yang negatif tentang diri", "cf_pakar": 0.90},
            "G34": {"nama": "Kejadian menyalahkan diri secara episodik terhadap permasalahan hidup yang sebelumnya mempunyai evaluasi diri positif", "cf_pakar": 1.0},
            "G35": {"nama": "Kesulitan dalam membuat keputusan", "cf_pakar": 0.98}
        },
        "rekomendasi": "Membantu mengembangkan kembali harga diri positif melalui kegiatan positif"
    }
}

# Menyimpan riwayat jawaban user agar tidak ditanya dua kali saat backtracking DFS
gejala_dialami = {} 
semua_gejala_nama = {}

# Mengumpulkan semua nama gejala untuk referensi saat print
for p_data in knowledge_base.values():
    for g_kode, g_data in p_data["gejala"].items():
        if g_kode not in semua_gejala_nama:
            semua_gejala_nama[g_kode] = g_data["nama"]

# ---------------------------------------------------------------------
# 2. MESIN INFERENSI DENGAN DFS (DEPTH-FIRST SEARCH) MURNI (REKURSIF)
# ---------------------------------------------------------------------

def dfs_penelusuran_gejala(kode_penyakit, list_gejala, index, cf_terkumpul, gejala_cocok):
    """
    Fungsi Rekursif untuk menelusuri cabang (gejala) dari suatu Rule (Penyakit) secara mendalam.
    Sesuai dengan konsep Graph Traversal pada DFS.
    """
    # BASE CASE DFS: Jika sudah menelusuri semua gejala di cabang penyakit ini sampai daun terakhir
    if index >= len(list_gejala):
        return cf_terkumpul, gejala_cocok
    
    g_kode = list_gejala[index]
    
    # Memeriksa node saat ini. Jika belum pernah dikunjungi/ditanya, tanyakan!
    if g_kode not in gejala_dialami:
        print(f"\n[Evaluasi {knowledge_base[kode_penyakit]['nama_penyakit']}]")
        print(f"Apakah Anda mengalami [{g_kode}] {semua_gejala_nama[g_kode]}?")
        
        while True:
            jawaban = input("Pilih angka (1-5): ").strip()
            if jawaban == '1': cf_user = 1.0; break
            elif jawaban == '2': cf_user = 0.8; break
            elif jawaban == '3': cf_user = 0.6; break
            elif jawaban == '4': cf_user = 0.4; break
            elif jawaban == '5': cf_user = 0.0; break
            else: 
                print("Input tidak valid! Harap masukkan angka 1-5.")
                
        # Simpan state di memory agar DFS cabang lain tidak menanya ulang
        gejala_dialami[g_kode] = cf_user
        
    # Ambil nilai yang sudah disimpan di memori
    cf_user_val = gejala_dialami[g_kode]
    
    # Jika bernilai positif (user mengalami), hitung probabilitasnya
    if cf_user_val > 0.0:
        cf_pakar = knowledge_base[kode_penyakit]["gejala"][g_kode]["cf_pakar"]
        cf_gejala_final = cf_pakar * cf_user_val
        
        cf_terkumpul.append(cf_gejala_final)
        gejala_cocok.append(g_kode)
        
    # REKURSIF DFS: Menyelam lebih dalam ke node (gejala) berikutnya pada cabang penyakit ini
    return dfs_penelusuran_gejala(kode_penyakit, list_gejala, index + 1, cf_terkumpul, gejala_cocok)


def sistem_pakar():
    print("="*60)
    print("   SELAMAT DATANG DI SISTEM PAKAR DIAGNOSA SPESIALIS JIWA")
    print("="*60)
    print("Silakan pilih tingkat keyakinan Anda terhadap gejala di bawah ini:\n")
    print("1. Sangat Yakin (1.0)")
    print("2. Yakin (0.8)")
    print("3. Cukup Yakin (0.6)")
    print("4. Sedikit Yakin (0.4)")
    print("5. Tidak Mengalami (0.0)\n")
    print("Memulai penelusuran (Depth-First Search)...")
    
    hasil_diagnosa = []
    
    # Iterasi setiap node ROOT (Penyakit / Rule)
    for p_kode, p_data in knowledge_base.items():
        # Mendapatkan daftar node child (gejala) dari penyakit ini
        list_g_kode = list(p_data["gejala"].keys())
        
        # Panggil fungsi rekursif DFS
        cf_terkumpul, gejala_cocok = dfs_penelusuran_gejala(
            kode_penyakit=p_kode, 
            list_gejala=list_g_kode, 
            index=0, 
            cf_terkumpul=[], 
            gejala_cocok=[]
        )
        
        # Jika dari penelusuran DFS ditemukan gejala yang cocok, hitung CF total
        if len(cf_terkumpul) > 0:
            nilai_cf_akhir = hitung_cf_kombinasi(cf_terkumpul)
            
            # --- TAMBAHAN MODIFIKASI RASIO GEJALA ---
            # Hitung persentase dari jumlah gejala yang cocok dibanding total gejala penyakit tsb
            total_gejala_penyakit = len(p_data["gejala"])
            rasio_gejala = len(gejala_cocok) / total_gejala_penyakit
            
            # Kalikan nilai CF akhir dengan rasio tersebut
            nilai_cf_penyesuaian = nilai_cf_akhir * rasio_gejala
            
            persentase = round(nilai_cf_penyesuaian * 100, 2)
            # ----------------------------------------
            
            hasil_diagnosa.append({
                "kode_penyakit": p_kode,
                "nama_penyakit": p_data["nama_penyakit"],
                "gejala_match": len(gejala_cocok),
                "total_gejala_penyakit": total_gejala_penyakit, # Info tambahan disimpan ke dictionary
                "keyakinan": persentase,
                "rekomendasi": p_data["rekomendasi"]
            })

    # ---------------------------------------------------------------------
    # 3. MENAMPILKAN HASIL AKHIR
    # ---------------------------------------------------------------------
    print("\n" + "="*60)
    print("PROSES DFS SELESAI. MENGHITUNG HASIL DIAGNOSA...")
    print("="*60)

    if not hasil_diagnosa:
        print("\nAnda tidak mengalami gejala yang mengarah pada penyakit jiwa dalam sistem kami.")
        print("Tetap jaga kesehatan mental Anda!")
        return

    # INI DIURUTKAN BERDASARKAN PERSENTASE
    hasil_diagnosa = sorted(hasil_diagnosa, key=lambda x: x['keyakinan'], reverse=True)

    print("\nHASIL DIAGNOSA:")
    
    # INI UNTUK MEMUNCULKAN HASIL DIAGNOSA YANG UDAH DIANALISIS SEBELUMNYA
    for idx, hasil in enumerate(hasil_diagnosa):
        print(f"\n{idx+1}. {hasil['nama_penyakit']} ({hasil['kode_penyakit']})")
        print(f"   Tingkat Keyakinan Sistem : {hasil['keyakinan']}%")
        
        # ---- BAGIAN INI YANG DIPERBAIKI (Tampilan Output) ----
        print(f"   Gejala yang cocok        : {hasil['gejala_match']} dari {hasil['total_gejala_penyakit']} gejala")
        # ------------------------------------------------------
        
        print(f"   Rekomendasi              : {hasil['rekomendasi']}")

    print("\n" + "="*60)
    print("CATATAN: Hasil ini adalah screening awal sistem pakar.")
    print("Segera hubungi profesional medis/psikiater untuk diagnosa resmi.")
    print("="*60)

# Jalankan Program Utama
if __name__ == "__main__":
    sistem_pakar()