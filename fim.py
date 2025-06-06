from pathlib import Path
import hashlib
import time 

BASE_DIR = Path(__file__).resolve().parent
monitoring_list = [BASE_DIR / 'monitored_file.txt'] # Modify accordingly

def calculate_file_hash(file_path):
  """Calculates and returns the hash of a file"""
  file_hash = hashlib.sha256() 
  with open(file_path,'rb') as file: 
    file_data = file.read() 
    file_hash.update(file_data) 
  return file_hash.hexdigest() 

def log_change(file_path):
    """Creates a log file containing the times and paths of files that has been changed"""
    log_dir = BASE_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'file_changes.log'
    with log_file.open('a') as f:          
        f.write(f"{time.ctime()}: {file_path} has changed.\n")

def reset_log():
    """Wipe logs/file_changes.log so we start on a clean slate"""
    log_dir = BASE_DIR / "logs"          
    (log_dir / "file_changes.log").write_text("") # Remove log content for the previous round of monitoring

def monitor_files():
    """Monitor files for changes by comparing their hashes"""
    prior_hashes = {}
    try:
        while True:
            for file_path in monitoring_list:
                if not file_path.exists():
                    print(f'File is missing: {file_path}')
                    continue
                
                new_hash = calculate_file_hash(file_path)
                    
                if file_path not in prior_hashes:
                        prior_hashes[file_path] = new_hash
                        print(f'Original hash stored for: {file_path}')
                elif prior_hashes[file_path] != new_hash:
                    print(f'File has changed: {file_path}')
                    log_change(file_path)
                    prior_hashes[file_path] = new_hash
            time.sleep(5)
    except KeyboardInterrupt:                
        print("\nStopped by user.")

if __name__ == "__main__":
    reset_log()
    monitor_files()
