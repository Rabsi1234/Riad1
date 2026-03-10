import os, time, requests

GROQ_KEY = "REMOVED_API_KEY"
MODEL_NAME = "llama-3.3-70b-versatile"
DATA_PATH = "/var/www/html/montage_2008/Religion/data/"
BASE_OUTPUT = "/var/www/html/montage_2008/religion_lab/summaries/"

# علامة الـ BOM لضمان اللغة العربية في المتصفحات
UTF8_BOM = b'\xef\xbb\xbf'

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

PROMPT_SYSTEM = """أنت خبير في المنهاج الأردني. اشرح النص المرفق بأسلوب 'نانو دسم' وعميق.
المطلوب:
1. شرح تفصيلي لكل فقرة دون تكرار.
2. 3 أمثلة من المجتمع الأردني.
3. بنك أسئلة (10 أسئلة وأجوبة نموذجية).
اكتب باللغة العربية الفصحى فقط."""

def call_groq(content):
    try:
        data = {
            "model": MODEL_NAME,
            "messages": [{"role": "system", "content": PROMPT_SYSTEM}, {"role": "user", "content": content}],
            "temperature": 0.4, "max_tokens": 3500
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
        
        # إذا الملف موجود ومكتوب صح (أكبر من 500 حرف) لا تصرف رصيد وتخطاه
        if os.path.exists(dst) and os.path.getsize(dst) > 500:
            print(f"⏩ الصفحة {p} جاهزة أصلاً، تم التخطي لتوفير الرصيد.")
            continue
            
        if not os.path.exists(src): continue
        
        print(f"🧠 جاري إنتاج شرح دسم (عربي مضمون) للصفحة {p}...")
        with open(src, 'r', encoding='utf-8') as f_in:
            raw_text = f_in.read()
            
        response_text = call_groq(raw_text)
        
        if response_text:
            # كتابة الملف بنظام الباينري لإضافة الختم (BOM) لضمان ظهور العربي
            with open(dst, 'wb') as f_out:
                f_out.write(UTF8_BOM)
                f_out.write(response_text.encode('utf-8'))
            print(f"✅ تم حفظ الصفحة {p} بنجاح.")
            time.sleep(35) # أمان للمفتاح
        else:
            print(f"❌ فشل في معالجة الصفحة {p}")

print("✨ المهمة انتهت بنجاح كامل!")
