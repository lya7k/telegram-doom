import urllib.request
import os

print("🚀 Начинаем сборку полностью автономной версии DOOM...\n")

# Функция для скачивания файлов, притворяясь обычным браузером
def download(url, filename):
    print(f"📥 Скачиваю {filename}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response, open(filename, 'wb') as out_file:
            out_file.write(response.read())
    except Exception as e:
        print(f"❌ Ошибка скачивания {filename}: {e}")

# Ссылки на самые стабильные файлы движка
files = {
    "js-dos.js": "https://js-dos.com/v7/build/releases/latest/js-dos/js-dos.js",
    "js-dos.css": "https://js-dos.com/v7/build/releases/latest/js-dos/js-dos.css",
    "wdosbox.js": "https://js-dos.com/v7/build/releases/latest/js-dos/wdosbox.js",
    "wdosbox.wasm": "https://js-dos.com/v7/build/releases/latest/js-dos/wdosbox.wasm"
}

# 1. Скачиваем движок эмулятора
for name, url in files.items():
    download(url, name)

# 2. Скачиваем саму игру, если ее еще нет в папке
if not os.path.exists("doom.jsdos"):
    download("https://cdn.dos.zone/custom/dos/doom.jsdos", "doom.jsdos")
else:
    print("✅ Файл doom.jsdos уже есть в папке.")

# 3. Генерируем полностью независимый HTML-файл
print("🛠 Создаю независимый index.html...")

html_content = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Telegram DOOM</title>
    
    <!-- Единственный внешний скрипт - официальный от Telegram, он никогда не падает -->
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    
    <!-- Подключаем ЛОКАЛЬНЫЕ файлы эмулятора. Никаких чужих серверов! -->
    <link rel="stylesheet" href="js-dos.css">
    <script src="js-dos.js"></script>
    
    <style>
        html, body, #jsdos {
            width: 100%; height: 100%; margin: 0; padding: 0;
            background-color: #000; overflow: hidden;
        }
    </style>
</head>
<body>
    <div id="jsdos"></div>
    
    <script>
        Telegram.WebApp.expand();

        // Указываем эмулятору искать ядро в текущей папке, а не в интернете
        emulators.pathPrefix = "./";

        // Запускаем локальную игру
        Dos(document.getElementById("jsdos")).run("doom.jsdos");
    </script>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("\n🎉 ГОТОВО! Создан полностью независимый клиент.")
print("Теперь загрузи все появившиеся файлы на свой GitHub!")