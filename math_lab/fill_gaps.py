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
                {"role": "system", "content": "أنت بروفيسور رياضيات توجيهي علمي أردني خبير بمنهاج كولينز. شرحك عميق جداً، يستخدم LaTeX بدقة، ويركز على الحلول النموذجية الوزارية."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )
        return completion.choices[0].message.content
    except Exception:
        current_key_index += 1
        time.sleep(15)
        return call_ai(prompt)

base_dir = "/var/www/html/montage_2008/math_lab/summaries/"

# الدروس المفقودة فقط بالترتيب الصحيح
missing_lessons = [
    {"name": "الوحدة_5_الدرس_2_المستقيمات_في_الفضاء", "range": range(126, 142)},
    {"name": "الوحدة_5_الدرس_3_الضرب_القياسي", "range": range(142, 154)},
    {"name": "الوحدة_5_اختبار_نهاية_الوحدة", "range": range(154, 160)}
]

for lesson in missing_lessons:
    lesson_dir = os.path.join(base_dir, lesson["name"])
    os.makedirs(lesson_dir, exist_ok=True)
    for page in lesson["range"]:
        file_path = os.path.join(lesson_dir, f"math_pro_page_{page}.txt")
        if os.path.exists(file_path): continue 
        
        print(f"🚀 بناء احترافي للصفحة {page} (درس: {lesson['name']})...")
        prompt = f"""
        اشرح الصفحة {page} من درس ({lesson['name']}) توجيهي علمي أردني.
        1. القواعد الرياضية بـ LaTeX دقيق (مثل معادلة المستقيم المتجهة والضرب القياسي).
        2. حل أمثلة الكتاب خطوة بخطوة مع توضيح 'لماذا فعلنا ذلك'.
        3. خطوات الحل واضحة للطالب المتوسط (بأسلوب الأستاذ المتمكن).
        4. 3 أسئلة قدرات عليا (نمط وزاري) مع الحل.
        5. نصيحة ذهبية لتجنب الأخطاء الشائعة في هذا الدرس.
        """
        analysis = call_ai(prompt)
        with open(file_path, "w", encoding="utf-8-sig") as f:
            f.write(analysis)
        time.sleep(20)
