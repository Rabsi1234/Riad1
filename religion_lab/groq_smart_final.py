import os, time, requests

GROQ_KEY = "REMOVED_API_KEY"
MODEL_NAME = "llama-3.3-70b-versatile"
DATA_PATH = "/var/www/html/montage_2008/Religion/data/"
BASE_OUTPUT = "/var/www/html/montage_2008/religion_lab/summaries/"

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

PROMPT_SYSTEM = "أنت معلم خبير. اشرح النص المرفق شرحاً دقيقاً ومفصلاً بأسلوب نانو دسم، مع أمثلة أردنية و10 أسئلة وأجوبة. يمنع التكرار نهائياً."

def call_groq(content):
    try:
        data = {
            "model": MODEL_NAME,
            "messages": [{"role": "system", "content": PROMPT_SYSTEM}, {"role": "user", "content": content}],
            "temperature": 0.4, "max_tokens": 3000
        }
        res = requests.post("https://api.groq.com/openai/v1/chat/completions", 
                            headers={"Authorization": f"Bearer {GROQ_KEY}"}, json=data, timeout=60)
        return res.json()['choices'][0]['message']['content'] if res.status_code == 200 else None
    except: return None

for start, end, folder in lessons:
    path = os.path.join(BASE_OUTPUT, folder)
    if not os.path.exists(path): os.makedirs(path)
    for p in range(start, end + 1):
        src, dst = f"{DATA_PATH}{p}.txt", f"{path}/{p}.txt"
        if not os.path.exists(src) or (os.path.exists(dst) and os.path.getsize(dst) > 1000): continue
        print(f"🔄 معالجة ذكية للصفحة {p}...")
        res = call_groq(open(src, 'r', encoding='utf-8').read())
        if res:
            with open(dst, 'w', encoding='utf-8') as f: f.write(res)
            time.sleep(15)
