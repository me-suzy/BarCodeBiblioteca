'''
Da, exact! Iată ce face fiecare opțiune:

## 📋 Explicație Meniu:

**1️⃣ Test - Generează 100 coduri**
- Creează folder `test_100_coduri/`
- Generează 100 de imagini cu coduri de bare: BOOK0001 până la BOOK0100
- Perfect pentru a testa că totul funcționează
- Durată: ~10-20 secunde

**2️⃣ Producție - Generează 10,000 coduri**
- Creează folder `biblioteca_10k/`
- Generează 10,000 de imagini: BOOK0001 până la BOOK10000
- Se face în 10 batch-uri câte 1000
- Durată: ~5-10 minute
- ⚠️ Ocupă ~500 MB spațiu pe disc

**3️⃣ Generează PDF pentru printare**
- Creează un PDF gata de printat
- Format: 21 etichete per pagină A4 (grid 3×7)
- Tu alegi câte etichete vrei (ex: 100, 500, 10000)
- Fiecare etichetă are codul de bare desenat în ea
- Perfect pentru printare și lipire pe cărți

**4️⃣ Ieșire**
- Închide aplicația

---

## 🎯 Recomandare pas cu pas:

**Pas 1:** Alege opțiunea **1** pentru test (vezi că funcționează)

**Pas 2:** După ce vezi că merge, alege opțiunea **3** și generează PDF cu 21 de etichete (o pagină de test)

**Pas 3:** Dacă totul e OK, rulează din nou și alege opțiunea **2** pentru toate cele 10,000

---

## ✅ Verificare rapidă:

Ai instalat toate librăriile?
```bash
pip install python-barcode pillow qrcode[pil] reportlab
```

Rulează aplicația:
```bash
python biblioteca_complete.py
```

**Ce opțiune vrei să testezi prima?** (recomand opțiunea 1 pentru început)
'''



# biblioteca_complete.py - TOT în unul
import barcode
from barcode.writer import ImageWriter
import qrcode
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os
import math

# ═══════════════════════════════════════════════════════
# PARTEA 1: Generator Coduri de Bare
# ═══════════════════════════════════════════════════════

class GeneratorCoduriDeBare:
    """Generator automat de coduri de bare pentru bibliotecă"""

    def __init__(self, folder_output="coduri_generate"):
        self.folder_output = folder_output
        if not os.path.exists(folder_output):
            os.makedirs(folder_output)

    def genereaza_code128(self, cod_text, nume_fisier=None):
        """Generează cod de bare CODE128 (1D)"""
        if nume_fisier is None:
            nume_fisier = f"{cod_text}_code128"

        try:
            CODE128 = barcode.get_barcode_class('code128')
            cod_bare = CODE128(cod_text, writer=ImageWriter())

            cale_completa = os.path.join(self.folder_output, nume_fisier)

            options = {
                'module_width': 0.3,
                'module_height': 15,
                'quiet_zone': 2,
                'font_size': 12,
                'text_distance': 3,
                'write_text': True
            }

            saved_path = cod_bare.save(cale_completa, options=options)
            return saved_path

        except Exception as e:
            print(f"❌ Eroare CODE128: {e}")
            return None

    def genereaza_qr_code(self, cod_text, nume_fisier=None):
        """Generează QR Code (2D)"""
        if nume_fisier is None:
            nume_fisier = f"{cod_text}_qr.png"

        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=2,
            )
            qr.add_data(cod_text)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            cale_completa = os.path.join(self.folder_output, nume_fisier)
            img.save(cale_completa)
            return cale_completa

        except Exception as e:
            print(f"❌ Eroare QR: {e}")
            return None

    def genereaza_batch_carti(self, prefix="BOOK", start=1, count=100):
        """Generează coduri în batch"""
        fisiere_generate = []
        print(f"🚀 Generez {count} coduri de bare...")

        for i in range(start, start + count):
            cod = f"{prefix}{i:04d}"
            fisier = self.genereaza_code128(cod)
            if fisier:
                fisiere_generate.append(fisier)

            if (i - start + 1) % 100 == 0:
                print(f"  ✓ {i - start + 1}/{count} coduri...")

        print(f"✅ {len(fisiere_generate)} coduri în {self.folder_output}/")
        return fisiere_generate


# ═══════════════════════════════════════════════════════
# PARTEA 2: Generator PDF cu Etichete
# ═══════════════════════════════════════════════════════

class GeneratorEtichetePDF:
    """Generează PDF-uri cu etichete pentru printare (21 per pagină A4)"""

    def __init__(self):
        self.generator = GeneratorCoduriDeBare(folder_output="temp_barcode")

        # Dimensiuni
        self.latime_pagina, self.inaltime_pagina = A4
        self.latime_eticheta = 70 * mm
        self.inaltime_eticheta = 37 * mm

        # Grid 3x7 = 21 etichete
        self.etichete_pe_rand = 3
        self.etichete_pe_coloana = 7
        self.etichete_per_pagina = 21

    def genereaza_pdf_etichete(self, prefix="BOOK", start=1, count=100,
                                nume_pdf="etichete_biblioteca.pdf"):
        """Generează PDF cu etichete"""
        c = canvas.Canvas(nume_pdf, pagesize=A4)
        numar_pagini = math.ceil(count / self.etichete_per_pagina)

        print(f"📄 Generez PDF: {numar_pagini} pagini, {count} etichete...")

        for i in range(start, start + count):
            cod = f"{prefix}{i:04d}"
            index = i - start

            # Calculează poziția
            pozitie_pe_pagina = index % self.etichete_per_pagina
            rand = pozitie_pe_pagina // self.etichete_pe_rand
            coloana = pozitie_pe_pagina % self.etichete_pe_rand

            x = 10*mm + coloana * self.latime_eticheta
            y = self.inaltime_pagina - (10*mm + (rand + 1) * self.inaltime_eticheta)

            # Chenar
            c.setStrokeColorRGB(0.8, 0.8, 0.8)
            c.setLineWidth(0.5)
            c.rect(x, y, self.latime_eticheta, self.inaltime_eticheta)

            # Text cod
            c.setFont("Helvetica-Bold", 11)
            c.drawString(x + 5*mm, y + self.inaltime_eticheta - 8*mm, cod)

            # Generează barcode real și inserează
            barcode_path = self.generator.genereaza_code128(cod, f"temp_{cod}")
            if barcode_path and os.path.exists(barcode_path):
                try:
                    # Inserează imaginea barcode
                    c.drawImage(
                        barcode_path,
                        x + 3*mm,
                        y + 8*mm,
                        width=64*mm,
                        height=20*mm,
                        preserveAspectRatio=True,
                        mask='auto'
                    )
                except Exception as e:
                    # Fallback: text simplu
                    c.setFont("Courier", 8)
                    c.drawString(x + 5*mm, y + 5*mm, f"||||| {cod} |||||")

            # Pagină nouă la fiecare 21 etichete
            if (index + 1) % self.etichete_per_pagina == 0 and i < start + count - 1:
                c.showPage()
                print(f"  ✓ Pagina {(index + 1) // self.etichete_per_pagina}/{numar_pagini}")

        c.save()

        # Curăță fișierele temporare
        import shutil
        if os.path.exists("temp_barcode"):
            shutil.rmtree("temp_barcode")

        print(f"✅ PDF: {nume_pdf}")
        return nume_pdf


# ═══════════════════════════════════════════════════════
# MENIU PRINCIPAL
# ═══════════════════════════════════════════════════════

def meniu_principal():
    print("="*60)
    print("🏛️  GENERATOR MASIV CODURI BIBLIOTECĂ")
    print("="*60)
    print("\n1️⃣  Test - Generează 100 coduri")
    print("2️⃣  Producție - Generează 10,000 coduri")
    print("3️⃣  Generează PDF pentru printare (21 etichete/pagină)")
    print("4️⃣  Ieșire")
    print("="*60)

    alegere = input("\nAlege opțiunea (1-4): ").strip()

    if alegere == "1":
        # Test 100 coduri
        print("\n📦 Generez 100 coduri de test...")
        gen = GeneratorCoduriDeBare(folder_output="test_100_coduri")
        gen.genereaza_batch_carti(prefix="BOOK", start=1, count=100)
        print(f"\n✅ Codurile sunt în: {os.path.abspath('test_100_coduri')}")

    elif alegere == "2":
        # Producție 10,000
        confirm = input("\n⚠️  Generez 10,000 coduri (durează ~5 min). Continui? (da/nu): ")
        if confirm.lower() in ['da', 'yes', 'y']:
            print("\n🚀 START generare 10,000 coduri...\n")
            gen = GeneratorCoduriDeBare(folder_output="biblioteca_10k")

            for batch in range(10):
                start_batch = batch * 1000 + 1
                print(f"📦 Batch {batch + 1}/10")
                gen.genereaza_batch_carti(
                    prefix="BOOK",
                    start=start_batch,
                    count=1000
                )

            print(f"\n✅ 10,000 coduri în: {os.path.abspath('biblioteca_10k')}")

    elif alegere == "3":
        # PDF
        count = int(input("\nCâte etichete vrei în PDF? (ex: 100): "))
        print(f"\n📄 Generez PDF cu {count} etichete...")

        gen_pdf = GeneratorEtichetePDF()
        pdf_path = gen_pdf.genereaza_pdf_etichete(
            prefix="BOOK",
            start=1,
            count=count,
            nume_pdf=f"etichete_{count}.pdf"
        )

        print(f"\n✅ PDF: {os.path.abspath(pdf_path)}")

    elif alegere == "4":
        print("\n👋 La revedere!")
        return

    else:
        print("\n❌ Opțiune invalidă!")

    # Reafișează meniul
    input("\n[Apasă ENTER pentru meniu]")
    meniu_principal()


if __name__ == "__main__":
    try:
        meniu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Întrerupt de utilizator. La revedere!")
    except Exception as e:
        print(f"\n❌ EROARE: {e}")
        import traceback
        traceback.print_exc()