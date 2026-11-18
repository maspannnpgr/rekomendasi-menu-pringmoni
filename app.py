# Streamlit App - Sistem Rekomendasi Menu Restoran Pringsewu (Pringmoni)
# Metode: HYBRID RECOMMENDER SYSTEM (Content-Based Filtering + Collaborative Filtering)

import streamlit as st
import pandas as pd
import numpy as np
import re
import math
from collections import Counter

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Pringmoni - Hybrid Recommender System",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (CSS)
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.02rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .rec-card {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border: 1px solid #86EFAC;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .badge-cbf {
        display: inline-block;
        padding: 3px 8px;
        font-size: 0.72rem;
        font-weight: 600;
        border-radius: 6px;
        background-color: #2563EB;
        color: white;
    }
    .badge-cf {
        display: inline-block;
        padding: 3px 8px;
        font-size: 0.72rem;
        font-weight: 600;
        border-radius: 6px;
        background-color: #D97706;
        color: white;
    }
    .badge-hybrid {
        display: inline-block;
        padding: 4px 10px;
        font-size: 0.75rem;
        font-weight: 700;
        border-radius: 6px;
        background-color: #16A34A;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 1. DATASET MENU PRINGSEWU & ATRIBUT KONTEN (ITEM PROFILE)
# -------------------------------------------------------------
@st.cache_data
def get_menu_dataset():
    data = [
        {
            "id": 1,
            "nama": "Ayam Bakar Madu Pringsewu",
            "kategori": "Makanan Utama",
            "harga": 38000,
            "rasa": "Manis Gurih Harum",
            "bahan_utama": "Ayam Rempah Madu",
            "cara_masak": "Bakar Panggang",
            "suhu_saji": "Hangat",
            "deskripsi": "Ayam bakar bumbu madu khas Pringsewu dengan cita rasa manis legit, rempah meresap, dan aroma bakaran menggugah selera."
        },
        {
            "id": 2,
            "nama": "Ayam Goreng Lengkuas",
            "kategori": "Makanan Utama",
            "harga": 36000,
            "rasa": "Gurih Asin Renyah",
            "bahan_utama": "Ayam Rempah Lengkuas",
            "cara_masak": "Goreng Kremes",
            "suhu_saji": "Hangat",
            "deskripsi": "Ayam goreng kampung empuk bertabur serundeng lengkuas gurih renyah dengan aroma rempah tradisional."
        },
        {
            "id": 3,
            "nama": "Gurame Bakar Cobek",
            "kategori": "Makanan Utama",
            "harga": 65000,
            "rasa": "Pedas Manis Segar",
            "bahan_utama": "Ikan Gurame Cabai Rawit Jeruk Limau",
            "cara_masak": "Bakar Cobek",
            "suhu_saji": "Hangat",
            "deskripsi": "Ikan gurame segar dibakar empuk disiram sambal cobek pedas segar dengan perasan jeruk limau harum."
        },
        {
            "id": 4,
            "nama": "Gurame Goreng Terbang",
            "kategori": "Makanan Utama",
            "harga": 63000,
            "rasa": "Gurih Renyah Crispy",
            "bahan_utama": "Ikan Gurame Tepung Bumbu",
            "cara_masak": "Goreng Crispy",
            "suhu_saji": "Hangat",
            "deskripsi": "Ikan gurame dibelah mekar digoreng garing renyah hingga ke tulang, disajikan dengan sambal kecap pedas."
        },
        {
            "id": 5,
            "nama": "Bebek Goreng Sambal Korek",
            "kategori": "Makanan Utama",
            "harga": 45000,
            "rasa": "Gurih Pedas Nampol",
            "bahan_utama": "Bebek Cabai Rawit Bawang",
            "cara_masak": "Goreng Ungkep",
            "suhu_saji": "Hangat",
            "deskripsi": "Daging bebek empuk gurih berbumbu ungkep rempah disajikan bersama lumuran sambal korek ulek mentah pedas nampol."
        },
        {
            "id": 6,
            "nama": "Bebek Bakar Kecap Pedas",
            "kategori": "Makanan Utama",
            "harga": 46000,
            "rasa": "Manis Pedas Gurih",
            "bahan_utama": "Bebek Kecap Manis Cabai",
            "cara_masak": "Bakar Panggang",
            "suhu_saji": "Hangat",
            "deskripsi": "Potongan bebek empuk dibakar aroma arang dengan olesan kecap manis dan cabai racikan pedas nikmat."
        },
        {
            "id": 7,
            "nama": "Nasi Timbel Komplit",
            "kategori": "Makanan Utama",
            "harga": 42000,
            "rasa": "Gurih Manis Segar",
            "bahan_utama": "Nasi Daun Pisang Ayam Tahu Tempe Sayur Asem",
            "cara_masak": "Kukus Paket",
            "suhu_saji": "Hangat",
            "deskripsi": "Nasi timbel dibungkus daun pisang wangi komplit dengan ayam goreng, tahu tempe, lalapan, sambal, dan sayur asem."
        },
        {
            "id": 8,
            "nama": "Sop Buntut Spesial",
            "kategori": "Sup & Sayur",
            "harga": 68000,
            "rasa": "Gurih Segar Kaya Rempah Kuah",
            "bahan_utama": "Daging Buntut Sapi Wortel Kentang Pala Kuah Kaldu",
            "cara_masak": "Rebus Sup Kaldu",
            "suhu_saji": "Panas Berkuah",
            "deskripsi": "Potongan buntut sapi lembut dimasak perlahan dalam kuah kaldu rempah bening kaya pala dan cengkeh harum."
        },
        {
            "id": 9,
            "nama": "Sop Iga Sapi Kuah Asam",
            "kategori": "Sup & Sayur",
            "harga": 62000,
            "rasa": "Asam Segar Gurih Pedas Kuah",
            "bahan_utama": "Daging Iga Sapi Tomat Hijau Belimbing Wuluh Kuah Kaldu",
            "cara_masak": "Rebus Sup Kaldu",
            "suhu_saji": "Panas Berkuah",
            "deskripsi": "Iga sapi berdaging tebal dalam kuah kaldu asam segar perpaduan tomat hijau dan belimbing wuluh."
        },
        {
            "id": 10,
            "nama": "Sayur Asem Jakarta",
            "kategori": "Sup & Sayur",
            "harga": 18000,
            "rasa": "Asam Manis Gurih Segar Kuah",
            "bahan_utama": "Jagung Manis Kacang Tanah Melinjo Labu Siam Asam Jawa Kuah",
            "cara_masak": "Rebus Sup Sayur",
            "suhu_saji": "Hangat Berkuah",
            "deskripsi": "Kuah sayur asem khas dengan paduan asam jawa segar, jagung manis pipil, melinjo, dan kacang tanah gurih."
        },
        {
            "id": 11,
            "nama": "Tumis Kangkung Terasi",
            "kategori": "Sup & Sayur",
            "harga": 19000,
            "rasa": "Gurih Asin Pedas Harum",
            "bahan_utama": "Kangkung Cabai Merah Terasi Udang Bawang",
            "cara_masak": "Tumis Cah",
            "suhu_saji": "Hangat",
            "deskripsi": "Kangkung segar dimasak tumis cepat dengan cabai dan terasi udang harum khas cita rasa nusantara."
        },
        {
            "id": 12,
            "nama": "Tahu & Tempe Mendoan",
            "kategori": "Camilan & Tambahan",
            "harga": 16000,
            "rasa": "Gurih Asin Lembut Renyah",
            "bahan_utama": "Tempe Kedelai Tahu Tepung Terigu Daun Bawang",
            "cara_masak": "Goreng Mendoan",
            "suhu_saji": "Hangat",
            "deskripsi": "Tempe mendoan hangat renyah disajikan dengan sambal kecap cabai rawit pedas."
        },
        {
            "id": 13,
            "nama": "Es Teh Manis Pringsewu",
            "kategori": "Minuman",
            "harga": 8000,
            "rasa": "Manis Segar Dingin",
            "bahan_utama": "Teh Melati Gula Alami Es Batu",
            "cara_masak": "Seduh Dingin",
            "suhu_saji": "Dingin",
            "deskripsi": "Racikan teh melati tradisional aroma wangi dipadukan dengan manis gula murni dan es batu dingin menyegarkan."
        },
        {
            "id": 14,
            "nama": "Es Jeruk Kelapa Muda",
            "kategori": "Minuman",
            "harga": 22000,
            "rasa": "Manis Asam Segar Alami Dingin",
            "bahan_utama": "Perasan Jeruk Segar Serutan Kelapa Muda Air Kelapa Es Batu",
            "cara_masak": "Campur Dingin",
            "suhu_saji": "Dingin",
            "deskripsi": "Perpaduan perasan jeruk peras asli manis asam dengan gurih lembutnya serutan kelapa muda dan air kelapa asli."
        },
        {
            "id": 15,
            "nama": "Jus Alpukat Kocok",
            "kategori": "Minuman",
            "harga": 25000,
            "rasa": "Manis Gurih Lembut Creamy Dingin",
            "bahan_utama": "Buah Alpukat Mentega Susu Cokelat Kental Manis Es Batu",
            "cara_masak": "Blender Kocok",
            "suhu_saji": "Dingin",
            "deskripsi": "Buah alpukat mentega segar dikocok lembut berpadu lelehan susu kental manis cokelat premium."
        },
        {
            "id": 16,
            "nama": "Wedang Jahe Rempah",
            "kategori": "Minuman",
            "harga": 16000,
            "rasa": "Pedas Hangat Manis Harum",
            "bahan_utama": "Jahe Merah Gula Aren Kayu Manis Cengkeh",
            "cara_masak": "Rebus Seduh",
            "suhu_saji": "Panas",
            "deskripsi": "Minuman seduhan jahe merah bakar berpadu gula aren dan rempah alami untuk menghangatkan tubuh."
        }
    ]
    df = pd.DataFrame(data)
    df["content_features"] = (
        df["kategori"] + " " +
        df["rasa"] + " " +
        df["bahan_utama"] + " " +
        df["cara_masak"] + " " +
        df["suhu_saji"] + " " +
        df["deskripsi"]
    )
    return df

# -------------------------------------------------------------
# 2. MODEL 1: CONTENT-BASED FILTERING (TF-IDF & COSINE SIM)
# -------------------------------------------------------------
def tokenize(text):
    tokens = re.findall(r'\b[a-z]{3,}\b', text.lower())
    stopwords = {"dan", "yang", "dengan", "khas", "untuk", "dari", "dalam", "disajikan", "adalah"}
    return [t for t in tokens if t not in stopwords]

@st.cache_data
def get_cbf_matrix(df):
    corpus = [tokenize(text) for text in df["content_features"]]
    vocab = sorted(list(set(word for doc in corpus for word in doc)))
    n_docs = len(corpus)
    
    idf = {}
    for word in vocab:
        doc_count = sum(1 for doc in corpus if word in doc)
        idf[word] = math.log((1 + n_docs) / (1 + doc_count)) + 1.0

    tfidf_matrix = np.zeros((n_docs, len(vocab)))
    for i, doc in enumerate(corpus):
        counts = Counter(doc)
        doc_len = len(doc) if len(doc) > 0 else 1
        for j, word in enumerate(vocab):
            tf = counts[word] / doc_len
            tfidf_matrix[i, j] = tf * idf[word]
            
        norm = np.linalg.norm(tfidf_matrix[i])
        if norm > 0:
            tfidf_matrix[i] = tfidf_matrix[i] / norm

    cbf_sim_matrix = np.dot(tfidf_matrix, tfidf_matrix.T)
    return cbf_sim_matrix

# -------------------------------------------------------------
# 3. MODEL 2: COLLABORATIVE FILTERING (ITEM-BASED CO-PURCHASE/RATING)
# -------------------------------------------------------------
@st.cache_data
def get_cf_user_item_matrix(menu_names, num_users=50, seed=42):
    """Menghasilkan User-Item Interaction Matrix realistis dari 50 profil pelanggan."""
    np.random.seed(seed)
    n_menus = len(menu_names)
    matrix = np.zeros((num_users, n_menus))
    
    # Kelompok selera pelanggan
    for u in range(num_users):
        user_type = u % 4
        if user_type == 0:  # Pecinta Ayam & Bebek Bakar
            favs = [0, 1, 5, 6, 12, 13]
        elif user_type == 1:  # Pecinta Seafood Gurame & Pedas
            favs = [2, 3, 10, 11, 13]
        elif user_type == 2:  # Pecinta Menu Sup & Hangat
            favs = [7, 8, 9, 11, 15]
        else:  # Santai & Minuman/Camilan
            favs = [6, 11, 12, 13, 14]
            
        for m in range(n_menus):
            if m in favs:
                if np.random.rand() < 0.85:
                    matrix[u, m] = np.random.choice([4.0, 5.0], p=[0.3, 0.7])
            else:
                if np.random.rand() < 0.15:
                    matrix[u, m] = np.random.choice([1.0, 2.0, 3.0])
                    
    return pd.DataFrame(matrix, columns=menu_names, index=[f"Pelanggan_{i+1:02d}" for i in range(num_users)])

@st.cache_data
def get_cf_item_similarity_matrix(user_item_df):
    """Menghitung Item-Item Collaborative Filtering Similarity berdasarkan interaksi rating pelanggan."""
    R = user_item_df.values
    # Centered Cosine / Adjusted Cosine
    norms = np.linalg.norm(R, axis=0)
    # Hindari pembagian dengan nol
    norms[norms == 0] = 1e-9
    norm_R = R / norms
    cf_sim = np.dot(norm_R.T, norm_R)
    return cf_sim

# -------------------------------------------------------------
# 4. HYBRID ENGINE: WEIGHTED FUSION (CBF + CF)
# -------------------------------------------------------------
def get_hybrid_recommendations(target_menu, df_menu, cbf_matrix, cf_matrix, alpha=0.5, top_n=4):
    """
    Menghitung Skor Rekomendasi Hybrid:
    Hybrid_Score = (alpha * CBF_Score) + ((1 - alpha) * CF_Score)
    """
    if target_menu not in df_menu["nama"].values:
        return pd.DataFrame()
        
    idx = df_menu[df_menu["nama"] == target_menu].index[0]
    
    cbf_scores = cbf_matrix[idx]
    cf_scores = cf_matrix[idx]
    
    hybrid_scores = (alpha * cbf_scores) + ((1 - alpha) * cf_scores)
    
    results = []
    for i, score in enumerate(hybrid_scores):
        if i != idx:  # Jangan rekomendasikan item yang sama
            results.append({
                "id": df_menu.iloc[i]["id"],
                "nama": df_menu.iloc[i]["nama"],
                "kategori": df_menu.iloc[i]["kategori"],
                "harga": df_menu.iloc[i]["harga"],
                "rasa": df_menu.iloc[i]["rasa"],
                "cara_masak": df_menu.iloc[i]["cara_masak"],
                "deskripsi": df_menu.iloc[i]["deskripsi"],
                "cbf_score": cbf_scores[i],
                "cf_score": cf_scores[i],
                "hybrid_score": score
            })
            
    res_df = pd.DataFrame(results).sort_values(by="hybrid_score", ascending=False).head(top_n)
    return res_df

# -------------------------------------------------------------
# 5. USER INTERFACE (STREAMLIT)
# -------------------------------------------------------------
df_menu = get_menu_dataset()
cbf_sim_matrix = get_cbf_matrix(df_menu)
user_item_df = get_cf_user_item_matrix(df_menu["nama"].tolist())
cf_sim_matrix = get_cf_item_similarity_matrix(user_item_df)

# Sidebar
st.sidebar.image("https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=400&q=80", use_container_width=True)
st.sidebar.markdown("### 🎛️ Pengaturan Bobot Hybrid")

alpha = st.sidebar.slider(
    "Bobot Content-Based (CBF):",
    min_value=0.0,
    max_value=1.0,
    value=0.6,
    step=0.05,
    help="1.0 = Murni CBF (Kemiripan Karakteristik Menu). 0.0 = Murni CF (Pola Rating Pelanggan Lain)."
)
cf_weight = 1.0 - alpha
st.sidebar.write(f"📊 **Komposisi Model:**")
st.sidebar.progress(alpha)
st.sidebar.caption(f"🔵 **CBF:** {alpha*100:.0f}%  |  🟠 **CF:** {cf_weight*100:.0f}%")

top_k = st.sidebar.slider("Jumlah Rekomendasi (Top-N):", min_value=2, max_value=6, value=4, step=1)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Kelompok PBL:** Resto POS & Self-Order (Pringmoni)  
**Topik:** Sistem Rekomendasi Berbasis Web  
**Metode:** Hybrid Recommender System (CBF + CF)  
""")

# Judul Utama
st.markdown('<div class="main-title">🍽️ Pringmoni - Hybrid Recommender System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Sistem Rekomendasi Menu Cerdas: Menggabungkan Kemiripan Karakteristik Menu (CBF) dan Pola Pembelian Pelanggan Lain (CF)</div>', unsafe_allow_html=True)

tabs = st.tabs(["🚀 Rekomendasi Hybrid", "🔬 Perbandingan Skor (CBF vs CF vs Hybrid)", "👥 Data Interaksi Pelanggan (CF Matrix)", "📖 Panduan Metode"])

# TAB 1: REKOMENDASI HYBRID
with tabs[0]:
    col1, col2 = st.columns([1, 1.3])
    
    with col1:
        st.subheader("1. Pilih Menu Acuan Pelanggan")
        target_menu = st.selectbox(
            "Pilih Menu yang Sedang Dilihat / Dipesan:",
            options=df_menu["nama"].tolist(),
            index=0
        )
        
        target_data = df_menu[df_menu["nama"] == target_menu].iloc[0]
        st.markdown(f"""
        <div style="background-color: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 10px; padding: 16px; margin-top: 10px;">
            <span class="badge-cbf">{target_data['kategori']}</span>
            <h3 style="margin: 8px 0 4px 0; color: #1E3A8A;">{target_data['nama']}</h3>
            <p style="color: #475569; font-size: 0.95rem;">{target_data['deskripsi']}</p>
            <div style="font-size: 0.88rem; line-height: 1.6;">
                <b>💰 Harga:</b> Rp {target_data['harga']:,}<br>
                <b>👅 Profil Rasa:</b> {target_data['rasa']}<br>
                <b>🥩 Bahan Utama:</b> {target_data['bahan_utama']}<br>
                <b>🔥 Cara Masak:</b> {target_data['cara_masak']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.subheader("2. 💡 Rekomendasi Menu Terbaik (Hybrid)")
        recs = get_hybrid_recommendations(target_menu, df_menu, cbf_sim_matrix, cf_sim_matrix, alpha=alpha, top_n=top_k)
        
        if not recs.empty:
            for idx, row in recs.iterrows():
                hybrid_pct = row['hybrid_score'] * 100
                cbf_pct = row['cbf_score'] * 100
                cf_pct = row['cf_score'] * 100
                
                st.markdown(f"""
                <div class="rec-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="badge-cbf">{row['kategori']}</span>
                        <span class="badge-hybrid">Skor Hybrid: {hybrid_pct:.1f}%</span>
                    </div>
                    <h4 style="margin: 8px 0 4px 0; color: #166534;">{row['nama']}</h4>
                    <p style="margin: 0 0 8px 0; color: #4B5563; font-size: 0.9rem;">{row['deskripsi']}</p>
                    <div style="margin-bottom: 6px;">
                        <span class="badge-cbf">Kemiripan Konten: {cbf_pct:.1f}%</span>
                        <span class="badge-cf">Preferensi Pelanggan: {cf_pct:.1f}%</span>
                    </div>
                    <div style="font-size: 0.85rem; color: #374151;">
                        <b>Harga:</b> Rp {row['harga']:,} | <b>Rasa:</b> {row['rasa']} | <b>Olah:</b> {row['cara_masak']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

# TAB 2: PERBANDINGAN SKOR (CBF vs CF vs HYBRID)
with tabs[1]:
    st.subheader(f"📊 Analisis Komposisi Rekomendasi terhadap Menu: {target_menu}")
    st.write("Tabel di bawah menunjukkan transparansi perhitungan skor antara kemiripan konten (CBF) dan pola perilaku pelanggan lain (CF):")
    
    comp_df = recs[["nama", "kategori", "cbf_score", "cf_score", "hybrid_score"]].copy()
    comp_df["cbf_score"] = (comp_df["cbf_score"] * 100).round(1).astype(str) + "%"
    comp_df["cf_score"] = (comp_df["cf_score"] * 100).round(1).astype(str) + "%"
    comp_df["hybrid_score"] = (comp_df["hybrid_score"] * 100).round(1).astype(str) + "%"
    
    st.dataframe(comp_df.rename(columns={
        "nama": "Menu Rekomendasi",
        "cbf_score": f"Skor CBF ({alpha*100:.0f}%)",
        "cf_score": f"Skor CF ({cf_weight*100:.0f}%)",
        "hybrid_score": "Skor Akhir Hybrid"
    }), use_container_width=True)
    
    # Grafik Batang Perbandingan
    chart_data = recs.set_index("nama")[["cbf_score", "cf_score", "hybrid_score"]]
    st.bar_chart(chart_data)

# TAB 3: DATA INTERAKSI PELANGGAN (CF MATRIX)
with tabs[2]:
    st.subheader("👥 Matriks Interaksi Pengguna (User-Item Rating Matrix)")
    st.write(f"Matriks ini memuat data preferensi historis dari {len(user_item_df)} profil pelanggan untuk menghitung kemiripan collaborative:")
    st.dataframe(user_item_df.head(15), use_container_width=True)
    
    st.subheader("📐 Matriks Item-to-Item Similarity (Collaborative Filtering)")
    cf_display = pd.DataFrame(cf_sim_matrix, index=df_menu["nama"], columns=df_menu["nama"]).round(2)
    st.dataframe(cf_display, use_container_width=True)

# TAB 4: PANDUAN METODE
with tabs[3]:
    st.subheader("💡 Mengapa Menggunakan Hybrid Recommender System?")
    st.markdown("""
    #### 1. Masalah pada Content-Based Filtering (CBF) Murni:
    - **Overspecialization**: Rekomendasi terlalu monoton karena hanya menyarankan item yang atributnya identik (misal: pesan ayam bakar hanya ditawari ayam bakar lagi).
    
    #### 2. Masalah pada Collaborative Filtering (CF) Murni:
    - **Cold-Start Problem**: Menu baru yang belum pernah dipesan/diberi rating oleh pelanggan tidak akan pernah direkomendasikan.
    
    #### 3. Solusi Hybrid (Weighted Model):
    - Formula Penggabungan:
    $$\\text{Skor Hybrid} = (\\alpha \\times \\text{Skor CBF}) + ((1 - \\alpha) \\times \\text{Skor CF})$$
    - **Jika menu baru**: Slider $\\alpha$ dapat dinaikkan ke $1.0$ (mengutamakan kemiripan bahan & rasa CBF).
    - **Jika data pesanan ramai**: Slider $\\alpha$ diseimbangkan menjadi $0.5$ - $0.6$ untuk menangkap rekomendasi menu favorit pelanggan lain secara dinamis.
    """)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #9CA3AF;'>Pringmoni Hybrid Recommender System © 2026 - PBL TRPL</p>", unsafe_allow_html=True)
