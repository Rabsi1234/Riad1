<?php
header('Content-Type: text/html; charset=utf-8');
$lesson = isset($_GET['lesson']) ? $_GET['lesson'] : null;
?>
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>معمل الفيزياء - القائمة الشاملة</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/MathJax.js?config=TeX-MML-AM_CHTML"></script>
    <style>
        body { font-family: 'Arial', sans-serif; background: #080808; color: #FFFFFF; padding: 20px; line-height: 1.8; }
        .nav-menu { background: #141414; padding: 15px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #333; }
        .nav-link { color: #00FF00; text-decoration: none; margin: 5px; display: inline-block; padding: 8px 15px; background: #222; border-radius: 5px; }
        .nav-link:hover { background: #00FF00; color: #000; }
        .page-box { background: #141414; border-right: 6px solid #00FF00; margin-bottom: 40px; padding: 30px; border-radius: 12px; }
        h3 { color: #81C784; background: rgba(0,255,0,0.1); padding: 10px; border-radius: 5px; }
        pre { white-space: pre-wrap; font-size: 18px; color: #fff; }
    </style>
</head>
<body>
    <h1>🔬 معمل الفيزياء: القائمة الكاملة</h1>
    <div class="nav-menu">
        <strong>اختر الدرس:</strong><br>
        <?php
        $dirs = array_filter(glob('*'), 'is_dir');
        foreach ($dirs as $dir) {
            echo "<a class='nav-link' href='?lesson=$dir'>$dir</a>";
        }
        ?>
    </div>
    <hr>
    <?php
    if ($lesson) {
        echo "<h2>عرض درس: " . htmlspecialchars($lesson) . "</h2>";
        $files = glob("$lesson/analysis_page_*.txt");
        natsort($files);
        foreach ($files as $file) {
            $content = file_get_contents($file);
            $formatted = nl2br(htmlspecialchars(preg_replace('/^\xEF\xBB\xBF/', '', $content)));
            $formatted = preg_replace('/\*\*(.*?)\*\*/', '<h3>$1</h3>', $formatted);
            echo "<div class='page-box'><h3>" . basename($file) . "</h3><pre>$formatted</pre></div>";
        }
    }
    ?>
</body>
</html>
