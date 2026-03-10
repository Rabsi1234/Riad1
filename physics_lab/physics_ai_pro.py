import os
import time
from groq import Groq

api_keys = [
    "YOUR_GROQ_API_KEY",
    "YOUR_GROQ_API_KEY",
    "YOUR_GROQ_API_KEY",
    "YOUR_GROQ_API_KEY",
    "YOUR_GROQ_API_KEY",
    "YOUR_GROQ_API_KEY"
]

current_key_index = 0

lessons = [
    {"name": "القوة_المغناطيسية", "range": range(10, 28)},
    {"name": "المجال_المغناطيسي_الناشئ_عن_تيار", "range": range(28, 41)},
    {"name": "الحث_الكهرمغناطيسي", "range": range(41, 63)},
    {"name": "دارات_التيار_الكهربائي_المتردد", "range": range(66, 82)},
    {"name": "الدارات_الإلكترونية", "range": range(82, 99)},
    {"name": "الطبيعة_الجسيمية_للضوء", "range": range(102, 137)},
    {"name": "تركيب_النواة_وخصائصها", "range": range(140, 152)},
    {"name": "الإشعاع_النووي", "range": range(152, 167)},
    {"name": "التفاعلات_النووية", "range": range(167, 181)}
]

def call_ai(prompt):
    global current_key_index
    client = Groq(api_key=api_keys[current_key_index])
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "أنت بروفيسور فيزياء خبير في المنهاج الأردني (توجيهي). ممنوع استخدام أي لغة غير العربية. اشرح بعمق وتفصيل ممل. ارسم المعادلات باستخدام $$ LaTeX $$ فقط."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"⚠️ خطأ في المفتاح {current_key_index}: {str(e)}")
        if "429" in str(e):
            time.sleep(15)
        current_key_index = (current_key_index + 1) % len(api_keys)
        return call_ai(prompt)

base_dir = "/var/www/html/montage_2008/physics_lab/summaries/"

for lesson in lessons:
    lesson_name = lesson["name"]
    lesson_dir = os.path.join(base_dir, lesson_name)
    os.makedirs(lesson_dir, exist_ok=True)
    
    print(f"\n🚀 معالجة درس: {lesson_name}")
    
    for page in lesson["range"]:
        file_path = os.path.join(lesson_dir, f"analysis_page_{page}.txt")
        
        if os.path.exists(file_path) and os.path.getsize(file_path) > 800:
            print(f"✅ صفحة {page} جاهزة مسبقاً بجودة عالية.")
            continue

        print(f"🔬 تحليل تفصيلي للصفحة {page}...")
        
        prompt = f"""
        حلل الصفحة {page} من درس ({lesson_name}) بأسلوب مدرس توجيهي أردني عبقري.
        
        الشروط الصارمة:
        1. اللغة: عربية فصحى فقط (ممنوع أي كلمات إنجليزية أو رموز غريبة).
        2. العمق: اشرح كل تفصيلة في الصفحة، لا تترك فقرة بدون تحليل.
        3. المعادلات: اكتبها بتنسيق LaTeX الرائع لتبدو مرسومة (مثلاً $$ \\epsilon = -N \\frac{{\\Delta \\Phi}}{{\\Delta t}} $$).
        4. المحتوى: 
           - مقدمة تربط الصفحة بما قبلها.
           - شرح تفصيلي للنصوص والقوانين.
           - مثال حسابي "مستوى وزارة" مع حل خطوة بخطوة.
           - 5 أسئلة متنوعة (علل، استنتج، حسابي) مع الإجابات.
           - ملخص "نقاط القوة" للطلاب.
        
        أريد أن يشعر الطالب أن الصفحة بين يديه أصبحت كنزاً من المعلومات.
        """
        
        analysis = call_ai(prompt)
        with open(file_path, "w", encoding="utf-8-sig") as f:
            f.write(analysis)
        
        time.sleep(3)

print("\n✨ تم الانتهاء من جميع الدروس بجودة البروفيسور!")
