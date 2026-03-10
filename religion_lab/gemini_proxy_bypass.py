import os
import google.generativeai as genai
import time
from google.generativeai import urllib3

# إيقاف أي بروكسي محلي قد يسبب الحظر
os.environ['no_proxy'] = '*'
os.environ['NO_PROXY'] = '*'

# المفتاح الأخير
GEMINI_KEY = "AIzaSyAPBfJ_kt7AZLXlvB1NJj7RwAjgHl5f4hE"
genai.configure(api_key=GEMINI_KEY)

# سنركز على الموديل الأكثر قبولاً
model = genai.GenerativeModel('gemini-1.5-flash')

lessons = [
    (6, 12, "01_السنن_الإلهية_في_الكون_والإنسان"),
    (13, 146, "Rest_of_Lessons") # تجربة سريعة للباقي
]

DATA_PATH = "/var/www/html/montage_2008/Religion/data/"
BASE_OUTPUT = "/var/www/html/montage_2008/religion_lab/summaries/"

prompt_template = "قم بتلخيص النص التالي وشرحه بأسلوب تعليمي: {content}"

for start, end, folder in lessons:
    out_dir = os.path.join(BASE_OUTPUT, folder)
    if not os.path.exists(out_dir): os.makedirs(out_dir)

    for p in range(start, end + 1):
        src = f"{DATA_PATH}{p}.txt"
        if not os.path.exists(src): continue
        
        with open(src, 'r', encoding='utf-8') as f:
            text = f.read()

        print(f"🚀 محاولة اختراق الحظر لصفحة {p}...")
        try:
            # محاولة الطلب بدون أي قيود شبكة
            response = model.generate_content(prompt_template.format(content=text))
            if response.text:
                with open(f"{out_dir}/{p}.txt", 'w', encoding='utf-8') as f_out:
                    f_out.write(response.text)
                print(f"✅ نجحت العملية! تم حفظ الصفحة {p}")
                time.sleep(5)
        except Exception as e:
            print(f"❌ لا يزال الحظر قائماً: {str(e)[:50]}")
            print("💡 رياض، السيرفر محجوب جغرافياً. الحل الأخير هو تشغيل السكريبت من جهازك الشخصي ورفع الملفات للسيرفر.")
            exit()
