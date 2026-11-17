# Streamlit App - Sistem Rekomendasi Menu Restoran Pringsewu (Pringmoni)
import streamlit as st
import pandas as pd
import numpy as np
import itertools
from collections import Counter

# Set konfigurasi halaman
st.set_page_config(
    page_title="Pringmoni - Sistem Rekomendasi Menu",
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
    .metric-card {
        background-color: #F3F4F6;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #2563EB;
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
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 1. DATABASE & DUMMY TRANSAKSI (STUDI KASUS RESTO PRINGSEWU)
# -------------------------------------------------------------
MENU_DATABASE = {
    "Ayam Bakar Madu Pringsewu": {"kategori": "Makanan Utama", "harga": 38000, "deskripsi": "Ayam bakar bumbu madu khas Pringsewu yang gurih manis."},
    "Gurame Bakar Cobek": {"kategori": "Makanan Utama", "harga": 65000, "deskripsi": "Ikan gurame segar dibakar dengan sambal cobek pedas segar."},
    "Nasi Timbel Komplit": {"kategori": "Makanan Utama", "harga": 42000, "deskripsi": "Nasi timbel dibungkus daun pisang dengan ayam goreng, tahu tempe, sayur asem."},
    "Bebek Goreng Sambal Korek": {"kategori": "Makanan Utama", "harga": 45000, "deskripsi": "Bebek ungkep bumbu rempah garing dengan sambal korek pedas nampol."},
    "Sop Buntut Spesial": {"kategori": "Sup & Sayur", "harga": 68000, "deskripsi": "Buntut sapi empuk dengan kuah rempah bening kaya rasa."},
    "Sayur Asem Jakarta": {"kategori": "Sup & Sayur", "harga": 18000, "deskripsi": "Kuah sayur asem segar berpadu jagung, kacang tanah, dan melinjo."},
    "Karedok Sayur Segar": {"kategori": "Sup & Sayur", "harga": 20000, "deskripsi": "Sayuran mentah segar disiram bumbu kacang gurih pedas khas Sunda."},
    "Tumis Kangkung Terasi": {"kategori": "Sup & Sayur", "harga": 19000, "deskripsi": "Kangkung segar ditumis cepat dengan cabai dan terasi harum."},
    "Tahu & Tempe Mendoan": {"kategori": "Camilan & Tambahan", "harga": 16000, "deskripsi": "Mendoan hangat renyah disajikan dengan sambal kecap rawit."},
    "Sambal Terasi Dadak": {"kategori": "Camilan & Tambahan", "harga": 8000, "deskripsi": "Sambal terasi segar diulek mendadak pedas mantap."},
    "Nasi Putih Pulen": {"kategori": "Makanan Utama", "harga": 7000, "deskripsi": "Nasi putih hangat berkualitas dari beras pulen pilihan."},
    "Es Teh Manis Pringsewu": {"kategori": "Minuman", "harga": 8000, "deskripsi": "Teh racikan melati segar dingin khas resto keluarga."},
    "Es Jeruk Kelapa Muda": {"kategori": "Minuman", "harga": 22000, "deskripsi": "Perpaduan perasan jeruk manis alami dan serutan kelapa muda murni."},
    "Jus Alpukat Kocok": {"kategori": "Minuman", "harga": 25000, "deskripsi": "Alpukat mentega lembut dengan lelehan susu kental manis cokelat."},
    "Wedang Jahe Rempah": {"kategori": "Minuman", "harga": 16000, "deskripsi": "Minuman hangat tradisional untuk menghangatkan badan."}
}

@st.cache_data
def generate_sample_transactions(n=350, seed=42):
    """Menghasilkan dataset transaksi realistis untuk Restoran Pringsewu."""
    np.random.seed(seed)
    transactions = []
    
    # Pola kebiasaan pelanggan
    patterns = [
        ["Ayam Bakar Madu Pringsewu", "Nasi Putih Pulen", "Sayur Asem Jakarta", "Es Teh Manis Pringsewu", "Sambal Terasi Dadak"],
        ["Gurame Bakar Cobek", "Nasi Putih Pulen", "Tumis Kangkung Terasi", "Es Jeruk Kelapa Muda", "Tahu & Tempe Mendoan"],
        ["Nasi Timbel Komplit", "Sayur Asem Jakarta", "Tahu & Tempe Mendoan", "Es Teh Manis Pringsewu"],
        ["Bebek Goreng Sambal Korek", "Nasi Putih Pulen", "Sambal Terasi Dadak", "Es Jeruk Kelapa Muda"],
        ["Sop Buntut Spesial", "Nasi Putih Pulen", "Tahu & Tempe Mendoan", "Es Teh Manis Pringsewu"],
        ["Ayam Bakar Madu Pringsewu", "Nasi Timbel Komplit", "Es Jeruk Kelapa Muda", "Jus Alpukat Kocok"]
    ]
    
    all_items = list(MENU_DATABASE.keys())
    
    for i in range(1, n + 1):
        # 75% mengikuti pola umum pelanggan, 25% acak
        if np.random.rand() < 0.75:
            base_pattern = patterns[np.random.randint(0, len(patterns))].copy()
            # Variasi acak (menambah atau mengurangi 1 item)
            k = np.random.randint(max(2, len(base_pattern)-2), len(base_pattern)+1)
            selected = list(np.random.choice(base_pattern, size=min(k, len(base_pattern)), replace=False))
            # 30% peluang menambah menu acak
            if np.random.rand() < 0.3:
                extra = np.random.choice(all_items)
                if extra not in selected:
                    selected.append(extra)
        else:
            size = np.random.randint(2, 6)
            selected = list(np.random.choice(all_items, size=size, replace=False))
            
        transactions.append({
            "TransactionID": f"TRX-PRING-{1000 + i}",
            "Items": selected,
            "Total_Items": len(selected)
        })
    return pd.DataFrame(transactions)

# -------------------------------------------------------------
# 2. ALGORITMA REKOMENDASI (ASSOCIATION RULES / APRIORI SIMPLE)
# -------------------------------------------------------------
def calculate_rules(df_trans, min_support=0.03, min_confidence=0.15):
    """Menghitung Association Rules (Support, Confidence, Lift) dari transaksi."""
    total_trans = len(df_trans)
    
    # 1. Hitung frekuensi 1-item
    item_counts = Counter()
    for items in df_trans['Items']:
        for item in items:
            item_counts[item] += 1
            
    # 2. Hitung frekuensi pasangan (2-itemsets)
    pair_counts = Counter()
    for items in df_trans['Items']:
        unique_items = sorted(list(set(items)))
        for pair in itertools.combinations(unique_items, 2):
            pair_counts[pair] += 1
            
    # 3. Bentuk Rules: If Antecedent (A) -> Then Consequent (B)
    rules = []
    for (item1, item2), count in pair_counts.items():
        support = count / total_trans
        if support >= min_support:
            # Rule 1: item1 -> item2
            conf1 = count / item_counts[item1]
            lift1 = conf1 / (item_counts[item2] / total_trans)
            if conf1 >= min_confidence:
                rules.append({
                    'Antecedent': item1,
                    'Consequent': item2,
                    'Support': support,
                    'Confidence': conf1,
                    'Lift': lift1
                })
                
            # Rule 2: item2 -> item1
            conf2 = count / item_counts[item2]
            lift2 = conf2 / (item_counts[item1] / total_trans)
            if conf2 >= min_confidence:
                rules.append({
                    'Antecedent': item2,
                    'Consequent': item1,
                    'Support': support,
                    'Confidence': conf2,
                    'Lift': lift2
                })
                
    return pd.DataFrame(rules).sort_values(by=['Lift', 'Confidence'], ascending=False)

def get_recommendations(selected_items, rules_df, top_k=4):
    """Memberikan rekomendasi item pendamping berdasarkan item yang sudah dipilih pelanggan."""
    if not selected_items or rules_df.empty:
        return pd.DataFrame()
    
    matched = rules_df[rules_df['Antecedent'].isin(selected_items)]
    # Filter item yang belum dipilih
    recommendations = matched[~matched['Consequent'].isin(selected_items)].copy()
    
    if recommendations.empty:
        return pd.DataFrame()
        
    # Agregasi skor bila direkomendasikan oleh beberapa item
    agg = recommendations.groupby('Consequent').agg({
        'Confidence': 'max',
        'Lift': 'mean',
        'Support': 'mean',
        'Antecedent': lambda x: ", ".join(list(x.unique()))
    }).reset_index()
    
    agg = agg.rename(columns={'Antecedent': 'Direkomendasikan_Karena'})
    agg = agg.sort_values(by=['Lift', 'Confidence'], ascending=False).head(top_k)
    return agg

# -------------------------------------------------------------
# 3. INTERFACE APLIKASI WEB (STREAMLIT)
# -------------------------------------------------------------
df_trans = generate_sample_transactions()
rules_df = calculate_rules(df_trans)

# Sidebar
st.sidebar.image("https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=400&q=80", use_container_width=True)
st.sidebar.markdown("### ⚙️ Pengaturan Rekomendasi")
min_conf = st.sidebar.slider("Minimum Confidence", 0.1, 0.9, 0.2, step=0.05)
min_sup = st.sidebar.slider("Minimum Support", 0.01, 0.20, 0.04, step=0.01)

rules_df_custom = calculate_rules(df_trans, min_support=min_sup, min_confidence=min_conf)

st.sidebar.info(f"📊 Rules Terbentuk: **{len(rules_df_custom)} Aturan**")
st.sidebar.markdown("---")
st.sidebar.markdown("""
**Kelompok PBL:** Sistem POS Restoran (Pringmoni)  
**Topik:** Sistem Rekomendasi Berbasis Web  
**Metode:** Association Rule Mining (Market Basket Analysis)
""")

# Halaman Utama
st.markdown('<div class="main-title">🍽️ Pringmoni - Recommender System</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Sistem Rekomendasi Menu Pendamping Pintar Berbasis Riwayat Transaksi Restoran Pringsewu</div>', unsafe_allow_html=True)

tabs = st.tabs(["🛒 Simulasi Pemesanan (Self-Order)", "📈 Analisis Aturan Asosiasi (Rules)", "📁 Eksplorasi Riwayat Transaksi"])

# TAB 1: SIMULASI SELF-ORDER
with tabs[0]:
    col1, col2 = st.columns([1.1, 1])
    
    with col1:
        st.subheader("1. Pilih Menu Pesanan Pelanggan")
        st.write("Simulasikan pelanggan yang sedang memilih menu di meja restoran via aplikasi Self-Order:")
        
        all_menu_items = list(MENU_DATABASE.keys())
        selected_menu = st.multiselect(
            "Pilih satu atau beberapa menu:",
            options=all_menu_items,
            default=["Ayam Bakar Madu Pringsewu", "Nasi Putih Pulen"]
        )
        
        if selected_menu:
            st.markdown("##### 🧾 Rincian Pesanan Saat Ini:")
            total_bayar = 0
            for item in selected_menu:
                info = MENU_DATABASE.get(item, {"kategori": "-", "harga": 0})
                total_bayar += info['harga']
                st.write(f"- **{item}** `({info['kategori']})` — Rp {info['harga']:,}")
            st.success(f"**Subtotal Sementara:** Rp {total_bayar:,}")
        else:
            st.warning("Silakan pilih minimal 1 menu untuk melihat rekomendasi otomatis.")

    with col2:
        st.subheader("2. 💡 Rekomendasi Menu Pendamping")
        st.write("Sistem mendeteksi pola pembelian dan merekomendasikan menu yang sering dipesan bersamaan:")
        
        if selected_menu:
            recs = get_recommendations(selected_menu, rules_df_custom, top_k=4)
            if not recs.empty:
                for idx, row in recs.iterrows():
                    rec_item = row['Consequent']
                    info = MENU_DATABASE.get(rec_item, {"kategori": "-", "harga": 0, "deskripsi": ""})
                    
                    st.markdown(f"""
                    <div class="rec-card">
                        <span class="badge">{info['kategori']}</span>
                        <h4 style="margin: 8px 0 4px 0; color: #1E40AF;">{rec_item}</h4>
                        <p style="margin: 0 0 8px 0; color: #4B5563; font-size: 0.9rem;">{info['deskripsi']}</p>
                        <div style="font-size: 0.85rem; color: #1F2937;">
                            <b>Harga:</b> Rp {info['harga']:,} | 
                            <b>Confidence:</b> {row['Confidence']*100:.1f}% | 
                            <b>Lift Ratio:</b> {row['Lift']:.2f}x
                        </div>
                        <div style="font-size: 0.75rem; color: #6B7280; margin-top: 4px;">
                            <i>(Sering dipesan bersamaan dengan: <b>{row['Direkomendasikan_Karena']}</b>)</i>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Belum ada aturan rekomendasi yang memenuhi ambang batas saat ini. Coba pilih menu lain atau turunkan ambang batas (threshold) di sidebar.")
        else:
            st.info("Pilih menu di samping untuk mengaktifkan mesin rekomendasi.")

# TAB 2: ATURAN ASOSIASI (RULES ANALYSIS)
with tabs[1]:
    st.subheader("📊 Association Rules Table (Market Basket Analysis)")
    st.markdown("""
    Aturan dibentuk dengan rumus:
    - **Support**: Seberapa sering item A dan B dibeli bersamaan dibandingkan seluruh transaksi.
    - **Confidence**: Peluang pelanggan membeli item B jika mereka telah memilih item A.
    - **Lift Ratio**: Kekuatan keterikatan asosiasi (> 1.0 mengindikasikan korelasi positif yang signifikan).
    """)
    
    if not rules_df_custom.empty:
        display_rules = rules_df_custom.copy()
        display_rules['Support'] = display_rules['Support'].apply(lambda x: f"{x*100:.1f}%")
        display_rules['Confidence'] = display_rules['Confidence'].apply(lambda x: f"{x*100:.1f}%")
        display_rules['Lift'] = display_rules['Lift'].apply(lambda x: f"{x:.2f}")
        
        st.dataframe(display_rules.rename(columns={
            'Antecedent': 'Jika Membeli (A)',
            'Consequent': 'Maka Disarankan (B)',
            'Lift': 'Lift Ratio'
        }), use_container_width=True)
        
        # Visualisasi Top Rules
        st.subheader("📈 Top 10 Hubungan Menu Terkuat (Berdasarkan Nilai Lift)")
        top_10 = rules_df_custom.head(10).copy()
        top_10['Rule_Name'] = top_10['Antecedent'] + " ➔ " + top_10['Consequent']
        chart_data = top_10.set_index('Rule_Name')['Lift']
        st.bar_chart(chart_data)
    else:
        st.warning("Tidak ada aturan yang terbentuk pada parameter saat ini.")

# TAB 3: DATASET TRANSAKSI
with tabs[2]:
    st.subheader("📁 Data Riwayat Transaksi Pelanggan (Studi Kasus)")
    st.write(f"Total Transaksi Terdata: **{len(df_trans)} transaksi**")
    
    df_preview = df_trans.copy()
    df_preview['Items'] = df_preview['Items'].apply(lambda x: ", ".join(x))
    st.dataframe(df_preview, use_container_width=True)
    
    # Menu Terpopuler
    st.subheader("🏆 Frekuensi Penjualan Menu Terlaris")
    flat_items = [item for sublist in df_trans['Items'] for item in sublist]
    count_df = pd.DataFrame(Counter(flat_items).most_common(10), columns=['Menu', 'Jumlah Dipesan']).set_index('Menu')
    st.bar_chart(count_df)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #9CA3AF;'>Pringmoni Recommendation Engine © 2026 - Proyek PBL TRPL</p>", unsafe_allow_html=True)
