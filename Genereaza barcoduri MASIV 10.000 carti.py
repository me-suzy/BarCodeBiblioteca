# generator_inteligent_biblioteca.py
import sqlite3
import barcode
from barcode.writer import ImageWriter
from datetime import datetime
import os
import json

class GestiuneCoduriInteligenta:
    """
    Sistem complet de gestionare coduri cu protecție duplicate
    """

    def __init__(self, db_path="coduri_biblioteca.db"):
        """
        Inițializare cu bază de date SQLite pentru tracking
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        # Creează tabelele
        self._creaza_tabele()

        print(f"✅ Conectat la: {db_path}")
        self._afiseaza_statistici()

    def _creaza_tabele(self):
        """
        Creează structura bazei de date
        """
        # Tabel pentru coduri generate
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS coduri_generate (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cod TEXT UNIQUE NOT NULL,
                tip TEXT NOT NULL,
                data_generare TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'liber',
                folosit_pentru TEXT,
                observatii TEXT
            )
        ''')

        # Tabel pentru scanări (log)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS log_scanari (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cod TEXT NOT NULL,
                actiune TEXT NOT NULL,
                data_scanare TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                rezultat TEXT,
                detalii TEXT
            )
        ''')

        # Tabel pentru asocieri cărți
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS asocieri_carti (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cod_bare TEXT UNIQUE NOT NULL,
                titlu TEXT,
                autor TEXT,
                isbn TEXT,
                aleph_doc_number TEXT,
                data_asociere TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cod_bare) REFERENCES coduri_generate(cod)
            )
        ''')

        self.conn.commit()

    def _afiseaza_statistici(self):
        """
        Afișează statistici despre coduri
        """
        total = self.cursor.execute(
            "SELECT COUNT(*) FROM coduri_generate"
        ).fetchone()[0]

        folosite = self.cursor.execute(
            "SELECT COUNT(*) FROM coduri_generate WHERE status = 'folosit'"
        ).fetchone()[0]

        libere = total - folosite

        print(f"\n📊 STATISTICI:")
        print(f"   Total coduri: {total}")
        print(f"   Folosite: {folosite}")
        print(f"   Libere: {libere}")

    def genereaza_coduri_batch(self, prefix="BOOK", start=1, count=1000):
        """
        Generează coduri în batch cu verificare duplicate

        Args:
            prefix: Prefix (BOOK, USER, etc.)
            start: Număr început
            count: Câte să genereze

        Returns:
            Dict cu rezultate și statistici
        """
        rezultate = {
            'generate_ok': 0,
            'duplicate_detectate': 0,
            'erori': 0,
            'coduri_noi': []
        }

        print(f"\n🚀 Generez {count} coduri cu prefix '{prefix}'...")

        for i in range(start, start + count):
            # Generează codul (4 cifre cu padding)
            cod = f"{prefix}{i:05d}"  # 5 cifre pentru 50k+ cărți

            try:
                # Verifică dacă există deja
                exista = self.cursor.execute(
                    "SELECT cod FROM coduri_generate WHERE cod = ?",
                    (cod,)
                ).fetchone()

                if exista:
                    print(f"  ⚠️  DUPLICAT detectat: {cod} - SĂRIT!")
                    rezultate['duplicate_detectate'] += 1

                    # Log duplicat
                    self.cursor.execute('''
                        INSERT INTO log_scanari (cod, actiune, rezultat, detalii)
                        VALUES (?, 'generare', 'duplicat', 'Cod deja existent în sistem')
                    ''', (cod,))

                    continue

                # Inserează cod nou
                self.cursor.execute('''
                    INSERT INTO coduri_generate (cod, tip, status)
                    VALUES (?, ?, 'liber')
                ''', (cod, prefix))

                rezultate['generate_ok'] += 1
                rezultate['coduri_noi'].append(cod)

                # Generează imaginea codului de bare
                self._genereaza_imagine_cod(cod)

                # Progress
                if i % 100 == 0:
                    print(f"  ✓ {i - start + 1}/{count} coduri procesate...")

            except Exception as e:
                print(f"  ❌ Eroare la {cod}: {str(e)}")
                rezultate['erori'] += 1

        self.conn.commit()

        # Afișează raport
        print(f"\n{'='*50}")
        print(f"📊 RAPORT GENERARE:")
        print(f"   ✅ Generate OK: {rezultate['generate_ok']}")
        print(f"   ⚠️  Duplicate detectate: {rezultate['duplicate_detectate']}")
        print(f"   ❌ Erori: {rezultate['erori']}")
        print(f"{'='*50}\n")

        return rezultate

    def _genereaza_imagine_cod(self, cod):
        """
        Generează imaginea codului de bare
        """
        folder = "coduri_imagine"
        if not os.path.exists(folder):
            os.makedirs(folder)

        CODE128 = barcode.get_barcode_class('code128')
        cod_bare = CODE128(cod, writer=ImageWriter())

        cale = os.path.join(folder, cod)
        cod_bare.save(cale, options={
            'module_width': 0.3,
            'module_height': 15,
            'quiet_zone': 2,
            'font_size': 12,
            'text_distance': 3,
            'write_text': True
        })

    def verifica_cod_la_scanare(self, cod_scanat):
        """
        Verifică codul când e scanat

        Returns:
            Dict cu status și informații
        """
        # Verifică dacă există în sistem
        rezultat = self.cursor.execute('''
            SELECT cod, status, folosit_pentru, data_generare
            FROM coduri_generate
            WHERE cod = ?
        ''', (cod_scanat,)).fetchone()

        if not rezultat:
            # Cod inexistent
            response = {
                'valid': False,
                'status': 'inexistent',
                'mesaj': f'⛔ COD NECUNOSCUT: {cod_scanat}',
                'alerta': 'EROARE',
                'culoare': 'rosu'
            }

            # Log
            self.cursor.execute('''
                INSERT INTO log_scanari (cod, actiune, rezultat, detalii)
                VALUES (?, 'scanare', 'inexistent', 'Cod nu există în sistem')
            ''', (cod_scanat,))
            self.conn.commit()

            return response

        cod, status, folosit_pentru, data_generare = rezultat

        if status == 'folosit':
            # Cod deja folosit - DUPLICAT!

            # Găsește detalii carte asociată
            carte = self.cursor.execute('''
                SELECT titlu, autor, data_asociere
                FROM asocieri_carti
                WHERE cod_bare = ?
            ''', (cod,)).fetchone()

            if carte:
                titlu, autor, data_asociere = carte
                detalii = f"Deja asociat cu: {titlu} de {autor}"
            else:
                detalii = f"Folosit pentru: {folosit_pentru}"

            response = {
                'valid': False,
                'status': 'duplicat',
                'mesaj': f'⚠️  COD DUPLICAT: {cod}',
                'detalii': detalii,
                'alerta': 'DUPLICAT',
                'culoare': 'portocaliu',
                'folosit_pentru': folosit_pentru,
                'data_folosire': data_asociere if carte else data_generare
            }

            # Log duplicat
            self.cursor.execute('''
                INSERT INTO log_scanari (cod, actiune, rezultat, detalii)
                VALUES (?, 'scanare', 'duplicat', ?)
            ''', (cod, detalii))
            self.conn.commit()

            return response

        # Cod valid și liber
        response = {
            'valid': True,
            'status': 'liber',
            'mesaj': f'✅ COD VALID: {cod}',
            'detalii': 'Cod liber, poate fi folosit',
            'alerta': 'OK',
            'culoare': 'verde'
        }

        # Log scanare OK
        self.cursor.execute('''
            INSERT INTO log_scanari (cod, actiune, rezultat, detalii)
            VALUES (?, 'scanare', 'ok', 'Cod valid și disponibil')
        ''', (cod,))
        self.conn.commit()

        return response

    def asociaza_cod_cu_carte(self, cod_bare, titlu, autor=None, isbn=None,
                              aleph_doc=None):
        """
        Asociază un cod de bare cu o carte

        Returns:
            Bool success
        """
        try:
            # Verifică cod disponibil
            verificare = self.verifica_cod_la_scanare(cod_bare)

            if not verificare['valid']:
                print(f"❌ Nu pot asocia: {verificare['mesaj']}")
                return False

            # Marchează codul ca folosit
            self.cursor.execute('''
                UPDATE coduri_generate
                SET status = 'folosit',
                    folosit_pentru = ?
                WHERE cod = ?
            ''', (titlu, cod_bare))

            # Creează asocierea
            self.cursor.execute('''
                INSERT INTO asocieri_carti
                (cod_bare, titlu, autor, isbn, aleph_doc_number)
                VALUES (?, ?, ?, ?, ?)
            ''', (cod_bare, titlu, autor, isbn, aleph_doc))

            self.conn.commit()

            print(f"✅ Asociere reușită: {cod_bare} → {titlu}")
            return True

        except Exception as e:
            print(f"❌ Eroare asociere: {str(e)}")
            return False

    def gaseste_coduri_libere(self, count=10):
        """
        Găsește coduri libere disponibile
        """
        rezultate = self.cursor.execute('''
            SELECT cod FROM coduri_generate
            WHERE status = 'liber'
            LIMIT ?
        ''', (count,)).fetchall()

        return [r[0] for r in rezultate]

    def raport_duplicate(self):
        """
        Generează raport despre toate duplicatele detectate
        """
        duplicate = self.cursor.execute('''
            SELECT cod, COUNT(*) as numar_aparitii
            FROM log_scanari
            WHERE rezultat = 'duplicat'
            GROUP BY cod
            ORDER BY numar_aparitii DESC
        ''').fetchall()

        print(f"\n🔍 RAPORT DUPLICATE:")
        print(f"{'='*60}")

        if not duplicate:
            print("   ✅ Nu există duplicate detectate!")
        else:
            print(f"   Coduri scanate de multiple ori:")
            for cod, numar in duplicate[:20]:  # Top 20
                print(f"   ⚠️  {cod}: {numar} încercări de scanare")

        print(f"{'='*60}\n")

        return duplicate

    def export_raport_json(self, nume_fisier="raport_coduri.json"):
        """
        Exportă raport complet în JSON
        """
        # Statistici generale
        total = self.cursor.execute(
            "SELECT COUNT(*) FROM coduri_generate"
        ).fetchone()[0]

        folosite = self.cursor.execute(
            "SELECT COUNT(*) FROM coduri_generate WHERE status = 'folosit'"
        ).fetchone()[0]

        # Duplicate
        duplicate = self.cursor.execute('''
            SELECT cod, COUNT(*) as aparitii
            FROM log_scanari
            WHERE rezultat = 'duplicat'
            GROUP BY cod
        ''').fetchall()

        # Asocieri recente
        asocieri = self.cursor.execute('''
            SELECT cod_bare, titlu, autor, data_asociere
            FROM asocieri_carti
            ORDER BY data_asociere DESC
            LIMIT 50
        ''').fetchall()

        raport = {
            'data_raport': datetime.now().isoformat(),
            'statistici': {
                'total_coduri': total,
                'folosite': folosite,
                'libere': total - folosite,
                'procent_utilizare': round((folosite / total * 100) if total > 0 else 0, 2)
            },
            'duplicate': [
                {'cod': cod, 'aparitii': count}
                for cod, count in duplicate
            ],
            'asocieri_recente': [
                {
                    'cod': cod,
                    'titlu': titlu,
                    'autor': autor,
                    'data': data
                }
                for cod, titlu, autor, data in asocieri
            ]
        }

        with open(nume_fisier, 'w', encoding='utf-8') as f:
            json.dump(raport, f, indent=2, ensure_ascii=False)

        print(f"📄 Raport exportat: {nume_fisier}")
        return raport

    def curata_sistem(self, confirmare=False):
        """
        Curăță sistemul (ATENȚIE: șterge tot!)
        """
        if not confirmare:
            print("⚠️  ATENȚIE: Această acțiune șterge TOATE datele!")
            print("   Pentru confirmare, rulează cu confirmare=True")
            return False

        self.cursor.execute("DELETE FROM log_scanari")
        self.cursor.execute("DELETE FROM asocieri_carti")
        self.cursor.execute("DELETE FROM coduri_generate")
        self.conn.commit()

        print("🗑️  Sistem curățat complet!")
        return True

    def __del__(self):
        """
        Închide conexiunea la destrucție
        """
        if hasattr(self, 'conn'):
            self.conn.close()


# ═══════════════════════════════════════════════════════
# EXEMPLU DE UTILIZARE
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    # Inițializare sistem
    sistem = GestiuneCoduriInteligenta()

    print("\n" + "="*60)
    print("🏛️  SISTEM GESTIUNE CODURI BIBLIOTECĂ - 50,000 cărți")
    print("="*60)

    # ──────────────────────────────────────────────────
    # TEST 1: Generează coduri
    # ──────────────────────────────────────────────────
    print("\n📦 TEST 1: Generare coduri...")
    rezultat = sistem.genereaza_coduri_batch(
        prefix="BOOK",
        start=1,
        count=100
    )

    # ──────────────────────────────────────────────────
    # TEST 2: Încearcă să regenerezi (detectează duplicate)
    # ──────────────────────────────────────────────────
    print("\n📦 TEST 2: Încercare regenerare (test duplicate)...")
    rezultat2 = sistem.genereaza_coduri_batch(
        prefix="BOOK",
        start=1,
        count=10  # Primele 10 sunt duplicate!
    )

    # ──────────────────────────────────────────────────
    # TEST 3: Scanează cod (simulare)
    # ──────────────────────────────────────────────────
    print("\n📱 TEST 3: Simulare scanare coduri...")

    # Scanează cod valid
    verificare1 = sistem.verifica_cod_la_scanare("BOOK00001")
    print(f"   {verificare1['mesaj']}")
    print(f"   Detalii: {verificare1['detalii']}")

    # Scanează cod inexistent
    verificare2 = sistem.verifica_cod_la_scanare("BOOK99999")
    print(f"\n   {verificare2['mesaj']}")

    # Asociază cod cu carte
    print("\n📚 TEST 4: Asociere cod cu carte...")
    sistem.asociaza_cod_cu_carte(
        cod_bare="BOOK00001",
        titlu="Amintiri din copilărie",
        autor="Ion Creangă",
        isbn="978-973-46-4053-9"
    )

    # Încearcă să asociezi din nou (duplicat!)
    print("\n⚠️  TEST 5: Încercare asociere duplicată...")
    sistem.asociaza_cod_cu_carte(
        cod_bare="BOOK00001",
        titlu="Altă carte",
        autor="Alt autor"
    )

    # Raport duplicate
    print("\n📊 TEST 6: Raport duplicate...")
    sistem.raport_duplicate()

    # Export raport
    print("\n📄 TEST 7: Export raport...")
    sistem.export_raport_json()

    # Găsește coduri libere
    print("\n🔍 TEST 8: Coduri libere disponibile...")
    libere = sistem.gaseste_coduri_libere(count=10)
    print(f"   Primele 10 coduri libere:")
    for cod in libere:
        print(f"   - {cod}")

    print("\n" + "="*60)
    print("✅ TOATE TESTELE FINALIZATE!")
    print("="*60)