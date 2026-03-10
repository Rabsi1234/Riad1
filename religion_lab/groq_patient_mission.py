import os
import time
import requests

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

prompt_template = "أنت خبير تربوي أردني. اشرح النص التالي بأسلوب نانو مكثف (تلخيص، شرح، أمثلة، أسئلة وأجوبة): {content}"

def call_groq_with_retry(content):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt_template.format(content=content)}],
        "temperature": 0.4
    }
    
    while True:
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            elif response.status_code == 429:
                print("    ⏳ وصلنا للحد المسموح.. سأنتظر 20 ثانية وأحاول مجدداً...")
                time.sleep(20)
                continue
            else:
                print(f"    ❌ خطأ API: {response.status_code}")
                return None
        except Exception as e:
            print(f"    ❌ خطأ اتصال: {e}")
            time.sleep(5)
            continue

for start, end, folder in lessons:
    out_dir = os.path.join(BASE_OUTPUT, folder)
    if not os.path.exists(out_dir): os.makedirs(out_dir)

    for p in range(start, end + 1):
        dst_f = os.path.join(out_dir, f"{p}.txt")
        src_f = f"{DATA_PATH}{p}.txt"

        # السكريبت سيتخطى ما تم حفظه بنجاح ويكمل النواقص
        if os.path.exists(dst_f) or not os.path.exists(src_f):
            continue

        with open(src_f, 'r', encoding='utf-8') as f:
            raw_text = f.read()

        print(f"🧠 تحليل صفحة {p}...")
        result = call_groq_with_retry(raw_text)
        
        if result:
            with open(dst_f, 'w', encoding='utf-8') as f_out:
                f_out.write(result)
            print(f"✅ تم الحفظ.")
            time.sleep(10) # انتظار إجباري بين الصفحات لتجنب الحظر
