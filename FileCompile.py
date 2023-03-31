import tkinter as tk
from tkinter import filedialog, messagebox
from pdfminer.high_level import extract_text
from bs4 import BeautifulSoup
from ebooklib import epub
import ebooklib
import os

def read_pdf(file_path):
    text = extract_text(file_path)
    text = text.replace('\f', '')  # Remove form feed characters
    return text


def read_epub(file_path):
    book = epub.read_epub(file_path)
    text = ''
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        content = item.get_content().decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')
        text += soup.get_text()
        text += "\n\n"  # Add space between chapters
    return text

def read_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return text

def read_file(file_path):
    _, ext = os.path.splitext(file_path)
    if ext.lower() == '.pdf':
        return read_pdf(file_path)
    elif ext.lower() == '.epub':
        return read_epub(file_path)
    elif ext.lower() == '.txt':
        return read_txt(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

def create_ui():
    app = tk.Tk()
    app.title("File Merger")

    selected_files = []

    def add_files():
        file_paths = filedialog.askopenfilenames(filetypes=[("Supported files", "*.pdf;*.epub;*.txt")])
        selected_files.extend(file_paths)
        update_file_list()

    def remove_files():
        selected_indices = file_listbox.curselection()
        for index in reversed(selected_indices):
            del selected_files[index]
        update_file_list()

    def update_file_list():
        file_listbox.delete(0, tk.END)
        for file_path in selected_files:
            file_listbox.insert(tk.END, os.path.basename(file_path))

    def export():
        if not selected_files:
            messagebox.showerror("Error", "No files selected for export.")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if output_path:
            try:
                with open(output_path, 'w', encoding='utf-8') as output_file:
                    for file_path in selected_files:
                        try:
                            text = read_file(file_path)
                            output_file.write(text)
                            output_file.write("\n\n")  # Add space between files
                        except Exception as e:
                            messagebox.showerror("Error", f"Failed to read file '{file_path}'. Error: {e}")
                            return

                messagebox.showinfo("Success", "Files have been merged and exported.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export merged file. Error: {e}")

    # UI layout
    tk.Button(app, text="Add Files", command=add_files).grid(row=0, column=0)
    tk.Button(app, text="Remove Files", command=remove_files).grid(row=0, column=1)
    tk.Button(app, text="Export", command=export).grid(row=0, column=2)

    file_listbox = tk.Listbox(app, selectmode=tk.MULTIPLE, width=100)
    file_listbox.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

    scrollbar = tk.Scrollbar(app, orient="vertical", command=file_listbox.yview)
    scrollbar.grid(row=1, column=3, sticky=tk.N+tk.S)
    file_listbox.config(yscrollcommand=scrollbar.set)

    app.mainloop()

if __name__ == "__main__":
    create_ui()
