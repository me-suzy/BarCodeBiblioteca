# generator_utilizatori_complete.py
import barcode
from barcode.writer import ImageWriter
import qrcode
from PIL import Image
import sqlite3
import os
from datetime import datetime

# ═══════════════════════════════════════════════════════
# PARTEA 1: Generator Coduri de Bare
# ═══════════════════════════════════════════════════════

class GeneratorCoduriDeBare:
    """Generator automat de coduri de bare"""

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


# ═══════════════════════════════════════════════════════
# PARTEA 2: Generator Coduri Utilizatori + Bază de Date
# ═══════════════════════════════════════════════════════

class GeneratorCoduriUtilizatori:
    """Generator specializat pentru coduri utilizatori cu bază de date"""

    def __init__(self, db_path="coduri_biblioteca.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.generator = GeneratorCoduriDeBare(folder_output="coduri_utilizatori")

        # Creează tabel dacă nu există
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS coduri_utilizatori (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cod TEXT UNIQUE NOT NULL,
                tip TEXT DEFAULT 'USER',
                status TEXT DEFAULT 'liber',
                data_generare TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                folosit_pentru TEXT,
                utilizator_nume TEXT,
                utilizator_email TEXT,
                data_atribuire TIMESTAMP,
                observatii TEXT
            )
        ''')
        self.conn.commit()

    def genereaza_coduri_utilizatori(self, prefix="USER", start=1, count=1000):
        """Generează coduri pentru utilizatori (carnete)"""
        rezultate = {
            'generate_ok': 0,
            'duplicate': 0,
            'erori': 0,
            'coduri_noi': []
        }

        print(f"\n{'='*60}")
        print(f"🎫 Generez {count} coduri utilizatori cu prefix '{prefix}'")
        print(f"{'='*60}\n")

        for i in range(start, start + count):
            cod = f"{prefix}{i:05d}"  # USER00001, USER00002, etc.

            try:
                # Verifică duplicat
                exista = self.cursor.execute(
                    "SELECT cod FROM coduri_utilizatori WHERE cod = ?",
                    (cod,)
                ).fetchone()

                if exista:
                    rezultate['duplicate'] += 1
                    continue

                # Inserează în baza de date
                self.cursor.execute('''
                    INSERT INTO coduri_utilizatori (cod, tip, status)
                    VALUES (?, ?, 'liber')
                ''', (cod, prefix))

                # Generează imagine cod de bare
                barcode_path = self.generator.genereaza_code128(cod)

                if barcode_path:
                    rezultate['generate_ok'] += 1
                    rezultate['coduri_noi'].append(cod)
                else:
                    rezultate['erori'] += 1

                # Progress
                if (i - start + 1) % 100 == 0:
                    print(f"  ✓ Generat: {i - start + 1}/{count} coduri...")

            except Exception as e:
                print(f"  ❌ Eroare la {cod}: {e}")
                rezultate['erori'] += 1

        self.conn.commit()

        # Raport final
        print(f"\n{'='*60}")
        print(f"📊 RAPORT GENERARE")
        print(f"{'='*60}")
        print(f"✅ Generate cu succes: {rezultate['generate_ok']}")
        print(f"⚠️  Duplicate (sărite):  {rezultate['duplicate']}")
        print(f"❌ Erori:              {rezultate['erori']}")
        print(f"📁 Locație imagini:    {os.path.abspath('coduri_utilizatori')}")
        print(f"💾 Bază de date:       {os.path.abspath(self.db_path)}")
        print(f"{'='*60}\n")

        return rezultate

    def atribuie_utilizator(self, cod, nume, email=None, observatii=None):
        """Atribuie un cod unui utilizator"""
        try:
            self.cursor.execute('''
                UPDATE coduri_utilizatori
                SET status = 'atribuit',
                    utilizator_nume = ?,
                    utilizator_email = ?,
                    data_atribuire = CURRENT_TIMESTAMP,
                    observatii = ?
                WHERE cod = ? AND status = 'liber'
            ''', (nume, email, observatii, cod))

            self.conn.commit()

            if self.cursor.rowcount > 0:
                print(f"✅ Codul {cod} atribuit lui {nume}")
                return True
            else:
                print(f"❌ Codul {cod} nu există sau e deja atribuit!")
                return False

        except Exception as e:
            print(f"❌ Eroare: {e}")
            return False

    def elibereaza_cod(self, cod):
        """Eliberează un cod (îl face disponibil din nou)"""
        try:
            self.cursor.execute('''
                UPDATE coduri_utilizatori
                SET status = 'liber',
                    utilizator_nume = NULL,
                    utilizator_email = NULL,
                    data_atribuire = NULL,
                    observatii = NULL
                WHERE cod = ?
            ''', (cod,))

            self.conn.commit()
            print(f"✅ Codul {cod} a fost eliberat")
            return True

        except Exception as e:
            print(f"❌ Eroare: {e}")
            return False

    def vezi_statistici(self):
        """Afișează statistici despre coduri"""
        stats = {}

        # Total coduri
        total = self.cursor.execute(
            "SELECT COUNT(*) FROM coduri_utilizatori"
        ).fetchone()[0]

        # Libere
        libere = self.cursor.execute(
            "SELECT COUNT(*) FROM coduri_utilizatori WHERE status = 'liber'"
        ).fetchone()[0]

        # Atribuite
        atribuite = self.cursor.execute(
            "SELECT COUNT(*) FROM coduri_utilizatori WHERE status = 'atribuit'"
        ).fetchone()[0]

        print(f"\n{'='*60}")
        print(f"📊 STATISTICI CODURI UTILIZATORI")
        print(f"{'='*60}")
        print(f"📦 Total coduri:      {total}")
        print(f"✅ Libere:            {libere} ({libere*100//total if total > 0 else 0}%)")
        print(f"👤 Atribuite:         {atribuite} ({atribuite*100//total if total > 0 else 0}%)")
        print(f"{'='*60}\n")

        return {'total': total, 'libere': libere, 'atribuite': atribuite}

    def cauta_utilizator(self, nume_partial):
        """Caută utilizatori după nume"""
        rezultate = self.cursor.execute('''
            SELECT cod, utilizator_nume, utilizator_email, data_atribuire
            FROM coduri_utilizatori
            WHERE utilizator_nume LIKE ? AND status = 'atribuit'
        ''', (f'%{nume_partial}%',)).fetchall()

        if rezultate:
            print(f"\n🔍 Găsite {len(rezultate)} rezultate pentru '{nume_partial}':\n")
            for cod, nume, email, data in rezultate:
                print(f"  📇 {cod} - {nume} ({email or 'fără email'}) - {data}")
        else:
            print(f"\n❌ Nu s-au găsit utilizatori cu '{nume_partial}'")

        return rezultate

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()


# ═══════════════════════════════════════════════════════
# MENIU INTERACTIV
# ═══════════════════════════════════════════════════════

def meniu_principal():
    gen = GeneratorCoduriUtilizatori()

    while True:
        print(f"\n{'='*60}")
        print(f"🎫 GENERATOR CODURI UTILIZATORI - Sistem Bibliotecă")
        print(f"{'='*60}")
        print("1️⃣  Generează coduri noi (batch)")
        print("2️⃣  Atribuie cod unui utilizator")
        print("3️⃣  Eliberează cod")
        print("4️⃣  Vezi statistici")
        print("5️⃣  Caută utilizator")
        print("6️⃣  Ieșire")
        print(f"{'='*60}")

        alegere = input("\n👉 Alege opțiunea (1-6): ").strip()

        if alegere == "1":
            # Generează coduri
            try:
                count = int(input("Câte coduri vrei să generezi? (ex: 100): "))
                prefix = input("Prefix (apasă ENTER pentru 'USER'): ").strip() or "USER"

                # Verifică ultimul cod generat
                ultim = gen.cursor.execute(
                    "SELECT cod FROM coduri_utilizatori WHERE tip = ? ORDER BY id DESC LIMIT 1",
                    (prefix,)
                ).fetchone()

                if ultim:
                    # Extrage numărul din ultimul cod
                    try:
                        ultim_nr = int(ultim[0].replace(prefix, ''))
                        start = ultim_nr + 1
                    except:
                        start = 1
                else:
                    start = 1

                print(f"\n📍 Start de la: {prefix}{start:05d}")
                confirm = input("Continui? (da/nu): ").strip().lower()

                if confirm in ['da', 'yes', 'y']:
                    gen.genereaza_coduri_utilizatori(prefix=prefix, start=start, count=count)

            except ValueError:
                print("❌ Număr invalid!")

        elif alegere == "2":
            # Atribuie cod
            cod = input("Cod utilizator (ex: USER00001): ").strip().upper()
            nume = input("Nume utilizator: ").strip()
            email = input("Email (opțional): ").strip() or None
            obs = input("Observații (opțional): ").strip() or None

            gen.atribuie_utilizator(cod, nume, email, obs)

        elif alegere == "3":
            # Eliberează cod
            cod = input("Cod de eliberat (ex: USER00001): ").strip().upper()
            gen.elibereaza_cod(cod)

        elif alegere == "4":
            # Statistici
            gen.vezi_statistici()

        elif alegere == "5":
            # Caută
            nume = input("Caută utilizator (nume parțial): ").strip()
            gen.cauta_utilizator(nume)

        elif alegere == "6":
            print("\n👋 La revedere!")
            break

        else:
            print("❌ Opțiune invalidă!")


if __name__ == "__main__":
    try:
        # Verifică librării
        print("🔍 Verificare librării...")
        import barcode
        from barcode.writer import ImageWriter
        import qrcode
        print("✅ Toate librăriile sunt instalate!\n")

        meniu_principal()

    except ImportError as e:
        print(f"\n❌ EROARE: Lipsesc librării!")
        print(f"   {e}")
        print("\n💡 Instalează cu:")
        print("   pip install python-barcode pillow qrcode[pil]")
    except KeyboardInterrupt:
        print("\n\n👋 Întrerupt de utilizator!")
    except Exception as e:
        print(f"\n❌ EROARE: {e}")
        import traceback
        traceback.print_exc()