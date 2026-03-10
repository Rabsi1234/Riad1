# -*- coding: utf-8 -*-
import os
import shutil
import re

base_path = "/var/www/html/montage_2008/religion_lab/summaries"
# المجلد المكركب اللي فيه كل الملفات
source_folder = os.path.join(base_path, "باقي_المادة")

# خريطة الدروس الحقيقية (توزيع الصفحات)
lessons = [
    (41, 50, "06_آداب_المعاشرة_الزوجية"),
    (51, 60, "07_حقوق_الأولاد_في_الإسلام"),
    (61, 75, "08_نظام_الميراث_في_الإسلام"),
    (76, 85, "09_العفة_وضوابطها"),
    (86, 95, "10_النهج_النبوي_في_الدعوة"),
    (96, 105, "11_فقه_الأولويات"),
    (106, 115, "12_حق_الطريق_وأدب_الحوار"),
    (116, 125, "13_الحرية_في_الإسلام"),
    (126, 140, "14_قضايا_معاصرة"),
    (141, 150, "15_الإشاعة_ومراجعة_عامة")
]

def organize():
    if not os.path.exists(source_folder):
        print(f"❌ المجلد {source_folder} غير موجود!")
        return

    # جلب كل الملفات اللي بتبدأ بـ pro_page
    files = [f for f in os.listdir(source_folder) if f.startswith("pro_page_")]
    
    for file_name in files:
        # استخراج رقم الصفحة من اسم الملف
        match = re.search(r'pro_page_(\144+)\.txt', file_name) # تعديل بسيط للقراءة
        # إذا ما ضبط الريجكس، بنستخدم الطريقة التقليدية
        try:
            pg_num = int(file_name.split('_')[-1].split('.')[0])
        except:
            continue

        # البحث عن المجلد المناسب حسب رقم الصفحة
        for start, end, folder_name in lessons:
            if start <= pg_num <= end:
                target_dir = os.path.join(base_path, folder_name)
                os.makedirs(target_dir, exist_ok=True)
                
                # نقل الملف
                shutil.move(os.path.join(source_folder, file_name), os.path.join(target_dir, file_name))
                print(f"✅ نقلت صفحة {pg_num} إلى مجلد: {folder_name}")
                break

if __name__ == "__main__":
    organize()
