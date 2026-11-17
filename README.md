# Pringmoni - Sistem Rekomendasi Menu Restoran (Market Basket Analysis)

Aplikasi web sistem rekomendasi berbasis **Streamlit** untuk studi kasus pemesanan menu **Restoran Pringsewu** (PBL Proyek Pringmoni).

## 🚀 Fitur Utama
1. **Simulasi Self-Order Interaktif**: Pelanggan memilih menu makanan, sistem langsung menyarankan menu pendamping (*Recommended Add-ons*) seperti minuman, sambal, atau hidangan pelengkap yang relevan.
2. **Analisis Algoritma Asosiasi (Apriori / Association Rule Mining)**: Menampilkan metrik *Support*, *Confidence*, dan *Lift Ratio* untuk setiap pola keterikatan menu.
3. **Visualisasi Data Interaktif**: Grafik frekuensi pemesanan menu terlaris dan grafik asosiasi menu terkuat.
4. **Parameter Dinamis**: Slider interaktif untuk menyesuaikan ambang batas *minimum confidence* dan *minimum support*.

## 🛠️ Menjalankan Secara Lokal

```bash
# 1. Masuk ke folder proyek
cd sistem_rekomendasi_pringsewu

# 2. Install dependensi
pip install -r requirements.txt

# 3. Jalankan aplikasi Streamlit
streamlit run app.py
```

## 🌐 Deploy ke Publik (Streamlit Community Cloud)

1. Buat repository baru di GitHub (misal: `rekomendasi-menu-pringmoni`).
2. Upload file:
   - `app.py`
   - `requirements.txt`
   - `README.md`
3. Buka [share.streamlit.io](https://share.streamlit.io/) dan login dengan GitHub.
4. Klik **New app**, pilih repository dan branch Anda, arahkan main file path ke `app.py`, lalu klik **Deploy!**.
5. Link publik langsung aktif dan siap dicantumkan dalam laporan.
