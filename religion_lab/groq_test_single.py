import os
import requests

GROQ_KEY = "REMOVED_API_KEY"
MODEL_NAME = "llama-3.3-70b-versatile"

# برومبت يمنع التكرار نهائياً ويطلب جودة بدل الكمية
PROMPT_SYSTEM = """
أنت عالم ومفكر إسلامي. اشرح النص المرفق شرحاً أكاديمياً دقيقاً.
القواعد:
1. يمنع تكرار أي جملة أو فكرة مرتين.
2. الشرح يجب أن يكون غنياً بالمعلومات (أريد جودة في المحتوى).
3. قسم الشرح إلى: (المفاهيم العميقة، التفسير العملي، الربط بالواقع الأردني).
4. بنك الأسئلة يجب أن يكون ذكياً (أسئلة استنتاجية وليس مجرد نسخ).
"""

def call_groq(content):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
    data = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": PROMPT_SYSTEM},
            {"role": "user", "content": f"حلل هذا النص بذكاء ودون تكرار: \n\n {content}"}
        ],
        "temperature": 0.4, # تقليل الحرارة لزيادة الدقة ومنع الهبد
        "max_tokens": 2000 
    }
    res = requests.post(url, headers=headers, json=data)
    return res.json()['choices'][0]['message']['content'] if res.status_code == 200 else "Error"

# تجربة على الصفحة 6 فقط
with open("/var/www/html/montage_2008/Religion/data/6.txt", 'r', encoding='utf-8') as f:
    result = call_groq(f.read())
    
with open("/var/www/html/montage_2008/religion_lab/summaries/6.txt", 'w', encoding='utf-8') as f_out:
    f_out.write(result)
print("✅ تمت تجربة الصفحة 6 بنجاح. افحصها الآن.")
