"""
Menghasilkan gambar tabel "berantakan" (messy) untuk Aktivitas 2 (kerja kelompok)
di pertemuan2.qmd — laporan konseling & survei kesejahteraan mahasiswa yang disusun
untuk dibaca manusia: ada baris judul gabungan, baris header seksi per minggu, baris
subtotal, dan beberapa variabel digabung dalam satu kolom (Nama+NIM, Prodi+Angkatan,
Tanggal+Jenis Layanan). Dipakai mahasiswa sebagai bahan latihan menata ulang jadi tidy.
Dijalankan dari slides/libs/ (output ditulis ke ./aktivitas2_tabel_berantakan.png).
Perlu Pillow dan font Calibri (C:/Windows/Fonts/).
"""

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "C:/Windows/Fonts/"
f_reg = lambda sz: ImageFont.truetype(FONT_DIR + "calibri.ttf", sz)
f_bold = lambda sz: ImageFont.truetype(FONT_DIR + "calibrib.ttf", sz)
f_ital = lambda sz: ImageFont.truetype(FONT_DIR + "calibrii.ttf", sz)

COLS = [
    ("No", 60),
    ("Nama Mahasiswa (NIM)", 300),
    ("Prodi / Angkatan", 210),
    ("Tanggal & Jenis Layanan", 300),
    ("Skor Kesejahteraan (1-5)", 160),
    ("Catatan Konselor", 470),
]
COL_X = []
x = 0
for _, w in COLS:
    COL_X.append(x)
    x += w
TABLE_W = x

ROW_H_TITLE = 56
ROW_H_SUB = 40
ROW_H_BLANK = 18
ROW_H_HEADER = 66
ROW_H_SECTION = 40
ROW_H_DATA = 40
ROW_H_SUBTOTAL = 40
ROW_H_TOTAL = 50

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
TITLE_BG = (20, 73, 127)       # #14497F, warna aksen dipakai di deck
TITLE_FG = (255, 255, 255)
SUB_BG = (223, 230, 240)
HEADER_BG = (220, 230, 241)
SECTION_BG = (255, 242, 204)   # kuning muda
SUBTOTAL_BG = (217, 217, 217)  # abu-abu
TOTAL_BG = (198, 224, 180)     # hijau muda
GRID = (150, 150, 150)

rows = []  # (kind, height, cells) ; cells: None -> merged full-width text, or list per column
rows.append(("title", ROW_H_TITLE, "LAPORAN KUNJUNGAN KONSELING & SURVEI KESEJAHTERAAN MAHASISWA"))
rows.append(("subtitle", ROW_H_SUB, "Unit Layanan Psikologi — Fakultas Psikologi Universitas Airlangga  |  Semester Gasal 2026/2027"))
rows.append(("blank", ROW_H_BLANK, ""))
rows.append(("header", ROW_H_HEADER, [c[0] for c in COLS]))

rows.append(("section", ROW_H_SECTION, "MINGGU KE-1 (1–7 September 2026)"))
rows.append(("data", ROW_H_DATA, ["1", "Anisa Rahma (2021012345)", "Psikologi / 2021",
                                   "2 Sep – Konseling Individu", "2.8",
                                   "Stres akademik tinggi, follow-up minggu depan"]))
rows.append(("data", ROW_H_DATA, ["2", "Budi Santoso (2022019876)", "Psikologi / 2022",
                                   "3 Sep – Konseling Individu", "3.5",
                                   "Adaptasi kuliah, kondisi membaik"]))
rows.append(("data", ROW_H_DATA, ["3", "Citra Dewi (2020045612)", "Manajemen / 2020",
                                   "5 Sep – Skrining PWB", "4.1",
                                   "Tidak perlu tindak lanjut"]))
rows.append(("subtotal", ROW_H_SUBTOTAL, "Rata-rata Minggu ke-1 (n=3): 3.47"))

rows.append(("section", ROW_H_SECTION, "MINGGU KE-2 (8–14 September 2026)"))
rows.append(("data", ROW_H_DATA, ["4", "Dimas Prakoso (2021078654)", "Psikologi / 2021",
                                   "9 Sep – Konseling Kelompok", "3.0",
                                   "Ikut sesi kelompok manajemen stres"]))
rows.append(("data", ROW_H_DATA, ["5", "Eka Putri (2023011223)", "Psikologi / 2023",
                                   "10 Sep – Skrining PWB", "2.5",
                                   "Dirujuk ke psikolog klinis"]))
rows.append(("subtotal", ROW_H_SUBTOTAL, "Rata-rata Minggu ke-2 (n=2): 2.75"))

rows.append(("section", ROW_H_SECTION, "MINGGU KE-3 (15–21 September 2026)"))
rows.append(("data", ROW_H_DATA, ["6", "Fajar Nugroho (2022033445)", "Teknik / 2022",
                                   "16 Sep – Konseling Individu", "3.8",
                                   "Kondisi stabil"]))
rows.append(("data", ROW_H_DATA, ["7", "Gita Lestari (2021056789)", "Psikologi / 2021",
                                   "18 Sep – Konseling Individu", "3.2",
                                   "Perlu follow-up 2 minggu lagi"]))
rows.append(("subtotal", ROW_H_SUBTOTAL, "Rata-rata Minggu ke-3 (n=2): 3.50"))

rows.append(("total", ROW_H_TOTAL, "TOTAL KESELURUHAN (n=7)  —  Rata-rata Skor Kesejahteraan = 3.28"))

TABLE_H = sum(r[1] for r in rows)
PAD = 24
IMG_W = TABLE_W + PAD * 2
IMG_H = TABLE_H + PAD * 2

img = Image.new("RGB", (IMG_W, IMG_H), WHITE)
d = ImageDraw.Draw(img)

def text_wrapped(draw, xy, text, font, max_width, fill, align_center=False, line_spacing=4):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    x0, y0 = xy
    lh = font.getbbox("Ag")[3] - font.getbbox("Ag")[1] + line_spacing
    total_h = lh * len(lines)
    y = y0 - total_h / 2 + lh / 2
    for line in lines:
        tw = draw.textlength(line, font=font)
        tx = x0 - tw / 2 if align_center else x0
        draw.text((tx, y - lh / 2 + line_spacing / 2), line, font=font, fill=fill)
        y += lh

y = PAD
for kind, h, cells in rows:
    x0, y0, x1, y1 = PAD, y, PAD + TABLE_W, y + h
    if kind == "title":
        d.rectangle([x0, y0, x1, y1], fill=TITLE_BG)
        text_wrapped(d, (x0 + TABLE_W / 2, y0 + h / 2), cells, f_bold(22), TABLE_W - 40, TITLE_FG, align_center=True)
    elif kind == "subtitle":
        d.rectangle([x0, y0, x1, y1], fill=SUB_BG)
        text_wrapped(d, (x0 + TABLE_W / 2, y0 + h / 2), cells, f_ital(15), TABLE_W - 40, BLACK, align_center=True)
    elif kind == "blank":
        d.rectangle([x0, y0, x1, y1], fill=WHITE)
    elif kind == "header":
        d.rectangle([x0, y0, x1, y1], fill=HEADER_BG)
        for (label, w), cx in zip(COLS, COL_X):
            cx0 = PAD + cx
            text_wrapped(d, (cx0 + w / 2, y0 + h / 2), label, f_bold(15), w - 14, BLACK, align_center=True)
            d.line([cx0, y0, cx0, y1], fill=GRID, width=1)
        d.line([x0, y1, x1, y1], fill=BLACK, width=2)
    elif kind == "section":
        d.rectangle([x0, y0, x1, y1], fill=SECTION_BG)
        d.text((x0 + 14, y0 + h / 2 - 9), cells, font=f_bold(16), fill=BLACK)
    elif kind == "data":
        d.rectangle([x0, y0, x1, y1], fill=WHITE)
        for val, (label, w), cx in zip(cells, COLS, COL_X):
            cx0 = PAD + cx
            align_c = label.startswith("No") or label.startswith("Skor")
            text_wrapped(d, (cx0 + (w / 2 if align_c else 12), y0 + h / 2), val, f_reg(14), w - 16, BLACK,
                         align_center=align_c)
            d.line([cx0, y0, cx0, y1], fill=GRID, width=1)
    elif kind == "subtotal":
        d.rectangle([x0, y0, x1, y1], fill=SUBTOTAL_BG)
        d.text((x0 + TABLE_W - 14 - d.textlength(cells, font=f_bold(15)), y0 + h / 2 - 9),
                cells, font=f_bold(15), fill=BLACK)
    elif kind == "total":
        d.rectangle([x0, y0, x1, y1], fill=TOTAL_BG)
        text_wrapped(d, (x0 + TABLE_W / 2, y0 + h / 2), cells, f_bold(17), TABLE_W - 40, BLACK, align_center=True)

    d.line([x0, y0, x1, y0], fill=GRID, width=1)
    y += h

# garis luar tabel & garis bawah terakhir
d.rectangle([PAD, PAD, PAD + TABLE_W, PAD + TABLE_H], outline=BLACK, width=2)

out_path = "aktivitas2_tabel_berantakan.png"
img.save(out_path)
print("saved", out_path, img.size)
