import streamlit as st
import dfs

st.set_page_config(
    page_title="Sistem Pakar Diagnosa Spesialis Jiwa",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        background: -webkit-linear-gradient(45deg, #4CAF50, #2E86AB);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 800;
        margin-bottom: 5px;
        padding-top: 20px;
    }
    .sub-header {
        font-size: 1.1rem;
        text-align: center;
        margin-bottom: 40px;
        font-weight: 500;
        opacity: 0.8;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🧠 Sistem Pakar Diagnosa Jiwa</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Forward Chaining • Depth-First Search (DFS) • Certainty Factor</div>', unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.header("💻 Tentang Sistem Pakar")
    st.info("Sistem ini adalah wadah screening awal (kecerdasan buatan) yang bertindak sebagai pakar untuk menganalisis risiko permasalahan kejiwaan Anda berdasar pola gejala yang dialami.")
    
    st.markdown("### 🔍 Metode & Logika")
    st.write("Sistem menggunakan kaidah runut maju (**Forward Chaining**) yang dilanjutkan dengan algoritma pencarian mendalam **Depth-First Search (DFS)**. Kombinasi bobot gejala kemudian dikalkulasi secara pasti dengan metode **Certainty Factor (CF)**.")
    
    st.markdown("### 🗂️ Cakupan Penyakit")
    st.caption("Penyakit utama yang diproses sistem ini meliputi:")
    for p_kode, p_data in dfs.knowledge_base.items():
        st.write(f"- **{p_data['nama_penyakit']}**")

st.info("💡 **Petunjuk Pengisian:** Jawablah rangkaian pertanyaan di bawah ini dengan sejujurnya sesuai dengan frekuensi perasaan / kondisi yang paling Anda alami beberapa waktu terakhir.")

cf_options = {
    "Tidak Mengalami (0.0)": 0.0,
    "Sedikit Yakin (0.4)": 0.4,
    "Cukup Yakin (0.6)": 0.6,
    "Yakin (0.8)": 0.8,
    "Sangat Yakin (1.0)": 1.0
}

st.write("---")
st.markdown("### 📋 Kuesioner Analisis Gejala")
st.write("Mohon pilih skala yang tersedia di bawah setiap pertanyaan.")

dfs.gejala_dialami.clear()

list_gejala = list(dfs.semua_gejala_nama.items())
user_inputs = {}

for i, (g_kode, g_nama) in enumerate(list_gejala):
    st.markdown(f"**Pertanyaan {i+1} dari {len(list_gejala)}**")
    pilihan = st.selectbox(
        label=f"{g_nama}?", 
        options=list(cf_options.keys()),
        index=0,
        key=g_kode
    )
    user_inputs[g_kode] = cf_options[pilihan]
    st.write("")

st.write("---")

st.markdown("<br>", unsafe_allow_html=True)
submit_button = st.button("🔍 LAKUKAN DIAGNOSA SEKARANG", use_container_width=True, type="primary")

if submit_button:
    with st.spinner('Menganalisis pola gejala Anda menggunakan algoritma Depth-First Search...'):
        
        dfs.gejala_dialami.update(user_inputs)
        
        hasil_diagnosa = []
        
        for p_kode, p_data in dfs.knowledge_base.items():
            list_g_kode = list(p_data["gejala"].keys())
            
            # DFS Traversal 
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
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("### 📊 Laporan Hasil Deteksi")
        
        if not hasil_diagnosa or hasil_diagnosa[0]['keyakinan'] == 0:
            st.success("✨ **Kabar Baik!** Anda tidak memiliki indikasi gejala yang mengarah pada penyakit jiwa dalam sistem pakar kami. Tetap pertahankan produktivitas, apresiasi diri sendiri, dan jaga terus kesehatan mental Anda!")
        else:
            hasil_diagnosa = [h for h in hasil_diagnosa if h['keyakinan'] > 0]
            
            for idx, hasil in enumerate(hasil_diagnosa):
                if idx == 0:
                    st.markdown(f"#### 🥇 Diagnosa Dominan: {hasil['nama_penyakit']} ({hasil['kode_penyakit']})")
                else:
                    st.markdown(f"#### {idx+1}. Kemungkinan Lain: {hasil['nama_penyakit']} ({hasil['kode_penyakit']})")
                
                if hasil['keyakinan'] >= 75:
                    st.error(f"**Tingkat Keyakinan Sistem: {hasil['keyakinan']}% (Tinggi)**")
                elif hasil['keyakinan'] >= 45:
                    st.warning(f"**Tingkat Keyakinan Sistem: {hasil['keyakinan']}% (Sedang)**")
                else:
                    st.success(f"**Tingkat Keyakinan Sistem: {hasil['keyakinan']}% (Rendah)**")
                
                st.progress(min(hasil['keyakinan'] / 100, 1.0))
                
                st.write(f"🎯 **Akurasi Gejala:** Sistem mendeteksi kecocokan pada **{hasil['gejala_match']}** gejala yang Anda alami, dari keseluruhan **{hasil['total_gejala_penyakit']}** gejala identik penderita *{hasil['nama_penyakit']}*.")
                
                # Recommendation box
                st.info(f"💡 **Rekomendasi Pakar / Solusi Penanganan:**\n\n{hasil['rekomendasi']}")
                
                st.divider() 
            
            st.caption("⚠️ **Catatan Penting:** Diagnosis ini sepenuhnya ditentukan dari pembobotan matematis kecerdasan buatan (*Certainty Factor*) dan bukan vonis sah medis. Apabila Anda merasa sangat terhalang dalam beraktivitas, pertimbangkan untuk berbicara pada Psikolog atau Psikiater Profesional.")
