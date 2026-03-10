import os
import time
from groq import Groq

api_keys = [
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

def call_ai(prompt):
    global current_key_index
    client = Groq(api_key=api_keys[current_key_index % len(api_keys)])
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "أنت بروفيسور رياضيات توجيهي علمي أردني. تخصصك هو منهاج 'كولينز' المطور. شرحك يجب أن يكون دقيقاً جداً، يستخدم المصطلحات العلمية الصحيحة، ولا يقبل بأي تبسيط مخل."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        return completion.choices[0].message.content
    except Exception as e:
        current_key_index += 1
        time.sleep(15)
        return call_ai(prompt)

base_dir = "/var/www/html/montage_2008/math_lab/summaries/"

lessons = [
    {"name": "الدرس_1_تكامل_اقترانات_خاصة", "range": range(8, 26)},
    {"name": "الدرس_2_التكامل_بالتعويض", "range": range(26, 45)},
    {"name": "الدرس_3_التكامل_بالكسور_الجزئية", "range": range(45, 58)},
    {"name": "الدرس_4_التكامل_بالأجزاء", "range": range(58, 72)},
    {"name": "الدرس_5_المساحات_والحجوم", "range": range(72, 88)},
    {"name": "الدرس_6_المعادلات_التفاضلية", "range": range(89, 103)},
    {"name": "الدرس_1_المتجهات_في_الفضاء", "range": range(108, 124)},
    {"name": "الدرس_1_التوزيع_الهندسي_وذي_الحدين", "range": range(160, 176)},
    {"name": "الدرس_2_التوزيع_الطبيعي", "range": range(176, 198)}
]

for lesson in lessons:
    lesson_dir = os.path.join(base_dir, lesson["name"])
    os.makedirs(lesson_dir, exist_ok=True)
    for page in lesson["range"]:
        file_path = os.path.join(lesson_dir, f"math_pro_page_{page}.txt")
        if os.path.exists(file_path): continue 
        
        print(f"🔥 إعادة بناء احترافية: صفحة {page}...")
        prompt = f"""
        حلل واشرح الصفحة {page} من درس ({lesson['name']}) لمنهاج التوجيهي العلمي الأردني (جيل 2006/2007).
        1. اشرح القوانين بـ LaTeX معقد واحترافي (تكاملات، متجهات، توزيعات).
        2. حل أمثلة الكتاب الحقيقية بخطوات رياضية كاملة (لا تقبل أنصاف الحلول).
        3. إضافة 3 أسئلة قدرات عليا بمستوى 'وزاري متميز'.
        4. ممنوع شرح أي قانون ابتدائي (مثل مساحة المثلث) إلا إذا كان داخل مسألة تكامل بين منحنيين.
        """
        analysis = call_ai(prompt)
        with open(file_path, "w", encoding="utf-8-sig") as f:
            f.write(analysis)
        time.sleep(15) # تبريد المفاتيح لضمان استمرار اليوم كاملاً
