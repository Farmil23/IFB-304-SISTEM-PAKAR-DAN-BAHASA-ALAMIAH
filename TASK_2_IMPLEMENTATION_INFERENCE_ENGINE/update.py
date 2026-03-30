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
# Diambil dari data Pakar (Kode Penyakit, Gejala, CF Pakar, Rekomendasi)
# INI KNOWLEDGE NANTI DITAMBAHKAN
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

# ---------------------------------------------------------------------
# 2. MESIN INFERENSI (INFERENCE ENGINE) - Forward Chaining & DFS [KITA PAKAI INI YA SEBAGAI PURA PURA DULU]
# ---------------------------------------------------------------------

def sistem_pakar():
    print("="*60)
    print("   SELAMAT DATANG DI SISTEM PAKAR DIAGNOSA SPESIALIS JIWA")
    print("="*60)
    # [UPDATE] Pesan disesuaikan karena sekarang menggunakan bobot keyakinan
    print("Silakan pilih tingkat keyakinan Anda terhadap gejala di bawah ini:\n")
    print("1. Sangat Yakin (1.0)")
    print("2. Yakin (0.8)")
    print("3. Cukup Yakin (0.6)")
    print("4. Sedikit Yakin (0.4)")
    print("5. Tidak Mengalami (0.0)\n")

    # [UPDATE] gejala_dialami diubah jadi dictionary untuk menyimpan {g_kode: nilai_cf_user}
    gejala_dialami = {}

    semua_gejala = {}
    
    # P KODE = "P01, P02, P03"
    # P DATA = isi dari setiap P
    # G KODE = Kode dari setiap gejala yang ada di dalam P DATA
    # G DATA = isi dari G KODE, nama, cf dll

    for p_kode, p_data in knowledge_base.items():   
        for g_kode, g_data in p_data["gejala"].items():
            if g_kode not in semua_gejala:
                semua_gejala[g_kode] = g_data["nama"]
                
    # SEMUA GEJALA DISINI AKAN MENYIMPAN SEMUA G KODE
    # CONTOH YA, {G01 : NAMA GEJALANYA}

    # LALU SETIAP G KODE YANG ADA DI SEMUA GEJALA AKAN DI LOOPING LAGI BERSAMA DATANYA YA
    for g_kode, g_nama in semua_gejala.items():
        while True:
            
            # INI DIKHUSUSKAN UNYUK MEMINTA GEJALA USER
            # [UPDATE] Meminta input angka 1-5 alih-alih Y/T
            print(f"\nApakah Anda mengalami [{g_kode}] {g_nama}?")
            jawaban = input("Pilih angka (1-5): ").strip()
            
            # [UPDATE] Mapping jawaban user ke nilai CF User
            if jawaban == '1': cf_user = 1.0; break
            elif jawaban == '2': cf_user = 0.8; break
            elif jawaban == '3': cf_user = 0.6; break
            elif jawaban == '4': cf_user = 0.4; break
            elif jawaban == '5': cf_user = 0.0; break
            else: 
                print("Input tidak valid! Harap masukkan angka 1-5.")

        if cf_user > 0.0:
            # DISINI AKU NAMBAHIN SETIAP GEJALA USER JIKA JAWABANNYA BUKAN 5 KE GEJALA YANG DIALAMI
            # [UPDATE] Menyimpan g_kode beserta bobot keyakinan (cf_user)-nya
            gejala_dialami[g_kode] = cf_user

    print("\n" + "="*60)
    print("SEDANG MEMPROSES DIAGNOSA (FORWARD CHAINING)...")
    print("="*60)

    hasil_diagnosa = [] 

    # P KODE = "P01, P02, P03"
    # P DATA = isi dari setiap P
    
    for p_kode, p_data in knowledge_base.items():
        cf_terkumpul = []
        gejala_cocok = []
        
        # TEKNIK DFS
        # G USER = ISI DARI GEJALA DIALAMI YAITU SEKARANG [ G01, ETC ] DARI KEYS DICTIONARY
        # [UPDATE] Mengambil g_user dan nilai cf_user dari dictionary gejala_dialami
        for g_user, cf_user_val in gejala_dialami.items():
            if g_user in p_data["gejala"]: 
                # JIKA MEMANG GEJALA USER ADA DI DALAM PENYAKIT MAKA KUMPULKAN CF DAN GEJALA YANG COCOKNYA DIMASUKKAN
                # [UPDATE] Rumus MYCIN murni: CF(Gejala) = CF Pakar * CF User
                cf_pakar = p_data["gejala"][g_user]["cf_pakar"]
                cf_gejala_final = cf_pakar * cf_user_val
                
                cf_terkumpul.append(cf_gejala_final)
                gejala_cocok.append(g_user)
                
        # Jika ada minimal 1 gejala yang cocok untuk penyakit ini, hitung CF
        if len(cf_terkumpul) > 0:
            nilai_cf_akhir = hitung_cf_kombinasi(cf_terkumpul)
            persentase = round(nilai_cf_akhir * 100, 2)
            
            hasil_diagnosa.append({
                "kode_penyakit": p_kode,
                "nama_penyakit": p_data["nama_penyakit"],
                "gejala_match": len(gejala_cocok),
                "keyakinan": persentase,
                "rekomendasi": p_data["rekomendasi"]
            })

    # ---------------------------------------------------------------------
    # 3. MENAMPILKAN HASIL AKHIR
    # ---------------------------------------------------------------------
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
        print(f"   Gejala yang cocok        : {hasil['gejala_match']} gejala")
        print(f"   Rekomendasi              : {hasil['rekomendasi']}")

    print("\n" + "="*60)
    print("CATATAN: Hasil ini adalah screening awal sistem pakar.")
    print("Segera hubungi profesional medis/psikiater untuk diagnosa resmi.")
    print("="*60)

# Jalankan Program Utama
if __name__ == "__main__":
    sistem_pakar()