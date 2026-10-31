import sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. style.css の修正
with open('prototype/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = css.replace('.container {\n    max-width: 1100px;', '.container {\n    max-width: 1200px;')
css = css.replace('.main-nav {\n    display: flex;\n    align-items: center;\n    gap: 24px;\n}', 
                  '.main-nav {\n    display: flex;\n    align-items: center;\n    gap: 16px;\n}')
css = css.replace('.header-inner {\n    display: flex;\n    justify-content: space-between;\n    align-items: center;\n    height: 70px;\n}',
                  '.header-inner {\n    display: flex;\n    justify-content: space-between;\n    align-items: center;\n    height: 70px;\n    flex-wrap: nowrap;\n}')

with open('prototype/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# 2. shop.html のナビ修正
with open('prototype/shop.html', 'r', encoding='utf-8') as f:
    shop = f.read()

shop = shop.replace('<a href="#prints" class="nav-link">限定版画・ポストカード</a>', '<a href="#prints" class="nav-link">限定版画・複製画</a>')
shop = shop.replace('<a href="#experience" class="nav-link">和の鉛筆画体験（インバウンド）</a>', '<a href="#experience" class="nav-link">和の鉛筆画体験</a>')
shop = shop.replace('Original Art Products & Experience Booking', 'Art Products & Cultural Experience')

with open('prototype/shop.html', 'w', encoding='utf-8') as f:
    f.write(shop)

print('Adjusted header styles and nav text successfully')
