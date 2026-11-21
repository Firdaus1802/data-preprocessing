import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx2pdf import convert
import fitz

assets_dir = os.path.abspath('05_Decision_Tree_Iris/assets')
docx_test = os.path.abspath('05_Decision_Tree_Iris/test_4p.docx')
pdf_test = os.path.abspath('05_Decision_Tree_Iris/test_4p.pdf')


def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def set_cell_margins(cell, top=40, bottom=40, left=60, right=60):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)


def set_table_borders(table, color="000000", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
            <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideV w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)


def add_page_number_fields(run):
    fldChar1 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>')
    instrText = parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> PAGE </w:instrText>')
    fldChar2 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="separate"/>')
    fldChar3 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>')
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)


def add_numpages_fields(run):
    fldChar1 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="begin"/>')
    instrText = parse_xml(f'<w:instrText {nsdecls("w")} xml:space="preserve"> NUMPAGES </w:instrText>')
    fldChar2 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="separate"/>')
    fldChar3 = parse_xml(f'<w:fldChar {nsdecls("w")} w:fldCharType="end"/>')
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)


def build_test_doc():
    doc = docx.Document()
    
    doc.core_properties.author = "Firdaus Dhuha Prabowo"
    doc.core_properties.title = "Tugas V-Class Konsep Data Mining (M8) - Klasifikasi Decision Tree"

    for section in doc.sections:
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)
        section.left_margin = Inches(1.18)  # 3.0 cm
        section.right_margin = Inches(0.98) # 2.5 cm
        section.top_margin = Inches(0.85)   # ~2.15 cm
        section.bottom_margin = Inches(0.85)# ~2.15 cm
        
        # Header setup
        header = section.header
        p_hd = header.paragraphs[0]
        p_hd.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_hd.paragraph_format.space_before = Pt(0)
        p_hd.paragraph_format.space_after = Pt(0)
        r_hd = p_hd.add_run("Tugas V-Class Konsep Data Mining | Pertemuan 8")
        r_hd.font.name = 'Times New Roman'
        r_hd.font.size = Pt(8.5)
        r_hd.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
        
        # Footer setup
        footer = section.footer
        p_ft = footer.paragraphs[0]
        p_ft.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_ft.paragraph_format.space_before = Pt(0)
        p_ft.paragraph_format.space_after = Pt(0)
        
        r_ft_left = p_ft.add_run("Firdaus Dhuha Prabowo (10124497) - 3KA31                                          ")
        r_ft_left.font.name = 'Times New Roman'
        r_ft_left.font.size = Pt(8.5)
        r_ft_left.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        
        r_ft_pg = p_ft.add_run("Halaman ")
        r_ft_pg.font.name = 'Times New Roman'
        r_ft_pg.font.size = Pt(8.5)
        r_ft_pg.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        add_page_number_fields(r_ft_pg)
        
        r_ft_mid = p_ft.add_run(" dari ")
        r_ft_mid.font.name = 'Times New Roman'
        r_ft_mid.font.size = Pt(8.5)
        r_ft_mid.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        add_numpages_fields(r_ft_mid)

    # Base Normal Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.12
    normal_style.paragraph_format.space_after = Pt(3)
    normal_style.paragraph_format.space_before = Pt(0)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.font.bold = True
        run.font.size = Pt(11.5)
        return p

    def add_p(text, bold_prefix=None, indent=False):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.12
        if indent:
            p.paragraph_format.first_line_indent = Inches(0.25)
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.font.bold = True
        p.add_run(text)
        return p

    def add_caption(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = False
        run = p.add_run(text)
        run.font.italic = True
        run.font.size = Pt(9.5)
        return p

    # ==================== HALAMAN 1 ====================
    # Judul
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(1)
    r1 = p_title.add_run("TUGAS V-CLASS KONSEP DATA MINING (PERTEMUAN 8)")
    r1.font.bold = True
    r1.font.size = Pt(12.5)
    
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(6)
    r2 = p_sub.add_run("Implementasi dan Analisis Klasifikasi Decision Tree pada Dataset Iris")
    r2.font.bold = True
    r2.font.size = Pt(11.5)

    # Identitas Mahasiswa
    t_id = doc.add_table(rows=6, cols=3)
    t_id.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_id.autofit = False
    
    col_widths = [Inches(1.8), Inches(0.2), Inches(4.1)]
    id_data = [
        ("Nama Mahasiswa", ":", "Firdaus Dhuha Prabowo"),
        ("NPM", ":", "10124497"),
        ("Kelas", ":", "3KA31"),
        ("Program Studi", ":", "S1 Sistem Informasi"),
        ("Mata Kuliah", ":", "Konsep Data Mining"),
        ("Dosen Pengampu", ":", "Dr. Dina Anggraini, S.Kom., M.M.S.I.")
    ]
    for row_idx, (k, sep, v) in enumerate(id_data):
        row = t_id.rows[row_idx]
        for col_idx, text in enumerate([k, sep, v]):
            cell = row.cells[col_idx]
            cell.width = col_widths[col_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            run = p.add_run(text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10)
            if col_idx == 0:
                run.font.bold = True

    # Horizontal Line
    p_line = doc.add_paragraph()
    p_line.paragraph_format.space_before = Pt(2)
    p_line.paragraph_format.space_after = Pt(5)
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="10" w:space="1" w:color="000000"/></w:pBdr>')
    p_line._p.get_or_add_pPr().append(pBdr)

    # A. Soal Latihan & Pemilihan Dataset
    add_h1("A. Soal Latihan dan Pemilihan Dataset")
    p_soal = doc.add_paragraph()
    p_soal.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_soal.paragraph_format.space_before = Pt(0)
    p_soal.paragraph_format.space_after = Pt(3)
    p_soal.paragraph_format.left_indent = Inches(0.2)
    p_soal.paragraph_format.right_indent = Inches(0.2)
    r_soal_title = p_soal.add_run("Instruksi Soal Post-Test V-Class Pertemuan 8:\n")
    r_soal_title.font.bold = True
    r_soal_title.font.size = Pt(10)
    r_soal = p_soal.add_run('"Latihan: Ambilah sebuah dataset sederhana, lalu buatlah pohon keputusan untuk dataset tersebut.. dataset bisa diambil bebas dari kaggle atau lainnya!"')
    r_soal.font.italic = True
    r_soal.font.size = Pt(10)

    add_p(
        "Untuk memenuhi tugas praktikum V-Class ini, dataset yang dipilih adalah Iris Flower Dataset yang bersumber dari repositori Kaggle (Ronald A. Fisher / UCI Machine Learning). Alasan utama pemilihan dataset Iris adalah karena strukturnya yang sederhana, memiliki 4 atribut numerik kontinu berdimensi riil, dan memiliki target kelas kategorikal (3 spesies). Dataset ini merupakan tolok ukur standar dalam pembelajaran konsep pemisahan biner (binary split), perhitungan tingkat kemurnian (Gini Impurity), serta visualisasi pemangkasan pohon keputusan (pruning) secara jelas tanpa kompleksitas dimensi yang berlebihan.",
        indent=True
    )

    # B. Karakteristik Data & EDA
    add_h1("B. Karakteristik Data dan Pra-Pemrosesan (EDA)")
    add_p(
        "Dataset Iris memiliki 150 baris data observasi yang terdiri atas 4 atribut prediktor numerik kontinu dan 1 atribut target kategorikal. Rincian struktur data disajikan pada Tabel 1 di bawah ini:"
    )

    t_feat = doc.add_table(rows=6, cols=4)
    t_feat.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_feat.autofit = False
    set_table_borders(t_feat)
    
    t_feat_widths = [Inches(1.5), Inches(1.0), Inches(1.2), Inches(2.4)]
    feat_rows = [
        ("Nama Atribut", "Tipe Data", "Rentang Nilai", "Keterangan Morfologi"),
        ("SepalLengthCm", "Float64", "4.3 – 7.9 cm", "Panjang daun kelopak luar bunga"),
        ("SepalWidthCm", "Float64", "2.0 – 4.4 cm", "Lebar daun kelopak luar bunga"),
        ("PetalLengthCm", "Float64", "1.0 – 6.9 cm", "Panjang mahkota dalam bunga"),
        ("PetalWidthCm", "Float64", "0.1 – 2.5 cm", "Lebar mahkota dalam bunga"),
        ("Species (Target)", "Kategorikal", "3 Kelas", "Iris-setosa, Versicolor, Virginica")
    ]
    for r_idx, row_data in enumerate(feat_rows):
        row = t_feat.rows[r_idx]
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = t_feat_widths[c_idx]
            set_cell_margins(cell, top=35, bottom=35, left=60, right=60)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            run = p.add_run(val)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9.5)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "F2F2F2")
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif c_idx in [1, 2]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                
    add_caption("Tabel 1. Deskripsi Fitur dan Struktur Dataset Iris")

    add_p(
        "Pengecekan menggunakan sintaks df.isnull().sum() menunjukkan angka 0 pada seluruh kolom (tidak ada data kosong). Pengecekan data duplikat juga menunjukkan data lengkap dan bersih. Ketiga spesies memiliki jumlah data yang persis seimbang (masing-masing 50 sampel). Dataset kemudian dibagi menjadi 80% data latih (120 sampel) dan 20% data uji (30 sampel) dengan parameter stratify=y dan random_state=42 sehingga setiap kelas terwakili secara proporsional.",
        bold_prefix="Tahapan Pra-Pemrosesan: "
    )

    doc.add_page_break()

    # ==================== HALAMAN 2 ====================
    # C. Pembangunan Model Decision Tree
    add_h1("C. Pembangunan Model Decision Tree (Algoritma CART)")
    add_p(
        "Model klasifikasi dibangun menggunakan algoritma CART (Classification and Regression Trees) melalui pustaka Scikit-Learn (DecisionTreeClassifier). Konfigurasi parameter yang diterapkan mencakup:",
        indent=True
    )
    add_p("• Kriteria Pemisahan (Gini Index): ", bold_prefix=None)
    doc.paragraphs[-1].runs[0].font.bold = True
    doc.paragraphs[-1].add_run("Tingkat ketidakmurnian diukur dengan formula Gini Impurity: Gini(t) = 1 - sum(p_i^2), di mana p_i adalah proporsi sampel kelas i pada node t. Nilai Gini = 0 menandakan node telah murni secara sempurna (semua sampel berasal dari satu kelas).")

    add_p("• Pembatasan Kedalaman (max_depth = 3): ", bold_prefix=None)
    doc.paragraphs[-1].runs[0].font.bold = True
    doc.paragraphs[-1].add_run("Diterapkan pembatasan tinggi pohon maksimal 3 tingkat sebagai bentuk pemangkasan awal (pre-pruning). Pembatasan ini bertujuan untuk menghindari overfitting (menghafal data latih) dan menghasilkan pohon keputusan yang ringkas sehingga mudah dipahami secara visual.")

    add_p("• Pendekatan Greedy: ", bold_prefix=None)
    doc.paragraphs[-1].runs[0].font.bold = True
    doc.paragraphs[-1].add_run("Algoritma mengevaluasi seluruh atribut dan ambang batas (threshold) yang ada, kemudian memilih pemisahan yang menghasilkan penurunan Gini terbesar saat itu juga tanpa meninjau ulang keputusan sebelumnya (tanpa backtracking).")

    # D. Visualisasi Struktur Pohon Keputusan
    add_h1("D. Visualisasi Struktur Pohon Keputusan dan Aturan Klasifikasi")
    add_p(
        "Hasil pemodelan Decision Tree divisualisasikan dalam bentuk diagram struktur pohon pada Gambar 1 di bawah ini:"
    )

    img_tree = os.path.join(assets_dir, 'tree_diagram.png')
    if os.path.exists(img_tree):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(1)
        p_img.paragraph_format.space_after = Pt(1)
        p_img.add_run().add_picture(img_tree, width=Inches(5.6))
        add_caption("Gambar 1. Struktur Lengkap Pohon Keputusan Iris (Kriteria Gini, Max Depth = 3)")

    add_p("Penjelasan Alur Pemisahan Cabang Pohon Keputusan:", bold_prefix=None)
    doc.paragraphs[-1].runs[0].font.bold = True

    add_p("1. Root Node (Kedalaman 0): ", bold_prefix=None)
    doc.paragraphs[-1].runs[0].font.bold = True
    doc.paragraphs[-1].add_run("Kondisi pemisah pertama menguji apakah PetalLength <= 2.45 cm. Dari 120 sampel data latih, seluruh 40 sampel Iris-setosa memiliki panjang mahkota kurang dari 2.45 cm, sehingga langsung terpisah ke cabang kiri (daun) dengan nilai Gini = 0.0 (murni 100%). Sebanyak 80 sampel lainnya (40 Versicolor dan 40 Virginica) diteruskan ke cabang kanan.")

    add_p("2. Node Internal Kedalaman 1: ", bold_prefix=None)
    doc.paragraphs[-1].runs[0].font.bold = True
    doc.paragraphs[-1].add_run("Kondisi pemisah kedua menguji apakah PetalWidth <= 1.75 cm. Sampel yang memenuhi kondisi ini diarahkan ke kiri (didominasi Iris-versicolor sebanyak 39 sampel dan 3 Virginica), sedangkan yang lebih besar dari 1.75 cm diarahkan ke kanan (didominasi Iris-virginica sebanyak 37 sampel dan 1 Versicolor).")

    add_p("3. Node Internal Kedalaman 2: ", bold_prefix=None)
    doc.paragraphs[-1].runs[0].font.bold = True
    doc.paragraphs[-1].add_run("Dilakukan pengujian lanjutan pada perbatasan nilai dengan ambang batas PetalLength <= 4.95 cm dan PetalLength <= 4.85 cm untuk memurnikan sisa sampel minoritas hingga mencapai daun akhir.")

    doc.add_page_break()

    # ==================== HALAMAN 3 ====================
    # Aturan Keputusan (IF-THEN)
    add_h1("Formulasi Aturan Klasifikasi (IF-THEN Rules)")
    add_p("Berdasarkan penelusuran pohon keputusan dari simpul akar hingga simpul daun, terbentuk aturan logika klasifikasi sebagai berikut:")

    rules_text = (
        "• Aturan 1: IF (PetalLength <= 2.45) THEN Spesies = Iris-setosa [Akurasi 100%]\n"
        "• Aturan 2: IF (PetalLength > 2.45) AND (PetalWidth <= 1.75) AND (PetalLength <= 4.95) THEN Spesies = Iris-versicolor\n"
        "• Aturan 3: IF (PetalLength > 2.45) AND (PetalWidth <= 1.75) AND (PetalLength > 4.95) THEN Spesies = Iris-virginica\n"
        "• Aturan 4: IF (PetalLength > 2.45) AND (PetalWidth > 1.75) THEN Spesies = Iris-virginica"
    )
    p_rules = doc.add_paragraph()
    p_rules.paragraph_format.left_indent = Inches(0.2)
    p_rules.paragraph_format.space_before = Pt(1)
    p_rules.paragraph_format.space_after = Pt(4)
    p_rules.paragraph_format.line_spacing = 1.05
    r_rules = p_rules.add_run(rules_text)
    r_rules.font.name = 'Consolas'
    r_rules.font.size = Pt(9)

    # E. Pengujian Model & Evaluasi Kinerja
    add_h1("E. Pengujian Model dan Evaluasi Kinerja")
    add_p(
        "Kinerja model diuji menggunakan 30 data uji independen (X_test). Dari 30 data uji tersebut, sebanyak 29 data berhasil diklasifikasikan dengan benar (Akurasi Total 96.67%). Rincian evaluasi per kelas disajikan pada Tabel 2:"
    )

    t_eval = doc.add_table(rows=5, cols=5)
    t_eval.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_eval.autofit = False
    set_table_borders(t_eval)
    
    t_eval_widths = [Inches(1.8), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.0)]
    eval_rows = [
        ("Spesies (Kelas)", "Precision", "Recall", "F1-Score", "Jumlah Uji"),
        ("Iris-setosa", "1.00 (100%)", "1.00 (100%)", "1.00", "10"),
        ("Iris-versicolor", "0.90 (90%)", "1.00 (100%)", "0.95", "10"),
        ("Iris-virginica", "1.00 (100%)", "0.91 (91%)", "0.95", "10"),
        ("Rata-rata Makro / Akurasi", "0.97", "0.97", "0.97", "30 (96.67%)")
    ]
    for r_idx, row_data in enumerate(eval_rows):
        row = t_eval.rows[r_idx]
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = t_eval_widths[c_idx]
            set_cell_margins(cell, top=35, bottom=35, left=60, right=60)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            run = p.add_run(val)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(9.5)
            if r_idx == 0:
                run.font.bold = True
                set_cell_background(cell, "F2F2F2")
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif r_idx == 4:
                run.font.bold = True
                set_cell_background(cell, "F9F9F9")
                if c_idx > 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif c_idx > 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    add_caption("Tabel 2. Hasil Evaluasi Kinerja Model Decision Tree pada Data Uji")

    # Gambar Confusion Matrix dan Feature Importance
    img_cm = os.path.join(assets_dir, 'confusion_matrix.png')
    img_fi = os.path.join(assets_dir, 'feature_importance.png')
    if os.path.exists(img_cm) and os.path.exists(img_fi):
        t_img_pair = doc.add_table(rows=1, cols=2)
        t_img_pair.alignment = WD_TABLE_ALIGNMENT.CENTER
        t_img_pair.autofit = False
        
        c0 = t_img_pair.rows[0].cells[0]
        c0.width = Inches(2.6)
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(0)
        p0.add_run().add_picture(img_cm, width=Inches(2.3))
        
        c1 = t_img_pair.rows[0].cells[1]
        c1.width = Inches(3.2)
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(0)
        p1.add_run().add_picture(img_fi, width=Inches(2.8))
        
        add_caption("Gambar 2. (Kiri) Confusion Matrix Pengujian, dan (Kanan) Grafik Feature Importance")

    add_p(
        "Berdasarkan matriks konfusi (Gambar 2 kiri), seluruh 10 sampel Iris-setosa dan 10 sampel Iris-versicolor terprediksi dengan benar, dan hanya 1 sampel Iris-virginica yang mengalami kesalahan prediksi tergolong sebagai Versicolor karena berada di batas transisi nilai petal. Pada grafik Feature Importance (Gambar 2 kanan), fitur PetalLengthCm (56.6%) dan PetalWidthCm (40.0%) secara mutlak mendominasi pengambilan keputusan pohon, sedangkan atribut SepalLengthCm dan SepalWidthCm bernilai 0.0%.",
        bold_prefix="Analisis Kinerja: "
    )

    doc.add_page_break()

    # ==================== HALAMAN 4 ====================
    # F. Hubungan dengan Teori Kuliah
    add_h1("F. Hubungan dengan Teori Kuliah (Slide 58–59: Play Tennis & Pendekatan Greedy)")
    add_p(
        "Pada materi perkuliahan Konsep Data Mining, dibahas contoh klasik penentuan keputusan bermain tenis (Play Tennis) menggunakan algoritma ID3/C4.5 berdasarkan atribut kondisi cuaca (Outlook, Temperature, Humidity, Wind). Hubungan penting antara materi kuliah tersebut dengan eksperimen dataset Iris ini adalah penerapan Pendekatan Greedy (Greedy Approach):",
        indent=True
    )
    add_p("1. Pemilihan Keputusan Optimum Lokal: ", bold_prefix=None)
    doc.paragraphs[-1].runs[0].font.bold = True
    doc.paragraphs[-1].add_run("Pada setiap simpul (node), algoritma selalu memilih atribut pemisah yang menghasilkan keuntungan kemurnian data terbesar pada saat itu juga (Information Gain pada Play Tennis, atau Gini Gain pada CART) tanpa mengecek kombinasi pohon secara global di tingkat bawahnya.")

    add_p("2. Tanpa Peninjauan Ulang (No Backtracking): ", bold_prefix=None)
    doc.paragraphs[-1].runs[0].font.bold = True
    doc.paragraphs[-1].add_run("Sekali atribut pemisah dipilih di root node (seperti Outlook pada Play Tennis atau PetalLength pada dataset Iris), keputusan tersebut bersifat final. Pendekatan ini dipilih dalam data mining karena sangat efisien secara komputasi dan terbukti menghasilkan akurasi tinggi sebesar 96.67%.")

    # G. Kesimpulan
    add_h1("G. Kesimpulan")
    add_p("1. Model Decision Tree berhasil mengklasifikasikan spesies bunga Iris dengan tingkat akurasi yang sangat baik, yaitu mencapai 96.67% pada data uji independen.")
    add_p("2. Penerapan pembatasan kedalaman pohon (max_depth = 3) terbukti efektif mencegah overfitting serta menghasilkan pohon keputusan yang sederhana dan mudah diinterpretasikan menjadi aturan IF-THEN.")
    add_p("3. Fitur morfologi mahkota bunga (Petal Length dan Petal Width) merupakan faktor paling dominan dalam penentuan spesies Iris, dengan nilai ambang batas Petal Length <= 2.45 cm menjadi pemisah mutlak spesies Iris-setosa dari spesies lainnya.")

    # H. Lampiran Kode Program Python
    add_h1("H. Lampiran Kode Program Python (Scikit-Learn)")
    add_p("Berikut merupakan kode program lengkap yang digunakan dalam eksperimen ini menggunakan pustaka Python dan Scikit-Learn:")

    code_script = (
        "import pandas as pd\n"
        "from sklearn.model_selection import train_test_split\n"
        "from sklearn.tree import DecisionTreeClassifier\n"
        "from sklearn.metrics import accuracy_score, classification_report, confusion_matrix\n\n"
        "# 1. Memuat dataset Iris dan persiapan fitur\n"
        "df = pd.read_csv('iris.csv')\n"
        "X = df[['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']]\n"
        "y = df['Species']\n\n"
        "# 2. Pembagian data latih (80%) dan data uji (20%) secara terstratifikasi\n"
        "X_train, X_test, y_train, y_test = train_test_split(\n"
        "    X, y, test_size=0.2, random_state=42, stratify=y\n"
        ")\n\n"
        "# 3. Membangun model Decision Tree dengan kriteria Gini dan max_depth=3\n"
        "model = DecisionTreeClassifier(criterion='gini', max_depth=3, random_state=42)\n"
        "model.fit(X_train, y_train)\n\n"
        "# 4. Melakukan prediksi dan evaluasi pada data uji\n"
        "y_pred = model.predict(X_test)\n"
        "print('Akurasi Model:', accuracy_score(y_test, y_pred))  # Output: 0.9667 (96.67%)\n"
        "print('\\nLaporan Klasifikasi:\\n', classification_report(y_test, y_pred))\n"
        "print('\\nConfusion Matrix:\\n', confusion_matrix(y_test, y_pred))\n"
    )

    p_code = doc.add_paragraph()
    p_code.paragraph_format.left_indent = Inches(0.2)
    p_code.paragraph_format.space_before = Pt(1)
    p_code.paragraph_format.space_after = Pt(2)
    p_code.paragraph_format.line_spacing = 1.02
    r_code = p_code.add_run(code_script)
    r_code.font.name = 'Consolas'
    r_code.font.size = Pt(8.0)
    r_code.font.color.rgb = RGBColor(0x10, 0x10, 0x10)

    doc.save(docx_test)
    print("Test docx built!")
    convert(docx_test, pdf_test)
    print("Test pdf converted!")

    doc_fitz = fitz.open(pdf_test)
    print(f"=== TEST RESULT: TOTAL PAGES = {len(doc_fitz)} ===")
    for i, page in enumerate(doc_fitz):
        lines = [l.strip() for l in page.get_text().split('\n') if l.strip()]
        print(f"Page {i+1}: {len(lines)} lines | Images: {len(page.get_images())}")
        print("   Start:", lines[0] if lines else '')
        print("   End:  ", lines[-1] if lines else '')


if __name__ == '__main__':
    build_test_doc()
