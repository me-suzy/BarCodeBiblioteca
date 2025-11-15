# barcode_scanner_easyocr.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageGrab, ImageEnhance
import easyocr
import requests
import re
from datetime import datetime

class AutoBarcodeScanner:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔍 Barcode Scanner Auto")
        self.root.geometry("450x300")
        self.root.configure(bg="#667eea")

        self.start_x = None
        self.start_y = None
        self.selection_window = None
        self.canvas = None
        self.rect = None

        # URL-ul aplicației PHP
        self.php_url = "http://localhost/scan_barcode.php"

        # Inițializează EasyOCR (doar prima dată e mai lent)
        print("⏳ Încărcare EasyOCR...")
        self.reader = easyocr.Reader(['en'], gpu=False)
        print("✅ EasyOCR gata!")

        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg="#667eea")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        title = tk.Label(
            main_frame,
            text="🔍 Scanner Automat Coduri",
            font=("Segoe UI", 18, "bold"),
            bg="#667eea",
            fg="white"
        )
        title.pack(pady=10)

        instructions = tk.Label(
            main_frame,
            text="1. Deschide imaginea cu coduri de bare\n" +
                 "2. Apasă butonul de scanare\n" +
                 "3. Selectează codul cu mouse-ul\n" +
                 "4. Codul este trimis AUTOMAT la baza de date!",
            font=("Segoe UI", 10),
            bg="#667eea",
            fg="white",
            justify="center"
        )
        instructions.pack(pady=10)

        scan_button = tk.Button(
            main_frame,
            text="📸 Scanează Cod",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#667eea",
            padx=30,
            pady=15,
            cursor="hand2",
            command=self.start_selection
        )
        scan_button.pack(pady=15)

        status_frame = tk.Frame(main_frame, bg="#667eea")
        status_frame.pack(pady=10)

        self.status_label = tk.Label(
            status_frame,
            text="✅ Gata de scanare",
            font=("Segoe UI", 10, "bold"),
            bg="#667eea",
            fg="#90EE90"
        )
        self.status_label.pack()

    def start_selection(self):
        self.root.withdraw()
        self.root.after(200, self.create_overlay)

    def create_overlay(self):
        self.selection_window = tk.Toplevel()
        self.selection_window.attributes('-fullscreen', True)
        self.selection_window.attributes('-alpha', 0.3)
        self.selection_window.attributes('-topmost', True)

        self.canvas = tk.Canvas(
            self.selection_window,
            cursor="cross",
            bg="gray",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)

        self.canvas.create_text(
            self.selection_window.winfo_screenwidth() // 2,
            50,
            text="🖱️ Trage cu mouse-ul peste COD DE BARE\nESC = Anulare",
            font=("Segoe UI", 18, "bold"),
            fill="yellow"
        )

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.selection_window.bind("<Escape>", self.cancel)

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)

    def on_drag(self, event):
        if self.start_x and self.start_y:
            if self.rect:
                self.canvas.delete(self.rect)
            self.rect = self.canvas.create_rectangle(
                self.start_x, self.start_y, event.x, event.y,
                outline="lime", width=4, dash=(5, 5)
            )

    def on_release(self, event):
        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)

        self.selection_window.destroy()
        self.root.after(100, lambda: self.process_barcode(x1, y1, x2, y2))

    def cancel(self, event=None):
        if self.selection_window:
            self.selection_window.destroy()
        self.root.deiconify()

    def process_barcode(self, x1, y1, x2, y2):
        self.root.deiconify()
        self.status_label.config(text="⏳ Procesare OCR...", fg="yellow")
        self.root.update()

        try:
            # Capturează imaginea
            screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))

            # Îmbunătățește imaginea pentru OCR
            screenshot = screenshot.convert('L')  # Gri
            enhancer = ImageEnhance.Contrast(screenshot)
            screenshot = enhancer.enhance(2)  # Mărește contrastul

            # Salvează temporar
            temp_img = "temp_barcode.png"
            screenshot.save(temp_img)

            # OCR cu EasyOCR
            results = self.reader.readtext(temp_img)

            # Extrage textul
            text = ' '.join([result[1] for result in results])

            # Curăță textul
            barcode = self.extract_barcode(text)

            if barcode:
                # Trimite automat la PHP
                self.send_to_database(barcode)
            else:
                self.status_label.config(text="❌ Nu am găsit cod!", fg="red")
                messagebox.showerror("Eroare", f"Nu am putut citi codul!\nText detectat: {text}")

        except Exception as e:
            self.status_label.config(text="❌ Eroare", fg="red")
            messagebox.showerror("Eroare", f"Eroare la procesare:\n{str(e)}")

    def extract_barcode(self, text):
        """Extrage codul de bare din textul OCR"""
        # Curăță textul
        text = text.strip().upper()

        # Caută pattern-uri comune (BOOK0001, USER001, etc)
        patterns = [
            r'BOOK\d+',
            r'USER\d+',
            r'[A-Z]+\d+',
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)

        # Dacă nu găsește pattern, returnează tot textul curățat
        cleaned = re.sub(r'[^A-Z0-9]', '', text)
        return cleaned if len(cleaned) > 3 else None

    def send_to_database(self, barcode):
        """Trimite codul la aplicația PHP"""
        try:
            # Trimite POST la PHP
            response = requests.post(
                self.php_url,
                data={'barcode': barcode},
                timeout=5
            )

            if response.status_code == 200:
                result = response.json()

                if result.get('success'):
                    self.status_label.config(text="✅ Salvat în DB!", fg="lime")
                    messagebox.showinfo(
                        "✅ Succes!",
                        f"Cod scanat: {barcode}\n\n" +
                        f"{result.get('message', 'Salvat cu succes!')}"
                    )
                else:
                    self.status_label.config(text="⚠️ Eroare DB", fg="orange")
                    messagebox.showwarning(
                        "Atenție",
                        f"Cod: {barcode}\n\n{result.get('message', 'Eroare necunoscută')}"
                    )
            else:
                raise Exception(f"HTTP {response.status_code}")

        except requests.exceptions.ConnectionError:
            self.status_label.config(text="❌ Nu conectez la PHP", fg="red")
            messagebox.showerror(
                "Eroare Conexiune",
                f"Nu pot conecta la {self.php_url}\n\n" +
                "Verifică dacă XAMPP este pornit!"
            )
        except Exception as e:
            self.status_label.config(text="❌ Eroare", fg="red")
            messagebox.showerror("Eroare", f"Eroare la trimitere:\n{str(e)}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AutoBarcodeScanner()
    app.run()