# generator_masiv_biblioteca.py
from generator_coduri_bare import GeneratorCoduriDeBare
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import math

class GeneratorEtichetePDF:
    """
    Generează PDF-uri cu etichete pentru printare
    Format: 21 etichete per pagină A4 (3x7)
    """

    def __init__(self):
        self.generator = GeneratorCoduriDeBare()

        # Dimensiuni A4
        self.latime_pagina, self.inaltime_pagina = A4

        # Dimensiuni etichetă (în mm convertite în points)
        self.latime_eticheta = 70 * mm
        self.inaltime_eticheta = 37 * mm

        # Grid
        self.etichete_pe_rand = 3
        self.etichete_pe_coloana = 7
        self.etichete_per_pagina = self.etichete_pe_rand * self.etichete_pe_coloana

    def genereaza_pdf_etichete(self, prefix="BOOK", start=1, count=100,
                                nume_pdf="etichete_biblioteca.pdf"):
        """
        Generează PDF cu toate etichetele pentru printare

        Args:
            prefix: Prefix coduri (BOOK, USER, etc.)
            start: Număr început
            count: Câte etichete
            nume_pdf: Numele fișierului PDF
        """
        c = canvas.Canvas(nume_pdf, pagesize=A4)

        numar_pagini = math.ceil(count / self.etichete_per_pagina)
        print(f"📄 Generez {numar_pagini} pagini cu {count} etichete...")

        index_eticheta = 0

        for i in range(start, start + count):
            cod = f"{prefix}{i:04d}"

            # Calculează poziția pe pagină
            pagina = index_eticheta // self.etichete_per_pagina
            pozitie_pe_pagina = index_eticheta % self.etichete_per_pagina

            rand = pozitie_pe_pagina // self.etichete_pe_rand
            coloana = pozitie_pe_pagina % self.etichete_pe_rand

            # Calculează coordonate
            x = 10 * mm + coloana * self.latime_eticheta
            y = self.inaltime_pagina - (10 * mm + (rand + 1) * self.inaltime_eticheta)

            # Desenează chenar etichetă (pentru ghidare la decupare)
            c.setStrokeColorRGB(0.8, 0.8, 0.8)
            c.rect(x, y, self.latime_eticheta, self.inaltime_eticheta)

            # Adaugă textul codului
            c.setFont("Helvetica-Bold", 12)
            c.drawString(x + 5*mm, y + self.inaltime_eticheta - 10*mm, cod)

            # Generează și adaugă codul de bare (imaginar - în realitate trebuie să generezi imaginea)
            # Aici ar trebui să generezi imaginea cu barcode și să o inserezi
            # Pentru simplificare, scriem doar textul
            c.setFont("Helvetica", 8)
            c.drawString(x + 5*mm, y + 5*mm, f"||||| {cod} |||||")

            index_eticheta += 1

            # Pagină nouă după fiecare 21 etichete
            if index_eticheta % self.etichete_per_pagina == 0 and i < start + count - 1:
                c.showPage()
                print(f"  ✓ Pagina {pagina + 1}/{numar_pagini} completă")

        c.save()
        print(f"✅ PDF generat: {nume_pdf}")
        return nume_pdf


# ═══════════════════════════════════════════════════════
# EXEMPLU UTILIZARE - Generare 10,000 coduri
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🏛️ Generator Masiv de Coduri pentru Bibliotecă\n")

    # Opțiunea 1: Generează primele 100 de coduri (TEST)
    print("📦 TESTE - Generez primele 100 coduri...")
    gen = GeneratorCoduriDeBare(folder_output="test_coduri")
    gen.genereaza_batch_carti(prefix="BOOK", start=1, count=100)

    # Opțiunea 2: Generează TOATE cele 10,000 (PRODUCȚIE)
    input("\n⚠️  Apasă ENTER pentru a genera TOATE cele 10,000 de coduri (va dura ~5 minute)...")

    print("\n🚀 START Generare 10,000 coduri...")
    gen_prod = GeneratorCoduriDeBare(folder_output="biblioteca_10k")

    # Generează în batch-uri de 1000 pentru progres
    for batch in range(10):
        start_batch = batch * 1000 + 1
        print(f"\n📦 Batch {batch + 1}/10 (coduri {start_batch}-{start_batch + 999})")
        gen_prod.genereaza_batch_carti(
            prefix="BOOK",
            start=start_batch,
            count=1000
        )

    print("\n" + "="*50)
    print("🎉 FINALIZAT! 10,000 de coduri generate!")
    print("📁 Locație: biblioteca_10k/")
    print("="*50)

    # Opțiunea 3: Generează PDF pentru printare
    input("\n📄 Apasă ENTER pentru a genera PDF-uri pentru printare...")

    gen_pdf = GeneratorEtichetePDF()
    gen_pdf.genereaza_pdf_etichete(
        prefix="BOOK",
        start=1,
        count=10000,
        nume_pdf="etichete_biblioteca_complete.pdf"
    )

    print("\n✅ PDF gata de printat!")
