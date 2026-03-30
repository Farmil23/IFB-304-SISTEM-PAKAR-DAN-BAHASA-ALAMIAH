

# CLASS KNOWLEDGE BASE (DATA)
class KnowledgeBase:
    def __init__(self):
       # GEJALA YANG DIKETAHUI BERDASARKAN RANCANGAN
        self.gejala = {
            "G01": {"nama": "Logical Fallacy (Sesat Pikir)", "cf": 0.85},
            "G02": {"nama": "Intrinsic Hallucination (Kontradiksi Data RAG)", "cf": 0.90},
            "G03": {"nama": "Extrinsic Hallucination (Fakta Tak Terverifikasi)", "cf": 0.80},
            "G04": {"nama": "Circular Reasoning (Jawaban Berputar)", "cf": 0.75},
            "G05": {"nama": "Instruction Inconsistency (Format Salah)", "cf": 0.70},
            "G06": {"nama": "Self-Contradiction (Kontradiksi Internal)", "cf": 0.88},
            "G07": {"nama": "Knowledge Cutoff Evasion (Mengarang Kejadian Baru)", "cf": 0.65}
        }
        
        # ATURAN SESUAI DENGAN RANCANGAN 
        self.diagnosa = {
            "P01": {"nama": "Critical Reasoning Failure", "gejala": ["G01", "G06"]},
            "P02": {"nama": "Hallucination Detected", "gejala": ["G02", "G03", "G07"]},
            "P03": {"nama": "Contextual Drift", "gejala": ["G04", "G05"]}
        }
        
class InferenceEngine:
    
    # MENGAMBIL KNOWLEDGE BASE 
    def __init__(self, kb):
        self.kb = kb
    
    # FUNGSI UNTUK MENGHITUNG GEJALA YANG DIPILIH USER DAN SESUAI DENGAN ATURAN
    def hitung_final_cf(self, gejala_user, gejala_aturan):
        """
            Implementasi perhitungan untuk setiap cf yang sesuai dengan aturan
            Rumus yang digunakan : 
                CF_GABUNGAN  = CF_LAMA + CF_BARU * (1 - CF_LAMA)
        """
        
        cf_list = []
        for g_id in gejala_aturan:
            if g_id in gejala_user:
                cf_list.append(self.kb.gejala[g_id]["cf"])
            
        if not cf_list:
            return 0
        
        cf_total = cf_list[0]
        
        for i in range (1, len(cf_list)):
            cur_cf = cf_list[i]
            
            cf_total = cf_total + cur_cf * (1 - cf_total)
        
        return cf_total
    
# FUNGSI UTAMA
def main():
    
    
    kb = KnowledgeBase() # MENGAMBIL DATA
    engine = InferenceEngine(kb) # MENGAMBIL ENGINE UNTUK CF AKHIR
    
    # INTRO USER
    print("=== Expert System: LLM Output Quality Judge ===")
    print("Identifikasi masalah pada output LLM Anda:")
    
    # MENAMPILKAN GEJALA DAN NAMANYA
    for k, v in kb.gejala.items():
        print (f"Kode Gejala : {k}, Nama Gejala: {v["nama"]}")
        
    print("-" * 50)
    print("Pilihlah Gejala Contoh : G01, G02, G03")
    # INPUT UNTUK USER MEMASUKKAN GEJALA
    gejala_user = input("Masukkan Gejala :").upper().replace(" ", "").split(",")
    print("-" * 50)
    
    # UNTUK MENGHENTIKAN PROGRESS JIKA GEJALA TIDAK ADA YANG COCOK
    found = False
    
    for p_id, detail in kb.diagnosa.items():
        hasil_cf = engine.hitung_final_cf(gejala_user=gejala_user, gejala_aturan= detail["gejala"])
        
        if hasil_cf > 0:
            found = True
            print(f"Diagnosa : {detail['nama']}")
            print(f"Kepastian: {hasil_cf * 100:.2f}%")
            print(f"Status   : {'KRITIS' if hasil_cf > 0.8 else 'PERLU PERBAIKAN'}")
            print("-" * 20)
            
    if not found:
        print("Output LLM teridentifikasi AMAN/BERKUALITAS.")
            
if __name__ == "__main__":
    main()