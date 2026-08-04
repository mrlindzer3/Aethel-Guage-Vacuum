import subprocess
import sys

def run_module(script_name):
    print(f"\n--- Executing Module: {script_name} ---")
    result = subprocess.run([sys.executable, script_name], capture_output=False)
    if result.returncode != 0:
        print(f"[!] Module {script_name} encountered an error.")
    else:
        print(f"[+] Module {script_name} executed successfully.")

if __name__ == "__main__":
    print("=== INITIALIZING 8K @ 220 FPS VERIFICATION PIPELINE ===")
    run_module("modules/display_validator.py")
    run_module("modules/render_stress.py")
    print("\n=== ALL STRESS MODULES COMPLETED ===")
