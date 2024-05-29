import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
import model_loader
import text_processor

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        # Процесс чтения и обработки текста с использованием активной модели
        processed_text, found_effects = text_processor.process_text(file_path)
        if not found_effects:
            messagebox.showinfo("Result", "Физико-технические эффекты не найдены")
        else:
            text_area.config(state=tk.NORMAL)
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, processed_text)
            text_area.config(state=tk.DISABLED)
            save_button.config(state=tk.NORMAL)

def save_results():
    output_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if output_file_path:
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(text_area.get(1.0, tk.END))
        messagebox.showinfo("Success", "The processed text has been saved successfully.")

root = tk.Tk()
root.title("Text Processing Tool")

tk.Label(root, text="Выбор модели:").pack()

model_var = tk.StringVar(value="modelT5_large")
tk.Radiobutton(root, text="T5", variable=model_var, value="modelT5_large", command=lambda: model_loader.set_active_model("modelT5_large")).pack(anchor=tk.CENTER)
tk.Radiobutton(root, text="keyT5", variable=model_var, value="keyT5-custom_Large", command=lambda: model_loader.set_active_model("keyT5-custom_Large")).pack(anchor=tk.CENTER)
tk.Radiobutton(root, text="bert", variable=model_var, value="bert", command=lambda: model_loader.set_active_model("bert")).pack(anchor=tk.CENTER)

load_button = tk.Button(root, text="Load", command=load_file)
load_button.pack(pady=10, padx=10)

text_area = scrolledtext.ScrolledText(root, width=80, height=20, state=tk.DISABLED)
text_area.pack(padx=10, pady=10)

save_button = tk.Button(root, text="Save", command=save_results, state=tk.DISABLED)
save_button.pack(pady=10)

root.mainloop()
