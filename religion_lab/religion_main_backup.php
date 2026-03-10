<?php
header('Content-Type: text/html; charset=utf-8');
$lesson = isset($_GET['lesson']) ? $_GET['lesson'] : null;

// المسار داخل معمل التربية الإسلامية
$current_summaries_path = "summaries/";
// مسار الصور (عدله حسب وين حاطط صور كتاب الدين)
$images_path = "../Religion/data/"; 
?>
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>📚 نانو التربية الإسلامية - الأستاذ تيم</title>
    <style>
        html { background-color: #0a0a0a; scrollbar-color: #333 #0a0a0a; scrollbar-width: thin; }
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: #0a0a0a; }
        ::-webkit-scrollbar-thumb { background: #222; border-radius: 10px; border: 2px solid #0a0a0a; }
        ::-webkit-scrollbar-thumb:hover { background: #27ae60; }
        :root { 
            --islam-green: #2ecc71; 
            --dark-bg: #050505; 
            --panel-bg: #111; 
        }
        * { box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, sans-serif; background: var(--dark-bg); color: #fff; margin: 0; height: 100vh; overflow: hidden; display: flex; flex-direction: column; }
        
        .top-nav { height: 60px; background: #000; border-bottom: 2px solid var(--islam-green); display: flex; align-items: center; padding: 0 20px; gap: 15px; z-index: 100; }
        .btn-main { text-decoration: none; color: #fff; padding: 8px 15px; border-radius: 5px; border: 1px solid #333; font-size: 13px; background: #1a1a1a; transition: 0.3s; }
        .btn-main:hover { border-color: var(--islam-green); color: var(--islam-green); }
        
        .nano-container { display: flex; flex: 1; overflow: hidden; width: 100%; }
        
        .side-panel { width: 350px; background: var(--panel-bg); border-left: 1px solid #222; display: flex; flex-direction: column; }
        .side-lessons { height: 45%; overflow-y: auto; border-bottom: 2px solid #222; }
        .lesson-item { padding: 12px 15px; border-bottom: 1px solid #222; color: #ccc; text-decoration: none; font-size: 14px; display: block; transition: 0.2s; }
        .lesson-item:hover, .active-lesson { background: #1a1a1a; color: var(--islam-green); border-right: 4px solid var(--islam-green); }
        
        .side-images { flex: 1; overflow-y: auto; padding: 15px; background: #000; }
        .img-wrapper { position: relative; margin-bottom: 20px; border: 1px solid #333; border-radius: 8px; cursor: pointer; }
        .img-wrapper img { width: 100%; display: block; border-radius: 8px; }
        .img-label { position: absolute; top: 5px; left: 5px; background: var(--islam-green); color: #fff; padding: 2px 8px; border-radius: 4px; font-size: 11px; }
        
        .main-content { flex: 1; background: #0a0a0a; padding: 30px; overflow-y: auto; }
        .page-card { background: #161616; padding: 25px; border-radius: 12px; border-right: 6px solid var(--islam-green); margin-bottom: 40px; line-height: 1.8; font-size: 19px; }
        .page-card h3 { color: var(--islam-green); border-bottom: 1px solid #333; padding-bottom: 10px; margin-top: 0; }
        
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-thumb { background: #333; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--islam-green); }
    </style>
</head>
<body>
    <div class="top-nav">
        <div style="font-weight: bold; color: var(--islam-green); font-size: 18px; margin-left: 20px;">📖 نانو التربية الإسلامية</div>
        <a href="?lesson=<?= urlencode($lesson) ?>" class="btn-main">تحديث</a>
        <a href="../master_encyclopedia.php" class="btn-main" style="border-color: #ff4444;">الخروج</a>
    </div>

    <div class="nano-container">
        <div class="side-panel">
            <div class="side-lessons">
                <div style="padding: 10px; font-weight: bold; color: #555; font-size: 11px;">📂 الدروس المتاحة</div>
                <?php
                if (is_dir($current_summaries_path)) {
                    $dirs = array_filter(glob($current_summaries_path . '*'), 'is_dir');
                    natsort($dirs);
                    foreach ($dirs as $dir) {
                        $name = basename($dir);
                        $displayName = str_replace('_', ' ', preg_replace('/^\d+_/', '', $name));
                        $activeClass = ($lesson == $name) ? 'active-lesson' : '';
                        echo "<a href='?lesson=".urlencode($name)."' class='lesson-item $activeClass'>📖 $displayName</a>";
                    }
                }
                ?>
            </div>
            <div class="side-images">
                <?php if ($lesson):
                    $files = glob($current_summaries_path . $lesson . "/pro_page_*.txt");
                    natsort($files);
                    foreach ($files as $file):
                        preg_match('/pro_page_(\d+)/', basename($file), $matches);
                        $p_num = $matches[1] ?? '0';
                        $img_file = $images_path . $p_num . ".png"; ?>
                        <div class='img-wrapper' onclick='document.getElementById("page-<?=$p_num?>").scrollIntoView({behavior:"smooth"})'>
                            <span class='img-label'>صورة <?=$p_num?></span>
                            <img src='<?=$img_file?>' onerror="this.src='https://via.placeholder.com/350x500/111/2ecc71?text=P+<?=$p_num?>';">
                        </div>
                <?php endforeach; endif; ?>
            </div>
        </div>
        <div class="main-content">
            <?php if ($lesson && !empty($files)):
                foreach ($files as $file):
                    preg_match('/pro_page_(\d+)/', basename($file), $matches);
                    $p_num = $matches[1] ?? '0';
                    $content = file_get_contents($file);
                    $content = preg_replace('/^\xEF\xBB\xBF/', '', $content);
                    echo "<div class='page-card' id='page-$p_num'><h3>📝 شرح الصفحة $p_num</h3><div>" . nl2br(htmlspecialchars($content)) . "</div></div>";
                endforeach;
            else:
                echo "<div style='text-align:center; margin-top:150px; color:#444;'><h2>اختر درساً للبدء في تصفح الشرح</h2></div>";
            endif; ?>
        </div>
    </div>
</body>
</html>
