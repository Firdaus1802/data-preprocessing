# Data Preprocessing - Konsep Data Mining

Repositori ini memuat tahap pra-pemrosesan data (*Data Understanding & Preprocessing*) untuk mata kuliah Konsep Data Mining, S1 Sistem Informasi Universitas Gunadarma (Kelas 3KA31 - Kelompok 4).

Repositori ini difokuskan pada empat modul dataset utama pilihan kelompok, serta modul-modul eksperimen cadangan yang disimpan di dalam direktori arsip. Setiap notebook aktif dirancang bersih dan modular dengan deskripsi teknis di setiap langkah kode program.

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
├── 04_Superstore_Sales/
│   ├── trains.csv                             # Dataset transaksi penjualan Superstore (9.818 baris, 18 atribut)
│   ├── train.csv                              # Salinan dataset identik (kompatibilitas nama)
│   └── superstore_sales_preprocessing.ipynb   # Notebook preprocessing (Dimensi, Missing Value, Duplikat, Outlier)
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

Setiap notebook mencakup lima tahapan utama pra-pemrosesan data (disusun dalam 24 langkah modular terstandarisasi, dengan total 73 sel: 1 sel judul dan 24 paket operasi yang memuat deskripsi langkah, kode program, output komputasi, serta sel narasi `Penjelasan Hasil`):

1. **Pemeriksaan Dimensi & Struktur Data:** Menghitung jumlah record, jumlah kolom atribut, tipe data, serta sampel data (`head` dan `tail`).
2. **Analisis Missing Value:** Mendeteksi nilai kosong per kolom, total agregat, persentase nilai kosong, serta visualisasi sebaran menggunakan Heatmap awal sebelum penanganan.
3. **Penanggulangan Missing Value & Verifikasi Heatmap:** Menerapkan teknik imputasi data yang sesuai karakteristik atribut (Modus/Median/Label Khusus) dan memvalidasi kebersihan data secara visual dengan Heatmap pasca penanggulangan (0 missing value tersisa).
4. **Analisis & Penanggulangan Data Duplikat:** Mendeteksi baris duplikat penuh, menghapus data duplikat (`drop_duplicates()`) guna menjaga validitas data, serta menghitung integritas identifier transaksi (`Transaction_ID`, `id`, `InvoiceNo`, `Order ID`).
5. **Deteksi Outlier:** Mengidentifikasi data pencilan atau anomali menggunakan metode statistik Interquartile Range (IQR John Tukey) dan visualisasi Boxplot.

---

## Ringkasan Temuan Data

### 1. Retail Dataset Bian (`01_Retail_Bian`)

- **Jumlah Baris & Kolom:** 5.050 baris item transaksi dan 5 atribut (`Transaction_ID`, `Transaction_Date`, `Product`, `Category`, `Quantity`).
- **Identifier:** Kolom `Transaction_ID` mencakup 1.500 nomor transaksi unik dengan 22 ragam produk ritel.
- **Missing Value:** Ditemukan 50 nilai kosong (25 pada kolom `Category` dan 25 pada kolom `Quantity`) yang divisualisasikan dengan Heatmap.
- **Duplikat & Penanggulangan:** Ditemukan 40 baris duplikat penuh transaksi yang dihapus menggunakan `drop_duplicates()`, menghasilkan 5.010 baris data bersih.
- **Outlier:** Berdasarkan ukuran keranjang belanja per transaksi, kuartil $Q1 = 3,0$, $Q3 = 4,0$, $IQR = 1,0$, dengan batas atas outlier $5,5$ item. Setelah duplikat dibersihkan, volume belanja maksimal adalah 5 item sehingga tidak ada lagi transaksi yang melebihi batas atas (0 outlier).

### 2. Healthcare Stroke Dataset (`02_Healthcare_Stroke`)

- **Jumlah Baris & Kolom:** 5.110 baris data pasien dan 12 atribut klinis serta demografis.
- **Identifier:** Kolom `id` mencakup 5.110 nomor rekam medis pasien unik.
- **Missing Value:** Ditemukan 201 nilai kosong (3,93% pada kolom `bmi` atau 0,33% terhadap seluruh sel) yang divisualisasikan dengan Heatmap.
- **Duplikat & Penanggulangan:** 0 baris duplikat penuh, verifikasi `drop_duplicates()` memastikan dataset tetap utuh 5.110 baris.
- **Distribusi Target:** 249 pasien positif stroke (4,87%) dan 4.861 pasien negatif stroke (95,13%).
- **Outlier:** Berdasarkan analisis parameter klinis menggunakan metode IQR, atribut `avg_glucose_level` memiliki kuartil $Q1 = 77,25$, $Q3 = 114,09$, $IQR = 36,84$, dan batas atas outlier $169,36$ mg/dL. Ditemukan 627 pasien outlier dengan kadar gula darah tinggi hingga 271,74 mg/dL.

### 3. Retail Dirty Transactions Dataset (`03_Retail_Dirty_Transactions`)

- **Jumlah Baris & Kolom:** 5.500 baris transaksi dan 3 atribut (`InvoiceNo`, `Description`, `Quantity`).
- **Identifier:** Kolom `InvoiceNo` mencakup 1.201 nomor faktur unik dengan 20 ragam produk kebutuhan harian.
- **Missing Value:** Ditemukan 279 nilai kosong (5,07% pada kolom `Description` atau 1,69% terhadap total sel) yang divisualisasikan dengan Heatmap.
- **Duplikat & Penanggulangan:** Ditemukan 114 baris duplikat penuh yang dihapus menggunakan `drop_duplicates()`, menghasilkan 5.386 baris data transaksi bersih.
- **Karakteristik Data Kotor (Dirty):**
  - Terdapat 558 baris transaksi batal (*cancellation*) yang diawali kode `'C'` pada `InvoiceNo`.
  - Terdapat 286 baris transaksi dengan kuantitas negatif (-1 s.d -3) yang merepresentasikan retur barang.
- **Outlier:** Berdasarkan ukuran keranjang belanja per faktur `InvoiceNo`, kuartil $Q1 = 2,0$, $Q3 = 7,0$, $IQR = 5,0$, dan batas atas outlier adalah $14,5$ item. Ditemukan 1 transaksi outlier dengan volume belanja 16 item (`INV1467`).

### 4. Superstore Sales Dataset (`04_Superstore_Sales` / `trains.csv`)

- **Jumlah Baris & Kolom:** 9.818 baris transaksi ritel dan 18 atribut (`Row ID`, `Order ID`, `Order Date`, `Ship Date`, `Ship Mode`, `Customer ID`, `Customer Name`, `Segment`, `Country`, `City`, `State`, `Postal Code`, `Region`, `Product ID`, `Category`, `Sub-Category`, `Product Name`, `Sales`).
- **Identifier:** Kolom `Order ID` mencakup 4.922 nomor pesanan unik belanja.
- **Missing Value:** Ditemukan 50 nilai kosong (hanya pada atribut `Postal Code` untuk area non-standar logistik) atau 0,03% terhadap total sel keseluruhan (0,51% pada kolom `Postal Code`).
- **Duplikat & Penanggulangan:** Ditemukan 18 baris duplikat penuh yang dihapus menggunakan `drop_duplicates()`, menghasilkan 9.800 baris data transaksi bersih.
- **Distribusi Kategori:** Office Supplies mendominasi 5.909 transaksi (60,30%), Furniture 2.078 transaksi (21,20%), dan Technology 1.813 transaksi (18,50%).
- **Outlier:** Berdasarkan nilai moneter penjualan (`Sales`), kuartil $Q1 = \$17,25$, $Q3 = \$210,61$, $IQR = \$193,36$, dan batas atas outlier adalah $\$500,64$. Ditemukan 1.145 transaksi outlier (11,68% dari total data) bernilai tinggi hingga mencapai $\$22.638,48$ untuk pengadaan peralatan kantor komersial.

---

## Cara Menjalankan

1. Masuk ke direktori notebook yang ingin diuji (`01_Retail_Bian`, `02_Healthcare_Stroke`, `03_Retail_Dirty_Transactions`, atau `04_Superstore_Sales`).
2. Jalankan notebook menggunakan Jupyter Notebook, JupyterLab, atau VS Code.
3. Pastikan file CSV terkait berada pada direktori yang sama dengan notebook.
4. Eksekusi sel dari atas ke bawah untuk melihat hasil perhitungan dan visualisasi diagram.
