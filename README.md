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
├── 05_MarketBasket_Optimisation/
│   ├── Market_Basket_Optimisation.csv      # Dataset benchmark Kaggle transaksi supermarket (7.501 baris)
│   ├── market_basket_optimisation.csv      # Dataset terstruktur dengan kolom transaction_id dan item1-20
│   └── market_basket_optimisation_preprocessing.ipynb # Notebook preprocessing (Dimensi, Missing Value, Duplikat, Outlier)
├── 06_Healthcare_Stroke/
│   ├── healthcare_dataset_stroke_data.csv  # Dataset rekam medis pasien stroke (5.110 baris, 12 atribut)
│   └── healthcare_stroke_preprocessing.ipynb # Notebook preprocessing (Dimensi, Missing Value, Duplikat, Outlier)
├── 07_Retail_Dirty_Transactions/
│   ├── retail_transactions_5500_dirty.csv  # Dataset transaksi ritel kotor / dirty (5.500 baris, 3 atribut)
│   └── retail_dirty_preprocessing.ipynb    # Notebook preprocessing (Dimensi, Missing Value, Duplikat, Outlier)
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

### 5. Market Basket Optimisation Dataset (`05_MarketBasket_Optimisation`)

- **Jumlah Baris & Kolom:** 7.501 baris transaksi dan 21 atribut (`transaction_id`, `item1` s.d `item20`).
- **Identifier:** Kolom `transaction_id` mencakup 7.501 nomor struk unik dengan 119 ragam produk ritel supermarket.
- **Missing Value:** 120.657 nilai kosong (76,60% terhadap seluruh sel atau 80,43% terhadap kolom produk) yang mencerminkan sifat alami data keranjang belanja horizontal.
- **Duplikat:** 2.325 baris transaksi dengan kombinasi item identik.
- **Outlier:** Rata-rata ukuran keranjang belanja adalah 3,91 item ($Min = 1, Max = 20$). Kuartil $Q1 = 2$, $Q3 = 5$, $IQR = 3$, dan batas atas outlier adalah 9,5 item. Ditemukan 395 transaksi outlier dengan volume belanja grosir tinggi (10 hingga 20 item).

### 6. Healthcare Stroke Dataset (`06_Healthcare_Stroke`)

- **Jumlah Baris & Kolom:** 5.110 baris data pasien dan 12 atribut klinis serta demografis.
- **Identifier:** Kolom `id` mencakup 5.110 nomor rekam medis pasien unik.
- **Missing Value:** Ditemukan 201 nilai kosong (3,93% pada kolom `bmi` atau 0,33% terhadap seluruh sel) yang divisualisasikan dengan Heatmap.
- **Duplikat:** 0 baris duplikat penuh.
- **Distribusi Target:** 249 pasien positif stroke (4,87%) dan 4.861 pasien negatif stroke (95,13%).
- **Outlier:** Berdasarkan analisis parameter klinis menggunakan metode IQR, atribut `avg_glucose_level` memiliki kuartil $Q1 = 77,25$, $Q3 = 114,09$, dan batas atas outlier $169,36$ mg/dL. Ditemukan 627 pasien outlier dengan kadar gula darah tinggi hingga 271,7 mg/dL.

### 7. Retail Dirty Transactions Dataset (`07_Retail_Dirty_Transactions`)

- **Jumlah Baris & Kolom:** 5.500 baris transaksi dan 3 atribut (`InvoiceNo`, `Description`, `Quantity`).
- **Identifier:** Kolom `InvoiceNo` mencakup 1.201 nomor faktur unik dengan 20 ragam produk kebutuhan harian.
- **Missing Value:** Ditemukan 279 nilai kosong (5,07% pada kolom `Description` atau 1,69% terhadap total sel) yang divisualisasikan dengan Heatmap.
- **Duplikat:** 114 baris duplikat penuh.
- **Karakteristik Data Kotor (Dirty):**
  - Terdapat 558 baris transaksi batal (*cancellation*) yang diawali kode `'C'` pada `InvoiceNo`.
  - Terdapat 286 baris transaksi dengan kuantitas negatif (-1 s.d -3) yang merepresentasikan retur barang.
- **Outlier:** Berdasarkan ukuran keranjang belanja per faktur `InvoiceNo`, kuartil $Q1 = 1,0$, $Q3 = 7,0$, $IQR = 6,0$, dan batas atas outlier adalah 16,0 item. Seluruh transaksi berada dalam rentang wajar (maksimal 16 item per faktur belanja).

---

## Cara Menjalankan

1. Masuk ke direktori notebook yang ingin diuji (`01_BreadBasket`, `02_MarketBasket`, `03_Retail_Bian`, `04_MarketBasket_Analysis`, `05_MarketBasket_Optimisation`, `06_Healthcare_Stroke`, atau `07_Retail_Dirty_Transactions`).
2. Jalankan notebook menggunakan Jupyter Notebook, JupyterLab, atau VS Code.
3. Pastikan file CSV terkait berada pada direktori yang sama dengan notebook.
4. Eksekusi sel dari atas ke bawah untuk melihat hasil perhitungan dan visualisasi.
