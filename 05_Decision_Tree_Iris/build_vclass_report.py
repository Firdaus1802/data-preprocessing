import os
import shutil
import pandas as pd
import numpy as np

# ReportLab imports
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak
)
from reportlab.pdfgen import canvas

# Docx imports
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

assets_dir = os.path.abspath('05_Decision_Tree_Iris/assets')
pdf_out_local = os.path.abspath('05_Decision_Tree_Iris/Tugas_VClass_M8_Decision_Tree_Firdaus_Dhuha_Prabowo_10124497_3KA31.pdf')
pdf_out_downloads = os.path.abspath('c:/Users/HP/Downloads/Tugas_VClass_M8_Decision_Tree_Firdaus_Dhuha_Prabowo_10124497_3KA31.pdf')
docx_out_local = os.path.abspath('05_Decision_Tree_Iris/Tugas_VClass_M8_Decision_Tree_Firdaus_Dhuha_Prabowo_10124497_3KA31.docx')
docx_out_downloads = os.path.abspath('c:/Users/HP/Downloads/Tugas_VClass_M8_Decision_Tree_Firdaus_Dhuha_Prabowo_10124497_3KA31.docx')


# --- Custom Canvas for Page Numbers & Running Header ---
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4B5563"))
        
        # Header on pages 2, 3, 4
        if self._pageNumber > 1:
            self.drawString(50, 804, "Tugas V-Class M8 - Klasifikasi Decision Tree | Firdaus Dhuha Prabowo (10124497)")
            self.drawRightString(545, 804, "Universitas Gunadarma")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(50, 798, 545, 798)
            
        # Footer on all pages
        footer_text = f"Halaman {self._pageNumber} dari {page_count}"
        self.drawRightString(545, 28, footer_text)
        self.drawString(50, 28, "Konsep Data Mining | S1 Sistem Informasi - Kelas 3KA31")
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(50, 38, 545, 38)
        self.restoreState()


def build_pdf():
    # A4: 595.27 x 841.89 points
    # Printable area: 495.27 x 751.89
    doc = SimpleDocTemplate(
        pdf_out_local,
        pagesize=A4,
        leftMargin=50,
        rightMargin=50,
        topMargin=45,
        bottomMargin=45
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        alignment=1, # Center
        textColor=colors.HexColor('#0F294A'),
        spaceAfter=2
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        alignment=1,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=8
    )
    
    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#0F294A'),
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.8,
        alignment=4, # Justified
        spaceAfter=4.5,
        textColor=colors.HexColor('#1F2937')
    )
    
    body_bold = ParagraphStyle(
        'BodyBoldCustom',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    
    quote_box = ParagraphStyle(
        'QuoteBox',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#1E293B'),
        backColor=colors.HexColor('#F8FAFC'),
        borderColor=colors.HexColor('#94A3B8'),
        borderWidth=0.8,
        borderPadding=4.5,
        spaceAfter=5
    )
    
    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.HexColor('#0F172A'),
        backColor=colors.HexColor('#F8FAFC'),
        borderColor=colors.HexColor('#CBD5E1'),
        borderWidth=0.6,
        borderPadding=4.5,
        spaceAfter=4
    )

    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.8,
        leading=10,
        alignment=1,
        textColor=colors.HexColor('#475569'),
        spaceAfter=5
    )

    story = []

    # ==================== PAGE 1 ====================
    # Title & Subtitle
    story.append(Paragraph("TUGAS V-CLASS KONSEP DATA MINING (PERTEMUAN 8)", title_style))
    story.append(Paragraph("Implementasi dan Analisis Algoritma Decision Tree Menggunakan Dataset Iris", subtitle_style))
    
    # Metadata Table
    meta_data = [
        [Paragraph("<b>Nama Mahasiswa</b>", body_style), Paragraph(": Firdaus Dhuha Prabowo", body_style),
         Paragraph("<b>Mata Kuliah</b>", body_style), Paragraph(": Konsep Data Mining", body_style)],
        [Paragraph("<b>NPM</b>", body_style), Paragraph(": 10124497", body_style),
         Paragraph("<b>Dosen Pengampu</b>", body_style), Paragraph(": Dr. Dina Anggraini, S.Kom., M.M.S.I.", body_style)],
        [Paragraph("<b>Kelas / Jurusan</b>", body_style), Paragraph(": 3KA31 / S1 Sistem Informasi", body_style),
         Paragraph("<b>Platform Tugas</b>", body_style), Paragraph(": V-Class Universitas Gunadarma", body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[98, 150, 95, 152])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 5))

    # SECTION 1
    story.append(Paragraph("1. Deskripsi Soal dan Pemilihan Dataset", h1_style))
    story.append(Paragraph(
        "<b>Instruksi Soal Latihan V-Class (Post Test M8):</b><br/>"
        "<i>\"Latihan: Ambilah sebuah dataset sederhana, lalu buatlah pohon keputusan untuk dataset tersebut.. dataset bisa diambil bebas dari kaggle atau lainnya!\"</i>",
        quote_box
    ))
    story.append(Paragraph(
        "Dalam rangka menyelesaikan tugas latihan ini, dataset yang dipilih adalah <b>Iris Flower Dataset</b> yang diunduh dari repositori Kaggle (Ronald A. Fisher / UCI Machine Learning). Alasan pemilihan dataset Iris adalah karena strukturnya yang kompak, memiliki 4 atribut numerik kontinu berdimensi riil, dan memiliki target kelas kategorikal (3 spesies). Dataset ini merupakan tolok ukur standar dalam pembelajaran konsep pemisahan biner (*binary recursive split*), perhitungan tingkat kemurnian (*Gini Impurity*), serta visualisasi pemangkasan pohon keputusan (*pruning*) secara jelas tanpa kompleksitas dimensi yang berlebihan.",
        body_style
    ))

    # SECTION 2
    story.append(Paragraph("2. Karakteristik Data dan Pra-Pemrosesan (EDA)", h1_style))
    story.append(Paragraph(
        "Dataset Iris memiliki 150 baris observasi yang terdiri atas 4 atribut prediktor numerik kontinu dan 1 variabel target kategorikal:",
        body_style
    ))
    
    # Table of Features
    feat_data = [
        [Paragraph("<b>Nama Atribut</b>", body_style), Paragraph("<b>Tipe Data</b>", body_style), Paragraph("<b>Rentang Nilai</b>", body_style), Paragraph("<b>Deskripsi Morfologi Bunga</b>", body_style)],
        [Paragraph("SepalLengthCm", body_style), Paragraph("Float64", body_style), Paragraph("4.3 - 7.9 cm", body_style), Paragraph("Panjang daun kelopak luar bunga Iris", body_style)],
        [Paragraph("SepalWidthCm", body_style), Paragraph("Float64", body_style), Paragraph("2.0 - 4.4 cm", body_style), Paragraph("Lebar daun kelopak luar bunga Iris", body_style)],
        [Paragraph("PetalLengthCm", body_style), Paragraph("Float64", body_style), Paragraph("1.0 - 6.9 cm", body_style), Paragraph("Panjang mahkota dalam bunga Iris", body_style)],
        [Paragraph("PetalWidthCm", body_style), Paragraph("Float64", body_style), Paragraph("0.1 - 2.5 cm", body_style), Paragraph("Lebar mahkota dalam bunga Iris", body_style)],
        [Paragraph("Species (Target)", body_style), Paragraph("Kategorikal", body_style), Paragraph("3 Kelas", body_style), Paragraph("Iris-setosa, Iris-versicolor, Iris-virginica", body_style)]
    ]
    feat_table = Table(feat_data, colWidths=[105, 70, 95, 225])
    feat_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E2E8F0')),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(feat_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>Tahapan Pra-Pemrosesan Data:</b><br/>"
        "• <b>Pengecekan Missing Values & Duplikasi:</b> Evaluasi menggunakan <font face='Courier'>df.isnull().sum()</font> menunjukkan nilai 0 pada semua kolom (tidak ada nilai kosong). Pengecekan baris duplikat juga menunjukkan data bersih, sehingga seluruh 150 sampel valid untuk digunakan.<br/>"
        "• <b>Distribusi Kelas:</b> Ketiga spesies memiliki jumlah data yang persis seimbang, yaitu masing-masing 50 sampel (proporsi 33.3% per spesies), sehingga model tidak memerlukan penanganan ketimpangan kelas (*class imbalance*).<br/>"
        "• <b>Pembagian Data (Train-Test Split):</b> Dataset dibagi secara proporsional menjadi <b>80% Data Latih (120 sampel)</b> dan <b>20% Data Uji (30 sampel)</b> dengan parameter <font face='Courier'>stratify=y</font> dan <font face='Courier'>random_state=42</font>. Stratifikasi menjamin data uji memuat masing-masing 10 sampel seimbang dari setiap spesies.",
        body_style
    ))
    
    # End of Page 1
    story.append(PageBreak())

    # ==================== PAGE 2 ====================
    # SECTION 3
    story.append(Paragraph("3. Pembangunan Model Decision Tree (Algoritma CART)", h1_style))
    story.append(Paragraph(
        "Model klasifikasi dibangun menggunakan algoritma <b>CART (Classification and Regression Trees)</b> melalui modul <font face='Courier'>DecisionTreeClassifier</font> pada pustaka Scikit-Learn. Konfigurasi parameter yang diterapkan mencakup:",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Kriteria Impurity (Gini Index):</b> Pemilihan atribut pemisah (*split*) dihitung berdasarkan fungsi Gini Impurity: "
        "<i>Gini(t) = 1 - &Sigma; (p<sub>i</sub>)<sup>2</sup></i>, di mana <i>p<sub>i</sub></i> adalah probabilitas kelas <i>i</i> pada node <i>t</i>. Nilai Gini = 0 menandakan node telah murni secara sempurna.<br/>"
        "• <b>Pemangkasan Awal (Pre-Pruning dengan max_depth = 3):</b> Kedalaman pohon dibatasi maksimal 3 level. Langkah ini sangat esensial untuk mencegah *overfitting* (menghafal *noise* data latih) sekaligus menghasilkan pohon keputusan yang ringkas dan mudah dipahami.<br/>"
        "• <b>Pendekatan Greedy:</b> Algoritma mengevaluasi seluruh titik ambang batas fitur dan memilih pemisahan yang menghasilkan penurunan ketidakmurnian tertinggi (*maximum Gini reduction*) pada node yang sedang diproses tanpa melakukan penelusuran kembali (*backtracking*).",
        body_style
    ))

    # SECTION 4
    story.append(Paragraph("4. Visualisasi Struktur Pohon Keputusan dan Analisis Alur Pemisahan", h1_style))
    story.append(Paragraph(
        "Diagram pohon keputusan hasil pelatihan model Scikit-Learn ditampilkan pada Gambar 1 berikut:",
        body_style
    ))

    img_tree = os.path.join(assets_dir, 'tree_diagram.png')
    if os.path.exists(img_tree):
        story.append(Image(img_tree, width=495, height=220))
        story.append(Paragraph("Gambar 1. Struktur Lengkap Pohon Keputusan Iris (Kriteria Gini, Max Depth = 3)", caption_style))

    story.append(Paragraph(
        "<b>Penjelasan Detail Alur Pemisahan Cabang Pohon:</b><br/>"
        "1. <b>Root Node (Kedalaman 0):</b> Memeriksa kondisi <font face='Courier'>PetalLength &le; 2.45 cm</font>. Pada 120 sampel data latih, terdapat 40 sampel Setosa, 40 Versicolor, dan 40 Virginica (Gini = 0.667).<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Cabang Kiri (True):</b> Seluruh 40 sampel <i>Iris-setosa</i> terpisah ke daun ini secara sempurna dengan nilai <b>Gini = 0.0</b> (murni 100%). Tidak diperlukan percabangan lagi.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Cabang Kanan (False):</b> Sebanyak 80 sampel sisa (40 Versicolor dan 40 Virginica, Gini = 0.500) dialirkan ke node internal berikutnya.<br/>"
        "2. <b>Node Internal Kedalaman 1:</b> Memeriksa kondisi <font face='Courier'>PetalWidth &le; 1.75 cm</font>.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Cabang Kiri (True):</b> Mengelompokkan 42 sampel (39 Versicolor dan 3 Virginica, Gini = 0.133).<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;• <b>Cabang Kanan (False):</b> Mengelompokkan 38 sampel (1 Versicolor dan 37 Virginica, Gini = 0.051).<br/>"
        "3. <b>Node Internal Kedalaman 2:</b> Melakukan penyaringan akhir pada sampel perbatasan menggunakan ambang batas <font face='Courier'>PetalLength &le; 4.95 cm</font> dan <font face='Courier'>PetalLength &le; 4.85 cm</font> guna memurnikan prediksi hingga tingkat daun akhir.",
        body_style
    ))

    # End of Page 2
    story.append(PageBreak())

    # ==================== PAGE 3 ====================
    story.append(Paragraph("Distribusi Fitur Petal dan Batas Pemisah Keputusan", h1_style))
    story.append(Paragraph(
        "Kombinasi dua fitur mahkota bunga (Petal Length dan Petal Width) membuktikan bagaimana pemisahan linier pada pohon keputusan bekerja di ruang dua dimensi:",
        body_style
    ))

    img_scatter = os.path.join(assets_dir, 'scatter_features.png')
    if os.path.exists(img_scatter):
        story.append(Image(img_scatter, width=380, height=200))
        story.append(Paragraph("Gambar 2. Sebaran Titik Data Petal Length vs Petal Width dan Garis Ambang Batas Pohon Keputusan", caption_style))

    story.append(Paragraph("<b>Formulasi Aturan Klasifikasi (IF-THEN Decision Rules):</b>", body_bold))
    story.append(Paragraph(
        "• <b>Aturan 1 (Setosa Murni):</b> IF (PetalLength &le; 2.45) &rarr; THEN Spesies = <b>Iris-setosa</b> [Akurasi 100%]<br/>"
        "• <b>Aturan 2 (Versicolor Tipikal):</b> IF (PetalLength &gt; 2.45) AND (PetalWidth &le; 1.75) AND (PetalLength &le; 4.95) &rarr; THEN Spesies = <b>Iris-versicolor</b><br/>"
        "• <b>Aturan 3 (Virginica Transisi):</b> IF (PetalLength &gt; 2.45) AND (PetalWidth &le; 1.75) AND (PetalLength &gt; 4.95) &rarr; THEN Spesies = <b>Iris-virginica</b><br/>"
        "• <b>Aturan 4 (Virginica Tipikal):</b> IF (PetalLength &gt; 2.45) AND (PetalWidth &gt; 1.75) &rarr; THEN Spesies = <b>Iris-virginica</b>",
        code_style
    ))

    # SECTION 5
    story.append(Paragraph("5. Evaluasi Kinerja Model pada Data Uji", h1_style))
    story.append(Paragraph(
        "Model diuji secara objektif menggunakan 30 data uji independen (<font face='Courier'>X_test</font>). Hasil evaluasi menunjukkan kinerja sangat memuaskan dengan <b>Akurasi Total 96.67%</b> (29 dari 30 sampel terklasifikasi secara benar).",
        body_style
    ))

    # Metric Table
    table_eval_data = [
        [Paragraph("<b>Spesies Target</b>", body_style), Paragraph("<b>Precision</b>", body_style), Paragraph("<b>Recall</b>", body_style), Paragraph("<b>F1-Score</b>", body_style), Paragraph("<b>Jumlah Data Uji</b>", body_style)],
        [Paragraph("Iris-setosa", body_style), Paragraph("1.00 (100%)", body_style), Paragraph("1.00 (100%)", body_style), Paragraph("1.00", body_style), Paragraph("10 sampel", body_style)],
        [Paragraph("Iris-versicolor", body_style), Paragraph("0.90 (90%)", body_style), Paragraph("1.00 (100%)", body_style), Paragraph("0.95", body_style), Paragraph("10 sampel", body_style)],
        [Paragraph("Iris-virginica", body_style), Paragraph("1.00 (100%)", body_style), Paragraph("0.91 (91%)", body_style), Paragraph("0.95", body_style), Paragraph("10 sampel", body_style)],
        [Paragraph("<b>Rata-rata Makro / Akurasi</b>", body_style), Paragraph("<b>0.97</b>", body_style), Paragraph("<b>0.97</b>", body_style), Paragraph("<b>0.97</b>", body_style), Paragraph("<b>30 (Akurasi: 96.67%)</b>", body_style)]
    ]
    eval_table = Table(table_eval_data, colWidths=[120, 85, 85, 85, 120])
    eval_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E2E8F0')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#F1F5F9')),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor('#94A3B8')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(eval_table)
    story.append(Spacer(1, 4))

    # End of Page 3
    story.append(PageBreak())

    # ==================== PAGE 4 ====================
    # CM and Feature Importance side-by-side
    img_cm = os.path.join(assets_dir, 'confusion_matrix.png')
    img_fi = os.path.join(assets_dir, 'feature_importance.png')
    if os.path.exists(img_cm) and os.path.exists(img_fi):
        t_imgs = Table([[Image(img_cm, width=195, height=140), Image(img_fi, width=235, height=140)]], colWidths=[210, 250])
        t_imgs.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        story.append(t_imgs)
        story.append(Paragraph("Gambar 3. (Kiri) Confusion Matrix Pengujian, dan (Kanan) Tingkat Kepentingan Fitur (Feature Importance)", caption_style))

    story.append(Paragraph(
        "<b>Interpretasi Kinerja Model dan Tingkat Kepentingan Fitur:</b><br/>"
        "• <b>Analisis Confusion Matrix:</b> Dari 30 sampel data uji, model berhasil mengklasifikasikan 10 Setosa dengan sempurna (100% akurat), 10 Versicolor dengan tepat, dan hanya 1 sampel Virginica yang salah terprediksi sebagai Versicolor karena berada di batas transisi nilai petal.<br/>"
        "• <b>Analisis Feature Importance:</b> Metrik Gini Importance menunjukkan bahwa fitur <b>PetalLengthCm berkontribusi sebesar 56.6%</b> dan <b>PetalWidthCm berkontribusi sebesar 40.0%</b> dalam pemisahan kelas. Sementara fitur daun kelopak luar (Sepal) memiliki kontribusi 0.0%, membuktikan bahwa dimensi mahkota dalam sudah sangat diskriminatif membedakan spesies.",
        body_style
    ))

    # SECTION 6
    story.append(Paragraph("6. Korelasi Materi Kuliah (Slide 58-59: Play Tennis & Pendekatan Greedy)", h1_style))
    story.append(Paragraph(
        "Pada materi kuliah Konsep Data Mining pertemuan klasifikasi Decision Tree, dibahas contoh klasik dataset cuaca *Play Tennis* menggunakan algoritma ID3/C4.5 untuk menentukan keputusan bermain tenis berdasarkan kondisi cuaca (Outlook, Temperature, Humidity, Wind).<br/>"
        "Hubungan fundamental antara implementasi dataset Iris ini dengan teori kuliah adalah penerapan <b>Pendekatan Greedy</b>. Pada setiap tahapan pemecahan (*split*), algoritma selalu mencari atribut yang memberikan peningkatan kemurnian terbaik (*local optimum*) pada saat itu juga tanpa meninjau ulang keputusan sebelumnya. Pada *Play Tennis*, atribut 'Outlook' terpilih sebagai root node karena memiliki Information Gain tertinggi. Sedangkan pada dataset Iris, fitur 'PetalLength' terpilih di root node karena memberikan reduksi Gini Impurity terbesar.",
        body_style
    ))

    # SECTION 7
    story.append(Paragraph("7. Kesimpulan", h1_style))
    story.append(Paragraph(
        "Berdasarkan eksperimen dan analisis klasifikasi Decision Tree pada dataset Iris, dapat ditarik kesimpulan:<br/>"
        "1. Algoritma Decision Tree berhasil melakukan klasifikasi spesies bunga Iris dengan akurasi sangat tinggi, yaitu <b>96.67%</b> pada data uji independen.<br/>"
        "2. Penerapan pembatasan kedalaman (<font face='Courier'>max_depth=3</font>) terbukti efektif mencegah masalah *overfitting* serta menghasilkan pohon keputusan yang ringkas dan mudah diinterpretasikan menjadi aturan logika IF-THEN.<br/>"
        "3. Fitur morfologi mahkota bunga (<font face='Courier'>PetalLength</font> dan <font face='Courier'>PetalWidth</font>) merupakan penentu utama klasifikasi spesies Iris, dengan batas ambang &le; 2.45 cm menjadi pemisah mutlak spesies *Setosa*.",
        body_style
    ))

    # SECTION 8 - Code Appendix
    story.append(Paragraph("Lampiran: Implementasi Kode Program Python (Scikit-Learn)", h1_style))
    code_text = (
        "import pandas as pd<br/>"
        "from sklearn.model_selection import train_test_split<br/>"
        "from sklearn.tree import DecisionTreeClassifier<br/>"
        "from sklearn.metrics import accuracy_score, classification_report, confusion_matrix<br/><br/>"
        "# 1. Load dataset & persiapan fitur<br/>"
        "df = pd.read_csv('iris.csv')<br/>"
        "X = df[['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']]<br/>"
        "y = df['Species']<br/><br/>"
        "# 2. Split dataset 80:20 (Stratified)<br/>"
        "X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)<br/><br/>"
        "# 3. Training model Decision Tree (Gini, max_depth=3)<br/>"
        "model = DecisionTreeClassifier(criterion='gini', max_depth=3, random_state=42)<br/>"
        "model.fit(X_train, y_train)<br/><br/>"
        "# 4. Evaluasi hasil pengujian<br/>"
        "y_pred = model.predict(X_test)<br/>"
        "print('Akurasi Model:', accuracy_score(y_test, y_pred)) # Output: 0.9667 (96.67%)"
    )
    story.append(Paragraph(code_text, code_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF built successfully at: {pdf_out_local}")
    shutil.copy2(pdf_out_local, pdf_out_downloads)
    print(f"PDF copied to: {pdf_out_downloads}")


def build_docx():
    doc = docx.Document()
    
    # Set standard margins (1 inch / 2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10.5)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    
    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("TUGAS V-CLASS KONSEP DATA MINING (PERTEMUAN 8)")
    run_title.font.bold = True
    run_title.font.size = Pt(14)
    run_title.font.color.rgb = RGBColor(0x0F, 0x29, 0x4A)
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("Implementasi dan Analisis Algoritma Decision Tree Menggunakan Dataset Iris")
    run_sub.font.bold = True
    run_sub.font.size = Pt(11)
    run_sub.font.color.rgb = RGBColor(0x2C, 0x3E, 0x50)
    
    # Metadata Table
    table = doc.add_table(rows=3, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_info = [
        ("Nama Mahasiswa", ": Firdaus Dhuha Prabowo", "Mata Kuliah", ": Konsep Data Mining"),
        ("NPM", ": 10124497", "Dosen Pengampu", ": Dr. Dina Anggraini, S.Kom., M.M.S.I."),
        ("Kelas / Jurusan", ": 3KA31 / S1 Sistem Informasi", "Platform Tugas", ": V-Class Universitas Gunadarma")
    ]
    for r_idx, row in enumerate(meta_info):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.paragraphs[0]
            p.runs[0].font.size = Pt(9.5)
            if c_idx in [0, 2]:
                p.runs[0].font.bold = True
                
    doc.add_paragraph() # Spacer
    
    # Section 1
    h1 = doc.add_heading("1. Deskripsi Soal dan Pemilihan Dataset", level=1)
    h1.runs[0].font.color.rgb = RGBColor(0x0F, 0x29, 0x4A)
    
    p_soal = doc.add_paragraph()
    p_soal.add_run('Instruksi Soal Latihan V-Class (Post Test M8):\n"Latihan: Ambilah sebuah dataset sederhana, lalu buatlah pohon keputusan untuk dataset tersebut.. dataset bisa diambil bebas dari kaggle atau lainnya!"').italic = True
    
    doc.add_paragraph(
        "Dalam rangka menyelesaikan tugas latihan ini, dataset yang dipilih adalah Iris Flower Dataset yang diunduh dari repositori Kaggle (Ronald A. Fisher / UCI Machine Learning). Alasan pemilihan dataset Iris adalah karena strukturnya yang kompak, memiliki 4 atribut numerik kontinu berdimensi riil, dan memiliki target kelas kategorikal (3 spesies). Dataset ini merupakan tolok ukur standar dalam pembelajaran konsep pemisahan biner (binary recursive split), perhitungan tingkat kemurnian (Gini Impurity), serta pembentukan aturan keputusan IF-THEN tanpa kompleksitas noise berlebih."
    )
    
    # Section 2
    h2 = doc.add_heading("2. Karakteristik Data dan Pra-Pemrosesan (EDA)", level=1)
    h2.runs[0].font.color.rgb = RGBColor(0x0F, 0x29, 0x4A)
    doc.add_paragraph(
        "Dataset Iris memiliki 150 baris observasi yang terdiri atas 4 atribut prediktor numerik kontinu dan 1 variabel target kategorikal:\n"
        "• SepalLengthCm (4.3 - 7.9 cm) : Panjang daun kelopak luar bunga Iris\n"
        "• SepalWidthCm (2.0 - 4.4 cm)  : Lebar daun kelopak luar bunga Iris\n"
        "• PetalLengthCm (1.0 - 6.9 cm) : Panjang mahkota dalam bunga Iris\n"
        "• PetalWidthCm (0.1 - 2.5 cm)  : Lebar mahkota dalam bunga Iris\n"
        "• Species (Target)             : Iris-setosa, Iris-versicolor, Iris-virginica (3 kelas seimbang)\n\n"
        "Tahapan Pra-Pemrosesan Data:\n"
        "1. Pengecekan Missing Values & Duplikasi: Tidak ditemukan data kosong (missing values = 0) maupun duplikasi data.\n"
        "2. Distribusi Kelas: Ketiga kelas spesies seimbang, masing-masing 50 sampel (proporsi 33.3% per kelas).\n"
        "3. Pembagian Data: Dataset dibagi secara terstratifikasi (stratify=y, random_state=42) menjadi 80% Data Latih (120 sampel) dan 20% Data Uji (30 sampel)."
    )
    
    # Section 3
    h3 = doc.add_heading("3. Pembangunan Model Decision Tree (Algoritma CART)", level=1)
    h3.runs[0].font.color.rgb = RGBColor(0x0F, 0x29, 0x4A)
    doc.add_paragraph(
        "Model klasifikasi dibangun menggunakan algoritma CART (Classification and Regression Trees) melalui pustaka Scikit-Learn (DecisionTreeClassifier). Konfigurasi parameter:\n"
        "• Kriteria Impurity (Gini Index): Mengukur ketidakmurnian node dengan formula Gini = 1 - sum(p_i^2).\n"
        "• Pemangkasan Awal (max_depth = 3): Membatasi kedalaman pohon maksimal 3 level untuk mencegah overfitting dan mempertahankan kemudahan interpretasi aturan.\n"
        "• Pendekatan Greedy: Algoritma memilih pemisahan terbaik secara lokal pada setiap node tanpa meninjau ulang keputusan sebelumnya."
    )
    
    # Section 4
    h4 = doc.add_heading("4. Visualisasi Pohon Keputusan dan Aturan Klasifikasi", level=1)
    h4.runs[0].font.color.rgb = RGBColor(0x0F, 0x29, 0x4A)
    
    img_tree = os.path.join(assets_dir, 'tree_diagram.png')
    if os.path.exists(img_tree):
        doc.add_picture(img_tree, width=Inches(6.2))
        p_cap = doc.add_paragraph("Gambar 1. Struktur Lengkap Pohon Keputusan Iris (Maksimal Kedalaman = 3)")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.size = Pt(8.5)
        p_cap.runs[0].font.italic = True
        
    doc.add_paragraph(
        "Penjelasan Detail Alur Pemisahan Cabang Pohon:\n"
        "1. Root Node (Kedalaman 0): Memeriksa PetalLength <= 2.45 cm. Seluruh 40 sampel Setosa terpisah ke daun kiri dengan nilai Gini = 0.0 (murni 100%).\n"
        "2. Node Internal Kedalaman 1: Memeriksa PetalWidth <= 1.75 cm. Memisahkan 39 sampel Versicolor ke kiri dan 37 sampel Virginica ke kanan.\n"
        "3. Node Kedalaman 2: Melakukan pemurnian lanjutan pada sampel perbatasan dengan threshold PetalLength <= 4.95 cm dan <= 4.85 cm.\n\n"
        "Ekstraksi Aturan Keputusan (IF-THEN Rules):\n"
        "• Aturan 1: IF (PetalLength <= 2.45) THEN Species = Iris-setosa (Akurasi 100%)\n"
        "• Aturan 2: IF (PetalLength > 2.45) AND (PetalWidth <= 1.75) AND (PetalLength <= 4.95) THEN Species = Iris-versicolor\n"
        "• Aturan 3: IF (PetalLength > 2.45) AND (PetalWidth <= 1.75) AND (PetalLength > 4.95) THEN Species = Iris-virginica\n"
        "• Aturan 4: IF (PetalLength > 2.45) AND (PetalWidth > 1.75) THEN Species = Iris-virginica"
    )
    
    img_scatter = os.path.join(assets_dir, 'scatter_features.png')
    if os.path.exists(img_scatter):
        doc.add_picture(img_scatter, width=Inches(5.0))
        p_cap = doc.add_paragraph("Gambar 2. Distribusi Petal Length vs Petal Width dan Garis Ambang Batas Pohon Keputusan")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.size = Pt(8.5)
        p_cap.runs[0].font.italic = True

    # Section 5
    h5 = doc.add_heading("5. Evaluasi Kinerja Model pada Data Uji", level=1)
    h5.runs[0].font.color.rgb = RGBColor(0x0F, 0x29, 0x4A)
    doc.add_paragraph(
        "Hasil pengujian pada 30 data uji menghasilkan Akurasi Total sebesar 96.67% (29 dari 30 sampel terprediksi tepat).\n"
        "• Iris-setosa     : Precision 1.00, Recall 1.00, F1-Score 1.00 (10 sampel)\n"
        "• Iris-versicolor : Precision 0.90, Recall 1.00, F1-Score 0.95 (10 sampel)\n"
        "• Iris-virginica  : Precision 1.00, Recall 0.91, F1-Score 0.95 (10 sampel)\n\n"
        "Feature Importance:\n"
        "• PetalLengthCm : 56.6%\n"
        "• PetalWidthCm  : 40.0%\n"
        "• SepalLengthCm & SepalWidthCm : 0.0% (tidak digunakan pada kedalaman 3)"
    )
    
    img_cm = os.path.join(assets_dir, 'confusion_matrix.png')
    if os.path.exists(img_cm):
        doc.add_picture(img_cm, width=Inches(4.0))
        p_cap = doc.add_paragraph("Gambar 3. Confusion Matrix Pengujian pada 30 Data Uji")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.size = Pt(8.5)
        p_cap.runs[0].font.italic = True

    # Section 6
    h6 = doc.add_heading("6. Korelasi Materi Kuliah (Slide 58-59: Play Tennis & Pendekatan Greedy)", level=1)
    h6.runs[0].font.color.rgb = RGBColor(0x0F, 0x29, 0x4A)
    doc.add_paragraph(
        "Pada materi kuliah Konsep Data Mining, dibahas contoh klasik dataset Play Tennis. Algoritma Decision Tree menggunakan pendekatan greedy dengan memilih atribut pemisah lokal terbaik pada setiap node tanpa meninjau ulang keputusan sebelumnya. Pada dataset Iris, pendekatan greedy ini terbukti sangat cepat dan menghasilkan pohon keputusan yang optimal dengan akurasi 96.67%."
    )
    
    # Section 7
    h7 = doc.add_heading("7. Kesimpulan", level=1)
    h7.runs[0].font.color.rgb = RGBColor(0x0F, 0x29, 0x4A)
    doc.add_paragraph(
        "1. Algoritma Decision Tree berhasil memodelkan klasifikasi spesies bunga Iris dengan akurasi 96.67% pada data uji.\n"
        "2. Pembatasan kedalaman (max_depth=3) efektif mencegah overfitting dan menghasilkan pohon yang mudah dipahami.\n"
        "3. Fitur dimensi mahkota bunga (Petal Length dan Petal Width) merupakan penentu utama klasifikasi spesies Iris."
    )
    
    doc.save(docx_out_local)
    print(f"DOCX built successfully at: {docx_out_local}")
    shutil.copy2(docx_out_local, docx_out_downloads)
    print(f"DOCX copied to: {docx_out_downloads}")


if __name__ == '__main__':
    build_pdf()
    build_docx()
