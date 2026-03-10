import os
import requests
import time

# قائمة المفاتيح الخاصة بك
API_KEYS = [
    "REMOVED_API_KEY",
    "REMOVED_API_KEY",
    "REMOVED_API_KEY",
    "REMOVED_API_KEY",
    "REMOVED_API_KEY",
    "REMOVED_API_KEY",
    "REMOVED_API_KEY",
    "REMOVED_API_KEY",
    "REMOVED_API_KEY",
    "REMOVED_API_KEY"
]

current_key_index = 0

# تعريف الدروس ونطاق الصفحات حسب الفهرس
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

def get_chat_response(prompt):
    global current_key_index
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    while current_key_index < len(API_KEYS):
        headers = {
            "Authorization": f"Bearer {API_KEYS[current_key_index]}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.4
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            elif response.status_code == 429: # كوتة انتهت
                print(f"⚠️ Key {current_key_index} limit reached. Switching...")
                current_key_index += 1
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                current_key_index += 1
        except Exception as e:
            print(f"❌ Exception: {e}")
            current_key_index += 1
    return None

prompt_template = """
أنت خبير تربوي متخصص في التربية الإسلامية للمنهاج الأردني.
بناءً على النص الأصلي المرفق من الصفحة، قم بإنشاء شرح "نانو" مكثف واحترافي يتضمن:
1. **تلخيص الصفحة**: الأفكار الجوهرية بأسلوب مركز.
2. **شرح مفصل**: تحليل المفاهيم والفقرات بوضوح وعمق.
3. **أمثلة توضيحية**: لتقريب الفهم للطالب.
4. **بنك الأسئلة**: استخرج أهم الأسئلة (ضع السؤال وإجابته المتوقعة والمقترحة).

النص الأصلي:
{content}
"""

for start, end, folder_name in lessons:
    print(f"📂 معالجة الدرس: {folder_name}")
    for p in range(start, end + 1):
        source_file = os.path.join(DATA_PATH, f"{p}.txt")
        output_folder = os.path.join(BASE_OUTPUT, folder_name)
        output_file = os.path.join(output_folder, f"{p}.txt")

        if not os.path.exists(source_file): continue
        if os.path.exists(output_file): 
            print(f"  ⏩ صفحة {p} موجودة مسبقاً.")
            continue

        with open(source_file, 'r', encoding='utf-8') as f:
            raw_text = f.read()

        print(f"  🧠 جاري تحليل صفحة {p} باستخدام مفتاح {current_key_index}...")
        ai_sharih = get_chat_response(prompt_template.format(content=raw_text))

        if ai_sharih:
            with open(output_file, 'w', encoding='utf-8') as f_out:
                f_out.write(ai_sharih)
            print(f"  ✅ تم حفظ شرح صفحة {p}")
            time.sleep(0.5) # حماية من السبام
        else:
            print("🛑 توقفت العملية: نفدت المفاتيح الشغالة أو حدث خطأ.")
            exit()

print("✨ انتهى استخراج الشرح لجميع الدروس والصفحات!")
