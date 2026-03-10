import os
import google.generativeai as genai
import time

# مفتاح Gemini الخاص بك
GEMINI_KEY = "AIzaSyBTEhWUtmbTin9YNcZlP5ogp8GEvWKKgTA"
genai.configure(api_key=GEMINI_KEY)

# قائمة الموديلات "الانتحارية" - سيجربها واحداً تلو الآخر
MODELS_TO_TRY = [
    'gemini-3.0-alpha',      # موديل الجيل القادم (إذا كان متاحاً لمفتاحك)
    'gemini-2.5-flash-exp',  # الموديل التجريبي 2.5
    'gemini-2.0-flash',      # الموديل السريع 2.0
    'gemini-1.5-flash',      # الموديل المستقر
    'gemini-1.5-pro'         # الموديل القوي
]

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

prompt_template = """
أنت خبير تربوي في المنهاج الأردني لمادة التربية الإسلامية.
بناءً على النص المرفق، قم بإنشاء شرح "نانو" مكثف يتضمن:
1. **تلخيص مركز**: أهم الأفكار.
2. **شرح تفصيلي**: تبسيط المفاهيم.
3. **أمثلة وبنك أسئلة**: (سؤال وجواب) متوقعة.
النص: {content}
"""

def generate_with_failover(content):
    for model_name in MODELS_TO_TRY:
        try:
            print(f"    🔄 جاري التجربة بالموديل: {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt_template.format(content=content))
            if response and response.text:
                return response.text, model_name
        except Exception as e:
            error_msg = str(e)[:50]
            print(f"    ❌ فشل {model_name}: {error_msg}")
            continue
    return None, None

for start, end, folder in lessons:
    print(f"📁 الدرس: {folder}")
    out_dir = os.path.join(BASE_OUTPUT, folder)
    if not os.path.exists(out_dir): os.makedirs(out_dir)

    for p in range(start, end + 1):
        src = f"{DATA_PATH}{p}.txt"
        out_f = f"{out_dir}/{p}.txt"

        if not os.path.exists(src) or os.path.exists(out_f): continue

        with open(src, 'r', encoding='utf-8') as f:
            text = f.read()

        print(f"  🧠 تحليل صفحة {p}...")
        result, success_model = generate_with_failover(text)
        
        if result:
            with open(out_f, 'w', encoding='utf-8') as f_out:
                f_out.write(result)
            print(f"  ✅ تم بنجاح باستخدام [{success_model}]")
            time.sleep(4)
        else:
            print(f"  🛑 للأسف: جميع الموديلات (بما فيها 2.5 و 3.0) لم تعمل مع هذا المفتاح.")
            exit() # توقف لفحص المفتاح
