import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import pyperclip
import os
import subprocess
import platform

class PythonPad:
    def __init__(self, root):
        self.root = root
        self.root.title("PythonPad")
        self.root.geometry("600x400")
        
        # Text widget
        self.text_area = tk.Text(self.root, wrap='word', undo=True)
        self.text_area.pack(expand=True, fill='both')
        
        # Menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)
        
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_program)
        
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.undo)
        self.edit_menu.add_command(label="Redo", command=self.redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut)
        self.edit_menu.add_command(label="Copy", command=self.copy)
        self.edit_menu.add_command(label="Paste", command=self.paste)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", command=self.select_all)
        self.edit_menu.add_command(label="Print", command=self.print_file)
        
        # Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_help)
        
        # Bind keyboard shortcuts
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-o>", lambda e: self.open_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-Shift-S>", lambda e: self.save_as_file())
        self.root.bind("<Control-q>", lambda e: self.exit_program())
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())
        self.root.bind("<Control-x>", lambda e: self.cut())
        self.root.bind("<Control-c>", lambda e: self.copy())
        self.root.bind("<Control-v>", lambda e: self.paste())
        self.root.bind("<Control-a>", lambda e: self.select_all())

        self.filename = None
        self.clipboard = None
    
    def new_file(self):
        if self.text_area.get("1.0", "end-1c"):
            response = messagebox.askyesnocancel("Save File", "Do you want to save changes?")
            if response:
                self.save_file()
            elif response is None:
                return
        self.text_area.delete("1.0", "end")
        self.filename = None
        self.root.title("PythonPad - Untitled")
    
    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.delete("1.0", "end")
                self.text_area.insert("1.0", content)
            self.filename = file_path
            self.root.title(f"PythonPad - {os.path.basename(file_path)}")
    
    def save_file(self):
        if not self.filename:
            self.save_as_file()
        else:
            with open(self.filename, 'w') as file:
                file.write(self.text_area.get("1.0", "end-1c"))
    
    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_area.get("1.0", "end-1c"))
            self.filename = file_path
            self.root.title(f"PythonPad - {os.path.basename(file_path)}")
    
    def exit_program(self):
        if self.text_area.get("1.0", "end-1c"):
            response = messagebox.askyesnocancel("Save File", "Do you want to save changes?")
            if response:
                self.save_file()
            elif response is None:
                return
        self.root.quit()
    
    def undo(self):
        try:
            self.text_area.edit_undo()
        except tk.TclError:
            pass
    
    def redo(self):
        try:
            self.text_area.edit_redo()
        except tk.TclError:
            pass
    
    def cut(self, event=None):
        try:
            self.copy()  # Cutting is just copying and then deleting the selection
            self.text_area.delete("sel.first", "sel.last")
        except tk.TclError:
            messagebox.showwarning("No Selection", "Please select text to cut.")
    
    def copy(self, event=None):
        try:
            self.clipboard = self.text_area.get("sel.first", "sel.last")
            pyperclip.copy(self.clipboard)  # Also copy to system clipboard
        except tk.TclError:
            messagebox.showwarning("No Selection", "Please select text to copy.")
    
    def paste(self, event=None):
        try:
            text_to_insert = pyperclip.paste()  # Get the text from system clipboard
            self.text_area.insert("insert", text_to_insert)
        except Exception as e:
            messagebox.showerror("Error", f"Error pasting text: {e}")
    
    def select_all(self, event=None):
        self.text_area.tag_add("sel", "1.0", "end")
        self.text_area.mark_set("insert", "end")
        self.text_area.see("insert")
    
    def print_file(self):
        if platform.system() == "Windows":
            # Use the built-in print dialog in Windows
            try:
                content = self.text_area.get("1.0", "end-1c")
                subprocess.run(["notepad", "/p", content])  # Placeholder for printing
            except Exception as e:
                messagebox.showerror("Error", f"Error printing file: {e}")
        elif platform.system() == "Linux":
            # Linux implementation for printing (CUPS or lp command can be used)
            try:
                content = self.text_area.get("1.0", "end-1c")
                with open("/tmp/temp_print.txt", "w") as f:
                    f.write(content)
                subprocess.run(["lp", "/tmp/temp_print.txt"])  # Placeholder for printing
            except Exception as e:
                messagebox.showerror("Error", f"Error printing file: {e}")
        else:
            messagebox.showwarning("Not Supported", "Printing is not supported on this platform.")
    
    def show_help(self):
        help_text = """PythonPad Help:

    - File Menu:
        * New: Create a new document.
        * Open: Open an existing document.
        * Save: Save the current document.
        * Save As: Save the document under a new name.
        * Exit: Close the editor.

    - Edit Menu:
        * Undo: Undo the last action.
        * Redo: Redo the last undone action.
        * Cut: Cut the selected text.
        * Copy: Copy the selected text.
        * Paste: Paste text from the clipboard.
        * Select All: Select all text in the document.
        * Print: Print the current document.

    - Keyboard Shortcuts:
        * Ctrl+N: New file
        * Ctrl+O: Open file
        * Ctrl+S: Save file
        * Ctrl+Shift+S: Save As
        * Ctrl+Q: Exit
        * Ctrl+Z: Undo
        * Ctrl+Y: Redo
        * Ctrl+X: Cut
        * Ctrl+C: Copy
        * Ctrl+V: Paste
        * Ctrl+A: Select All

    For further assistance, contact the developer."""
        
        messagebox.showinfo("Help", help_text)

# Initialize the Tkinter window and the application
root = tk.Tk()
app = PythonPad(root)
root.mainloop()
