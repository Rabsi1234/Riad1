import os
import time
import requests

GROQ_KEY = "REMOVED_API_KEY"
MODEL_NAME = "llama-3.3-70b-versatile"

lessons = [
    (6, 12, "01_السنن_الإلهية_في_الكون_والإنسان"),
    (13, 146, "All_Remaining_Lessons") # سيعالج كل الدروس المتبقية
]

DATA_PATH = "/var/www/html/montage_2008/Religion/data/"
BASE_OUTPUT = "/var/www/html/montage_2008/religion_lab/summaries/"

# البرومبت الجديد: "المعلم المفصل"
prompt_template = """
أنت خبير تربوي في المنهاج الأردني. النص التالي هو صفحة من كتاب التربية الإسلامية.
المطلوب منك هو إنتاج "شرح نانو" فائق التفصيل (أريد محتوى طويلاً يغطي كل كلمة في النص):

1. **تلخيص مركز**: أهم الأفكار الرئيسية في نقاط.
2. **شرح تفصيلي وشامل**: اشرح كل فقرة في النص الأصلي بعمق وبساطة، لا تترك أي معلومة دون شرح.
3. **أمثلة توضيحية**: أعطِ أمثلة واقعية من حياة الطلاب في الأردن لتوضيح المفاهيم.
4. **بنك أسئلة امتحانية**: اكتب 5 أسئلة (منوعة بين استنتاجي ومباشر) مع إجاباتها النموذجية بناءً على هذه الصفحة فقط.

النص المراد شرحه:
{content}
"""

def call_groq(content):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt_template.format(content=content)}],
        "temperature": 0.5,
        "max_tokens": 4096 # لضمان عدم انقطاع الشرح الطويل
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        elif response.status_code == 429:
            print("⏳ Rate limit.. waiting 30s")
            time.sleep(30)
            return call_groq(content) # إعادة محاولة
    except:
        return None

for start, end, folder in lessons:
    # ملاحظة: سأقوم هنا بمعالجة كل الملفات في data
    for p in range(6, 147): # من صفحة 6 إلى آخر صفحة
        src_f = f"{DATA_PATH}{p}.txt"
        if not os.path.exists(src_f): continue
        
        # تحديد المجلد الصحيح بناءً على رقم الصفحة (أو وضعه في مجلد عام مؤقتاً)
        # لتسهيل الأمر سنضعها في مجلدها الأصلي
        # (يفضل مسح الملفات القديمة التي حجمها صغير جداً ليعيد كتابتها)
        
        print(f"🧠 جاري إنتاج شرح "دسم" للصفحة {p}...")
        result = call_groq(open(src_f, 'r', encoding='utf-8').read())
        
        if result:
            # ابحث عن المجلد المناسب أو أنشئه
            # سأحفظها حالياً في مسار موحد ليسهل عليك فحصها
            save_path = f"{BASE_OUTPUT}detailed_summaries/"
            if not os.path.exists(save_path): os.makedirs(save_path)
            
            with open(f"{save_path}{p}.txt", 'w', encoding='utf-8') as f_out:
                f_out.write(result)
            print(f"✅ تم إنتاج شرح كامل للصفحة {p}")
            time.sleep(15)

