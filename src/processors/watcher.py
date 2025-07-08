from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import os
import subprocess
import shutil 
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.config import INPUT_DIR, OUTPUT_DIR

VENV_PYTHON = Path(__file__).parent.parent.parent / ".venv/bin/python"
EXTRACT_SCRIPT = Path(__file__).parent / "extract_table.py"


class FileHandler(FileSystemEventHandler):
    def on_created(self, event):

        if event.is_directory:
            return
        if not event.src_path.endswith('.pdf'):
            return

        time.sleep(1)
        
        filename = os.path.basename(event.src_path)
        try:
            subprocess.run([VENV_PYTHON, str(EXTRACT_SCRIPT), event.src_path], check=True)
        except subprocess.CalledProcessError as e:
            return
    
        dest_path = Path(OUTPUT_DIR) / filename
        shutil.move(event.src_path, dest_path)
        

if __name__ == "__main__":
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    Path(INPUT_DIR).mkdir(parents=True, exist_ok=True)
    
    event_handler = FileHandler()
    observer = Observer()
    
    observer.schedule(event_handler, path=str(INPUT_DIR), recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()