import os
import time
import requests
import json

GROQ_KEY = "REMOVED_API_KEY"
MODEL_NAME = "llama-3.3-70b-versatile"

lessons = [
    (6, 12, "01_السنن_الإلهية_في_الكون_والإنسان"),
    (13, 18, "02_تعظيم_الشعائر_الدينية"),
    (19, 24, "03_مكانة_الزكاة_وآثارها"),
    (25, 31, "04_عمارة_الأرض_في_الإسلام"),
    (32, 38, "05_نماذج_من_سلوك_الناس_في_القرآن_الكريم"),
    (39, 45, "06_الحج_مكانته_وآثاره"),
    (46, 52, "07_الإسلام_والتفكير"),
    (53, 59, "08_رعاية_الموهوبين_في_الإسلام"),
    (60, 66, "09_آفات_اللسان"),
    (67, 73, "10_فقه_الأولويات_في_الإسلام"),
    (74, 79, "11_الإسلام_والبحث_العلمي"),
    (80, 87, "12_الإسلام_والجمال"),
    (88, 95, "13_الحب_في_الإسلام"),
    (96, 103, "14_الإسلام_وإدارة_الأزمات"),
    (104, 110, "15_الجرائم_الإلكترونية"),
    (111, 117, "16_الإسلام_وكبار_السن"),
    (118, 124, "17_مكانة_الصحابة_الكرام"),
    (125, 130, "18_الإصلاح_بين_الناس"),
    (131, 138, "19_توظيف_التقنية_في_خدمة_الإسلام"),
    (139, 146, "20_الإشاعة")
]

DATA_PATH = "/var/www/html/montage_2008/Religion/data/"
BASE_OUTPUT = "/var/www/html/montage_2008/religion_lab/summaries/"

# برومبت يركز على اللغة العربية الفصحى
prompt_template = "أنت خبير تربوي أردني. اشرح النص التالي باللغة العربية الفصحى بأسلوب نانو مكثف (تلخيص، شرح، أمثلة، أسئلة وأجوبة): {content}"

def call_groq(content):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt_template.format(content=content)}],
        "temperature": 0.4
    }
    
    for attempt in range(3):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                # التأكد من استلام النص بترميز صحيح
                res_json = response.json()
                return res_json['choices'][0]['message']['content']
            elif response.status_code == 429:
                time.sleep(25)
                continue
        except:
            time.sleep(5)
    return None

for start, end, folder in lessons:
    out_dir = os.path.join(BASE_OUTPUT, folder)
    if not os.path.exists(out_dir): os.makedirs(out_dir)

    for p in range(start, end + 1):
        dst_f = os.path.join(out_dir, f"{p}.txt")
        src_f = f"{DATA_PATH}{p}.txt"

        # ملاحظة: سنقوم بمسح الملفات القديمة التي ظهرت فيها الرموز الغريبة لنعيد كتابتها صحيحة
        if not os.path.exists(src_f): continue

        with open(src_f, 'r', encoding='utf-8') as f:
            raw_text = f.read()

        print(f"🧠 تحليل ومعالجة صفحة {p} باللغة العربية...")
        result = call_groq(raw_text)
        
        if result:
            # المفتاح هنا هو إجبار encoding='utf-8'
            with open(dst_f, 'w', encoding='utf-8') as f_out:
                f_out.write(result)
            print(f"✅ تم الحفظ (ترميز سليم).")
            time.sleep(12)
