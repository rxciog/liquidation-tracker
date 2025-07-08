# Salary Processor

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
cd salary-processor
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

## Dependencies

- camelot-py: PDF table extraction
- watchdog: File system monitoring
- pypdf: PDF text extraction
- pandas: Data manipulation

## License

MIT License
