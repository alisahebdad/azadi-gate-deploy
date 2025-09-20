import os
import shutil
import subprocess
import json
import tempfile

# Configuration
REPO_URL = "git@github.com:alisahebdad/azadi-gate-deploy.git"  # Replace with your actual repo URL
DEST_DIR = "/home/data/azadi-gate/"
CONFIG_PATH = os.path.join(DEST_DIR, "config.json")
SERVICE_NAME = "gcsv2.service"

def run_command(command):
    """Run a shell command and return its output"""
    print(f"Running: {command}")
    process = subprocess.run(command, shell=True, text=True, capture_output=True)
    if process.returncode != 0:
        print(f"Error: {process.stderr}")
        raise Exception(f"Command failed: {command}")
    return process.stdout.strip()

def main():
    # Step 1: Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Created temporary directory: {temp_dir}")
        
        # Step 2: Clone the repository
        print("Cloning repository...")
        os.chdir(temp_dir)
        run_command(f"git clone {REPO_URL} .")
        
        # Step 3: Backup existing config if it exists
        if os.path.exists(CONFIG_PATH):
            print(f"Backing up existing config from {CONFIG_PATH}")
            with open(CONFIG_PATH, 'r') as f:
                existing_config = json.load(f)
                
            # Load the default config from the repo
            with open("config.json", 'r') as f:
                default_config = json.load(f)
            
            # Merge configs (keep existing values)
            for key, value in existing_config.items():
                if value:  # Only keep non-empty values
                    default_config[key] = value
            
            # Save the merged config
            with open("config.json", 'w') as f:
                json.dump(default_config, f, indent=2)
        
        # Step 4: Stop the service
        print("Stopping service...")
        run_command(f"sudo systemctl stop {SERVICE_NAME}")
        
        # Step 5: Copy files to destination
        print(f"Copying files to {DEST_DIR}")
        if not os.path.exists(DEST_DIR):
            os.makedirs(DEST_DIR)
        
        # Copy main executable
        shutil.copy("main", DEST_DIR)
        os.chmod(os.path.join(DEST_DIR, "main"), 0o755)  # Make executable
        
        # Copy config
        shutil.copy("config.json", DEST_DIR)
        
        # Step 6: Start the service
        print("Starting service...")
        run_command(f"sudo systemctl start {SERVICE_NAME}")
        
        print("Update completed successfully!")

if __name__ == "__main__":
    main()