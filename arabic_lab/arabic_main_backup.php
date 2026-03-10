<?php header('Content-Type: text/html; charset=utf-8'); $book = 
isset($_GET['book']) ? $_GET['book'] : 'كتاب_النحو_والصرف'; $lesson = 
isset($_GET['lesson']) ? $_GET['lesson'] : null; $base_path = 
"/var/www/html/montage_2008/arabic_lab/"; $current_book_path = 
$base_path . $book . "/"; if ($book == 'كتاب_النحو_والصرف') {
    $images_path = "../Arabic_Grammar/data/";
} else {
    $images_path = "../Arabic_Literature/data/";
}
?> <!DOCTYPE html> <html lang="ar" dir="rtl"> <head> <meta 
    charset="UTF-8"> <title>📖 معمل العربية الرقمي - الأستاذ 
    رياض</title> <style>
        .page-card:target { animation: pulse-gold 1.5s ease-out; 
        border-right-color: #d4af37 !important; } @keyframes 
        pulse-gold { 0% { background-color: #333; transform: 
        scale(1.02); } 100% { background-color: #181818; transform: 
        scale(1); } } html { background-color: #0a0a0a; 
        scrollbar-color: #d4af37 #0a0a0a; scrollbar-width: thin; }
        ::-webkit-scrollbar { width: 8px; } -webkit-scrollbar-track { 
        ::background: #0a0a0a; } -webkit-scrollbar-thumb { 
        ::background: #d4af37; border-radius: 10px; }
        :root { --arab-green: #27ae60; --dark-bg: #0a0a0a; 
        :--panel-bg: #141414; --gold: #d4af37; }
        * { box-sizing: border-box; } body { font-family: 'Segoe UI', 
        Tahoma, sans-serif; background: var(--dark-bg); color: #fff; 
        margin: 0; height: 100vh; overflow: hidden; display: flex; 
        flex-direction: column; } .top-nav { height: 65px; 
        background: #000; border-bottom: 3px solid var(--arab-green); 
        display: flex; align-items: center; padding: 0 20px; gap: 
        15px; z-index: 100; justify-content: space-between; } 
        .nav-right { display: flex; align-items: center; gap: 20px; } 
        .btn-main { text-decoration: none; color: #fff; padding: 8px 
        18px; border-radius: 6px; border: 1px solid #333; font-size: 
        14px; background: #1a1a1a; transition: 0.3s; } 
        .btn-main:hover { border-color: var(--arab-green); color: 
        var(--arab-green); } .btn-active { border-color: 
        var(--arab-green); background: var(--arab-green); color: 
        #fff; }
        .nano-container { display: flex; flex: 1; overflow: hidden; 
        width: 100%; } .side-panel { width: 380px; background: 
        var(--panel-bg); border-left: 1px solid #222; display: flex; 
        flex-direction: column; } .side-lessons { height: 50%; 
        overflow-y: auto; border-bottom: 2px solid #222; padding: 
        10px 0; } .lesson-item { padding: 14px 20px; border-bottom: 
        1px solid #1a1a1a; color: #bbb; text-decoration: none; 
        font-size: 14px; display: block; transition: 0.2s; 
        border-right: 4px solid transparent; } .lesson-item:hover, 
        .active-lesson { background: #1f1f1f; color: 
        var(--arab-green); border-right: 4px solid var(--arab-green); 
        }
        .side-images { flex: 1; overflow-y: auto; padding: 15px; 
        background: #000; } .img-wrapper { position: relative; 
        margin-bottom: 25px; border: 2px solid #222; border-radius: 
        10px; cursor: pointer; transition: 0.3s; } .img-wrapper:hover 
        { border-color: var(--gold); transform: scale(0.98); } 
        .img-wrapper img { width: 100%; display: block; 
        border-radius: 8px; } .img-label { position: absolute; top: 
        -10px; right: 10px; background: var(--gold); color: #000; 
        padding: 2px 12px; border-radius: 20px; font-weight: bold; 
        font-size: 11px; z-index: 5; } .main-content { flex: 1; 
        background: #0d0d0d; padding: 40px; overflow-y: auto; 
        scroll-behavior: smooth; } .page-card { background: #181818; 
        padding: 35px; border-radius: 15px; border-right: 8px solid 
        var(--arab-green); margin-bottom: 50px; line-height: 1.9; 
        font-size: 19px; position: relative; } .page-card h3 { color: 
        var(--arab-green); border-bottom: 1px solid #333; 
        padding-bottom: 15px; }
    </style> </head> <body> <div class="top-nav"> <div 
        class="nav-right">
            <div style="font-weight: bold; color: var(--arab-green); 
            font-size: 20px;">📖 معمل العربية الرقمي</div> <a 
            href="?book=كتاب_النحو_والصرف" class="btn-main <?= ($book 
            == 'كتاب_النحو_والصرف') ? 'btn-active' : '' ?>">📘 النحو 
            والصرف</a> <a href="?book=كتاب_الأدب_والنقد_والبلاغة" 
            class="btn-main <?= ($book == 
            'كتاب_الأدب_والنقد_والبلاغة') ? 'btn-active' : '' ?>">📙 
            الأدب والبلاغة</a>
        </div> <div><a href="../master_encyclopedia.php" 
        class="btn-main" style="border-color: var(--gold);">🏠 
        الموسوعة</a></div>
    </div> <div class="nano-container"> <div class="side-panel"> <div 
            class="side-lessons">
                <?php if (is_dir($current_book_path)) { $dirs = 
                    array_filter(glob($current_book_path . '*'), 
                    'is_dir'); natsort($dirs); foreach ($dirs as 
                    $dir) {
                        $name = basename($dir); $displayName = 
                        str_replace('_', ' ', $name); $activeClass = 
                        ($lesson == $name) ? 'active-lesson' : ''; 
                        echo "<a 
                        href='?book=".urlencode($book)."&lesson=".urlencode($name)."' 
                        class='lesson-item $activeClass'>🔹 
                        $displayName</a>";
                    }
                }
                ?> </div> <div class="side-images"> <?php if 
                ($lesson):
                    $files = glob($current_book_path . $lesson . 
                    "/*.html"); natsort($files); foreach ($files as 
                    $file):
                        preg_match('/\d+/', basename($file), 
                        $matches); $p_num = $matches[0]; $img_file = 
                        $images_path . $p_num . ".png"; ?> <div 
                        class='img-wrapper' 
                        onclick='speakLesson("page-<?=$p_num?>", 0.7, 
                        1200)'>
                            <span class='img-label'>ص <?=$p_num?> 
                            🔊</span> <img src='<?=$img_file?>' 
                            onerror="this.src='https://via.placeholder.com/350x500/111/d4af37?text=Page+<?=$p_num?>';">
                        </div> <?php endforeach; endif; ?> </div> 
        </div> <div class="main-content">
            <?php if ($lesson && !empty($files)): foreach ($files as 
                $file):
                    preg_match('/\d+/', basename($file), $matches); 
                    $p_num = $matches[0]; $content = 
                    file_get_contents($file); echo "<div 
                    class='page-card' id='page-$p_num'>
                            <span style='color:#d4af37; 
                            font-size:12px;'>🔊 جاري القراءة بصوت 
                            بشري...</span> <h3>✨ شرح صفحة 
                            $p_num</h3> <div 
                            class='lesson-text'>$content</div>
                          </div>"; endforeach; else: echo "<div 
                style='text-align:center; margin-top:150px; 
                color:#555;'><h2>اختر درساً لبدء الشرح الصوتي 
                🎧</h2></div>";
            endif; ?> </div> </div> <script 
    src="../voice_engine.js"></script>
</body>
</html>
