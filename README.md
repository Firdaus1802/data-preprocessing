# Data Preprocessing - Konsep Data Mining

Repositori ini memuat tahap pra-pemrosesan data (*Data Understanding & Preprocessing*) untuk mata kuliah Konsep Data Mining, S1 Sistem Informasi Universitas Gunadarma (Kelas 3KA31 - Kelompok 4).

Repositori ini difokuskan pada tiga modul dataset utama pilihan kelompok, serta modul-modul eksperimen cadangan yang disimpan di dalam direktori arsip.

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
├── 01_Retail_Bian/
│   ├── Dataset_Transaksi_Retail.csv           # Dataset transaksi ritel Bian (5.050 baris, 1.500 transaksi)
│   └── retail_preprocessing.ipynb             # Notebook preprocessing (Dimensi, Missing Value, Duplikat, Outlier)
├── 02_Healthcare_Stroke/
│   ├── healthcare_dataset_stroke_data.csv     # Dataset rekam medis pasien stroke (5.110 baris, 12 atribut)
│   └── healthcare_stroke_preprocessing.ipynb  # Notebook preprocessing (Dimensi, Missing Value, Duplikat, Outlier)
├── 03_Retail_Dirty_Transactions/
│   ├── retail_transactions_5500_dirty.csv     # Dataset transaksi ritel kotor / dirty (5.500 baris, 3 atribut)
│   └── retail_dirty_preprocessing.ipynb       # Notebook preprocessing (Dimensi, Missing Value, Duplikat, Outlier)
├── _backup_arsip/                             # Arsip eksperimen & modul cadangan
│   ├── arsip_01_BreadBasket/                  # Cadangan dataset BreadBasket (21.293 baris)
│   ├── arsip_02_MarketBasket/                 # Cadangan dataset matriks biner produk (1.500 baris)
│   ├── arsip_04_MarketBasket_Analysis/        # Cadangan dataset keranjang horizontal XLSX (1.863 baris)
│   ├── arsip_05_MarketBasket_Optimisation/    # Cadangan dataset benchmark Kaggle (7.501 baris)
│   └── README.md                              # Dokumentasi isi folder arsip
├── .gitignore
├── .markdownlint.json
└── README.md
```

---

## Cakupan Analisis Preprocessing

Setiap notebook mencakup empat tahapan utama pra-pemrosesan data (disusun dalam 21 langkah modular terstandarisasi):

1. **Pemeriksaan Dimensi & Struktur Data:** Menghitung jumlah record, jumlah kolom atribut, tipe data, serta sampel data (`head` dan `tail`).
2. **Analisis Missing Value:** Mendeteksi nilai kosong per kolom, total agregat, persentase nilai kosong, serta visualisasi sebaran menggunakan Heatmap.
3. **Analisis Data Duplikat & Transaksi Unik:** Mengevaluasi baris duplikat penuh serta menghitung integritas identifier transaksi (`Transaction_ID`, `id`, `InvoiceNo`).
4. **Deteksi Outlier:** Mengidentifikasi data pencilan atau anomali menggunakan metode statistik Interquartile Range (IQR) dan visualisasi Boxplot.

---

## Ringkasan Temuan Data

### 1. Retail Dataset Bian (`01_Retail_Bian`)

- **Jumlah Baris & Kolom:** 5.050 baris item transaksi dan 5 atribut (`Transaction_ID`, `Transaction_Date`, `Product`, `Category`, `Quantity`).
- **Identifier:** Kolom `Transaction_ID` mencakup 1.500 nomor transaksi unik dengan 22 ragam produk ritel.
- **Missing Value:** Ditemukan 50 nilai kosong (25 pada kolom `Category` dan 25 pada kolom `Quantity`) yang divisualisasikan dengan Heatmap.
- **Duplikat:** 40 baris duplikat penuh transaksi.
- **Outlier:** Berdasarkan ukuran keranjang belanja per transaksi, kuartil $Q1 = 3$, $Q3 = 4$, dengan batas atas outlier 5,5 item. Ditemukan 3 transaksi outlier dengan volume belanja 6 item (`TRX0147`, `TRX0533`, `TRX0561`).

### 2. Healthcare Stroke Dataset (`02_Healthcare_Stroke`)

- **Jumlah Baris & Kolom:** 5.110 baris data pasien dan 12 atribut klinis serta demografis.
- **Identifier:** Kolom `id` mencakup 5.110 nomor rekam medis pasien unik.
- **Missing Value:** Ditemukan 201 nilai kosong (3,93% pada kolom `bmi` atau 0,33% terhadap seluruh sel) yang divisualisasikan dengan Heatmap.
- **Duplikat:** 0 baris duplikat penuh.
- **Distribusi Target:** 249 pasien positif stroke (4,87%) dan 4.861 pasien negatif stroke (95,13%).
- **Outlier:** Berdasarkan analisis parameter klinis menggunakan metode IQR, atribut `avg_glucose_level` memiliki kuartil $Q1 = 77,25$, $Q3 = 114,09$, dan batas atas outlier $169,36$ mg/dL. Ditemukan 627 pasien outlier dengan kadar gula darah tinggi hingga 271,7 mg/dL.

### 3. Retail Dirty Transactions Dataset (`03_Retail_Dirty_Transactions`)

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

1. Masuk ke direktori notebook yang ingin diuji (`01_Retail_Bian`, `02_Healthcare_Stroke`, atau `03_Retail_Dirty_Transactions`).
2. Jalankan notebook menggunakan Jupyter Notebook, JupyterLab, atau VS Code.
3. Pastikan file CSV terkait berada pada direktori yang sama dengan notebook.
4. Eksekusi sel dari atas ke bawah untuk melihat hasil perhitungan dan visualisasi.
