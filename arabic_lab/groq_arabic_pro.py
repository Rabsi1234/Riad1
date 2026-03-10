# -*- coding: utf-8 -*-
import os
from openai import OpenAI
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "REMOVED_API_KEY"
DATA_PATH = "/var/www/html/montage_2008/Arabic_Literature/data"
BASE_OUT = "/var/www/html/montage_2008/arabic_lab/كتاب_الأدب_والنقد_والبلاغة"

def get_client():
    return OpenAI(api_key=API_KEY, base_url="https://api.groq.com/openai/v1")

# توزيع الدروس والصفحات التابعة لها
INDEX_MAP = [
    (7, 8, "01_البلاغة_وغايتها"),
    (9, 9, "02_الحقيقة_والمجاز"),
    (10, 11, "03_الاستعارة"),
    (12, 13, "04_المجاز_المرسل"),
    (20, 21, "05_أسلوب_النهي_ومعانيه"),
    (22, 23, "06_أسلوب_النداء_ومعانيه"),
    (24, 25, "07_أسلوب_الإطناب"),
    (31, 31, "08_مفهوم_النقد_الأدبي_أهميته"),
    (32, 35, "09_العناصر_العامة_للعمل_الأدبي"),
    (36, 38, "10_أبرز_قضايا_النقد_الأدبي_القديم"),
    (39, 43, "11_تحليل_نصوص_شعرية_نقدية"),
    (48, 49, "12_المناهج_النقدية_الخارجية"),
    (50, 50, "13_المناهج_النقدية_الداخلية"),
    (51, 54, "14_المذاهب_الأدبية"),
    (57, 63, "15_المعارضات_والتناص_والمفارقة"),
    (64, 65, "16_شعر_التفعيلة"),
    (66, 70, "17_التحليل_النقدي_الموضوعي"),
    (71, 73, "18_ملامح_الحركة_النقدية_في_الأردن")
]

def process():
    client = get_client()
    for start, end, folder_name in INDEX_MAP:
        folder_path = os.path.join(BASE_OUT, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        # معالجة كل صفحة بشكل مستقل داخل مجلد الدرس
        for pg in range(start, end + 1):
            output_file = os.path.join(folder_path, f"page_{pg}.html")
            
            # تخطي إذا كانت الصفحة مشروحة مسبقاً
            if os.path.exists(output_file):
                print(f"⏭️ الصفحة {pg} موجودة في {folder_name}، تخطي...")
                continue
                
            txt_file = os.path.join(DATA_PATH, f"{pg}.txt")
            if os.path.exists(txt_file):
                with open(txt_file, "r", encoding="utf-8") as f:
                    page_content = f.read()
                
                try:
                    prompt = (
                        f"أنت الأستاذ رياض. اشرح الصفحة رقم ({pg}) من درس '{folder_name}' "
                        "بناءً على النص المرفق. قدم شرحاً تفصيلياً، تحليل صور فنية، "
                        "واستخرج أهم النقاط والأسئلة المتوقعة من هذه الصفحة تحديداً."
                    )
                    
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "أنت الأستاذ رياض. تشرح بوضوح وبترميز UTF-8."},
                            {"role": "user", "content": prompt + "\n\nنص الصفحة:\n" + page_content}
                        ],
                        temperature=0.4
                    )
                    
                    explanation = response.choices[0].message.content
                    
                    html_template = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: 'Tahoma', sans-serif; background:#f0f4f8; padding:30px; line-height:1.7; }}
        .card {{ background:white; padding:25px; border-radius:12px; box-shadow:0 5px 15px rgba(0,0,0,0.08); max-width:900px; margin:auto; border-top:6px solid #3498db; }}
        h1 {{ color:#2c3e50; text-align:center; font-size:24px; }}
        .info {{ text-align:center; color:#7f8c8d; margin-bottom:20px; }}
        pre {{ white-space:pre-wrap; font-size:17px; color:#34495e; background:#fff; padding:15px; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>شرح الأستاذ رياض</h1>
        <div class="info">الدرس: {folder_name} | 📖 الصفحة: {pg}</div>
        <hr>
        <pre>{explanation}</pre>
    </div>
</body>
</html>"""
                    
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(html_template)
                    
                    print(f"✅ تم إنتاج: {folder_name} -> صفحة {pg}")
                    time.sleep(12) # تبريد لتجنب الحظر

                except Exception as e:
                    print(f"❌ خطأ في صفحة {pg}: {str(e)}")
                    time.sleep(20)

if __name__ == "__main__":
    process()
