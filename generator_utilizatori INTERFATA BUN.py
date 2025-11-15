'''
Perfect! Iată explicația detaliată pentru fiecare buton:

---

## 📦 **Butonul 1: "Generează Coduri"** (albastru)

**Ce face:**
- Generează coduri noi în batch (ex: USER00001, USER00002, etc.)
- Salvează fiecare cod în baza de date SQLite
- Creează câte o imagine PNG cu cod de bare pentru fiecare cod
- Afișează progress bar live în timp ce generează

**Cum funcționează:**
1. Click pe buton → Se deschide un formular
2. Introduci câte coduri vrei (ex: 100, 500, 1000)
3. Alegi prefix-ul (ex: USER, STUDENT, READER)
4. Click "GENEREAZĂ" → Începe procesul
5. Vezi progres în timp real: "Generare: 50/100"
6. La final vezi raport: câte au fost generate, câte duplicate, câte erori

**Exemplu:**
- Setez: 100 coduri, prefix "USER"
- Rezultat: USER00001.png, USER00002.png ... USER00100.png
- Plus 100 înregistrări în baza de date

---

## 👤 **Butonul 2: "Atribuie Cod"** (verde)

**Ce face:**
- Atribuie un cod liber unui utilizator specific
- Schimbă status-ul codului din "liber" → "atribuit"
- Salvează datele utilizatorului (nume, email, observații)
- Înregistrează data atribuirii

**Cum funcționează:**
1. Click pe buton → Formular cu 4 câmpuri
2. Introduci **Cod** (ex: USER00001)
3. Introduci **Nume** (ex: "Popescu Ion")
4. Opțional: **Email** (ex: "ion@gmail.com")
5. Opțional: **Observații** (ex: "Student anul 3")
6. Click "ATRIBUIE" → Codul devine al acelui utilizator

**Validare:**
- Nu poți atribui un cod care nu există
- Nu poți atribui un cod deja atribuit altcuiva
- Cod și Nume sunt obligatorii

**Exemplu:**
- Cod: USER00001
- Nume: "Popescu Ion"
- Email: "ion@biblioteca.ro"
- Observații: "Carnet valabil 1 an"
→ USER00001 devine carnetul lui Popescu Ion

---

## 🔓 **Butonul 3: "Eliberează Cod"** (roșu)

**Ce face:**
- Eliberează un cod atribuit (îl face din nou disponibil)
- Șterge toate datele utilizatorului de pe cod
- Schimbă status din "atribuit" → "liber"
- Folosit când un utilizator returnează carnetul

**Cum funcționează:**
1. Click pe buton → Formular simplu
2. Introduci codul (ex: USER00001)
3. Click "ELIBEREAZĂ"
4. Codul devine liber și poate fi reatribuit altcuiva

**Când se folosește:**
- Un student a terminat studiile
- Un utilizator și-a pierdut carnetul
- Vrei să reutilizezi un cod

**Exemplu:**
- Popescu Ion returnează carnetul USER00001
- Introduc USER00001 → Click "ELIBEREAZĂ"
- Acum USER00001 e liber și poate fi dat lui Ionescu Maria

---

## 📊 **Butonul 4: "Statistici"** (violet)

**Ce face:**
- Afișează un dashboard cu statistici live din baza de date
- Arată câte coduri totale există
- Câte sunt libere (disponibile)
- Câte sunt atribuite (în uz)
- Afișează și un grafic vizual (bară colorată cu procente)

**Informații afișate:**
```
📦 Total Coduri:    1000
✅ Libere:          750  (75%)
👤 Atribuite:       250  (25%)
```

Plus o bară grafică:
```
[████████████░░░░] 75% libere
```

**Când se folosește:**
- Să vezi câte coduri mai ai disponibile
- Să planifici când să generezi altele noi
- Rapoarte pentru management

**Actualizare:**
- Se actualizează automat de fiecare dată când apeși butonul
- Datele sunt LIVE din baza de date

---

## 🔍 **Butonul 5: "Caută Utilizator"** (portocaliu)

**Ce face:**
- Caută în baza de date după numele utilizatorului
- Afișează toate codurile atribuite acelui utilizator
- Căutarea funcționează și cu nume parțiale

**Cum funcționează:**
1. Click pe buton → Formular cu câmp de căutare
2. Introduci un nume sau parte din nume (ex: "Popescu" sau "Pop")
3. Click "CAUTĂ"
4. Vezi toate rezultatele cu detalii complete

**Rezultate afișate:**
```
📇 Cod: USER00001
   Nume: Popescu Ion
   Email: ion@gmail.com
   Atribuit: 2024-11-15 10:30:00
------------------------------------
📇 Cod: USER00234
   Nume: Popescu Maria
   Email: maria@yahoo.com
   Atribuit: 2024-11-14 14:20:00
```

**Căutare inteligentă:**
- "Pop" → găsește "Popescu Ion", "Popa Ana"
- "ion" → găsește "Popescu Ion", "Ionescu Maria"
- Nu e case-sensitive (nu contează literele mari/mici)

**Când se folosește:**
- Un utilizator vine și nu știi ce cod are
- Verifici dacă cineva are deja carnet
- Audit: vezi cine are coduri active

---

## ❌ **Butonul 6: "Ieșire"** (gri)

**Ce face:**
- Închide aplicația în mod sigur
- Salvează automat toate datele
- Închide conexiunea la baza de date corect

**Cum funcționează:**
1. Click pe buton
2. Apare mesaj: "Sigur vrei să închizi aplicația?"
3. Click "Da" → Aplicația se închide
4. Click "Nu" → Rămâi în aplicație

**Siguranță:**
- Nu pierzi date dacă închizi cu acest buton
- Toate modificările sunt deja salvate
- Baza de date se închide corect (fără corupție)

---

## 🎯 **Flux tipic de lucru:**

**Scenariul 1: Setup inițial**
1. (**Generează Coduri**) → Generez 1000 de coduri USER
2. (**Statistici**) → Verific: 1000 total, 1000 libere

**Scenariul 2: Înregistrare student nou**
1. (**Statistici**) → Văd că mai am 750 libere
2. (**Atribuie Cod**) → Atribui USER00251 lui "Ionescu Maria"
3. (**Caută Utilizator**) → Caut "Ionescu" să confirm

**Scenariul 3: Student absolvit**
1. (**Caută Utilizator**) → Caut "Popescu" să văd ce cod are
2. (**Eliberează Cod**) → Eliberez USER00001
3. (**Statistici**) → Văd că am 751 libere acum

---

**Întrebări? Vrei să modific ceva la vreun buton?** 🚀
'''

# generator_utilizatori_GUI.py
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
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

    def genereaza_coduri_utilizatori(self, prefix="USER", start=1, count=1000, callback=None):
        """Generează coduri pentru utilizatori (carnete)"""
        rezultate = {
            'generate_ok': 0,
            'duplicate': 0,
            'erori': 0,
            'coduri_noi': []
        }

        for i in range(start, start + count):
            cod = f"{prefix}{i:05d}"

            try:
                exista = self.cursor.execute(
                    "SELECT cod FROM coduri_utilizatori WHERE cod = ?",
                    (cod,)
                ).fetchone()

                if exista:
                    rezultate['duplicate'] += 1
                    continue

                self.cursor.execute('''
                    INSERT INTO coduri_utilizatori (cod, tip, status)
                    VALUES (?, ?, 'liber')
                ''', (cod, prefix))

                barcode_path = self.generator.genereaza_code128(cod)

                if barcode_path:
                    rezultate['generate_ok'] += 1
                    rezultate['coduri_noi'].append(cod)
                else:
                    rezultate['erori'] += 1

                if callback and (i - start + 1) % 10 == 0:
                    callback(i - start + 1, count)

            except Exception as e:
                rezultate['erori'] += 1

        self.conn.commit()
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
            return self.cursor.rowcount > 0

        except Exception as e:
            return False

    def elibereaza_cod(self, cod):
        """Eliberează un cod"""
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
            return True

        except Exception as e:
            return False

    def vezi_statistici(self):
        """Returnează statistici despre coduri"""
        total = self.cursor.execute(
            "SELECT COUNT(*) FROM coduri_utilizatori"
        ).fetchone()[0]

        libere = self.cursor.execute(
            "SELECT COUNT(*) FROM coduri_utilizatori WHERE status = 'liber'"
        ).fetchone()[0]

        atribuite = self.cursor.execute(
            "SELECT COUNT(*) FROM coduri_utilizatori WHERE status = 'atribuit'"
        ).fetchone()[0]

        return {'total': total, 'libere': libere, 'atribuite': atribuite}

    def cauta_utilizator(self, nume_partial):
        """Caută utilizatori după nume"""
        rezultate = self.cursor.execute('''
            SELECT cod, utilizator_nume, utilizator_email, data_atribuire
            FROM coduri_utilizatori
            WHERE utilizator_nume LIKE ? AND status = 'atribuit'
            ORDER BY data_atribuire DESC
        ''', (f'%{nume_partial}%',)).fetchall()

        return rezultate

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()


# ═══════════════════════════════════════════════════════
# PARTEA 3: INTERFAȚĂ GRAFICĂ
# ═══════════════════════════════════════════════════════

class InterfataGeneratorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎫 Generator Coduri Utilizatori - Bibliotecă")
        self.root.geometry("800x600")
        self.root.configure(bg="#2c3e50")

        self.generator = GeneratorCoduriUtilizatori()

        self.setup_ui()

    def setup_ui(self):
        """Configurează interfața"""
        # Header
        header = tk.Frame(self.root, bg="#34495e", height=80)
        header.pack(fill="x", padx=0, pady=0)

        title = tk.Label(
            header,
            text="🎫 Generator Coduri Utilizatori",
            font=("Segoe UI", 20, "bold"),
            bg="#34495e",
            fg="white"
        )
        title.pack(pady=20)

        # Main container
        main_container = tk.Frame(self.root, bg="#2c3e50")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Left panel - Butoane
        left_panel = tk.Frame(main_container, bg="#34495e", width=300)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)

        tk.Label(
            left_panel,
            text="⚡ Acțiuni Rapide",
            font=("Segoe UI", 14, "bold"),
            bg="#34495e",
            fg="white"
        ).pack(pady=15)

        # Butoane
        buttons = [
            ("📦 Generează Coduri", self.show_genereaza_coduri, "#3498db"),
            ("👤 Atribuie Cod", self.show_atribuie_cod, "#2ecc71"),
            ("🔓 Eliberează Cod", self.show_elibereaza_cod, "#e74c3c"),
            ("📊 Statistici", self.show_statistici, "#9b59b6"),
            ("🔍 Caută Utilizator", self.show_cauta_utilizator, "#f39c12"),
            ("❌ Ieșire", self.quit_app, "#95a5a6")
        ]

        for text, command, color in buttons:
            btn = tk.Button(
                left_panel,
                text=text,
                font=("Segoe UI", 11, "bold"),
                bg=color,
                fg="white",
                activebackground=self.darker_color(color),
                activeforeground="white",
                bd=0,
                cursor="hand2",
                padx=20,
                pady=12,
                command=command
            )
            btn.pack(fill="x", padx=15, pady=5)

        # Right panel - Conținut dinamic
        self.right_panel = tk.Frame(main_container, bg="#ecf0f1")
        self.right_panel.pack(side="right", fill="both", expand=True)

        # Mesaj de bun venit
        welcome = tk.Label(
            self.right_panel,
            text="👈 Selectează o acțiune din meniu",
            font=("Segoe UI", 14),
            bg="#ecf0f1",
            fg="#7f8c8d"
        )
        welcome.pack(expand=True)

    def darker_color(self, hex_color):
        """Face culoarea mai închisă"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darker_rgb = tuple(max(0, c - 30) for c in rgb)
        return f'#{darker_rgb[0]:02x}{darker_rgb[1]:02x}{darker_rgb[2]:02x}'

    def clear_right_panel(self):
        """Șterge conținutul panoului drept"""
        for widget in self.right_panel.winfo_children():
            widget.destroy()

    # ═════════════════════════════════════════════════════
    # FUNCȚII PENTRU FIECARE ACȚIUNE
    # ═════════════════════════════════════════════════════

    def show_genereaza_coduri(self):
        """Formular pentru generare coduri"""
        self.clear_right_panel()

        frame = tk.Frame(self.right_panel, bg="#ecf0f1")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            frame,
            text="📦 Generează Coduri Noi",
            font=("Segoe UI", 16, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        ).pack(pady=(0, 20))

        # Câmpuri
        fields_frame = tk.Frame(frame, bg="#ecf0f1")
        fields_frame.pack(pady=10)

        tk.Label(fields_frame, text="Câte coduri:", bg="#ecf0f1", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        count_entry = tk.Entry(fields_frame, font=("Segoe UI", 11), width=20)
        count_entry.grid(row=0, column=1, padx=5, pady=5)
        count_entry.insert(0, "100")

        tk.Label(fields_frame, text="Prefix:", bg="#ecf0f1", font=("Segoe UI", 11)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        prefix_entry = tk.Entry(fields_frame, font=("Segoe UI", 11), width=20)
        prefix_entry.grid(row=1, column=1, padx=5, pady=5)
        prefix_entry.insert(0, "USER")

        # Progress bar
        progress_frame = tk.Frame(frame, bg="#ecf0f1")
        progress_frame.pack(pady=20)

        progress_label = tk.Label(progress_frame, text="", bg="#ecf0f1", font=("Segoe UI", 10))
        progress_label.pack()

        progress_bar = ttk.Progressbar(progress_frame, length=400, mode='determinate')
        progress_bar.pack(pady=10)

        result_text = scrolledtext.ScrolledText(frame, height=8, width=50, font=("Courier New", 9))
        result_text.pack(pady=10)

        def genereaza():
            try:
                count = int(count_entry.get())
                prefix = prefix_entry.get().strip() or "USER"

                # Găsește start
                ultim = self.generator.cursor.execute(
                    "SELECT cod FROM coduri_utilizatori WHERE tip = ? ORDER BY id DESC LIMIT 1",
                    (prefix,)
                ).fetchone()

                if ultim:
                    try:
                        start = int(ultim[0].replace(prefix, '')) + 1
                    except:
                        start = 1
                else:
                    start = 1

                progress_bar['value'] = 0
                progress_bar['maximum'] = count

                def update_progress(current, total):
                    progress_bar['value'] = current
                    progress_label.config(text=f"Generare: {current}/{total}")
                    self.root.update_idletasks()

                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"🚀 Start generare...\n")
                result_text.insert(tk.END, f"Prefix: {prefix}\n")
                result_text.insert(tk.END, f"Start: {prefix}{start:05d}\n")
                result_text.insert(tk.END, f"Count: {count}\n\n")

                rezultate = self.generator.genereaza_coduri_utilizatori(
                    prefix=prefix,
                    start=start,
                    count=count,
                    callback=update_progress
                )

                result_text.insert(tk.END, f"\n{'='*40}\n")
                result_text.insert(tk.END, f"✅ Generate: {rezultate['generate_ok']}\n")
                result_text.insert(tk.END, f"⚠️  Duplicate: {rezultate['duplicate']}\n")
                result_text.insert(tk.END, f"❌ Erori: {rezultate['erori']}\n")
                result_text.insert(tk.END, f"{'='*40}\n")

                messagebox.showinfo("Succes!", f"✅ {rezultate['generate_ok']} coduri generate!")

            except ValueError:
                messagebox.showerror("Eroare", "Număr invalid!")

        tk.Button(
            frame,
            text="🚀 GENEREAZĂ",
            font=("Segoe UI", 12, "bold"),
            bg="#3498db",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2",
            command=genereaza
        ).pack(pady=10)

    def show_atribuie_cod(self):
        """Formular pentru atribuire cod"""
        self.clear_right_panel()

        frame = tk.Frame(self.right_panel, bg="#ecf0f1")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            frame,
            text="👤 Atribuie Cod Utilizator",
            font=("Segoe UI", 16, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        ).pack(pady=(0, 20))

        fields_frame = tk.Frame(frame, bg="#ecf0f1")
        fields_frame.pack(pady=10)

        tk.Label(fields_frame, text="Cod:", bg="#ecf0f1", font=("Segoe UI", 11)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        cod_entry = tk.Entry(fields_frame, font=("Segoe UI", 11), width=25)
        cod_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(fields_frame, text="Nume:", bg="#ecf0f1", font=("Segoe UI", 11)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        nume_entry = tk.Entry(fields_frame, font=("Segoe UI", 11), width=25)
        nume_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(fields_frame, text="Email:", bg="#ecf0f1", font=("Segoe UI", 11)).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        email_entry = tk.Entry(fields_frame, font=("Segoe UI", 11), width=25)
        email_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(fields_frame, text="Observații:", bg="#ecf0f1", font=("Segoe UI", 11)).grid(row=3, column=0, sticky="ne", padx=5, pady=5)
        obs_text = tk.Text(fields_frame, font=("Segoe UI", 10), width=25, height=4)
        obs_text.grid(row=3, column=1, padx=5, pady=5)

        def atribuie():
            cod = cod_entry.get().strip().upper()
            nume = nume_entry.get().strip()
            email = email_entry.get().strip() or None
            obs = obs_text.get(1.0, tk.END).strip() or None

            if not cod or not nume:
                messagebox.showerror("Eroare", "Cod și Nume sunt obligatorii!")
                return

            succes = self.generator.atribuie_utilizator(cod, nume, email, obs)

            if succes:
                messagebox.showinfo("Succes!", f"✅ Codul {cod} atribuit lui {nume}")
                cod_entry.delete(0, tk.END)
                nume_entry.delete(0, tk.END)
                email_entry.delete(0, tk.END)
                obs_text.delete(1.0, tk.END)
            else:
                messagebox.showerror("Eroare", f"❌ Codul {cod} nu există sau e deja atribuit!")

        tk.Button(
            frame,
            text="✅ ATRIBUIE",
            font=("Segoe UI", 12, "bold"),
            bg="#2ecc71",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2",
            command=atribuie
        ).pack(pady=20)

    def show_elibereaza_cod(self):
        """Formular pentru eliberare cod"""
        self.clear_right_panel()

        frame = tk.Frame(self.right_panel, bg="#ecf0f1")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            frame,
            text="🔓 Eliberează Cod",
            font=("Segoe UI", 16, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        ).pack(pady=(0, 20))

        tk.Label(frame, text="Introdu codul de eliberat:", bg="#ecf0f1", font=("Segoe UI", 11)).pack(pady=10)

        cod_entry = tk.Entry(frame, font=("Segoe UI", 14), width=20)
        cod_entry.pack(pady=10)

        def elibereaza():
            cod = cod_entry.get().strip().upper()

            if not cod:
                messagebox.showerror("Eroare", "Introdu un cod!")
                return

            succes = self.generator.elibereaza_cod(cod)

            if succes:
                messagebox.showinfo("Succes!", f"✅ Codul {cod} a fost eliberat!")
                cod_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Eroare", f"❌ Eroare la eliberarea codului!")

        tk.Button(
            frame,
            text="🔓 ELIBEREAZĂ",
            font=("Segoe UI", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            padx=30,
            pady=10,
            cursor="hand2",
            command=elibereaza
        ).pack(pady=20)

    def show_statistici(self):
        """Afișează statistici"""
        self.clear_right_panel()

        frame = tk.Frame(self.right_panel, bg="#ecf0f1")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            frame,
            text="📊 Statistici Coduri",
            font=("Segoe UI", 16, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        ).pack(pady=(0, 30))

        stats = self.generator.vezi_statistici()

        stats_frame = tk.Frame(frame, bg="white", relief="solid", bd=1)
        stats_frame.pack(pady=20, padx=40, fill="x")

        items = [
            ("📦 Total Coduri", stats['total'], "#3498db"),
            ("✅ Libere", stats['libere'], "#2ecc71"),
            ("👤 Atribuite", stats['atribuite'], "#9b59b6")
        ]

        for label, value, color in items:
            item_frame = tk.Frame(stats_frame, bg="white")
            item_frame.pack(fill="x", padx=20, pady=15)

            tk.Label(
                item_frame,
                text=label,
                font=("Segoe UI", 12),
                bg="white",
                fg="#7f8c8d"
            ).pack(side="left")

            tk.Label(
                item_frame,
                text=str(value),
                font=("Segoe UI", 20, "bold"),
                bg="white",
                fg=color
            ).pack(side="right")

        # Grafic simplu
        if stats['total'] > 0:
            canvas_frame = tk.Frame(frame, bg="#ecf0f1")
            canvas_frame.pack(pady=20)

            canvas = tk.Canvas(canvas_frame, width=400, height=40, bg="white", highlightthickness=0)
            canvas.pack()

            libere_proc = stats['libere'] * 400 // stats['total']

            canvas.create_rectangle(0, 0, libere_proc, 40, fill="#2ecc71", outline="")
            canvas.create_rectangle(libere_proc, 0, 400, 40, fill="#9b59b6", outline="")

            canvas.create_text(200, 20, text=f"{stats['libere']*100//stats['total']}% libere", font=("Segoe UI", 10, "bold"), fill="white")

    def show_cauta_utilizator(self):
        """Formular pentru căutare utilizator"""
        self.clear_right_panel()

        frame = tk.Frame(self.right_panel, bg="#ecf0f1")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            frame,
            text="🔍 Caută Utilizator",
            font=("Segoe UI", 16, "bold"),
            bg="#ecf0f1",
            fg="#2c3e50"
        ).pack(pady=(0, 20))

        search_frame = tk.Frame(frame, bg="#ecf0f1")
        search_frame.pack(pady=10)

        tk.Label(search_frame, text="Nume (parțial):", bg="#ecf0f1", font=("Segoe UI", 11)).pack(side="left", padx=5)
        search_entry = tk.Entry(search_frame, font=("Segoe UI", 11), width=25)
        search_entry.pack(side="left", padx=5)

        result_text = scrolledtext.ScrolledText(frame, height=15, width=60, font=("Courier New", 9))
        result_text.pack(pady=20, fill="both", expand=True)

        def cauta():
            nume = search_entry.get().strip()

            if not nume:
                messagebox.showerror("Eroare", "Introdu un nume pentru căutare!")
                return

            rezultate = self.generator.cauta_utilizator(nume)

            result_text.delete(1.0, tk.END)

            if rezultate:
                result_text.insert(tk.END, f"🔍 Găsite {len(rezultate)} rezultate pentru '{nume}':\n\n")
                result_text.insert(tk.END, f"{'='*60}\n")

                for cod, nume_user, email, data in rezultate:
                    result_text.insert(tk.END, f"📇 Cod: {cod}\n")
                    result_text.insert(tk.END, f"   Nume: {nume_user}\n")
                    result_text.insert(tk.END, f"   Email: {email or 'N/A'}\n")
                    result_text.insert(tk.END, f"   Atribuit: {data}\n")
                    result_text.insert(tk.END, f"{'-'*60}\n")
            else:
                result_text.insert(tk.END, f"❌ Nu s-au găsit utilizatori cu '{nume}'")

        tk.Button(
            search_frame,
            text="🔍 CAUTĂ",
            font=("Segoe UI", 11, "bold"),
            bg="#f39c12",
            fg="white",
            padx=20,
            pady=8,
            cursor="hand2",
            command=cauta
        ).pack(side="left", padx=5)

    def quit_app(self):
        """Închide aplicația"""
        if messagebox.askyesno("Confirmare", "Sigur vrei să închizi aplicația?"):
            self.root.quit()

    def run(self):
        """Pornește aplicația"""
        self.root.mainloop()


# ═══════════════════════════════════════════════════════
# START APLICAȚIE
# ═══════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        app = InterfataGeneratorGUI()
        app.run()
    except Exception as e:
        print(f"❌ EROARE: {e}")
        import traceback
        traceback.print_exc()