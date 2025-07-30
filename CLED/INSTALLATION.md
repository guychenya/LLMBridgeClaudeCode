# CLED Installation & User Guide

CLED (Claude LLM Environment Dispatcher) is a cross-platform visual installer and CLI for setting up your LLMBridgeClaudeCode environment. This guide walks you through every step.

---

## 1. Prerequisites
- **Python 3.8+** (https://www.python.org/downloads/)
- **pip** (comes with Python)
- **Ollama** (https://ollama.com/download)
- **Internet connection**
- **Disk space:** At least 10GB free (more if you want large models)

---

## 2. Setup Steps

### a. Clone the Repository
```bash
git clone <your-repo-url>
cd LLMBridgeClaudeCode
```

### b. Enter the CLED Directory
```bash
cd CLED
```

### c. (Optional) Create a Python Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

### d. Install Requirements
```bash
pip install -r requirements.txt
```

---

## 3. Using the Visual Installer

### a. Launch the Installer
```bash
python3 cled_installer.py
```

### b. Follow the Wizard Steps
- **System Check:** Verifies Python, pip, Ollama, disk space, and network.
- **Model Selection:** Choose which models to install (shows disk usage).
- **Python Environment:** Sets up `.venv` and installs requirements.
- **Connectivity Test:** Checks Ollama and model presence before download.
- **Install & Configure:** Downloads models, writes `.env`.
- **Finish:** Optionally start the server.

### c. Troubleshooting
- If a step fails, read the error message and fix the issue (e.g., install missing dependencies, free up disk space, start Ollama).
- You can re-run the installer at any time.

---

## 4. Using the CLI

### a. Install/Serve via CLI
```bash
python3 cled_cli.py install   # Launches the visual installer
python3 cled_cli.py serve     # Starts the server
python3 cled_cli.py ollama    # Shows Ollama models
```

---

## 5. Packaging as a Standalone App

To create a double-clickable app (macOS, Windows, Linux):
```bash
pip install pyinstaller
pyinstaller --onefile --windowed cled_installer.py
```
The resulting app will be in the `dist/` folder.

---

## 6. FAQ

**Q: Do I need to install all models?**  
A: No. Select only the models you want. The installer will warn about disk usage.

**Q: Can I re-run the installer?**  
A: Yes, you can run it as many times as you like.

**Q: Where is the configuration stored?**  
A: In the `.env` file in your project root.

**Q: How do I update models?**  
A: Use the installer or run `ollama pull <model>` manually.

---

## 7. Support
- For issues, open an issue on GitHub or contact the project maintainer.