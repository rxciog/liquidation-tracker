import camelot
import argparse
import sys
from pathlib import Path

from pypdf import PdfReader
import re
import calendar

import csv

sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.config import CSV_OUTPUT_PATH

def extract_table(file_path, filename):
        
    try:
        tables = camelot.read_pdf(file_path, flavor='stream', table_areas=['0,700,600,100'])

        if tables.n != 1:
            return False
        tables[0].df.to_csv(filename, mode='a', index=False, header=False)
    except Exception as e:
        return False

    return True
    

def extract_date(path):
    try:
        reader = PdfReader(path)

        text = reader.pages[0].extract_text()
        match = re.search(r"(\d{2}/\d{4})", text)
        
        if not match:
            return None
        
        month, year = match.group().split('/')
        month_name = calendar.month_name[int(month)]
        return month_name + year

    except Exception:
        return None
    

def calculate_total(filename):
    try:
        rows = []
        total = 0
        discount = 0

        with open(filename, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if 'BALANCE' not in row:
                    rows.append(row)


        for row in rows:
            if "Totales" in row:
                try:
                    discount += float(row[-2].replace(',',''))
                    total += float(row[-3].replace(',',''))
                except (ValueError, IndexError):
                    continue
                
        balance_row = ['','','','', "BALANCE", str(total), str(discount), str(total-discount)]
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
            writer.writerow([])
            writer.writerow(balance_row)
        
        return True
    
    except  Exception:
        return False
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract table from pdf")
    parser.add_argument('file_path')
    args = parser.parse_args()
    
    date = extract_date(args.file_path)
    if not date:
        print("Failed to extract  date")
        exit(1)
        
    filename = str(CSV_OUTPUT_PATH) + '/Liquidacion' + date + '.csv'
    
    if not extract_table(args.file_path, filename):
        print("Failed to extract table")
        exit(1)
    
    if not calculate_total(filename):
        print("Failed to calculate totals")
        exit(1)
    