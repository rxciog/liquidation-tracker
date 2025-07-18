# Liquidation Tracker

A Python application for automatically processing salary liquidation PDFs and extracting financial data.

## Features

- **Automatic PDF Processing**: Watches a directory for new PDF files
- **Table Extraction**: Extracts salary data from PDF documents using Camelot
- **CSV Export**: Converts extracted data to CSV format with calculations
- **File Organization**: Automatically moves processed files to organized directories

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/salary-processor.git
cd liquidation-tracker
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. **Start the file watcher**:
```bash
python scripts/run_watcher.py
```

2. **Process a single PDF**:
```bash
python src/processors/pdf_extractor.py path/to/your/file.pdf
```

3. Place PDF files in the `data/input/` directory and they will be automatically processed.

## Configuration

Update the paths in `src/utils/config.py` to match your setup:

- `INPUT_DIR`: Directory to watch for new PDF files
- `OUTPUT_DIR`: Directory where processed files are moved
- `CSV_OUTPUT_PATH`: Path where CSV files are saved

## Running the Watcher Automatically

### Linux: Create a Systemd Service

To run the watcher script automatically on Linux, follow these steps:

1. **Create a service file**:
    Create a new file called `liquidation-tracker.service` in `/etc/systemd/system/`:
    ```bash
    sudo nano /etc/systemd/system/liquidation-tracker.service
    ```

2. **Add the following content**:
    Replace `/path/to/liquidation-tracker` with the actual path to your project directory:
    ```ini
    [Unit]
    Description=Liquidation Tracker Watcher Service
    After=network.target

    [Service]
    Type=simple
    ExecStart= path/to/virtual/env /path/to/liquidation-tracker/scripts/run_watcher.py
    WorkingDirectory=/path/to/liquidation-tracker
    Restart=always
    User=your-username
    StandardOutput=journal
    StandardError=journal

    [Install]
    WantedBy=multi-user.target
    ```

3. **Reload systemd and enable the service**:
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable liquidation-tracker.service
    ```

4. **Start the service**:
    ```bash
    sudo systemctl start liquidation-tracker.service
    ```

5. **Check the service status**:
    ```bash
    sudo systemctl status liquidation-tracker.service
    ```

### Windows: Create a Task Scheduler Task

To run the watcher script automatically on Windows, follow these steps:

0. **Create bat file run_watcher.bat**
    ```bat
    @echo off
    cd C:\Users\User\liquidation-watcher
    call .venv\Scripts\activate.bat
    python watcher.py
    ```

1. **Open Task Scheduler**:
    Press `Win + S`, type "Task Scheduler," and open it.

2. **Create a new task**:
    - Click on "Create Task" in the right-hand panel.
    - Give the task a name, e.g., "Liquidation Tracker Watcher."
    - Under the "Security Options," select "Run whether user is logged on or not."

3. **Set the trigger**:
    - Go to the "Triggers" tab and click "New."
    - Select "At startup" or set a custom schedule.

4. **Set the action**:
    - Go to the "Actions" tab and click "New."
    - Select "Start a program."
    - In the "Program/script" field, enter the path to your bat file, e.g., `C:\Users\User\liquidation-watcher\run_watcher.bat`.


5. **Save and test the task**:
    - Click "OK" to save the task.
    - You may be prompted to enter your user credentials.
    - Test the task by right-clicking it and selecting "Run."

These steps will ensure the watcher script runs automatically on both Linux and Windows systems.
## Dependencies

- camelot-py: PDF table extraction
- watchdog: File system monitoring
- pypdf: PDF text extraction
- pandas: Data manipulation

## License

MIT License
