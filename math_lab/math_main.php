<?php
header('Content-Type: text/html; charset=utf-8');
$lesson = isset($_GET['lesson']) ? $_GET['lesson'] : null;
$current_summaries_path = "summaries/";
$images_path = "../Math_Student/data/";
?>
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>🔢 معمل الرياضيات - النسخة المعتمدة</title>
    
    <script>
      window.MathJax = {
        tex: {
          inlineMath: [['$', '$'], ['\\(', '\\)']],
          displayMath: [['$$', '$$'], ['\\[', '\\]']],
          processEscapes: true
        },
        options: {
          ignoreHtmlClass: 'no-mathjax',
          processHtmlClass: 'mathjax-process'
        }
      };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>

    <style>
        :root { --math-blue: #00d4ff; --dark-bg: #080808; --panel-bg: #141414; }
        body { font-family: 'Segoe UI', sans-serif; background: var(--dark-bg); color: #FFFFFF; margin: 0; height: 100vh; display: flex; flex-direction: column; overflow: hidden; }
        .top-nav { height: 65px; display: flex; gap: 10px; padding: 10px 20px; background: #000; border-bottom: 2px solid var(--math-blue); align-items: center; }
        .btn-main { text-decoration: none; color: #fff; padding: 10px; border-radius: 5px; border: 1px solid #333; background: #141414; flex: 1; text-align: center; font-size: 13px; transition: 0.3s; }
        .main-layout { display: flex; flex: 1; overflow: hidden; flex-direction: row-reverse; }
        .content-viewer { flex: 2; background: #0f0f0f; padding: 25px; overflow-y: auto; scroll-behavior: smooth; border-right: 1px solid #333; }
        .page-box { background: #1a1a1a; border-right: 5px solid var(--math-blue); padding: 25px; border-radius: 10px; margin-bottom: 40px; }
        .sidebar-container { width: 400px; display: flex; flex-direction: column; background: var(--panel-bg); border-left: 1px solid #333; }
        .lesson-list { height: 200px; overflow-y: auto; padding: 10px; border-bottom: 2px solid #333; }
        .unit-link { display: block; color: #ccc; text-decoration: none; padding: 10px; border-bottom: 1px solid #222; font-size: 13px; text-align: right; }
        .unit-link:hover, .unit-active { background: #1d1d1d; color: var(--math-blue); border-right: 3px solid var(--math-blue); }
        .page-image-viewer { flex: 1; overflow-y: auto; padding: 15px; background: #000; text-align: center; }
        .img-card { width: 100%; margin-bottom: 25px; border: 1px solid #333; border-radius: 8px; position: relative; cursor: pointer; transition: 0.2s; background: #050505; }
        .img-card:hover { transform: scale(1.02); border-color: var(--math-blue); }
        .img-card img { width: 100%; display: block; border-radius: 7px; }
        .img-tag { position: absolute; top: 8px; right: 8px; background: var(--math-blue); color: #000; padding: 3px 10px; font-size: 11px; font-weight: bold; border-radius: 4px; z-index: 5; }
        h3 { color: var(--math-blue); border-bottom: 1px solid #333; padding-bottom: 10px; }
        
        /* تحسين مظهر المعادلات */
        .math-content { line-height: 2; font-size: 19px; }
        mjx-container { direction: ltr !important; } /* لجعل المعادلات تظهر من اليسار لليمين */
    </style>
</head>
<body>
    <div class="top-nav">
        <a href="?type=math_student" class="btn-main" style="border-color:var(--math-blue); color:var(--math-blue);">📘 كتاب الرياضيات الأساسي</a>
        <a href="../master_encyclopedia.php" class="btn-main" style="border-color:#ff4444;">🏠 العودة للموسوعة</a>
    </div>
    <div class="main-layout">
        <div class="content-viewer">
            <?php
            if ($lesson) {
                $files = glob($current_summaries_path . $lesson . "/math_pro_page_*.txt");
                natsort($files);
                foreach ($files as $file) {
                    $p_num = filter_var(basename($file), FILTER_SANITIZE_NUMBER_INT);
                    $content = file_get_contents($file);
                    
                    // تنظيف النص وتجهيزه للرسم
                    $clean_content = preg_replace('/^\xEF\xBB\xBF/', '', $content);
                    // ملاحظة: أزلنا htmlspecialchars لكي يعمل الـ MathJax
                    $formatted = nl2br($clean_content); 

                    echo "<div class='page-box' id='page-anchor-$p_num'>";
                    echo "<h3>📊 تحليل المسألة: صفحة $p_num</h3>";
                    echo "<div class='math-content mathjax-process'>$formatted</div>";
                    echo "</div>";
                }
            } else {
                echo "<div style='text-align:center; margin-top:100px; opacity:0.3;'><h2>اختر درساً من القائمة اليمينية</h2></div>";
            }
            ?>
        </div>
        <div class="sidebar-container">
            <div class="lesson-list">
                <h4 style="color:var(--math-blue); margin-right:10px;">📂 وحدات المادة</h4>
                <?php
                $dirs = array_filter(glob($current_summaries_path . '*'), 'is_dir');
                foreach ($dirs as $dir) {
                    $name = basename($dir);
                    $active = ($lesson == $name) ? 'unit-active' : '';
                    echo "<a href='?lesson=$name' class='unit-link $active'>📁 ".str_replace('_', ' ', $name)."</a>";
                }
                ?>
            </div>
            <div class="page-image-viewer">
                <?php if ($lesson): ?>
                    <?php
                    foreach ($files as $file) {
                        $p_num = filter_var(basename($file), FILTER_SANITIZE_NUMBER_INT);
                        $img_file = $images_path . $p_num . ".png";
                        echo "
                        <div class='img-card' onclick='scrollToPage(\"$p_num\")'>
                            <span class='img-tag'>Page $p_num</span>
                            <img src='$img_file' onerror=\"this.src='https://via.placeholder.com/300x450?text=Page+$p_num';\">
                        </div>";
                    }
                    ?>
                <?php endif; ?>
            </div>
        </div>
    </div>
    <script>
    function scrollToPage(pNum) {
        const element = document.getElementById('page-anchor-' + pNum);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
    </script>
</body>
</html>
