# pip install python-barcode
# pip install pillow
# pip install qrcode[pil]

# generator_coduri_bare.py
import barcode
from barcode.writer import ImageWriter
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

class GeneratorCoduriDeBare:
    """
    Generator automat de coduri de bare pentru bibliotecă
    """

    def __init__(self, folder_output="coduri_generate"):
        """
        Inițializare generator

        Args:
            folder_output: Folderul unde se salvează imaginile
        """
        self.folder_output = folder_output

        # Creează folderul dacă nu există
        if not os.path.exists(folder_output):
            os.makedirs(folder_output)

    def genereaza_code128(self, cod_text, nume_fisier=None):
        """
        Generează cod de bare CODE128 (1D)

        Args:
            cod_text: Textul codului (ex: "BOOK001")
            nume_fisier: Numele fișierului de salvat (opțional)

        Returns:
            Calea către fișierul generat
        """
        if nume_fisier is None:
            nume_fisier = f"{cod_text}_code128"

        # Generează codul de bare
        CODE128 = barcode.get_barcode_class('code128')
        cod_bare = CODE128(cod_text, writer=ImageWriter())

        # Salvează imaginea
        cale_completa = os.path.join(self.folder_output, nume_fisier)
        cod_bare.save(cale_completa, options={
            'module_width': 0.3,      # Lățime bare
            'module_height': 15,      # Înălțime bare
            'quiet_zone': 2,          # Margini
            'font_size': 12,          # Mărime text
            'text_distance': 3,       # Distanță text-cod
            'write_text': True        # Afișează textul sub cod
        })

        return f"{cale_completa}.png"

    def genereaza_qr_code(self, cod_text, nume_fisier=None):
        """
        Generează QR Code (2D)

        Args:
            cod_text: Textul codului (ex: "BOOK001")
            nume_fisier: Numele fișierului de salvat (opțional)

        Returns:
            Calea către fișierul generat
        """
        if nume_fisier is None:
            nume_fisier = f"{cod_text}_qr.png"

        # Generează QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(cod_text)
        qr.make(fit=True)

        # Creează imaginea
        img = qr.make_image(fill_color="black", back_color="white")

        # Salvează
        cale_completa = os.path.join(self.folder_output, nume_fisier)
        img.save(cale_completa)

        return cale_completa

    def genereaza_batch_carti(self, prefix="BOOK", start=1, count=100):
        """
        Generează coduri de bare în batch pentru cărți

        Args:
            prefix: Prefixul codului (BOOK, USER, etc.)
            start: Numărul de început
            count: Câte coduri să genereze

        Returns:
            Listă cu căile fișierelor generate
        """
        fisiere_generate = []

        print(f"🚀 Generez {count} coduri de bare...")

        for i in range(start, start + count):
            # Generează codul (cu padding: BOOK0001, BOOK0002, etc.)
            cod = f"{prefix}{i:04d}"

            # Generează CODE128 (1D)
            fisier_code128 = self.genereaza_code128(cod)
            fisiere_generate.append(fisier_code128)

            # Progress bar simplu
            if i % 10 == 0:
                print(f"  ✓ Generat {i - start + 1}/{count} coduri...")

        print(f"✅ Gata! {count} coduri generate în {self.folder_output}/")
        return fisiere_generate

    def genereaza_eticheta_completa(self, cod_text, titlu_carte=None, autor=None):
        """
        Generează etichetă completă: cod de bare + text

        Args:
            cod_text: Codul de bare (ex: "BOOK001")
            titlu_carte: Titlul cărții (opțional)
            autor: Autorul (opțional)

        Returns:
            Calea către fișierul generat
        """
        # Generează cod de bare temporar
        temp_barcode = f"temp_{cod_text}"
        self.genereaza_code128(cod_text, temp_barcode)

        # Încarcă imaginea codului de bare
        img_barcode = Image.open(f"{self.folder_output}/{temp_barcode}.png")

        # Creează o imagine mai mare pentru etichetă
        latime_eticheta = 600
        inaltime_eticheta = 200 if (titlu_carte or autor) else 120

        eticheta = Image.new('RGB', (latime_eticheta, inaltime_eticheta), 'white')
        draw = ImageDraw.Draw(eticheta)

        # Încarcă font (sau folosește default)
        try:
            font_titlu = ImageFont.truetype("arial.ttf", 16)
            font_normal = ImageFont.truetype("arial.ttf", 12)
        except:
            font_titlu = ImageFont.load_default()
            font_normal = ImageFont.load_default()

        # Poziționează codul de bare
        pozitie_y = 20

        # Adaugă titlu și autor dacă există
        if titlu_carte:
            # Titlu carte (trunchiat dacă e prea lung)
            titlu_scurt = titlu_carte[:50] + "..." if len(titlu_carte) > 50 else titlu_carte
            draw.text((20, pozitie_y), titlu_scurt, fill='black', font=font_titlu)
            pozitie_y += 30

        if autor:
            autor_scurt = autor[:40] + "..." if len(autor) > 40 else autor
            draw.text((20, pozitie_y), f"de {autor_scurt}", fill='gray', font=font_normal)
            pozitie_y += 25

        # Centrează codul de bare
        img_barcode_redim = img_barcode.resize((400, 80))
        pozitie_x = (latime_eticheta - 400) // 2
        eticheta.paste(img_barcode_redim, (pozitie_x, pozitie_y))

        # Salvează
        nume_fisier = f"eticheta_{cod_text}.png"
        cale = os.path.join(self.folder_output, nume_fisier)
        eticheta.save(cale)

        # Șterge temporar
        os.remove(f"{self.folder_output}/{temp_barcode}.png")

        return cale


# ═══════════════════════════════════════════════════════
# EXEMPLU DE UTILIZARE
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    # Creează generator
    generator = GeneratorCoduriDeBare(folder_output="coduri_biblioteca")

    # ──────────────────────────────────────────────────
    # Opțiunea 1: Generează un singur cod
    # ──────────────────────────────────────────────────
    print("📦 Generez cod single...")
    fisier1 = generator.genereaza_code128("BOOK001")
    print(f"✅ Generat: {fisier1}")

    # ──────────────────────────────────────────────────
    # Opțiunea 2: Generează 100 coduri automat
    # ──────────────────────────────────────────────────
    print("\n📦 Generez batch 100 coduri...")
    fisiere = generator.genereaza_batch_carti(
        prefix="BOOK",
        start=1,
        count=100
    )

    # ──────────────────────────────────────────────────
    # Opțiunea 3: Generează etichetă completă cu text
    # ──────────────────────────────────────────────────
    print("\n📦 Generez etichetă completă...")
    eticheta = generator.genereaza_eticheta_completa(
        cod_text="BOOK001",
        titlu_carte="Amintiri din copilărie",
        autor="Ion Creangă"
    )
    print(f"✅ Eticheta: {eticheta}")

    # ──────────────────────────────────────────────────
    # Opțiunea 4: Generează și QR codes
    # ──────────────────────────────────────────────────
    print("\n📦 Generez QR code...")
    qr = generator.genereaza_qr_code("BOOK001")
    print(f"✅ QR: {qr}")

    print("\n🎉 Gata! Toate codurile sunt în folderul 'coduri_biblioteca/'")