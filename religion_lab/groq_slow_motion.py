import os, time, requests

GROQ_KEY = "REMOVED_API_KEY"
MODEL_NAME = "llama-3.3-70b-versatile"
DATA_PATH = "/var/www/html/montage_2008/Religion/data/"
BASE_OUTPUT = "/var/www/html/montage_2008/religion_lab/summaries/"
UTF8_BOM = b'\xef\xbb\xbf'

lessons = [
    (6, 12, "01_السنن_الإلهية_في_الكون_والإنسان"), (13, 18, "02_تعظيم_الشعائر_الدينية"),
    (19, 24, "03_مكانة_الزكاة_وآثارها"), (25, 31, "04_عمارة_الأرض_في_الإسلام"),
    (32, 38, "05_نماذج_من_سلوك_الناس_في_القرآن_الكريم"), (39, 45, "06_الحج_مكانته_وآثاره"),
    (46, 52, "07_الإسلام_والتفكير"), (53, 59, "08_رعاية_الموهوبين_في_الإسلام"),
    (60, 66, "09_آفات_اللسان"), (67, 73, "10_فقه_الأولويات_في_الإسلام"),
    (74, 79, "11_الإسلام_والبحث_العلمي"), (80, 87, "12_الإسلام_والجمال"),
    (88, 95, "13_الحب_في_الإسلام"), (96, 103, "14_الإسلام_وإدارة_الأزمات"),
    (104, 110, "15_الجرائم_الإلكترونية"), (111, 117, "16_الإسلام_وكبار_السن"),
    (118, 124, "17_مكانة_الصحابة_الكرام"), (125, 130, "18_الإصلاح_بين_الناس"),
    (131, 138, "19_توظيف_التقنية_في_خدمة_الإسلام"), (139, 146, "20_الإشاعة")
]

def call_groq(content):
    for attempt in range(3): # محاولة 3 مرات لكل صفحة
        try:
            res = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                headers={"Authorization": f"Bearer {GROQ_KEY}"}, 
                json={"model": MODEL_NAME, "messages": [
                    {"role": "system", "content": "أنت خبير تربوي أردني. اشرح النص بأسلوب دقيق وعميق مع أمثلة أردنية و10 أسئلة وأجوبة."},
                    {"role": "user", "content": content}
                ], "temperature": 0.4}, timeout=60)
            
            if res.status_code == 200:
                return res.json()['choices'][0]['message']['content']
            elif res.status_code == 429: # حظر مؤقت
                print(f"⚠️ حظر مؤقت.. سأنتظر 60 ثانية قبل المحاولة {attempt+1}")
                time.sleep(60)
        except: pass
    return None

for start, end, folder in lessons:
    path = os.path.join(BASE_OUTPUT, folder)
    if not os.path.exists(path): os.makedirs(path)
    for p in range(start, end + 1):
        dst = f"{path}/{p}.txt"
        if os.path.exists(dst) and os.path.getsize(dst) > 500: continue
        
        src = f"{DATA_PATH}{p}.txt"
        if not os.path.exists(src): continue

        print(f"🐢 معالجة هادئة للصفحة {p}...")
        text = open(src, 'r', encoding='utf-8').read()
        res = call_groq(text)
        
        if res:
            with open(dst, 'wb') as f:
                f.write(UTF8_BOM + res.encode('utf-8'))
            print(f"✅ تم بنجاح.")
            time.sleep(45) # انتظار طويل جداً لتفادي الحظر
        else:
            print(f"❌ فشل متكرر في {p}")

print("✨ انتهى السكريبت البطيء.")
