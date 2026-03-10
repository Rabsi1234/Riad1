# -*- coding: utf-8 -*-
import os
from openai import OpenAI
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

# الإعدادات الجديدة
API_KEY = "REMOVED_API_KEY"
DATA_PATH = "/var/www/html/montage_2008/Arabic_Grammar/data"
BASE_OUT = "/var/www/html/montage_2008/arabic_lab/كتاب_النحو_والصرف"

def get_client():
    return OpenAI(api_key=API_KEY, base_url="https://api.groq.com/openai/v1")

# فهرس النحو والصرف (حسب ما طلبت)
INDEX_MAP = [
    (5, 14, "01_معاني_زيادات_الأفعال"),
    (15, 29, "02_التصغير"),
    (30, 39, "03_النسب"),
    (40, 46, "04_الإبدال"),
    (47, 55, "05_الإعلال"),
    (56, 65, "06_موسيقا_الشعر")
]

def process():
    client = get_client()
    for start, end, folder_name in INDEX_MAP:
        folder_path = os.path.join(BASE_OUT, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        for pg in range(start, end + 1):
            output_file = os.path.join(folder_path, f"page_{pg}.html")
            
            if os.path.exists(output_file):
                print(f"⏭️ الصفحة {pg} موجودة في {folder_name}، تخطي...")
                continue
                
            txt_file = os.path.join(DATA_PATH, f"{pg}.txt")
            if os.path.exists(txt_file):
                with open(txt_file, "r", encoding="utf-8") as f:
                    page_content = f.read()
                
                try:
                    # البرومبت المطور (شرح + أمثلة + أسئلة + ملخص)
                    prompt = (
                        f"أنت الأستاذ رياض. اشرح الصفحة رقم ({pg}) من درس '{folder_name}' "
                        "بناءً على النص المرفق. المطلوب:\n"
                        "1. شرح القاعدة بوضوح.\n"
                        "2. أمثلة توضيحية كافية.\n"
                        "3. 3 أسئلة وأجوبة مقترحة بنمط التوجيهي.\n"
                        "4. ملخص سريع (تذكرني)."
                    )
                    
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "أنت الأستاذ رياض. تشرح بوضوح وبترميز UTF-8 مع أمثلة وتدريبات."},
                            {"role": "user", "content": prompt + "\n\nنص الصفحة الأصلي:\n" + page_content}
                        ],
                        temperature=0.4
                    )
                    
                    explanation = response.choices[0].message.content
                    
                    html_template = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: 'Tahoma', sans-serif; background:#f4f7f6; padding:30px; line-height:1.8; }}
        .card {{ background:white; padding:30px; border-radius:15px; box-shadow:0 10px 25px rgba(0,0,0,0.1); max-width:900px; margin:auto; border-right:8px solid #2ecc71; }}
        h1 {{ color:#27ae60; text-align:center; border-bottom:2px solid #eee; padding-bottom:10px; }}
        .info {{ text-align:center; color:#95a5a6; font-weight:bold; margin-bottom:20px; }}
        .content {{ white-space:pre-wrap; font-size:18px; color:#2c3e50; }}
    </style>
</head>
<body>
    <div class="card">
        
        <div class="info">المادة: نحو وصرف | الدرس: {folder_name} | 📖 صفحة: {pg}</div>
        <div class="content">{explanation}</div>
    </div>
</body>
</html>"""
                    
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(html_template)
                    
                    print(f"✅ تم إنتاج: {folder_name} -> صفحة {pg}")
                    time.sleep(10) # تبريد

                except Exception as e:
                    print(f"❌ خطأ في صفحة {pg}: {str(e)}")
                    time.sleep(5)
            else:
                print(f"❓ لم يتم العثور على ملف: {pg}.txt")

if __name__ == "__main__":
    process()
