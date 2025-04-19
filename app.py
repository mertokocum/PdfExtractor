import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
import os

class PDFSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Page Extractor")

        self.pdf_path = None

        # PDF seçme
        self.select_button = tk.Button(root, text="PDF Seç", command=self.select_pdf)
        self.select_button.pack(pady=10)

        # Seçilen PDF'i gösterme
        self.file_label = tk.Label(root, text="Henüz bir dosya seçilmedi.")
        self.file_label.pack()

        # Sayfa aralığı giriş kutusu
        self.range_label = tk.Label(root, text="Sayfa Aralığı (örn: 1-3):")
        self.range_label.pack()
        self.page_range_entry = tk.Entry(root)
        self.page_range_entry.pack()

        # PDF oluşturma
        self.split_button = tk.Button(root, text="Yeni PDF Oluştur", command=self.split_pdf)
        self.split_button.pack(pady=20)

    def select_pdf(self):
        self.pdf_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if self.pdf_path:
            self.file_label.config(text=os.path.basename(self.pdf_path))

    def split_pdf(self):
        if not self.pdf_path:
            messagebox.showerror("Hata", "Lütfen önce bir PDF dosyası seçin.")
            return

        page_range = self.page_range_entry.get()
        try:
            start, end = map(int, page_range.split('-'))
        except ValueError:
            messagebox.showerror("Hata", "Lütfen sayfa aralığını doğru formatta girin (örn: 2-5).")
            return

        try:
            reader = PdfReader(self.pdf_path)
            writer = PdfWriter()

            total_pages = len(reader.pages)
            if start < 1 or end > total_pages or start > end:
                raise IndexError("Geçersiz sayfa aralığı.")

            for i in range(start - 1, end):
                writer.add_page(reader.pages[i])

            output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
            if output_path:
                with open(output_path, "wb") as output_pdf:
                    writer.write(output_pdf)
                messagebox.showinfo("Başarılı", f"Yeni PDF oluşturuldu:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Hata", f"PDF işlenemedi:\n{str(e)}")

# Uygulamayı başlat
if __name__ == "__main__":
    root = tk.Tk()
    app = PDFSplitterApp(root)
    root.mainloop()
