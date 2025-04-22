# 🕷️ URL Extractor

**Recursive OSINT Recon Tool for Extracting and Filtering In-Scope URLs**

`url_extractor.py` is a modular Python recon tool designed to extract all accessible URLs from a target domain, recursively scanning directories, filtering by file type or keyword, and even analyzing JavaScript files for secrets or API patterns.

Built for red teamers, bug bounty hunters, and OSINT ops.

---

## 🚀 Features

- 🔁 **Recursive Directory Scanning** (with depth control)
- 🕵️ **Same-Origin Filtering** (stay in scope)
- 🧠 **Tag + Regex Based URL Extraction**
- 🎯 **Extension Filtering** (e.g. `.js`, `.php`)
- 🔍 **Path Pattern Matching** (e.g. `admin`, `debug`)
- 📄 **Export to File**
- 🧬 **JavaScript Secret Discovery** (`--analyze-js`)

---

## 🛠️ Installation

```bash
git clone https://github.com/MarcUrbano/URL-Extract.git
cd URL-Extract
pip install -r requirements.txt
python3 url_extract.py https://hackerone.com --depth 2 --match=assets --ext=svg
```

## Samples
![poc](https://github.com/user-attachments/assets/4bdf93bd-ca98-4a20-b6d3-9480e1ae8e0f)
![image](https://github.com/user-attachments/assets/918d451a-ea1b-4f48-9182-49cc1e3c776e)
![image](https://github.com/user-attachments/assets/ec7af43e-611e-4293-8b0d-21621353e1d5)



