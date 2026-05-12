#!/usr/bin/env python3
"""
GUI for Secure File Sharing System
Pure XOR with Chaotic Key Generation + High Entropy Steganography
Reworked to use customtkinter for a futuristic dark-mode UI
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
from file_qr_workflow import file_to_qr_with_hidden_key, qr_to_file_with_extracted_key


class SecureFileSharingGUI:
    def __init__(self, root):
        # configure customtkinter appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.root = root
        self.root.title("Secure File Sharing - Chaotic XOR Encryption")
        self.root.geometry("900x640")
        self.root.minsize(700, 520)

        # Use CTk root
        # wrap root in ctk style by replacing frame
        self.container = ctk.CTkFrame(self.root, fg_color="#0f1115")
        self.container.pack(fill="both", expand=True, padx=0, pady=0)

        # Initialize animation flags
        self._encrypt_anim = False
        self._decrypt_anim = False

        # Create main layout
        self.create_main_frame()

    def create_main_frame(self):
        """Create the main GUI layout using customtkinter widgets"""
        # slightly larger top frame and outer padding for a more spacious look
        top_frame = ctk.CTkFrame(self.container, fg_color="#0b0c0f", corner_radius=10)
        top_frame.pack(fill="x", padx=20, pady=(16, 14))

        # make the main title a bit larger
        title = ctk.CTkLabel(top_frame, text="🔐 Secure File Sharing", font=ctk.CTkFont(size=22, weight="bold"))
        title.pack(anchor="w", padx=12, pady=(12, 4))

        subtitle = ctk.CTkLabel(
            top_frame,
            text="Chaotic XOR Encryption + High Entropy Steganography",
            font=ctk.CTkFont(size=13),
            text_color="#9aa4b2"
        )
        subtitle.pack(anchor="w", padx=12, pady=(0, 12))

        # Tab view — let it fully expand (bigger tab area)
        self.tabview = ctk.CTkTabview(self.container)
        self.tabview.pack(fill="both", expand=True, padx=18, pady=18)

        # Add tabs
        self.tabview.add("Encrypt")
        self.tabview.add("Decrypt")
        self.tabview.add("About")

        # Build each tab
        self._build_encrypt_tab(self.tabview.tab("Encrypt"))
        self._build_decrypt_tab(self.tabview.tab("Decrypt"))
        self._build_info_tab(self.tabview.tab("About"))

        # status bar
        status_frame = ctk.CTkFrame(self.container, fg_color="#0b0c0f", height=60)
        status_frame.pack(fill="x", padx=18, pady=(10, 0))
        self.status_var = tk.StringVar(value="Ready")
        status_label = ctk.CTkLabel(status_frame, textvariable=self.status_var, anchor="w",
                                    font=ctk.CTkFont(size=11), text_color="#8f9aa8")
        status_label.pack(fill="both", padx=12)

    def _build_encrypt_tab(self, frame):
        # make columns flexible so controls expand; increase spacing and fonts for "bigger" feeling
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        pad_x = 16

        heading = ctk.CTkLabel(frame, text="Encrypt File and Create QR Code",
                               font=ctk.CTkFont(size=16, weight="bold"))
        heading.grid(row=0, column=0, columnspan=3, sticky="w", padx=pad_x, pady=(12, 10))

        # File selection
        ctk.CTkLabel(frame, text="Select File:").grid(row=1, column=0, sticky="w", padx=pad_x, pady=(6, 2))
        self.input_file_var = tk.StringVar()
        # slightly taller entry for better readability
        input_entry = ctk.CTkEntry(frame, textvariable=self.input_file_var, height=30)
        input_entry.grid(row=2, column=0, columnspan=2, sticky="we", padx=pad_x, pady=(0, 10))
        browse_btn = ctk.CTkButton(frame, text="Browse", width=140, height=32, command=self.browse_input_file)
        browse_btn.grid(row=2, column=2, padx=(0, pad_x), pady=(0, 8))

        # QR output
        ctk.CTkLabel(frame, text="QR Code Output:").grid(row=3, column=0, sticky="w", padx=pad_x, pady=(6, 2))
        self.output_qr_var = tk.StringVar()
        output_entry = ctk.CTkEntry(frame, textvariable=self.output_qr_var, height=30)
        output_entry.grid(row=4, column=0, columnspan=2, sticky="we", padx=pad_x, pady=(0, 10))
        ctk.CTkButton(frame, text="Browse", width=140, height=32, command=self.browse_output_qr).grid(
            row=4, column=2, padx=(0, pad_x), pady=(0, 8)
        )

        # Password
        ctk.CTkLabel(frame, text="Password:").grid(row=5, column=0, sticky="w", padx=pad_x, pady=(6, 2))
        self.password_var = tk.StringVar()
        ctk.CTkEntry(frame, textvariable=self.password_var, show="*", height=30).grid(
            row=6, column=0, columnspan=3, sticky="we", padx=pad_x, pady=(0, 14)
        )

        # Action button
        self.encrypt_btn = ctk.CTkButton(frame, text="🔒 Encrypt & Create QR Code", fg_color="#1f6feb",
                                         hover_color="#1454b5", command=self.encrypt_file, width=360,
                                         font=ctk.CTkFont(size=12, weight="bold"), height=38)
        self.encrypt_btn.grid(row=7, column=0, columnspan=3, padx=pad_x, pady=(6, 12))

        # Progress visual (animated)
        self.encrypt_progress = ctk.CTkProgressBar(frame)
        self.encrypt_progress.grid(row=8, column=0, columnspan=3, sticky="we", padx=pad_x, pady=(8, 8))
        self.encrypt_result = ctk.CTkLabel(frame, text="", text_color="#27ae60", font=ctk.CTkFont(size=11))
        self.encrypt_result.grid(row=9, column=0, columnspan=3, padx=pad_x, pady=(4, 12))

    def _build_decrypt_tab(self, frame):
        # make columns flexible so controls expand; increase spacing and fonts
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        pad_x = 16

        heading = ctk.CTkLabel(frame, text="Decrypt File from QR Code",
                               font=ctk.CTkFont(size=16, weight="bold"))
        heading.grid(row=0, column=0, columnspan=3, sticky="w", padx=pad_x, pady=(12, 10))

        # QR selection
        ctk.CTkLabel(frame, text="Select QR Code:").grid(row=1, column=0, sticky="w", padx=pad_x, pady=(6, 2))
        self.input_qr_var = tk.StringVar()
        in_qr_entry = ctk.CTkEntry(frame, textvariable=self.input_qr_var, height=30)
        in_qr_entry.grid(row=2, column=0, columnspan=2, sticky="we", padx=pad_x, pady=(0, 10))
        ctk.CTkButton(frame, text="Browse", width=140, height=32, command=self.browse_input_qr).grid(
            row=2, column=2, padx=(0, pad_x), pady=(0, 8)
        )

        # Output file
        ctk.CTkLabel(frame, text="Decrypted File Output:").grid(row=3, column=0, sticky="w", padx=pad_x, pady=(6, 2))
        self.output_file_var = tk.StringVar()
        out_entry = ctk.CTkEntry(frame, textvariable=self.output_file_var, height=30)
        out_entry.grid(row=4, column=0, columnspan=2, sticky="we", padx=pad_x, pady=(0, 10))
        ctk.CTkButton(frame, text="Browse", width=140, height=32, command=self.browse_output_file).grid(
            row=4, column=2, padx=(0, pad_x), pady=(0, 8)
        )

        info_label = ctk.CTkLabel(frame, text="ℹ️ Password will be automatically extracted from QR code",
                                   text_color="#9aa4b2")
        info_label.grid(row=5, column=0, columnspan=3, sticky="w", padx=pad_x, pady=(6, 12))

        # Action button
        self.decrypt_btn = ctk.CTkButton(frame, text="🔓 Decrypt File", fg_color="#1f6feb",
                                          hover_color="#1454b5", command=self.decrypt_file, width=320,
                                          font=ctk.CTkFont(size=12, weight="bold"), height=38)
        self.decrypt_btn.grid(row=6, column=0, columnspan=3, padx=pad_x, pady=(6, 12))

        # Progress visual
        self.decrypt_progress = ctk.CTkProgressBar(frame)
        self.decrypt_progress.grid(row=7, column=0, columnspan=3, sticky="we", padx=pad_x, pady=(8, 8))
        self.decrypt_result = ctk.CTkLabel(frame, text="", text_color="#27ae60", font=ctk.CTkFont(size=11))
        self.decrypt_result.grid(row=8, column=0, columnspan=3, padx=pad_x, pady=(4, 12))

    def _build_info_tab(self, frame):
        pad_x = 16
        heading = ctk.CTkLabel(frame, text="System Information", font=ctk.CTkFont(size=16, weight="bold"))
        heading.grid(row=0, column=0, sticky="w", padx=pad_x, pady=(12, 8))

        info_text = (
            "🔐 Secure File Sharing System\n\n"
            "TECHNOLOGIES USED:\n"
            "• Chaotic Key Generation: Logistic Map (r=3.99)\n"
            "• XOR Encryption: Pure XOR with key repetition\n"
            "• High Entropy Steganography: Block-level embedding\n\n"
            "HOW IT WORKS:\n"
            "1. Password → Chaotic Key (256 bytes)\n"
            "2. File → XOR Encrypted with Chaotic Key\n"
            "3. Encrypted Data → QR Code\n"
            "4. Password → Hidden in High-Entropy Blocks of QR Image\n\n"
            "USAGE:\n"
            "• Encrypt: Select file, set password, create QR code\n"
            "• Decrypt: Select QR code, extract file automatically\n\n"
            "FILE SUPPORT:\n"
            "• Any file type (text, images, documents, etc.)\n"
            "• Files of any size\n"
        )

        info_box = ctk.CTkTextbox(frame, width=820, height=360, fg_color="#0b0c0f", wrap="word")
        info_box.grid(row=1, column=0, padx=pad_x, pady=(4, 12))
        info_box.insert("0.0", info_text)
        info_box.configure(state="disabled")

    # File dialogs (use tkinter filedialog)
    def browse_input_file(self):
        filename = filedialog.askopenfilename(title="Select File to Encrypt", filetypes=[("All Files", "*.*")])
        if filename:
            self.input_file_var.set(filename)

    def browse_output_qr(self):
        filename = filedialog.asksaveasfilename(title="Save QR Code As", defaultextension=".png",
                                                filetypes=[("PNG Files", "*.png"), ("All Files", "*.*")])
        if filename:
            self.output_qr_var.set(filename)

    def browse_input_qr(self):
        filename = filedialog.askopenfilename(
            title="Select QR Code to Decrypt",
            filetypes=[("PNG Files", "*.png"), ("Image Files", "*.jpg *.jpeg *.png *.bmp"), ("All Files", "*.*")]
        )
        if filename:
            self.input_qr_var.set(filename)

    def browse_output_file(self):
        filename = filedialog.asksaveasfilename(title="Save Decrypted File As", filetypes=[("All Files", "*.*")])
        if filename:
            self.output_file_var.set(filename)

    # Progress animation helpers
    def _animate_progress(self, progress_widget, attr_name):
        if not getattr(self, attr_name):
            progress_widget.set(0.0)
            return
        # cycle the progress bar value
        cur = getattr(progress_widget, "_val", 0.0)
        cur += 0.02
        if cur > 1.0:
            cur = 0.0
        progress_widget._val = cur
        progress_widget.set(cur)
        self.root.after(40, lambda: self._animate_progress(progress_widget, attr_name))

    def _start_progress(self, which):
        if which == "encrypt":
            self._encrypt_anim = True
            self.encrypt_progress._val = 0.0
            self._animate_progress(self.encrypt_progress, "_encrypt_anim")
        else:
            self._decrypt_anim = True
            self.decrypt_progress._val = 0.0
            self._animate_progress(self.decrypt_progress, "_decrypt_anim")

    def _stop_progress(self, which):
        if which == "encrypt":
            self._encrypt_anim = False
            self.encrypt_progress.set(1.0)
        else:
            self._decrypt_anim = False
            self.decrypt_progress.set(1.0)

    # Encryption flow
    def encrypt_file(self):
        if not self.input_file_var.get():
            messagebox.showerror("Error", "Please select a file to encrypt")
            return
        if not self.output_qr_var.get():
            messagebox.showerror("Error", "Please specify QR code output location")
            return
        if not self.password_var.get():
            messagebox.showerror("Error", "Please enter a password")
            return

        self.encrypt_btn.configure(state="disabled")
        self.encrypt_result.configure(text="")
        self.status_var.set("Encrypting...")
        self._start_progress("encrypt")

        threading.Thread(target=self._encrypt_worker, daemon=True).start()

    def _encrypt_worker(self):
        try:
            file_to_qr_with_hidden_key(self.input_file_var.get(), self.output_qr_var.get(), self.password_var.get())
            self.root.after(0, self._encrypt_success)
        except Exception as e:
            self.root.after(0, lambda: self._encrypt_error(str(e)))

    def _encrypt_success(self):
        self._stop_progress("encrypt")
        self.encrypt_btn.configure(state="normal")
        self.encrypt_result.configure(text="✅ Success! QR code created with hidden password", text_color="#27ae60")
        self.status_var.set("Encryption completed successfully")
        messagebox.showinfo("Success", f"File encrypted and QR code created!\n\nSaved to: {self.output_qr_var.get()}")

    def _encrypt_error(self, error_msg):
        self._stop_progress("encrypt")
        self.encrypt_btn.configure(state="normal")
        self.encrypt_result.configure(text=f"❌ Error: {error_msg}", text_color="#ff726f")
        self.status_var.set("Encryption failed")
        messagebox.showerror("Encryption Error", f"Encryption failed:\n{error_msg}")

    # Decryption flow
    def decrypt_file(self):
        if not self.input_qr_var.get():
            messagebox.showerror("Error", "Please select a QR code to decrypt")
            return
        if not self.output_file_var.get():
            messagebox.showerror("Error", "Please specify decrypted file output location")
            return

        self.decrypt_btn.configure(state="disabled")
        self.decrypt_result.configure(text="")
        self.status_var.set("Decrypting...")
        self._start_progress("decrypt")

        threading.Thread(target=self._decrypt_worker, daemon=True).start()

    def _decrypt_worker(self):
        try:
            qr_to_file_with_extracted_key(self.input_qr_var.get(), self.output_file_var.get())
            self.root.after(0, self._decrypt_success)
        except Exception as e:
            self.root.after(0, lambda: self._decrypt_error(str(e)))

    def _decrypt_success(self):
        self._stop_progress("decrypt")
        self.decrypt_btn.configure(state="normal")
        self.decrypt_result.configure(text="✅ Success! File decrypted", text_color="#27ae60")
        self.status_var.set("Decryption completed successfully")
        messagebox.showinfo("Success", f"File decrypted successfully!\n\nSaved to: {self.output_file_var.get()}")

    def _decrypt_error(self, error_msg):
        self._stop_progress("decrypt")
        self.decrypt_btn.configure(state="normal")
        self.decrypt_result.configure(text=f"❌ Error: {error_msg}", text_color="#ff726f")
        self.status_var.set("Decryption failed")
        messagebox.showerror("Decryption Error", f"Decryption failed:\n{error_msg}")


def main():
    root = ctk.CTk()
    app = SecureFileSharingGUI(root)

    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")

    root.mainloop()


if __name__ == "__main__":
    main()
