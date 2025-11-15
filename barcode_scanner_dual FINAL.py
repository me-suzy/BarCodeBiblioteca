# barcode_scanner_improved.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageGrab, ImageEnhance, ImageFilter, ImageOps
import easyocr
import requests
import re
from datetime import datetime
import cv2
import numpy as np

class ImprovedBarcodeScanner:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔍 Scanner Coduri Îmbunătățit")
        self.root.geometry("500x420")
        self.root.configure(bg="#667eea")

        self.start_x = None
        self.start_y = None
        self.selection_window = None
        self.canvas = None
        self.rect = None
        self.scan_mode = None

        self.php_url = "http://localhost/scan_barcode.php"

        print("⏳ Încărcare EasyOCR...")
        self.reader = easyocr.Reader(['en'], gpu=False)
        print("✅ EasyOCR gata!")

        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg="#667eea")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        title = tk.Label(
            main_frame,
            text="🔍 Scanner Coduri Îmbunătățit",
            font=("Segoe UI", 20, "bold"),
            bg="#667eea",
            fg="white"
        )
        title.pack(pady=15)

        instructions = tk.Label(
            main_frame,
            text="Alege modul de scanare:",
            font=("Segoe UI", 12),
            bg="#667eea",
            fg="white"
        )
        instructions.pack(pady=10)

        auto_button = tk.Button(
            main_frame,
            text="🤖 Scanare AUTOMATĂ\n(OCR direct în DB)",
            font=("Segoe UI", 13, "bold"),
            bg="#28a745",
            fg="white",
            padx=30,
            pady=20,
            cursor="hand2",
            command=lambda: self.start_selection('auto')
        )
        auto_button.pack(pady=10)

        manual_button = tk.Button(
            main_frame,
            text="✍️ Scanare cu CONFIRMARE\n(OCR + Editare manuală)",
            font=("Segoe UI", 13, "bold"),
            bg="#ffc107",
            fg="#333",
            padx=30,
            pady=20,
            cursor="hand2",
            command=lambda: self.start_selection('manual')
        )
        manual_button.pack(pady=10)

        info_label = tk.Label(
            main_frame,
            text="💡 Îmbunătățit = Procesare mai bună a imaginii\n" +
                 "💡 Debugging = Salvează imaginile procesate",
            font=("Segoe UI", 9),
            bg="#667eea",
            fg="white",
            justify="center"
        )
        info_label.pack(pady=10)

        status_frame = tk.Frame(main_frame, bg="#667eea")
        status_frame.pack(pady=10)

        self.status_label = tk.Label(
            status_frame,
            text="✅ Gata de scanare",
            font=("Segoe UI", 11, "bold"),
            bg="#667eea",
            fg="#90EE90"
        )
        self.status_label.pack()

    def start_selection(self, mode):
        self.scan_mode = mode
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

        mode_text = "AUTOMATĂ" if self.scan_mode == 'auto' else "cu CONFIRMARE"

        self.canvas.create_text(
            self.selection_window.winfo_screenwidth() // 2,
            50,
            text=f"🖱️ Scanare {mode_text}\n\n" +
                 "Selectează ÎNTREG codul de bare (linii + text)\n" +
                 "ESC = Anulare",
            font=("Segoe UI", 16, "bold"),
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

    def preprocess_image(self, image):
        """Procesare avansată a imaginii pentru OCR mai bun"""

        # Convertește la numpy array
        img_array = np.array(image)

        # Salvează imaginea originală pentru debugging
        cv2.imwrite("debug_1_original.png", img_array)

        # 1. Convertește la grayscale
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array
        cv2.imwrite("debug_2_gray.png", gray)

        # 2. Mărește contrastul
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        cv2.imwrite("debug_3_contrast.png", enhanced)

        # 3. Denoising
        denoised = cv2.fastNlMeansDenoising(enhanced, None, 10, 7, 21)
        cv2.imwrite("debug_4_denoised.png", denoised)

        # 4. Binary threshold (alb-negru pur)
        _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        cv2.imwrite("debug_5_binary.png", binary)

        # 5. Inversează dacă text-ul e alb pe fundal negru
        if np.mean(binary) < 127:
            binary = cv2.bitwise_not(binary)
            cv2.imwrite("debug_6_inverted.png", binary)

        return binary

    def process_barcode(self, x1, y1, x2, y2):
        self.root.deiconify()
        self.status_label.config(text="⏳ Procesare avansată...", fg="yellow")
        self.root.update()

        try:
            # Capturează imaginea
            screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))

            # Procesare avansată
            processed_img = self.preprocess_image(screenshot)

            # Salvează imaginea procesată
            cv2.imwrite("temp_processed.png", processed_img)

            # Încearcă OCR cu multiple configurații
            detected_codes = []

            # Încercare 1: Standard
            self.status_label.config(text="⏳ OCR încercare 1/3...", fg="yellow")
            self.root.update()
            results1 = self.reader.readtext("temp_processed.png", detail=0)
            detected_codes.extend(results1)

            # Încercare 2: Cu inversare
            inverted = cv2.bitwise_not(processed_img)
            cv2.imwrite("temp_inverted.png", inverted)
            self.status_label.config(text="⏳ OCR încercare 2/3...", fg="yellow")
            self.root.update()
            results2 = self.reader.readtext("temp_inverted.png", detail=0)
            detected_codes.extend(results2)

            # Încercare 3: Cu resize (mărire)
            resized = cv2.resize(processed_img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
            cv2.imwrite("temp_resized.png", resized)
            self.status_label.config(text="⏳ OCR încercare 3/3...", fg="yellow")
            self.root.update()
            results3 = self.reader.readtext("temp_resized.png", detail=0)
            detected_codes.extend(results3)

            # Combină toate rezultatele
            all_text = ' '.join(detected_codes).upper()
            print(f"DEBUG: Text detectat din toate încercările: {all_text}")

            # Extrage codul
            barcode = self.extract_barcode(all_text)

            if barcode:
                if self.scan_mode == 'auto':
                    self.send_to_database(barcode)
                else:
                    self.confirm_and_send(barcode)
            else:
                # Dacă OCR eșuează complet, mergi direct la introducere manuală
                self.status_label.config(text="❌ OCR eșuat", fg="red")

                if self.scan_mode == 'manual':
                    # Deschide direct fereastra de introducere manuală
                    self.manual_input(all_text)
                else:
                    messagebox.showerror(
                        "Eroare OCR",
                        f"Nu am putut citi codul!\n\n" +
                        f"Text detectat: {all_text}\n\n" +
                        "Încearcă modul cu confirmare pentru introducere manuală."
                    )

        except Exception as e:
            self.status_label.config(text="❌ Eroare", fg="red")
            messagebox.showerror("Eroare", f"Eroare la procesare:\n{str(e)}")

    def extract_barcode(self, text):
        """Extrage codul de bare din textul OCR"""
        text = text.strip().upper().replace(' ', '').replace('\n', '')

        patterns = [
            r'BOOK\d+',
            r'USER\d+',
            r'[A-Z]{3,}\d+',
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)

        cleaned = re.sub(r'[^A-Z0-9]', '', text)
        return cleaned if len(cleaned) >= 4 else None

    def manual_input(self, detected_text=""):
        """Introducere complet manuală când OCR eșuează"""
        self.status_label.config(text="✍️ Introducere manuală", fg="orange")

        manual_window = tk.Toplevel(self.root)
        manual_window.title("Introducere Manuală")
        manual_window.geometry("450x300")
        manual_window.configure(bg="white")
        manual_window.transient(self.root)
        manual_window.grab_set()

        manual_window.update_idletasks()
        x = (manual_window.winfo_screenwidth() // 2) - (450 // 2)
        y = (manual_window.winfo_screenheight() // 2) - (300 // 2)
        manual_window.geometry(f"+{x}+{y}")

        tk.Label(
            manual_window,
            text="❌ OCR nu a putut citi codul",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#d32f2f"
        ).pack(pady=15)

        if detected_text:
            tk.Label(
                manual_window,
                text=f"Text detectat: {detected_text}",
                font=("Segoe UI", 9),
                bg="white",
                fg="#666"
            ).pack()

        tk.Label(
            manual_window,
            text="✍️ Introdu codul manual:",
            font=("Segoe UI", 11, "bold"),
            bg="white"
        ).pack(pady=15)

        code_entry = tk.Entry(
            manual_window,
            font=("Segoe UI", 16, "bold"),
            width=20,
            justify="center"
        )
        code_entry.pack(pady=10)
        code_entry.focus()

        button_frame = tk.Frame(manual_window, bg="white")
        button_frame.pack(pady=20)

        def save_code():
            final_code = code_entry.get().strip().upper()
            if final_code:
                manual_window.destroy()
                self.send_to_database(final_code)
            else:
                messagebox.showwarning("Atenție", "Introdu un cod valid!")

        def cancel_input():
            manual_window.destroy()
            self.status_label.config(text="❌ Anulat", fg="red")

        tk.Button(
            button_frame,
            text="✅ Salvează în DB",
            command=save_code,
            font=("Segoe UI", 12, "bold"),
            bg="#28a745",
            fg="white",
            padx=25,
            pady=12,
            cursor="hand2"
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="❌ Anulează",
            command=cancel_input,
            font=("Segoe UI", 12),
            bg="#dc3545",
            fg="white",
            padx=25,
            pady=12,
            cursor="hand2"
        ).pack(side="left", padx=10)

        code_entry.bind("<Return>", lambda e: save_code())
        code_entry.bind("<Escape>", lambda e: cancel_input())

    def confirm_and_send(self, detected_code):
        """Modul MANUAL - arată codul detectat și permite editare"""
        self.status_label.config(text="✍️ Confirmă codul", fg="orange")

        confirm_window = tk.Toplevel(self.root)
        confirm_window.title("Confirmă Codul")
        confirm_window.geometry("450x300")
        confirm_window.configure(bg="white")
        confirm_window.transient(self.root)
        confirm_window.grab_set()

        confirm_window.update_idletasks()
        x = (confirm_window.winfo_screenwidth() // 2) - (450 // 2)
        y = (confirm_window.winfo_screenheight() // 2) - (300 // 2)
        confirm_window.geometry(f"+{x}+{y}")

        tk.Label(
            confirm_window,
            text="✅ Cod detectat automat:",
            font=("Segoe UI", 12, "bold"),
            bg="white"
        ).pack(pady=15)

        detected_label = tk.Label(
            confirm_window,
            text=detected_code,
            font=("Segoe UI", 18, "bold"),
            bg="#e8f5e9",
            fg="#2e7d32",
            padx=20,
            pady=10
        )
        detected_label.pack(pady=10)

        tk.Label(
            confirm_window,
            text="✍️ Editează dacă este necesar:",
            font=("Segoe UI", 11),
            bg="white"
        ).pack(pady=10)

        code_entry = tk.Entry(
            confirm_window,
            font=("Segoe UI", 16, "bold"),
            width=20,
            justify="center"
        )
        code_entry.insert(0, detected_code)
        code_entry.pack(pady=10)
        code_entry.focus()
        code_entry.select_range(0, tk.END)

        button_frame = tk.Frame(confirm_window, bg="white")
        button_frame.pack(pady=20)

        def save_code():
            final_code = code_entry.get().strip().upper()
            if final_code:
                confirm_window.destroy()
                self.send_to_database(final_code)
            else:
                messagebox.showwarning("Atenție", "Introdu un cod valid!")

        def cancel_confirm():
            confirm_window.destroy()
            self.status_label.config(text="❌ Anulat", fg="red")

        tk.Button(
            button_frame,
            text="✅ Salvează în DB",
            command=save_code,
            font=("Segoe UI", 12, "bold"),
            bg="#28a745",
            fg="white",
            padx=25,
            pady=12,
            cursor="hand2"
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="❌ Anulează",
            command=cancel_confirm,
            font=("Segoe UI", 12),
            bg="#dc3545",
            fg="white",
            padx=25,
            pady=12,
            cursor="hand2"
        ).pack(side="left", padx=10)

        code_entry.bind("<Return>", lambda e: save_code())
        code_entry.bind("<Escape>", lambda e: cancel_confirm())

    def send_to_database(self, barcode):
        """Trimite codul la aplicația PHP"""
        try:
            self.status_label.config(text="⏳ Trimit la DB...", fg="yellow")
            self.root.update()

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
                    self.status_label.config(text="⚠️ Nu există în DB", fg="orange")
                    messagebox.showwarning(
                        "⚠️ Atenție",
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
    app = ImprovedBarcodeScanner()
    app.run()