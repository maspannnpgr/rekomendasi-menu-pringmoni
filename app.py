# Streamlit App - Sistem Rekomendasi Menu Restoran Pringsewu (Pringmoni)
# Metode: Content-Based Filtering (CBF) menggunakan TF-IDF & Cosine Similarity

import streamlit as st
import pandas as pd
import numpy as np
import re
import math
from collections import Counter

# Set konfigurasi halaman
st.set_page_config(
    page_title="Pringmoni - Content-Based Recommendation",
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
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .rec-card {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border: 1px solid #93C5FD;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .badge {
        display: inline-block;
        padding: 3px 8px;
        font-size: 0.75rem;
        font-weight: 600;
        border-radius: 6px;
        background-color: #2563EB;
        color: white;
    }
    .badge-sim {
        display: inline-block;
        padding: 3px 8px;
        font-size: 0.75rem;
        font-weight: 600;
        border-radius: 6px;
        background-color: #059669;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 1. DATASET KATALOG MENU PRINGSEWU BESERTA ATRIBUT KONTEN
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
            "deskripsi": "Nasi timbel dibungkus daun pisang wangi komplit dengan ayam goreng, tahu tempe, lalapan, sambal, dan semangkuk sayur asem."
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
            "deskripsi": "Tempe mendoan lebar digoreng setengah matang berbalut tepung daun bawang gurih disajikan dengan sambal kecap cabai rawit."
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
            "deskripsi": "Minuman seduhan jahe merah bakar berpadu gula aren dan rempah alami untuk menghangatkan dan menyegarkan tubuh."
        }
    ]
    df = pd.DataFrame(data)
    # Gabungkan semua fitur konten menjadi satu teks representasi (Soup Feature)
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
# 2. ALGORITMA CONTENT-BASED FILTERING (TF-IDF & COSINE SIMILARITY)
# -------------------------------------------------------------
def tokenize(text):
    """Membersihkan dan memecah teks menjadi token kata."""
    text = text.lower()
    tokens = re.findall(r'\b[a-z]{3,}\b', text)
    stopwords = {"dan", "yang", "dengan", "khas", "untuk", "dari", "dalam", "disajikan", "adalah"}
    return [t for t in tokens if t not in stopwords]

@st.cache_data
def calculate_cosine_similarity_matrix(df):
    """Menghitung matriks Cosine Similarity berbasis TF-IDF dari fitur konten menu."""
    corpus = [tokenize(text) for text in df["content_features"]]
    vocab = sorted(list(set(word for doc in corpus for word in doc)))
    n_docs = len(corpus)
    
    # 1. Hitung IDF (Inverse Document Frequency)
    idf = {}
    for word in vocab:
        doc_count = sum(1 for doc in corpus if word in doc)
        idf[word] = math.log((1 + n_docs) / (1 + doc_count)) + 1.0

    # 2. Hitung Matriks Vektor TF-IDF
    tfidf_matrix = np.zeros((n_docs, len(vocab)))
    for i, doc in enumerate(corpus):
        counts = Counter(doc)
        doc_len = len(doc) if len(doc) > 0 else 1
        for j, word in enumerate(vocab):
            tf = counts[word] / doc_len
            tfidf_matrix[i, j] = tf * idf[word]
            
        # Normalisasi L2-norm
        norm = np.linalg.norm(tfidf_matrix[i])
        if norm > 0:
            tfidf_matrix[i] = tfidf_matrix[i] / norm

    # 3. Hitung Cosine Similarity Matrix: S = A . A^T
    similarity_matrix = np.dot(tfidf_matrix, tfidf_matrix.T)
    return similarity_matrix, vocab

def get_cbf_recommendations(target_menu_name, df, sim_matrix, top_n=4):
    """Mengembalikan daftar Top-N menu yang paling mirip berdasarkan Cosine Similarity."""
    if target_menu_name not in df["nama"].values:
        return pd.DataFrame()
        
    idx = df[df["nama"] == target_menu_name].index[0]
    sim_scores = list(enumerate(sim_matrix[idx]))
    
    # Urutkan berdasarkan skor kemiripan tertinggi (abaikan menu itu sendiri)
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [item for item in sim_scores if item[0] != idx][:top_n]
    
    rec_indices = [item[0] for item in sim_scores]
    rec_scores = [item[1] for item in sim_scores]
    
    rec_df = df.iloc[rec_indices].copy()
    rec_df["similarity_score"] = rec_scores
    return rec_df

# -------------------------------------------------------------
# 3. INTERFACE APLIKASI WEB STREAMLIT
# -------------------------------------------------------------
df_menu = get_menu_dataset()
sim_matrix, vocab = calculate_cosine_similarity_matrix(df_menu)

# Sidebar
st.sidebar.image("https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=400&q=80", use_container_width=True)
st.sidebar.markdown("### ⚙️ Parameter Rekomendasi")
top_k = st.sidebar.slider("Jumlah Rekomendasi (Top-K):", min_value=2, max_value=6, value=4, step=1)
min_score_filter = st.sidebar.slider("Ambang Batas Minimum Similarity:", min_value=0.05, max_value=0.50, value=0.10, step=0.05)

st.sidebar.markdown("---")
st.sidebar.markdown("""
**Kelompok PBL:** Resto POS & Self-Order (Pringmoni)  
**Topik:** Sistem Rekomendasi Berbasis Web  
**Metode:** Content-Based Filtering (CBF)  
**Algoritma:** TF-IDF & Cosine Similarity  
""")

# Judul Utama
st.markdown('<div class="main-title">🍽️ Pringmoni - Content-Based Recommender System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Sistem Rekomendasi Menu Serupa Berdasarkan Analisis Kemiripan Konten (Kategori, Rasa, Bahan Baku, dan Cara Masak)</div>', unsafe_allow_html=True)

tabs = st.tabs(["🎯 Rekomendasi Menu Serupa", "📊 Matriks Kemiripan (Cosine Similarity)", "📋 Eksplorasi Fitur Konten Menu"])

# TAB 1: REKOMENDASI MENU SERUPA
with tabs[0]:
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.subheader("1. Pilih Menu Acuan (Target Item)")
        st.write("Pilih salah satu menu yang disukai pelanggan atau sedang dilihat pada katalog:")
        
        target_menu = st.selectbox(
            "Pilih Menu:",
            options=df_menu["nama"].tolist(),
            index=0
        )
        
        target_data = df_menu[df_menu["nama"] == target_menu].iloc[0]
        
        st.markdown(f"""
        <div style="background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 16px; margin-top: 10px;">
            <span class="badge">{target_data['kategori']}</span>
            <h3 style="margin: 8px 0 4px 0; color: #1E3A8A;">{target_data['nama']}</h3>
            <p style="color: #475569; font-size: 0.95rem;">{target_data['deskripsi']}</p>
            <div style="font-size: 0.88rem; line-height: 1.6;">
                <b>💰 Harga:</b> Rp {target_data['harga']:,}<br>
                <b>👅 Profil Rasa:</b> {target_data['rasa']}<br>
                <b>🥩 Bahan Utama:</b> {target_data['bahan_utama']}<br>
                <b>🔥 Cara Masak:</b> {target_data['cara_masak']}<br>
                <b>🌡️ Suhu Saji:</b> {target_data['suhu_saji']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.subheader(f"2. 💡 Menu Serupa yang Direkomendasikan")
        st.write(f"Menu yang memiliki kemiripan karakteristik tertinggi dengan **{target_menu}**:")
        
        recs = get_cbf_recommendations(target_menu, df_menu, sim_matrix, top_n=top_k)
        recs_filtered = recs[recs["similarity_score"] >= min_score_filter]
        
        if not recs_filtered.empty:
            for idx, row in recs_filtered.iterrows():
                sim_pct = row["similarity_score"] * 100
                st.markdown(f"""
                <div class="rec-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span class="badge">{row['kategori']}</span>
                        <span class="badge-sim">Tingkat Kemiripan: {sim_pct:.1f}%</span>
                    </div>
                    <h4 style="margin: 8px 0 4px 0; color: #1E40AF;">{row['nama']}</h4>
                    <p style="margin: 0 0 8px 0; color: #4B5563; font-size: 0.9rem;">{row['deskripsi']}</p>
                    <div style="font-size: 0.85rem; color: #1F2937;">
                        <b>Harga:</b> Rp {row['harga']:,} | 
                        <b>Rasa:</b> {row['rasa']} | 
                        <b>Pengolahan:</b> {row['cara_masak']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Tidak ada menu yang memenuhi ambang batas kemiripan saat ini. Coba turunkan slider ambang batas di sidebar.")

# TAB 2: MATRIKS KEMIRIPAN (COSINE SIMILARITY)
with tabs[1]:
    st.subheader("📐 Matriks Cosine Similarity Antar-Menu")
    st.markdown("""
    Matriks ini merepresentasikan derajat kemiripan konten antar semua pasangan menu:
    - **1.00**: Identik / sangat mirip
    - **0.00**: Sama sekali tidak memiliki kesamaan karakteristik
    """)
    
    sim_df = pd.DataFrame(sim_matrix, index=df_menu["nama"], columns=df_menu["nama"])
    st.dataframe(sim_df.round(2), use_container_width=True)
    
    st.subheader(f"📈 Grafik Tingkat Kemiripan terhadap: {target_menu}")
    target_idx = df_menu[df_menu["nama"] == target_menu].index[0]
    chart_series = pd.Series(sim_matrix[target_idx], index=df_menu["nama"]).drop(target_menu).sort_values(ascending=False).head(8)
    st.bar_chart(chart_series)

# TAB 3: DATASET DAN FITUR KONTEN
with tabs[2]:
    st.subheader("📋 Dataset Fitur Menu (Item Profile)")
    st.write("Atribut yang diekstraksi menjadi representasi teks vektor TF-IDF:")
    
    display_df = df_menu[["nama", "kategori", "harga", "rasa", "bahan_utama", "cara_masak", "suhu_saji"]].copy()
    st.dataframe(display_df, use_container_width=True)
    
    st.markdown("#### 🔍 Contoh Ekstraksi Kata Kunci Fitur (Tokens Vocabulary)")
    st.write(f"Total vocabulary unik terdeteksi: **{len(vocab)} kata unik**")
    st.write(", ".join([f"`{w}`" for w in vocab[:30]]) + ", ...")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #9CA3AF;'>Pringmoni Content-Based Recommender System © 2026 - TRPL PBL</p>", unsafe_allow_html=True)
