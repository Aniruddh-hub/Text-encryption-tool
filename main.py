import customtkinter as ctk
from tkinter import messagebox
import base64
import hashlib
from Crypto.Cipher import AES, DES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad

# App UI configuration
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class EncryptionApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Text Encryption & Decryption Tool")
        self.geometry("700x750")
        
        # Add a title label
        self.title_label = ctk.CTkLabel(self, text="SecuriText", font=ctk.CTkFont(size=28, weight="bold"))
        self.title_label.pack(pady=(20, 10))
        
        # Setup Tabview for algorithms
        self.tabview = ctk.CTkTabview(self, width=650, height=200)
        self.tabview.pack(padx=20, pady=10, fill="both", expand=False)

        self.tabview.add("AES")
        self.tabview.add("DES")
        self.tabview.add("RSA")
        
        # --- AES Configuration ---
        self.aes_key_label = ctk.CTkLabel(self.tabview.tab("AES"), text="AES Secret Key / Passphrase:", font=ctk.CTkFont(weight="bold"))
        self.aes_key_label.pack(pady=(10, 0), anchor="w", padx=20)
        self.aes_key_entry = ctk.CTkEntry(self.tabview.tab("AES"), placeholder_text="Enter secret key", show="*", width=400)
        self.aes_key_entry.pack(pady=5, padx=20, anchor="w")
        self.aes_info = ctk.CTkLabel(self.tabview.tab("AES"), text="Your passphrase is hashed (SHA-256) to generate a secure AES key.", text_color="gray")
        self.aes_info.pack(pady=5, padx=20, anchor="w")
        
        # --- DES Configuration ---
        self.des_key_label = ctk.CTkLabel(self.tabview.tab("DES"), text="DES Secret Key / Passphrase:", font=ctk.CTkFont(weight="bold"))
        self.des_key_label.pack(pady=(10, 0), anchor="w", padx=20)
        self.des_key_entry = ctk.CTkEntry(self.tabview.tab("DES"), placeholder_text="Enter secret key", show="*", width=400)
        self.des_key_entry.pack(pady=5, padx=20, anchor="w")
        self.des_info = ctk.CTkLabel(self.tabview.tab("DES"), text="Your passphrase is hashed (MD5) to generate an 8-byte DES key.", text_color="gray")
        self.des_info.pack(pady=5, padx=20, anchor="w")
        
        # --- RSA Configuration ---
        self.rsa_header_frame = ctk.CTkFrame(self.tabview.tab("RSA"), fg_color="transparent")
        self.rsa_header_frame.pack(fill="x", padx=10, pady=5)
        
        self.rsa_info = ctk.CTkLabel(self.rsa_header_frame, text="RSA uses a public key to encrypt and a private key to decrypt.", font=ctk.CTkFont(weight="bold"))
        self.rsa_info.pack(side="left", padx=10)
        
        self.rsa_gen_btn = ctk.CTkButton(self.rsa_header_frame, text="Generate New Key Pair", width=150, command=self.generate_rsa_keys)
        self.rsa_gen_btn.pack(side="right", padx=10)
        
        self.rsa_keys_frame = ctk.CTkFrame(self.tabview.tab("RSA"), fg_color="transparent")
        self.rsa_keys_frame.pack(fill="x", padx=10, pady=5)
        
        self.pub_key_label = ctk.CTkLabel(self.rsa_keys_frame, text="Public Key (For Encryption):")
        self.pub_key_label.grid(row=0, column=0, padx=5, sticky="w")
        self.pub_key_text = ctk.CTkTextbox(self.rsa_keys_frame, height=80)
        self.pub_key_text.grid(row=1, column=0, padx=5, sticky="ew")
        
        self.priv_key_label = ctk.CTkLabel(self.rsa_keys_frame, text="Private Key (For Decryption):")
        self.priv_key_label.grid(row=0, column=1, padx=5, sticky="w")
        self.priv_key_text = ctk.CTkTextbox(self.rsa_keys_frame, height=80)
        self.priv_key_text.grid(row=1, column=1, padx=5, sticky="ew")
        
        self.rsa_keys_frame.columnconfigure(0, weight=1)
        self.rsa_keys_frame.columnconfigure(1, weight=1)

        # --- Inputs and Outputs ---
        self.input_label = ctk.CTkLabel(self, text="Input Text:", font=ctk.CTkFont(weight="bold"))
        self.input_label.pack(padx=20, anchor="w")
        self.input_text = ctk.CTkTextbox(self, height=100)
        self.input_text.pack(padx=20, pady=5, fill="x")
        
        # Setup Action Buttons
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.pack(pady=10)
        self.encrypt_btn = ctk.CTkButton(self.button_frame, text="Encrypt", font=ctk.CTkFont(weight="bold"), fg_color="#28a745", hover_color="#218838", command=self.encrypt_action)
        self.encrypt_btn.grid(row=0, column=0, padx=10)
        self.decrypt_btn = ctk.CTkButton(self.button_frame, text="Decrypt", font=ctk.CTkFont(weight="bold"), fg_color="#dc3545", hover_color="#c82333", command=self.decrypt_action)
        self.decrypt_btn.grid(row=0, column=1, padx=10)
        
        # Output Text
        self.output_label = ctk.CTkLabel(self, text="Output Result:", font=ctk.CTkFont(weight="bold"))
        self.output_label.pack(padx=20, anchor="w")
        self.output_text = ctk.CTkTextbox(self, height=120)
        self.output_text.pack(padx=20, pady=5, fill="x")

    def generate_rsa_keys(self):
        try:
            # Generate 2048 bit RSA keys
            key = RSA.generate(2048)
            private_key = key.export_key().decode('utf-8')
            public_key = key.publickey().export_key().decode('utf-8')
            
            self.pub_key_text.delete("0.0", "end")
            self.pub_key_text.insert("0.0", public_key)
            self.priv_key_text.delete("0.0", "end")
            self.priv_key_text.insert("0.0", private_key)
            messagebox.showinfo("Success", "RSA Key Pair Generated Successfully!\n(Keep your private key secret)")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate keys: {e}")

    def get_aes_key(self, passphrase: str) -> bytes:
        # Generate 32 bytes key for AES-256
        return hashlib.sha256(passphrase.encode('utf-8')).digest()

    def get_des_key(self, passphrase: str) -> bytes:
        # Generate 8 bytes key for DES
        return hashlib.md5(passphrase.encode('utf-8')).digest()[:8]

    def encrypt_action(self):
        algo = self.tabview.get()
        input_data = self.input_text.get("0.0", "end").strip()
        
        if not input_data:
            messagebox.showwarning("Warning", "Input text is empty.")
            return

        try:
            if algo == "AES":
                key_str = self.aes_key_entry.get()
                if not key_str:
                    messagebox.showwarning("Warning", "AES Secret Key is required.")
                    return
                key = self.get_aes_key(key_str)
                cipher = AES.new(key, AES.MODE_CBC)
                ct_bytes = cipher.encrypt(pad(input_data.encode('utf-8'), AES.block_size))
                iv = base64.b64encode(cipher.iv).decode('utf-8')
                ct = base64.b64encode(ct_bytes).decode('utf-8')
                # Combining IV and IV:Ciphertext
                result = f"{iv}:{ct}"
                
            elif algo == "DES":
                key_str = self.des_key_entry.get()
                if not key_str:
                    messagebox.showwarning("Warning", "DES Secret Key is required.")
                    return
                key = self.get_des_key(key_str)
                cipher = DES.new(key, DES.MODE_CBC)
                ct_bytes = cipher.encrypt(pad(input_data.encode('utf-8'), DES.block_size))
                iv = base64.b64encode(cipher.iv).decode('utf-8')
                ct = base64.b64encode(ct_bytes).decode('utf-8')
                result = f"{iv}:{ct}"
                
            elif algo == "RSA":
                pub_key_str = self.pub_key_text.get("0.0", "end").strip()
                if not pub_key_str:
                    messagebox.showwarning("Warning", "RSA Public Key is required for encryption.")
                    return
                recipient_key = RSA.import_key(pub_key_str)
                cipher_rsa = PKCS1_OAEP.new(recipient_key)
                try:
                    enc_data = cipher_rsa.encrypt(input_data.encode('utf-8'))
                    result = base64.b64encode(enc_data).decode('utf-8')
                except ValueError as ve:
                    messagebox.showerror("Error", f"Encryption failed.\nThe text you are trying to encrypt might be too long for the standard RSA algorithm. Tip: use AES for massive texts.\n\nDetails: {ve}")
                    return

            self.output_text.delete("0.0", "end")
            self.output_text.insert("0.0", result)
        except Exception as e:
            messagebox.showerror("Encryption Error", str(e))

    def decrypt_action(self):
        algo = self.tabview.get()
        input_data = self.input_text.get("0.0", "end").strip()
        
        if not input_data:
            messagebox.showwarning("Warning", "Input text is empty.")
            return

        try:
            if algo == "AES":
                key_str = self.aes_key_entry.get()
                if not key_str:
                    messagebox.showwarning("Warning", "AES Secret Key is required.")
                    return
                if ":" not in input_data:
                    messagebox.showerror("Error", "Invalid AES encrypted format. Expected 'IV:Ciphertext'")
                    return
                iv, ct = input_data.split(":", 1)
                iv = base64.b64decode(iv)
                ct = base64.b64decode(ct)
                key = self.get_aes_key(key_str)
                cipher = AES.new(key, AES.MODE_CBC, iv)
                pt = unpad(cipher.decrypt(ct), AES.block_size)
                result = pt.decode('utf-8')
                
            elif algo == "DES":
                key_str = self.des_key_entry.get()
                if not key_str:
                    messagebox.showwarning("Warning", "DES Secret Key is required.")
                    return
                if ":" not in input_data:
                    messagebox.showerror("Error", "Invalid DES encrypted format. Expected 'IV:Ciphertext'")
                    return
                iv, ct = input_data.split(":", 1)
                iv = base64.b64decode(iv)
                ct = base64.b64decode(ct)
                key = self.get_des_key(key_str)
                cipher = DES.new(key, DES.MODE_CBC, iv)
                pt = unpad(cipher.decrypt(ct), DES.block_size)
                result = pt.decode('utf-8')
                
            elif algo == "RSA":
                priv_key_str = self.priv_key_text.get("0.0", "end").strip()
                if not priv_key_str:
                    messagebox.showwarning("Warning", "RSA Private Key is required for decryption.")
                    return
                private_key = RSA.import_key(priv_key_str)
                cipher_rsa = PKCS1_OAEP.new(private_key)
                try:
                    enc_data = base64.b64decode(input_data)
                    dec_data = cipher_rsa.decrypt(enc_data)
                    result = dec_data.decode('utf-8')
                except Exception as ex:
                    messagebox.showerror("Error", f"Decryption failed. Ensure the text isn't corrupted and the private key is correct.\n\nDetails: {ex}")
                    return

            self.output_text.delete("0.0", "end")
            self.output_text.insert("0.0", result)
        except Exception as e:
            messagebox.showerror("Decryption Error", f"Decryption failed. Please check keys and input format.\n\n{e}")

if __name__ == "__main__":
    app = EncryptionApp()
    app.mainloop()
