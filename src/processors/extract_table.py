from collections import namedtuple
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

DateInfo = namedtuple('DateInfo', ['day','month','year', 'month_name'])
DateRange = namedtuple('DateRange', ['start_date','end_date'])

def extract_table(file_path):
        
    try:
        tables = camelot.read_pdf(file_path, flavor='stream', table_areas=['0,700,600,100'])

        if tables.n != 1:
            return False
        
    except Exception as e:
        return False

    return tables
    

def extract_date(path):
    try:
        reader = PdfReader(path)

        text = reader.pages[0].extract_text()
        match = re.findall(r"(\d{2}/\d{2}/\d{4})", text)
        
        if not match or len(match) < 2:
            return None

        dates = match[:2] 
        
        start_day, start_month, start_year = dates[0].split('/')
        start_month_name = calendar.month_name[int(start_month)]
        start_date = DateInfo(start_day,start_month,start_year, start_month_name)
        
        end_day, end_month, end_year = dates[1].split('/')
        end_month_name = calendar.month_name[int(end_month)]
        end_date = DateInfo(end_day, end_month, end_year, end_month_name)

        return DateRange(start_date, end_date)

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
    
def write_csv(data, filename, date_range):
    
    try:
        with open(filename, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([f"Desde: {date_range.start_date.day}/{date_range.start_date.month}/{date_range.start_date.year}"])
            writer.writerow([f"Hasta: {date_range.end_date.day}/{date_range.end_date.month}/{date_range.end_date.year}"])
            writer.writerow([])
        data[0].df.to_csv(filename, mode='a', index=False, header=False)
    
    except Exception as e:
        return False
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Extract table from pdf")
    parser.add_argument('file_path')
    args = parser.parse_args()
    
    date_range = extract_date(args.file_path)
    if not date_range:
        print("Failed to extract  date")
        exit(1)
    
    filename_date = date_range.start_date.month_name + date_range.start_date.year    
    filename = str(CSV_OUTPUT_PATH) + '/Liquidacion' + filename_date + '.csv'
    
    data = extract_table(args.file_path)
    if not data:
        print("Failed to extract table")
        exit(1)
    
    if not write_csv(data, filename, date_range):
        print("Failed to write data in csv file")
        exit(1)
        
    if not calculate_total(filename):
        print("Failed to calculate totals")
        exit(1)
    