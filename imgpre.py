import pandas as pd
import io
import requests
# We import the necessary packages
# import the needed packages
import cv2
import re
import os, argparse
import pytesseract
from PIL import Image
from collections import namedtuple

def txt(filename):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # image=cv2.imread(f'static/uploads/{filename}',0)
    response = requests.get(
        f"https://trial22.blob.core.windows.net/photoes/{filename}")
    # print( type(response) ) # <class 'requests.models.Response'>
    img = Image.open(io.BytesIO(response.content))


    text=(pytesseract.image_to_string(img)).lower()
    new_vend_re = re.compile(r'^\d{12}.*')
    signed_re = re.compile(r'^signed: .*')
    price = re.findall(r'[\d,]+\.\d{2}', text)
    price = list(price)
    Total_inv_amt=max(price)
    inv_no = re.findall(r'\d{9}', text)
    inv_num = inv_no[0]
    dates_re = re.findall(r'\d+[/-]\d+[/-]\d{4}', text)
    inv_dt, due_dt = dates_re[0], dates_re[1]

    Inv = namedtuple('Inv',
                     'vend_num ship_dt desc wt wt_unit ref_no sub_total gst_amt invoice_amt Total_inv_amt inv_num inv_dt due_dt sign_stats sign_name sign_dt sign_timestamp mis currency mis2')
    line_items = []
    for line in text.split('\n'):
        if new_vend_re.match(line):
            vend_num, ship_dt, desc, total_amt = line.split('|')
            wt, wt_unit, ref_no, sub_total, gst_amt, invoice_amt = total_amt.split()

        if signed_re.match(line):
            try:
                sign_stats, sign_name, sign_dt, sign_timestamp, mis, currency, mis2 = line.split(' ')
                # print(sign_stats,sign_name,sign_dt,sign_timestamp,mis,currency,mis)

            except:
                sign_stats, sign_name, sign_surname, sign_dt, sign_timestamp, mis, currency, mis2 = line.split(' ')
                # sign_name=sign_name.join(sign_surname) #game changer for the double worded signature#worked 0205
                # print(sign_stats,sign_name,sign_surname,sign_dt,sign_timestamp,mis,currency,mis)

            try:
                line_items.append(
                    Inv(vend_num, ship_dt, desc, wt, wt_unit, ref_no, sub_total, gst_amt, invoice_amt, Total_inv_amt,
                        inv_num, inv_dt, due_dt, sign_stats, sign_name, sign_dt, sign_timestamp, mis, currency, mis2))

            except:
                line_items.append(
                    Inv(vend_num, ship_dt, desc, wt, wt_unit, ref_no, sub_total, gst_amt, invoice_amt, Total_inv_amt,
                        inv_num, inv_dt, due_dt, sign_stats, sign_name, sign_surname, sign_dt, sign_timestamp, mis,
                        currency, mis2))


    df=pd.DataFrame(line_items)

    return df
