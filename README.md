# Data Preprocessing - Konsep Data Mining

Repositori ini memuat tahap pra-pemrosesan data (*Data Understanding & Preprocessing*) untuk dataset transaksi belanja dalam mata kuliah Konsep Data Mining, S1 Sistem Informasi Universitas Gunadarma (Kelas 3KA31 - Kelompok 4).

Dataset yang telah dibersihkan disiapkan sebagai data masukan untuk pengujian analisis asosiasi pada proyek [data-mining-universitas-gunadarma](https://github.com/Firdaus1802/data-mining-universitas-gunadarma).

---

## Informasi Akademik

- Institusi: Universitas Gunadarma
- Program Studi: S1 Sistem Informasi
- Kelas / Kelompok: 3KA31 / Kelompok 4
- Mata Kuliah: Konsep Data Mining
- Dosen Pengampu: Dr. Dina Anggraini, S.Kom., M.M.S.I.

---

## Struktur Direktori

```text
Data mining IPYNB/
├── 01_BreadBasket/
│   ├── BreadBasket_DMS.csv                 # Dataset transaksi kafe & toko roti (21.293 baris)
│   └── bread_basket_preprocessing.ipynb    # Notebook preprocessing (Dimensi, Missing Value, Duplikat, Outlier)
├── 02_MarketBasket/
│   ├── market_basket_dataset.csv           # Dataset transaksi ritel (1.500 baris)
│   └── market_basket_preprocessing.ipynb   # Notebook preprocessing (Dimensi, Missing Value, Biner 0/1, Duplikat)
├── 03_Retail_Bian/
│   ├── Dataset_Transaksi_Retail.csv        # Dataset transaksi ritel sintetis Bian (5.050 baris, 1.500 transaksi)
│   └── retail_preprocessing.ipynb          # Notebook preprocessing (Dimensi, Missing Value, Duplikat, Outlier)
├── 04_MarketBasket_Analysis/
│   ├── market_basket_analysist.csv         # Dataset transaksi belanja riil horizontal (1.863 baris)
│   ├── market_basket_analysist.xlsx        # File Excel sumber data
│   └── market_basket_analysis_preprocessing.ipynb # Notebook preprocessing (Dimensi, Missing Value, Duplikat, Outlier)
├── _backup_arsip/                       # Arsip file eksperimen
└── README.md
```

---

## Cakupan Analisis Preprocessing

Setiap notebook mencakup empat tahapan utama pra-pemrosesan data:

1. **Pemeriksaan Dimensi & Struktur Data:** Menghitung jumlah record transaksi, jumlah kolom atribut, serta tipe data.
2. **Analisis Missing Value:** Mendeteksi nilai kosong, melakukan konversi representasi missing value khusus, serta visualisasi sebaran dengan Heatmap.
3. **Analisis Data Duplikat:** Mengevaluasi baris duplikat penuh serta memeriksa integritas identifier transaksi (`Transaction` / `transaction_id`).
4. **Deteksi Outlier:** Mengidentifikasi data transaksi anomali atau berukuran ekstrem menggunakan metode Interquartile Range (IQR) dan Boxplot.

---

## Ringkasan Temuan Data

### 1. BreadBasket Dataset (`01_BreadBasket`)

- **Jumlah Baris & Kolom:** 21.293 baris transaksi dan 4 atribut (`Date`, `Time`, `Transaction`, `Item`).
- **Identifier:** Kolom `Transaction` mencakup 9.531 nomor struk unik.
- **Missing Value:** 786 data kosong pada kolom `Item` (3,69%) yang dicatat sebagai string `'NONE'` dan dikonversi menjadi `NaN`.
- **Duplikat:** 1.653 baris duplikat penuh yang merepresentasikan pembelian item ganda dalam struk yang sama.
- **Outlier:** Berdasarkan banyaknya item per transaksi, kuartil $Q1 = 1$, $Q3 = 3$, dan batas atas outlier adalah 6 item. Ditemukan 72 transaksi outlier dengan volume belanja tinggi (hingga 11 item).

### 2. Market Basket Dataset (`02_MarketBasket`)

- **Jumlah Baris & Kolom:** 1.500 baris transaksi dan 10 atribut produk.
- **Missing Value:** 8.670 nilai kosong (~57% per produk) yang mencerminkan sifat alami data keranjang belanja (pelanggan hanya membeli beberapa produk per transaksi).
- **Penanganan Missing Value:** Ditransformasikan ke dalam representasi biner (0 dan 1) menggunakan One-Hot Encoding (`df.notna().astype(int)`).
- **Duplikat:** 774 baris transaksi dengan kombinasi belanja identik.
- **Outlier:** Berdasarkan banyaknya produk per transaksi, kuartil $Q1 = 3$, $Q3 = 5$, dan batas atas outlier adalah 8,0 produk. Ditemukan 1 transaksi outlier dengan volume belanja 9 produk (indeks transaksi #615).

### 3. Retail Dataset Bian (`03_Retail_Bian`)

- **Jumlah Baris & Kolom:** 5.050 baris item transaksi dan 5 atribut (`Transaction_ID`, `Transaction_Date`, `Product`, `Category`, `Quantity`).
- **Identifier:** Kolom `Transaction_ID` mencakup 1.500 nomor transaksi unik dengan 22 ragam produk ritel.
- **Missing Value:** Ditemukan 50 nilai kosong (25 pada kolom `Category` dan 25 pada kolom `Quantity`) yang divisualisasikan dengan Heatmap.
- **Duplikat:** 40 baris duplikat penuh transaksi.
- **Outlier:** Berdasarkan ukuran keranjang belanja per transaksi, kuartil $Q1 = 3$, $Q3 = 4$, dengan batas atas outlier 5,5 item. Ditemukan 3 transaksi outlier dengan volume belanja 6 item (`TRX0147`, `TRX0533`, `TRX0561`).

### 4. Market Basket Analysis Dataset (`04_MarketBasket_Analysis`)

- **Jumlah Baris & Kolom:** 1.863 baris transaksi dan 8 atribut (`itemset`, `item1` s.d `item7`).
- **Identifier:** Kolom `itemset` mencakup 1.863 nomor transaksi unik dengan 12 ragam produk belanja.
- **Missing Value:** 6.296 nilai kosong (42,24%) yang mencerminkan variasi belanja alami pada kolom item horizontal.
- **Duplikat:** 3 baris transaksi dengan kombinasi item identik.
- **Outlier:** Rata-rata ukuran keranjang belanja adalah 3,62 item. Kuartil $Q1 = 2$, $Q3 = 5$, dan batas atas outlier adalah 9,5 item. Seluruh transaksi berada dalam rentang normal (maksimal 7 item per keranjang).

---

## Cara Menjalankan

1. Masuk ke direktori notebook yang ingin diuji (`01_BreadBasket`, `02_MarketBasket`, `03_Retail_Bian`, atau `04_MarketBasket_Analysis`).
2. Jalankan notebook menggunakan Jupyter Notebook, JupyterLab, atau VS Code.
3. Pastikan file CSV terkait berada pada direktori yang sama dengan notebook.
4. Eksekusi sel dari atas ke bawah untuk melihat hasil perhitungan dan visualisasi.
