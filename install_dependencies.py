# ──────────────────────────────────────────────────────────────────────────
# FILE: install_dependencies.py
# ROLE: Programmatic Dependency Installer (No-Terminal Solution)
# ARCHITECTURE: Subprocess Pip Bridge
# ──────────────────────────────────────────────────────────────────────────

import sys
import subprocess

def install_package(package_name: str):
    """Programmatically runs pip to install a package using the active Python interpreter."""
    print(f"⏳ Installing {package_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✅ {package_name} successfully installed!")
    except Exception as e:
        print(f"❌ Failed to install {package_name}. Error: {e}")

if __name__ == "__main__":
    print("==================================================")
    print("🚀 AGV PLATFORM: Starting Automated Installer...")
    print(f"Active Interpreter: {sys.executable}")
    print("==================================================\n")
    
    # The essential packages required for the high-performance web server
    required_packages = ["fastapi", "uvicorn", "numpy"]
    
    for package in required_packages:
        install_package(package)
        
    print("\n==================================================")
    print("🎉 INSTALLATION COMPLETE! You are ready to run app.py")
    print("==================================================")
