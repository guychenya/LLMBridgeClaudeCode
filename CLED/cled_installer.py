import sys
import os
import shutil
import subprocess
import socket
import requests
from PyQt5.QtWidgets import (
    QApplication, QWizard, QWizardPage, QLabel, QVBoxLayout, QPushButton, QCheckBox, QLineEdit, QFileDialog, QMessageBox, QProgressBar, QHBoxLayout
)
from PyQt5.QtCore import Qt

CLED_LOGO = None  # Placeholder for future branding

# --- Utility Functions ---
def check_python():
    return sys.version_info >= (3, 8)

def check_pip():
    try:
        subprocess.check_output([sys.executable, "-m", "pip", "--version"])
        return True
    except Exception:
        return False

def check_ollama():
    return shutil.which("ollama") is not None

def check_disk_space(required_gb=10):
    stat = shutil.disk_usage(os.getcwd())
    return stat.free > required_gb * 1024 * 1024 * 1024

def check_network():
    try:
        requests.get("https://ollama.com", timeout=3)
        return True
    except Exception:
        return False

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) != 0

def check_venv():
    return os.path.exists(".venv")

def check_model(model):
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=2)
        if r.status_code == 200:
            tags = r.json().get("models", [])
            return any(model in m["name"] for m in tags)
    except Exception:
        pass
    return False

# --- Wizard Pages ---
class WelcomePage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Welcome to CLED Installer")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("This wizard will help you set up CLED (Claude LLM Environment Dispatcher)."))
        layout.addWidget(QLabel(""))
        layout.addWidget(QLabel("CLED will guide you through environment setup, model selection, and configuration."))
        self.setLayout(layout)

class SystemCheckPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("System Check")
        self.status_label = QLabel()
        self.retry_btn = QPushButton("Re-check")
        self.retry_btn.clicked.connect(self.check_all)
        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.retry_btn)
        self.setLayout(layout)
        self.complete = False
        self.check_all()

    def check_all(self):
        python_ok = check_python()
        pip_ok = check_pip()
        ollama_ok = check_ollama()
        disk_ok = check_disk_space()
        net_ok = check_network()
        msg = []
        if python_ok: msg.append("✔ Python 3.8+ found")
        else: msg.append("❌ Python 3.8+ not found")
        if pip_ok: msg.append("✔ pip found")
        else: msg.append("❌ pip not found")
        if ollama_ok: msg.append("✔ Ollama found")
        else: msg.append("❌ Ollama not found")
        if disk_ok: msg.append("✔ Sufficient disk space (>10GB)")
        else: msg.append("❌ Not enough disk space (>10GB required)")
        if net_ok: msg.append("✔ Network OK")
        else: msg.append("❌ Network issue (check your connection)")
        self.status_label.setText("\n".join(msg))
        self.complete = all([python_ok, pip_ok, ollama_ok, disk_ok, net_ok])
        self.completeChanged.emit()

    def isComplete(self):
        return self.complete

class ModelSelectionPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Model Selection")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select which models to install (disk usage shown):"))
        self.codellama13b = QCheckBox("codellama:13b (22GB)")
        self.codellama7b = QCheckBox("codellama:7b (8GB)")
        self.llama38b = QCheckBox("llama3:8b (16GB)")
        self.mistral7b = QCheckBox("mistral:7b (13GB)")
        for cb in [self.codellama13b, self.codellama7b, self.llama38b, self.mistral7b]:
            layout.addWidget(cb)
        self.setLayout(layout)

    def get_selected_models(self):
        models = []
        if self.codellama13b.isChecked():
            models.append("codellama:13b")
        if self.codellama7b.isChecked():
            models.append("codellama:7b")
        if self.llama38b.isChecked():
            models.append("llama3:8b")
        if self.mistral7b.isChecked():
            models.append("mistral:7b")
        return models

class VenvSetupPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Python Environment Setup")
        layout = QVBoxLayout()
        self.status_label = QLabel("Setting up Python virtual environment...")
        self.button = QPushButton("Create venv and install requirements")
        self.button.clicked.connect(self.setup_venv)
        layout.addWidget(self.status_label)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.complete = False

    def setup_venv(self):
        try:
            if not os.path.exists(".venv"):
                subprocess.check_call([sys.executable, "-m", "venv", ".venv"])
            pip_path = os.path.join(".venv", "bin", "pip") if os.name != "nt" else os.path.join(".venv", "Scripts", "pip.exe")
            subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])
            self.status_label.setText("✔ venv and requirements installed")
            self.complete = True
        except Exception as e:
            self.status_label.setText(f"❌ Error: {e}")
            self.complete = False
        self.completeChanged.emit()

    def isComplete(self):
        return self.complete

class ConnectivityTestPage(QWizardPage):
    def __init__(self, model_page):
        super().__init__()
        self.setTitle("Connectivity Test")
        self.model_page = model_page
        layout = QVBoxLayout()
        self.status_label = QLabel("Test Ollama and model availability before download.")
        self.button = QPushButton("Test Connectivity")
        self.button.clicked.connect(self.test_connectivity)
        layout.addWidget(self.status_label)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.complete = False

    def test_connectivity(self):
        # Test Ollama server
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=2)
            if r.status_code == 200:
                tags = [m["name"] for m in r.json().get("models", [])]
                missing = [m for m in self.model_page.get_selected_models() if m not in tags]
                if not missing:
                    self.status_label.setText("✔ All selected models already installed!")
                    self.complete = True
                else:
                    self.status_label.setText(f"⚠️ Missing models: {', '.join(missing)}. Will be downloaded next.")
                    self.complete = True
            else:
                self.status_label.setText("❌ Ollama server not responding.")
                self.complete = False
        except Exception as e:
            self.status_label.setText(f"❌ Ollama not running: {e}")
            self.complete = False
        self.completeChanged.emit()

    def isComplete(self):
        return self.complete

class InstallPage(QWizardPage):
    def __init__(self, model_page):
        super().__init__()
        self.setTitle("Install Models and Configure")
        self.model_page = model_page
        layout = QVBoxLayout()
        self.status_label = QLabel("Ready to install selected models and configure CLED.")
        self.progress = QProgressBar()
        self.button = QPushButton("Install and Configure")
        self.button.clicked.connect(self.install)
        layout.addWidget(self.status_label)
        layout.addWidget(self.progress)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.complete = False

    def install(self):
        models = self.model_page.get_selected_models()
        self.progress.setMaximum(len(models))
        for i, model in enumerate(models):
            if not check_model(model):
                try:
                    self.status_label.setText(f"Pulling {model}...")
                    QApplication.processEvents()
                    subprocess.check_call(["ollama", "pull", model])
                except Exception as e:
                    self.status_label.setText(f"❌ Error pulling {model}: {e}")
                    self.complete = False
                    self.completeChanged.emit()
                    return
            self.progress.setValue(i+1)
        # Write .env
        with open(".env", "w") as f:
            f.write("PREFERRED_PROVIDER=ollama\n")
            if "codellama:13b" in models:
                f.write("BIG_MODEL=codellama:13b\n")
            elif "codellama:7b" in models:
                f.write("BIG_MODEL=codellama:7b\n")
            elif "llama3:8b" in models:
                f.write("BIG_MODEL=llama3:8b\n")
            elif "mistral:7b" in models:
                f.write("BIG_MODEL=mistral:7b\n")
            if "codellama:7b" in models:
                f.write("SMALL_MODEL=codellama:7b\n")
            elif "llama3:8b" in models:
                f.write("SMALL_MODEL=llama3:8b\n")
            elif "mistral:7b" in models:
                f.write("SMALL_MODEL=mistral:7b\n")
            else:
                f.write("SMALL_MODEL=codellama:13b\n")
            f.write("OLLAMA_API_BASE=http://localhost:11434\nHOST=0.0.0.0\nPORT=8083\nLOG_LEVEL=INFO\n")
        self.status_label.setText("✔ Models installed and .env configured")
        self.complete = True
        self.completeChanged.emit()

    def isComplete(self):
        return self.complete

class FinalPage(QWizardPage):
    def __init__(self):
        super().__init__()
        self.setTitle("Finish")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("CLED installation complete!"))
        self.launch_btn = QPushButton("Start CLED Server")
        self.launch_btn.clicked.connect(self.launch_server)
        layout.addWidget(self.launch_btn)
        self.setLayout(layout)

    def launch_server(self):
        try:
            subprocess.Popen([sys.executable, "-m", "uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8083"])
            QMessageBox.information(self, "CLED", "Server started on port 8083.")
        except Exception as e:
            QMessageBox.critical(self, "CLED", f"Failed to start server: {e}")

class InstallerWizard(QWizard):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CLED Installer")
        self.model_page = ModelSelectionPage()
        self.addPage(WelcomePage())
        self.addPage(SystemCheckPage())
        self.addPage(self.model_page)
        self.addPage(VenvSetupPage())
        self.addPage(ConnectivityTestPage(self.model_page))
        self.addPage(InstallPage(self.model_page))
        self.addPage(FinalPage())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wizard = InstallerWizard()
    wizard.show()
    sys.exit(app.exec_())