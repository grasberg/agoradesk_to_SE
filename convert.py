import csv
from datetime import datetime

input_file = 'input.csv'
output_file = 'output.se'

def process_row(row):
    trade_id, trade_type, created_at, trading_partner, amount_asset, asset, amount, currency, method = row
    # Format the date
    date = datetime.strptime(created_at, '%a %b %d %Y %H:%M:%S %Z%z').strftime('%Y%m%d')

    if trade_type == "ONLINE_BUY":
        desc = f"{trading_partner} {amount_asset}"
        minus="-"
        minus2=""
        cstr2="4010"
    elif trade_type == "ONLINE_SELL":
        desc = f"{trading_partner} {amount_asset}"
        minus=""
        minus2="-"
        cstr2="3054"
    else:
        return None
    
    fee = float(amount) * 0.01
    rounded_fee = round(fee, 2)
    output = f'#VER A {counter} {date} "{desc}" {date}\n{{\n   #TRANS 1930 {{}} {minus}{amount}\n   #TRANS {cstr2} {{}} {minus2}{amount}\n   #TRANS 6571 {{}} {rounded_fee}\n   #TRANS 1930 {{}} -{rounded_fee}\n}}\n'

    return output

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    reader = csv.reader(infile)
    next(reader)  # Skip the header row

    counter = 0
    for row in reader:
        counter += 1
        processed_row = process_row(row)
        if processed_row:
            outfile.write(processed_row)
