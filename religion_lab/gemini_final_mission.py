import os
import google.generativeai as genai
import time

# المفتاح الجديد الذي زودتني به
GEMINI_KEY = "AIzaSyAPBfJ_kt7AZLXlvB1NJj7RwAjgHl5f4hE"
genai.configure(api_key=GEMINI_KEY)

# قائمة الموديلات التي سنقتحم بها الحظر (ترتيب ذكي)
MODELS_TO_TRY = [
    'gemini-2.0-flash',      # الأسرع والأحدث حالياً
    'gemini-2.0-flash-lite-preview-02-05', # موديل خفيف وجديد
    'gemini-1.5-flash',      # الأكثر قبولاً للمفاتيح المجانية
    'gemini-1.5-pro',        # للأداء العميق
    'models/gemini-1.0-pro'  # الموديل الكلاسيكي (كحل أخير)
]

# هيكلية الدروس
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
أنت خبير تربوي في المنهاج الأردني. قم بتحويل النص التالي لشرح "نانو":
1. تلخيص مركز.
2. شرح تفصيلي وعميق.
3. أمثلة توضيحية.
4. بنك أسئلة (سؤال وجواب متوقع).
النص: {content}
"""

def process_page(content):
    for m_name in MODELS_TO_TRY:
        try:
            print(f"    🔄 تجربة الموديل: {m_name}...")
            model = genai.GenerativeModel(m_name)
            response = model.generate_content(prompt_template.format(content=content))
            if response and response.text:
                return response.text, m_name
        except Exception as e:
            print(f"    ❌ فشل {m_name}: {str(e)[:40]}")
            continue
    return None, None

for start, end, folder in lessons:
    print(f"📁 معالجة: {folder}")
    out_path = os.path.join(BASE_OUTPUT, folder)
    if not os.path.exists(out_path): os.makedirs(out_path)

    for p in range(start, end + 1):
        src_f = f"{DATA_PATH}{p}.txt"
        dst_f = f"{out_path}/{p}.txt"

        if not os.path.exists(src_f) or os.path.exists(dst_f): continue

        with open(src_f, 'r', encoding='utf-8') as f:
            raw_data = f.read()

        print(f"  🧠 تحليل صفحة {p}...")
        ai_res, final_model = process_page(raw_data)
        
        if ai_res:
            with open(dst_f, 'w', encoding='utf-8') as f_out:
                f_out.write(ai_res)
            print(f"  ✅ تم الحفظ بنجاح بواسطة [{final_model}]")
            time.sleep(3) # أمان الكوتة المجانية
        else:
            print(f"  🛑 فشلت كل المحاولات لهذه الصفحة.")

print("✨ المهمة اكتملت!")
