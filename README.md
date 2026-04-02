<div align="center">
  <h1>🔐 Text Encryption & Decryption Tool</h1>
  <p>A cryptographic utility to secure sensitive data using industry-standard symmetric and asymmetric algorithms.</p>
</div>

<br>

## 📖 About the Project

The **Text Encryption Tool** is a security-focused application designed to protect sensitive text from unauthorized access. It allows users to seamlessly encrypt plaintext into ciphertext and decrypt it back using their choice of cryptographic algorithms. 

This project was built to explore and implement fundamental cybersecurity concepts, specifically focusing on data confidentiality and integrity.

<br>

## ✨ Features

- **🔄 Two-Way Cryptography:** Full support for both encrypting messages and decrypting them back to their original form using the correct keys.
- **🛡️ Multiple Algorithm Support:** Implements three distinct cryptographic standards:
  - **AES (Advanced Encryption Standard):** The current industry standard for fast, highly secure symmetric encryption.
  - **RSA (Rivest–Shamir–Adleman):** Public-key (asymmetric) encryption, allowing for secure key exchange and data transmission.
  - **DES (Data Encryption Standard):** A legacy symmetric-key algorithm, included for educational purposes and cryptographic history comparison.
- **🔑 Key Management:** Handles the generation, input, and application of cryptographic keys (public/private pairs for RSA, secret keys for AES/DES).
- **🖥️ Clean Interface:** Designed to be straightforward and user-friendly, abstracting complex math behind a simple encrypt/decrypt workflow.

<br>

## 🧠 Cryptographic Concepts Applied

- **Symmetric Encryption (AES, DES):** Uses a single shared secret key for both encryption and decryption. Ideal for bulk data.
- **Asymmetric Encryption (RSA):** Uses a mathematically linked key pair (Public and Private). Ideal for secure communication channels.

<br>

## 🛠️ Tech Stack
*(Note: Adjust these depending on the language you used)*
- **Language:** Python / Java / C++
- **Libraries:** `cryptography` / `PyCryptodome` (Python) OR `javax.crypto` (Java)

<br>

## 🚀 Getting Started

### Prerequisites
Ensure you have the required language environment installed on your machine.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Aniruddh-hub/text-encryption-tool.git
Navigate to the directory:
cd text-encryption-tool<br>
Install dependencies (if applicable):
pip install -r requirements.txt<br>
Run the application:
python main.py
<br>
⚠️ Security Disclaimer
This project is primarily for educational purposes. While it uses real cryptographic algorithms, it is recommended to use vetted, enterprise-grade key management systems (KMS) when handling actual highly classified or production data.
<br>

👨‍💻 Author
Aniruddha Mitra
GitHub: Aniruddh-hub
LinkedIn: Aniruddha Mitra
