# Pringmoni - Content-Based Menu Recommender System

Aplikasi web sistem rekomendasi berbasis **Streamlit** untuk studi kasus menu **Restoran Pringsewu** (PBL Pringmoni).

## 🚀 Metode Rekomendasi
Sistem ini menggunakan metode **Content-Based Filtering (CBF)** dengan algoritma:
- **TF-IDF (Term Frequency - Inverse Document Frequency)** untuk ekstraksi fitur teks konten menu (kategori, rasa, bahan baku, cara memasak, suhu saji, dan deskripsi).
- **Cosine Similarity** untuk mengukur derajat kemiripan antar-menu secara matematis ($0.0$ s/d $1.0$).

## ✨ Fitur Utama
1. **Rekomendasi Menu Serupa (Top-K)**: Pelanggan memilih menu acuan, sistem langsung merekomendasikan hidangan alternatif yang memiliki profil rasa dan bahan baku serupa beserta persentase kemiripannya.
2. **Matriks Cosine Similarity & Heatmap**: Visualisasi tabel derajat kemiripan antar semua menu dan diagram batang Top-8 menu paling mirip.
3. **Eksplorasi Profil Menu**: Melihat rincian fitur konten (*Item Profile*) dan perbendaharaan kata (*vocabulary*).
4. **Kontrol Interaktif**: Slider untuk mengatur jumlah rekomendasi (*Top-K*) dan ambang batas minimum kemiripan (*similarity threshold*).

## 🛠️ Menjalankan Secara Lokal
```bash
# 1. Pindah ke direktori
cd sistem_rekomendasi_pringsewu

# 2. Install dependensi
pip install -r requirements.txt

# 3. Jalankan aplikasi Streamlit
streamlit run app.py
```

## 🌐 Deploy ke Publik (Streamlit Community Cloud)
1. Buka repositori GitHub Anda: `maspannnpgr/rekomendasi-menu-pringmoni`
2. Perbarui file `app.py`, `README.md`, dan `requirements.txt`
3. Aplikasi di [share.streamlit.io](https://share.streamlit.io/) akan otomatis ter-update dan siap diakses publik!
