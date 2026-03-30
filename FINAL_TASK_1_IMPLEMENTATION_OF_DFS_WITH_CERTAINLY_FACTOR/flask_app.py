from flask import Flask, render_template, request, jsonify
import dfs

app = Flask(__name__)

@app.route('/')
def index():
    # Mengambil list gejala dari modul dfs.py
    gejala_list = [{"kode": k, "nama": v} for k, v in dfs.semua_gejala_nama.items()]
    return render_template('index.html', gejala=gejala_list)

@app.route('/diagnosa', methods=['POST'])
def diagnosa():
    data = request.json
    
    dfs.gejala_dialami.clear()
    
    user_inputs = {k: float(v) for k, v in data.items()}
    dfs.gejala_dialami.update(user_inputs)
    
    hasil_diagnosa = []

    for p_kode, p_data in dfs.knowledge_base.items():
        list_g_kode = list(p_data["gejala"].keys())
        
        # Eksekusi fungsi DFS bawaan
        cf_terkumpul, gejala_cocok = dfs.dfs_penelusuran_gejala(
            kode_penyakit=p_kode, 
            list_gejala=list_g_kode, 
            index=0, 
            cf_terkumpul=[], 
            gejala_cocok=[]
        )
        
        if len(cf_terkumpul) > 0:
            nilai_cf_akhir = dfs.hitung_cf_kombinasi(cf_terkumpul)
            total_gejala_penyakit = len(p_data["gejala"])
            rasio_gejala = len(gejala_cocok) / total_gejala_penyakit
            
            # Penyesuaian persentase
            nilai_cf_penyesuaian = nilai_cf_akhir * rasio_gejala
            persentase = round(nilai_cf_penyesuaian * 100, 2)
            
            hasil_diagnosa.append({
                "kode_penyakit": p_kode,
                "nama_penyakit": p_data["nama_penyakit"],
                "gejala_match": len(gejala_cocok),
                "total_gejala_penyakit": total_gejala_penyakit,
                "keyakinan": persentase,
                "rekomendasi": p_data["rekomendasi"]
            })
            
    hasil_diagnosa = sorted(hasil_diagnosa, key=lambda x: x['keyakinan'], reverse=True)
    hasil_diagnosa = [h for h in hasil_diagnosa if h['keyakinan'] > 0]
    
    return jsonify(hasil_diagnosa)

if __name__ == '__main__':
    app.run( port=5000)
