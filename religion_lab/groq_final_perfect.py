# -*- coding: utf-8 -*-
import os
from openai import OpenAI
import time

API_KEY = "REMOVED_API_KEY"
# المسار اللي فيه الكنز (النصوص الجاهزة)
DATA_PATH = "/var/www/html/montage_2008/Religion/data"
BASE_OUT = "/var/www/html/montage_2008/religion_lab/summaries"

def get_client():
    return OpenAI(api_key=API_KEY, base_url="https://api.groq.com/openai/v1")

# خريطة المجلدات والصفحات
INDEX_MAP = [
    (6, 12, "01_السنن_الإلهية_في_الكون_والإنسان"),
    (13, 18, "02_تعظيم_الشعائر_الدينية"),
    (19, 25, "03_مكانة_الزكاة_وآثارها"),
    (26, 32, "04_عمارة_الأرض_في_الإسلام"),
    (33, 40, "05_نماذج_من_سلوك_الناس_في_القرآن_الكريم"),
    (41, 150, "باقي_المادة")
]

def process():
    client = get_client()
    
    for start, end, folder_name in INDEX_MAP:
        folder_path = os.path.join(BASE_OUT, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        for pg in range(start, end + 1):
            txt_file = os.path.join(DATA_PATH, f"{pg}.txt")
            
            if not os.path.exists(txt_file):
                print(f"⚠️ صفحة {pg} غير موجودة في data، تخطي...")
                continue

            try:
                with open(txt_file, "r", encoding="utf-8") as f:
                    content = f.read()

                prompt = f"أنت الأستاذ تيم. اشرح الصفحة {pg} من كتاب الدين التوجيهي الأردني شرحاً مفصلاً (نقاط، قيم، 5 أسئلة وزارية)."
                
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[{"role": "user", "content": prompt + "\n\nنص الصفحة الأصلي:\n" + content}],
                    temperature=0.4
                )
                
                output_file = os.path.join(folder_path, f"pro_page_{pg}.txt")
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(response.choices[0].message.content)
                
                print(f"✅ تم شرح صفحة {pg} بنجاح من ملف الـ txt.")
                time.sleep(10) # تبريد

            except Exception as e:
                print(f"❌ خطأ في صفحة {pg}: {e}")
                time.sleep(20)

if __name__ == "__main__":
    process()
