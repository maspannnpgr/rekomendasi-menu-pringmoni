# Pringmoni - Hybrid Menu Recommender System (CBF + CF)

Aplikasi web sistem rekomendasi cerdas berbasis **Streamlit** untuk studi kasus menu **Restoran Pringsewu** (PBL Proyek Pringmoni).

## 🚀 Metode Rekomendasi
Sistem ini menggunakan arsitektur **Hybrid Recommender System** dengan menggabungkan:
1. **Content-Based Filtering (CBF)**: Mengekstrak profil konten menu (kategori, rasa, bahan baku, metode memasak) menggunakan **TF-IDF** dan **Cosine Similarity**.
2. **Collaborative Filtering (CF)**: Menganalisis pola kebiasaan dan rating pelanggan menggunakan **Item-Based Collaborative Filtering**.
3. **Weighted Hybrid Fusion**:
   $$\text{Skor Hybrid} = (\alpha \times \text{Skor CBF}) + ((1 - \alpha) \times \text{Skor CF})$$
   *(Slider $\alpha$ dapat diatur secara real-time di antarmuka web).*

## ✨ Fitur Aplikasi Web
- **Simulasi Rekomendasi Hybrid**: Menampilkan menu rekomendasi terbaik lengkap dengan persentase skor akhir, kontribusi skor CBF, dan kontribusi skor CF.
- **Transparansi Perhitungan**: Tabel dan grafik batang perbandingan kontribusi masing-masing algoritma.
- **Visualisasi Matriks Interaksi Pengguna**: Eksplorasi matriks rating pelanggan dan matriks kesamaan item-to-item CF.
- **Edukasi & Metodologi**: Panduan konsep mengapa sistem hybrid jauh lebih unggul dibanding model tunggal.

## 🛠️ Menjalankan Secara Lokal
```bash
# 1. Masuk ke direktori
cd sistem_rekomendasi_pringsewu

# 2. Install dependensi
pip install -r requirements.txt

# 3. Jalankan Streamlit
streamlit run app.py
```

## 🌐 Deploy Publik ke Streamlit Cloud
1. Upload file `app.py`, `requirements.txt`, dan `README.md` ke repositori GitHub: `maspannnpgr/rekomendasi-menu-pringmoni`
2. Kunjungi [share.streamlit.io](https://share.streamlit.io/) dan aplikasi akan otomatis ter-update secara online.
