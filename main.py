"""
Simple Python Dictionary with Tkinter GUI
Author: ItsDanielX
License: MIT
"""

import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

DATA_FILE = "dictionary.json"

class SimpleDictionaryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simple Dictionary — Tkinter")
        self.geometry("760x480")
        self.minsize(640, 400)

        self.data = {}
        self.load_data()

        self.create_widgets()
        self.refresh_word_list()

    def create_widgets(self):
        # Left frame: word list + search
        left = ttk.Frame(self)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=8, pady=8)

        search_frame = ttk.Frame(left)
        search_frame.pack(fill=tk.X)

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        search_entry.bind("<KeyRelease>", lambda e: self.on_search())

        search_btn = ttk.Button(search_frame, text="Search", command=self.on_search)
        search_btn.pack(side=tk.LEFT, padx=4)

        # Words listbox
        self.word_listbox = tk.Listbox(left, width=30)
        self.word_listbox.pack(fill=tk.BOTH, expand=True, pady=(8,0))
        self.word_listbox.bind("<<ListboxSelect>>", self.on_select_word)

        # Buttons under list
        list_btns = ttk.Frame(left)
        list_btns.pack(fill=tk.X, pady=6)

        add_btn = ttk.Button(list_btns, text="New", command=self.new_word_dialog)
        add_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        edit_btn = ttk.Button(list_btns, text="Edit", command=self.edit_selected)
        edit_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        del_btn = ttk.Button(list_btns, text="Delete", command=self.delete_selected)
        del_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        # Right frame: details
        right = ttk.Frame(self)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)

        top_right = ttk.Frame(right)
        top_right.pack(fill=tk.X)

        ttk.Label(top_right, text="Word:").pack(anchor=tk.W)
        self.word_var = tk.StringVar()
        self.word_entry = ttk.Entry(top_right, textvariable=self.word_var)
        self.word_entry.pack(fill=tk.X)

        ttk.Label(right, text="Definition:").pack(anchor=tk.W, pady=(6,0))
        self.definition_text = tk.Text(right, wrap=tk.WORD, height=12)
        self.definition_text.pack(fill=tk.BOTH, expand=True)

        # Bottom buttons
        bottom = ttk.Frame(right)
        bottom.pack(fill=tk.X, pady=8)

        save_btn = ttk.Button(bottom, text="Save / Update", command=self.save_current)
        save_btn.pack(side=tk.LEFT, padx=4)
        clear_btn = ttk.Button(bottom, text="Clear", command=self.clear_inputs)
        clear_btn.pack(side=tk.LEFT, padx=4)

        file_ops = ttk.Frame(bottom)
        file_ops.pack(side=tk.RIGHT)
        import_btn = ttk.Button(file_ops, text="Import JSON", command=self.import_json)
        import_btn.pack(side=tk.LEFT, padx=2)
        export_btn = ttk.Button(file_ops, text="Export JSON", command=self.export_json)
        export_btn.pack(side=tk.LEFT, padx=2)
        savefile_btn = ttk.Button(file_ops, text="Save File", command=self.save_data)
        savefile_btn.pack(side=tk.LEFT, padx=2)

        # Keyboard bindings
        self.bind_all("<Control-s>", lambda e: self.save_data())
        self.bind_all("<Control-f>", lambda e: search_entry.focus_set())

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.data = json.load(f)
            except Exception:
                messagebox.showwarning("Warning", f"Could not read {DATA_FILE}. Starting empty.")
                self.data = {}
        else:
            self.data = {}

    def save_data(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Saved", f"Saved to {DATA_FILE}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

    def refresh_word_list(self, filter_text=""):
        words = sorted(self.data.keys(), key=lambda s: s.lower())
        if filter_text:
            words = [w for w in words if filter_text.lower() in w.lower()]
        self.word_listbox.delete(0, tk.END)
        for w in words:
            self.word_listbox.insert(tk.END, w)

    def on_search(self):
        q = self.search_var.get().strip()
        self.refresh_word_list(q)

    def on_select_word(self, event=None):
        sel = self.word_listbox.curselection()
        if not sel:
            return
        word = self.word_listbox.get(sel[0])
        self.show_word(word)

    def show_word(self, word):
        self.word_var.set(word)
        self.definition_text.delete(1.0, tk.END)
        self.definition_text.insert(tk.END, self.data.get(word, ""))

    def clear_inputs(self):
        self.word_var.set("")
        self.definition_text.delete(1.0, tk.END)
        self.word_listbox.selection_clear(0, tk.END)

    def new_word_dialog(self):
        self.clear_inputs()
        self.word_entry.focus_set()

    def save_current(self):
        word = self.word_var.get().strip()
        if not word:
            messagebox.showwarning("Validation", "Please enter a word.")
            return
        definition = self.definition_text.get(1.0, tk.END).strip()
        if not definition:
            if not messagebox.askyesno("Empty definition", "Definition is empty. Save anyway?"):
                return
        self.data[word] = definition
        self.refresh_word_list(self.search_var.get().strip())
        self.save_data()

    def edit_selected(self):
        sel = self.word_listbox.curselection()
        if not sel:
            messagebox.showinfo("Info", "Select a word from the list first.")
            return
        word = self.word_listbox.get(sel[0])
        self.show_word(word)
        self.word_entry.focus_set()

    def delete_selected(self):
        sel = self.word_listbox.curselection()
        if not sel:
            messagebox.showinfo("Info", "Select a word from the list first.")
            return
        word = self.word_listbox.get(sel[0])
        if messagebox.askyesno("Confirm", f"Delete '{word}'?"):
            self.data.pop(word, None)
            self.refresh_word_list(self.search_var.get().strip())
            self.clear_inputs()
            self.save_data()

    def import_json(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                imported = json.load(f)
            if not isinstance(imported, dict):
                messagebox.showerror("Error", "Imported JSON must be an object mapping words to definitions.")
                return
            self.data.update(imported)
            self.refresh_word_list()
            messagebox.showinfo("Imported", f"Imported {len(imported)} entries from {os.path.basename(path)}")
            self.save_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import: {e}")

    def export_json(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Exported", f"Exported {len(self.data)} entries to {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {e}")


if __name__ == "__main__":
    app = SimpleDictionaryApp()
    app.mainloop()