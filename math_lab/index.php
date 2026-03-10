<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>معمل الرياضيات - الأستاذ تيم</title>
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; background-color: #f4f4f9; padding: 20px; }
        .container { max-width: 900px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
        .lesson-box { background: #e8f4fd; padding: 15px; margin-bottom: 10px; border-right: 5px solid #3498db; }
        pre { white-space: pre-wrap; word-wrap: break-word; font-size: 1.1em; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📐 شروحات مادة الرياضيات - التوجيهي الأردني</h1>
        <?php
        $dir = "summaries/";
        if (isset($_GET['file'])) {
            $file = $_GET['file'];
            echo "<a href='index.php'>⬅️ العودة للدروس</a><hr>";
            echo "<pre>" . file_get_contents($file) . "</pre>";
        } else {
            $folders = glob($dir . '*', GLOB_ONLYDIR);
            foreach ($folders as $folder) {
                echo "<div class='lesson-box'><h3>📂 " . basename($folder) . "</h3>";
                $files = glob($folder . '/*.txt');
                foreach ($files as $f) {
                    echo "<li><a href='index.php?file=$f'>" . basename($f) . "</a></li>";
                }
                echo "</div>";
            }
        }
        ?>
    </div>
</body>
</html>
