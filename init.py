import os
from PIL import Image

img_dir = "img/"
resize_dir = "resize2/"

png_files = [f for f in os.listdir(img_dir) if f.endswith(".png")]

mollys = dict()

RESIZE = False

for f in png_files:
    if RESIZE:
        img = Image.open(img_dir + f)
        img_resized = img.resize((1920, 1080), Image.LANCZOS).convert("RGB")
        img_resized.save(resize_dir + f, "JPEG",optimize=True, quality=90)
    
    map_name, agn, target, usefor, ind, num, cap = f.split(".")[0].split("_")
    num = int(num)
    if (map_name, agn, target, usefor, ind, cap) not in mollys:
        mollys[(map_name, agn, target, usefor, ind, cap)] = [num]
    else:
        mollys[(map_name, agn, target, usefor, ind, cap)].append(num)
        
items = []

template = r"""
<div class="imageItem" data-category="%s" agn="%s" target="%s" usefor="%s" 
        data-images='[%s]'>
    <img src="%s" alt="%s">
    <p class="caption"><b>%s</b></p>
</div>
"""

for keys in mollys:
    inds = sorted(mollys[keys])
    items.append(template % (keys[0], keys[1], keys[2], keys[3],
                             ", ".join([f'"{resize_dir}{keys[0]}_{keys[1]}_{keys[2]}_{keys[3]}_{keys[4]}_{i}_{keys[5]}.png"' for i in inds]),
                             f"{resize_dir}{keys[0]}_{keys[1]}_{keys[2]}_{keys[3]}_{keys[4]}_{inds[-1]}_{keys[5]}.png", 
                             f"{keys[0]}_{keys[1]}{keys[2]}_{keys[3]}_{keys[4]},",
                             keys[5]))


preHTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>발로란트 각독 각폭 모음</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h2>발로란트 각독 각폭 모음</h2>
        <h3> 맵 </h3>
        <div id="category-container">
            <button class="catbtn active" data-filter="all">전체</button>
            <button class="catbtn" data-filter="lotus">로터스</button>
            <button class="catbtn" data-filter="bind">바인드</button>
            <button class="catbtn" data-filter="sunset">선셋</button>
            <button class="catbtn" data-filter="icebox">아이스박스</button>
            <button class="catbtn" data-filter="ascent">어센트</button>
            <button class="catbtn" data-filter="abyss">어비스</button>
        </div>

        <h3> 요원 </h3>
        <div id="category-container">
            <button class="agnbtn active" agn-filter="all">전체</button>
            <button class="agnbtn" agn-filter="brimstone">브림스톤</button>
            <button class="agnbtn" agn-filter="deadlock">데드록</button>
        </div>

        <h3> 타겟 </h3>
        <div id="category-container">
            <button class="tarbtn active" tar-filter="all">전체</button>
            <button class="tarbtn" tar-filter="a">A</button>
            <button class="tarbtn" tar-filter="b">B</button>
            <button class="tarbtn" tar-filter="c">C</button>
            <button class="tarbtn" tar-filter="mid">미드</button>
        </div>
        <h3> 공수 </h3>
        <div id="category-container">
            <button class="useforbtn active" usefor-filter="all">전체</button>
            <button class="useforbtn" usefor-filter="off">공격</button>
            <button class="useforbtn" usefor-filter="def">수비</button>
        </div>
        <div id="gallery-container">
"""
            # <div class="imageItem" data-category="ascent"  target="mid" usefor="def">
            #     <img src="데드록어센트Bto중앙연결부.png" alt="데드록어센트Bto중앙연결부">
            # </div>
            
postHTML = r"""
        </div>
    </div>

    <div id="lightbox" class="lightbox">
        <div class="lightbox-content">
          <img id="lightboxImage" src="" alt="Lightbox Image">
          <div class="lightbox-nav">
            <button id="prevButton">&lt;</button>
            <button id="nextButton">&gt;</button>
          </div>
          <button id="closeButton">&times;</button>
        </div>
      </div>

    <script src="script.js"></script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf8') as f:
    f.write(preHTML + '\n'.join(items) + postHTML)
