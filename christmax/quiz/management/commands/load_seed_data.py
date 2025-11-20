"""Management command to load seed data for quiz app."""

from django.core.management.base import BaseCommand
from django.db import transaction

from quiz.models import Category, Question, Trophy


class Command(BaseCommand):
    """Load initial seed data for categories, questions, and trophies."""

    help = 'Load seed data for quiz categories, questions, and achievements'

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            '--clear', action='store_true', help='Clear existing data before loading'
        )

    def handle(self, *args, **options):
        """Execute the command."""
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Question.objects.all().delete()
            Category.objects.all().delete()
            Trophy.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Data cleared'))

        with transaction.atomic():
            self.load_categories()
            self.load_questions()
            self.load_trophies()

        self.stdout.write(self.style.SUCCESS('Seed data loaded successfully!'))

    def load_categories(self):
        """Load quiz categories with icons and prism language."""
        self.stdout.write('Loading categories...')

        categories = [
            {
                'name': 'HTML',
                'description': {
                    'en': 'HTML markup and semantic web',
                    'zh': 'HTML 標記語言與語意網路',
                },
                'icon_class': 'fa-brands fa-html5',
                'order': 1,
            },
            {
                'name': 'PYTHON',
                'description': {'en': 'Python programming language', 'zh': 'Python 程式語言'},
                'icon_class': 'fa-brands fa-python',
                'order': 2,
            },
            {
                'name': 'DJANGO',
                'description': {'en': 'Django web framework', 'zh': 'Django 網頁框架'},
                'icon_class': 'fa-solid fa-d',
                'order': 3,
            },
            {
                'name': 'JS',
                'description': {'en': 'JavaScript programming', 'zh': 'JavaScript 程式設計'},
                'icon_class': 'fa-brands fa-js',
                'order': 4,
            },
            {
                'name': 'CSS',
                'description': {'en': 'Cascading Style Sheets', 'zh': '層疊樣式表'},
                'icon_class': 'fa-brands fa-css3-alt',
                'order': 5,
            },
            {
                'name': 'RANDOM',
                'description': {'en': 'Mixed programming topics', 'zh': '混合程式主題'},
                'icon_class': 'fa-solid fa-shuffle',
                'order': 6,
            },
        ]

        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'icon_class': cat_data['icon_class'],
                    'order': cat_data['order'],
                },
            )
            if created:
                self.stdout.write(f'  Created category: {category}')

    def load_questions(self):
        """Load sample questions for each category and difficulty."""
        self.stdout.write('Loading questions...')

        questions = [
            # HTML - BEGINNER
            {
                'category': 'HTML',
                'difficulty': 'BEGINNER',
                'question_text': {
                    'en': 'What HTML tag is used for paragraphs?',
                    'zh': '哪個 HTML 標籤用於段落？',
                },
                'code_snippet': '<p>This is a paragraph</p>',
                'prism_language': 'html',
                'answer': 'p',
                'hint_text': {'en': 'Short for "paragraph"', 'zh': '「段落」的縮寫'},
                'explanation': {
                    'en': 'The <p> tag defines a paragraph in HTML',
                    'zh': '<p> 標籤在 HTML 中定義段落',
                },
            },
            {
                'category': 'HTML',
                'difficulty': 'BEGINNER',
                'question_text': {
                    'en': 'What tag creates a hyperlink?',
                    'zh': '哪個標籤創建超連結？',
                },
                'code_snippet': '<a href="https://example.com">Link</a>',
                'prism_language': 'html',
                'answer': 'a',
                'hint_text': {'en': 'Short for "anchor"', 'zh': '「錨點」的縮寫'},
                'explanation': {
                    'en': 'The <a> tag creates hyperlinks in HTML',
                    'zh': '<a> 標籤在 HTML 中創建超連結',
                },
            },
            # HTML - INTERMEDIATE
            {
                'category': 'HTML',
                'difficulty': 'INTERMEDIATE',
                'question_text': {
                    'en': 'What attribute specifies input type for forms?',
                    'zh': '哪個屬性指定表單輸入類型？',
                },
                'code_snippet': '<input type="text" />',
                'prism_language': 'html',
                'answer': 'type',
                'hint_text': {'en': 'Defines the kind of input field', 'zh': '定義輸入欄位的種類'},
                'explanation': {
                    'en': 'The type attribute specifies input field types like text, email, password',
                    'zh': 'type 屬性指定輸入欄位類型，如 text、email、password',
                },
            },
            # HTML - ADVANCED
            {
                'category': 'HTML',
                'difficulty': 'ADVANCED',
                'question_text': {
                    'en': 'What attribute makes content editable in browsers?',
                    'zh': '哪個屬性使內容在瀏覽器中可編輯？',
                },
                'code_snippet': '<div contenteditable="true">Edit me</div>',
                'prism_language': 'html',
                'answer': 'contenteditable',
                'hint_text': {
                    'en': 'Allows direct editing of element content',
                    'zh': '允許直接編輯元素內容',
                },
                'explanation': {
                    'en': 'contenteditable makes any HTML element editable by the user',
                    'zh': 'contenteditable 使任何 HTML 元素可由使用者編輯',
                },
            },
            # PYTHON - BEGINNER
            {
                'category': 'PYTHON',
                'difficulty': 'BEGINNER',
                'question_text': {
                    'en': 'What keyword defines a function?',
                    'zh': '哪個關鍵字定義函數？',
                },
                'code_snippet': 'def greet():\n    print("Hello")',
                'prism_language': 'python',
                'answer': 'def',
                'hint_text': {'en': 'Short for "define"', 'zh': '「定義」的縮寫'},
                'explanation': {
                    'en': 'The def keyword is used to define functions in Python',
                    'zh': 'def 關鍵字用於在 Python 中定義函數',
                },
            },
            {
                'category': 'PYTHON',
                'difficulty': 'BEGINNER',
                'question_text': {
                    'en': 'What function prints output to console?',
                    'zh': '哪個函數將輸出列印到控制台？',
                },
                'code_snippet': 'print("Hello World")',
                'prism_language': 'python',
                'answer': 'print',
                'hint_text': {'en': 'Used to display text', 'zh': '用於顯示文本'},
                'explanation': {
                    'en': 'print() outputs data to the console',
                    'zh': 'print() 將數據輸出到控制台',
                },
            },
            # PYTHON - INTERMEDIATE
            {
                'category': 'PYTHON',
                'difficulty': 'INTERMEDIATE',
                'question_text': {
                    'en': 'What method adds an item to a list?',
                    'zh': '哪個方法將項目添加到列表？',
                },
                'code_snippet': 'my_list = [1, 2, 3]\nmy_list.append(4)',
                'prism_language': 'python',
                'answer': 'append',
                'hint_text': {'en': 'Adds to the end of the list', 'zh': '添加到列表末尾'},
                'explanation': {
                    'en': 'append() adds an element to the end of a list',
                    'zh': 'append() 將元素添加到列表末尾',
                },
            },
            # PYTHON - ADVANCED
            {
                'category': 'PYTHON',
                'difficulty': 'ADVANCED',
                'question_text': {
                    'en': 'What keyword creates a generator function?',
                    'zh': '哪個關鍵字創建生成器函數？',
                },
                'code_snippet': 'def counter():\n    n = 0\n    while True:\n        yield n\n        n += 1',
                'prism_language': 'python',
                'answer': 'yield',
                'hint_text': {'en': 'Produces values one at a time', 'zh': '一次產生一個值'},
                'explanation': {
                    'en': 'yield makes a function return a generator that produces values lazily',
                    'zh': 'yield 使函數返回惰性產生值的生成器',
                },
            },
            # DJANGO - BEGINNER
            {
                'category': 'DJANGO',
                'difficulty': 'BEGINNER',
                'question_text': {
                    'en': 'What class do Django models inherit from?',
                    'zh': 'Django 模型繼承自哪個類？',
                },
                'code_snippet': 'class Post(models.Model):\n    title = models.CharField(max_length=200)',
                'prism_language': 'python',
                'answer': 'Model',
                'hint_text': {'en': 'Base class in models module', 'zh': 'models 模組中的基類'},
                'explanation': {
                    'en': 'All Django models inherit from models.Model',
                    'zh': '所有 Django 模型都繼承自 models.Model',
                },
            },
            {
                'category': 'DJANGO',
                'difficulty': 'BEGINNER',
                'question_text': {
                    'en': 'What command starts the development server?',
                    'zh': '哪個命令啟動開發伺服器？',
                },
                'code_snippet': 'python manage.py runserver',
                'prism_language': 'python',
                'answer': 'runserver',
                'hint_text': {'en': 'Runs the local server', 'zh': '運行本地伺服器'},
                'explanation': {
                    'en': "runserver starts Django's development web server",
                    'zh': 'runserver 啟動 Django 的開發網頁伺服器',
                },
            },
            # DJANGO - INTERMEDIATE
            {
                'category': 'DJANGO',
                'difficulty': 'INTERMEDIATE',
                'question_text': {
                    'en': 'What method retrieves all objects from database?',
                    'zh': '哪個方法從資料庫檢索所有物件？',
                },
                'code_snippet': 'posts = Post.objects.all()',
                'prism_language': 'python',
                'answer': 'all',
                'hint_text': {'en': 'Returns every record', 'zh': '返回每條記錄'},
                'explanation': {
                    'en': 'all() returns a QuerySet containing all objects',
                    'zh': 'all() 返回包含所有物件的 QuerySet',
                },
            },
            # DJANGO - ADVANCED
            {
                'category': 'DJANGO',
                'difficulty': 'ADVANCED',
                'question_text': {
                    'en': 'What method prefetches related objects to reduce queries?',
                    'zh': '哪個方法預先獲取相關物件以減少查詢？',
                },
                'code_snippet': 'posts = Post.objects.prefetch_related("comments")',
                'prism_language': 'python',
                'answer': 'prefetch_related',
                'hint_text': {
                    'en': 'Optimizes related object fetching',
                    'zh': '優化相關物件的獲取',
                },
                'explanation': {
                    'en': 'prefetch_related() reduces database queries for related objects',
                    'zh': 'prefetch_related() 減少相關物件的資料庫查詢',
                },
            },
            # JAVASCRIPT - BEGINNER
            {
                'category': 'JS',
                'difficulty': 'BEGINNER',
                'question_text': {
                    'en': 'What keyword declares a constant variable?',
                    'zh': '哪個關鍵字聲明常量變數？',
                },
                'code_snippet': 'const PI = 3.14159;',
                'prism_language': 'javascript',
                'answer': 'const',
                'hint_text': {'en': 'Cannot be reassigned', 'zh': '不能重新賦值'},
                'explanation': {
                    'en': 'const declares a constant that cannot be reassigned',
                    'zh': 'const 聲明一個不能重新賦值的常量',
                },
            },
            {
                'category': 'JS',
                'difficulty': 'BEGINNER',
                'question_text': {
                    'en': 'What function displays an alert dialog?',
                    'zh': '哪個函數顯示警告對話框？',
                },
                'code_snippet': 'alert("Hello!");',
                'prism_language': 'javascript',
                'answer': 'alert',
                'hint_text': {'en': 'Shows a popup message', 'zh': '顯示彈出訊息'},
                'explanation': {
                    'en': 'alert() displays a dialog with a message',
                    'zh': 'alert() 顯示帶有訊息的對話框',
                },
            },
            # JAVASCRIPT - INTERMEDIATE
            {
                'category': 'JS',
                'difficulty': 'INTERMEDIATE',
                'question_text': {
                    'en': 'What method adds an element to the end of an array?',
                    'zh': '哪個方法將元素添加到陣列末尾？',
                },
                'code_snippet': 'arr.push(5);',
                'prism_language': 'javascript',
                'answer': 'push',
                'hint_text': {'en': 'Pushes to the end', 'zh': '推送到末尾'},
                'explanation': {
                    'en': 'push() adds elements to the end of an array',
                    'zh': 'push() 將元素添加到陣列末尾',
                },
            },
            # JAVASCRIPT - ADVANCED
            {
                'category': 'JS',
                'difficulty': 'ADVANCED',
                'question_text': {
                    'en': 'What keyword waits for a promise to resolve?',
                    'zh': '哪個關鍵字等待 promise 解析？',
                },
                'code_snippet': 'const data = await fetch(url);',
                'prism_language': 'javascript',
                'answer': 'await',
                'hint_text': {'en': 'Pauses execution until resolved', 'zh': '暫停執行直到解析'},
                'explanation': {
                    'en': 'await pauses async function execution until promise resolves',
                    'zh': 'await 暫停非同步函數執行直到 promise 解析',
                },
            },
            # CSS - BEGINNER
            {
                'category': 'CSS',
                'difficulty': 'BEGINNER',
                'question_text': {
                    'en': 'What property sets text color?',
                    'zh': '哪個屬性設定文字顏色？',
                },
                'code_snippet': '.text { color: blue; }',
                'prism_language': 'css',
                'answer': 'color',
                'hint_text': {'en': 'Controls text color', 'zh': '控制文字顏色'},
                'explanation': {
                    'en': 'The color property sets the color of text',
                    'zh': 'color 屬性設定文字的顏色',
                },
            },
            {
                'category': 'CSS',
                'difficulty': 'BEGINNER',
                'question_text': {
                    'en': 'What property controls font size?',
                    'zh': '哪個屬性控制字體大小？',
                },
                'code_snippet': 'p { font-size: 16px; }',
                'prism_language': 'css',
                'answer': 'font-size',
                'hint_text': {'en': 'Sets the size of text', 'zh': '設定文字大小'},
                'explanation': {
                    'en': 'font-size controls the size of text',
                    'zh': 'font-size 控制文字大小',
                },
            },
            # CSS - INTERMEDIATE
            {
                'category': 'CSS',
                'difficulty': 'INTERMEDIATE',
                'question_text': {
                    'en': 'What display value creates a flex container?',
                    'zh': '哪個 display 值創建 flex 容器？',
                },
                'code_snippet': '.container { display: flex; }',
                'prism_language': 'css',
                'answer': 'flex',
                'hint_text': {'en': 'Enables flexbox layout', 'zh': '啟用 flexbox 布局'},
                'explanation': {
                    'en': 'display: flex creates a flex container for flexible layouts',
                    'zh': 'display: flex 創建用於靈活布局的 flex 容器',
                },
            },
            # CSS - ADVANCED
            {
                'category': 'CSS',
                'difficulty': 'ADVANCED',
                'question_text': {
                    'en': 'What property creates a grid layout?',
                    'zh': '哪個屬性創建網格布局？',
                },
                'code_snippet': '.grid { display: grid; }',
                'prism_language': 'css',
                'answer': 'grid',
                'hint_text': {'en': 'Two-dimensional layout system', 'zh': '二維布局系統'},
                'explanation': {
                    'en': 'display: grid creates a two-dimensional grid layout',
                    'zh': 'display: grid 創建二維網格布局',
                },
            },
            # RANDOM - Mixed difficulties
            {
                'category': 'RANDOM',
                'difficulty': 'BEGINNER',
                'question_text': {
                    'en': 'What HTTP method retrieves data from server?',
                    'zh': '哪個 HTTP 方法從伺服器檢索資料？',
                },
                'code_snippet': 'fetch("/api/data", { method: "GET" })',
                'prism_language': 'javascript',
                'answer': 'GET',
                'hint_text': {'en': 'Used to get data', 'zh': '用於獲取資料'},
                'explanation': {
                    'en': 'GET is the HTTP method for retrieving data',
                    'zh': 'GET 是用於檢索資料的 HTTP 方法',
                },
            },
            {
                'category': 'RANDOM',
                'difficulty': 'INTERMEDIATE',
                'question_text': {
                    'en': 'What format is commonly used for APIs?',
                    'zh': '哪種格式常用於 API？',
                },
                'code_snippet': '{"name": "John", "age": 30}',
                'prism_language': 'json',
                'answer': 'JSON',
                'hint_text': {'en': 'JavaScript Object Notation', 'zh': 'JavaScript 物件表示法'},
                'explanation': {
                    'en': 'JSON (JavaScript Object Notation) is the standard API data format',
                    'zh': 'JSON（JavaScript 物件表示法）是標準的 API 資料格式',
                },
            },
            {
                'category': 'RANDOM',
                'difficulty': 'ADVANCED',
                'question_text': {
                    'en': 'What protocol secures HTTP communications?',
                    'zh': '哪個協定保護 HTTP 通訊？',
                },
                'code_snippet': 'https://secure-site.com',
                'prism_language': 'markup',
                'answer': 'HTTPS',
                'hint_text': {'en': 'Encrypted HTTP', 'zh': '加密的 HTTP'},
                'explanation': {
                    'en': 'HTTPS (HTTP Secure) encrypts data between client and server',
                    'zh': 'HTTPS（HTTP 安全）加密客戶端和伺服器之間的資料',
                },
            },
        ]

        for q_data in questions:
            category = Category.objects.get(name=q_data['category'])
            question, created = Question.objects.get_or_create(
                category=category,
                difficulty=q_data['difficulty'],
                answer=q_data['answer'],
                question_text=q_data['question_text'],
                defaults={
                    'code_snippet': q_data.get('code_snippet', ''),
                    'prism_language': q_data.get('prism_language', ''),
                    'hint_text': q_data.get('hint_text', {}),
                    'explanation': q_data.get('explanation', {}),
                },
            )
            if created:
                self.stdout.write(f'  Created: {question}')

    def load_trophies(self):
        """Load achievement trophies."""
        self.stdout.write('Loading trophies...')

        trophies = [
            # Level-based achievements
            {
                'code': 'LEVEL_5',
                'requirement_type': 'LEVEL',
                'name': {'en': 'Beginner Graduate', 'zh': '新手畢業生'},
                'description': {'en': 'Reach player level 5', 'zh': '達到玩家等級 5'},
            },
            {
                'code': 'LEVEL_10',
                'requirement_type': 'LEVEL',
                'name': {'en': 'Rising Star', 'zh': '新星崛起'},
                'description': {'en': 'Reach player level 10', 'zh': '達到玩家等級 10'},
            },
            {
                'code': 'LEVEL_25',
                'requirement_type': 'LEVEL',
                'name': {'en': 'Expert Coder', 'zh': '專家程式員'},
                'description': {'en': 'Reach player level 25', 'zh': '達到玩家等級 25'},
            },
            {
                'code': 'LEVEL_50',
                'requirement_type': 'LEVEL',
                'name': {'en': 'Master Developer', 'zh': '大師開發者'},
                'description': {'en': 'Reach player level 50', 'zh': '達到玩家等級 50'},
            },
            {
                'code': 'LEVEL_100',
                'requirement_type': 'LEVEL',
                'name': {'en': 'Coding Legend', 'zh': '編碼傳奇'},
                'description': {'en': 'Reach player level 100', 'zh': '達到玩家等級 100'},
            },
            # Category mastery
            {
                'code': 'HTML_MASTER',
                'requirement_type': 'CATEGORY_MASTER',
                'name': {'en': 'HTML Master', 'zh': 'HTML 大師'},
                'description': {
                    'en': 'Complete 50 HTML questions correctly',
                    'zh': '正確完成 50 道 HTML 題目',
                },
            },
            {
                'code': 'PYTHON_MASTER',
                'requirement_type': 'CATEGORY_MASTER',
                'name': {'en': 'Python Master', 'zh': 'Python 大師'},
                'description': {
                    'en': 'Complete 50 Python questions correctly',
                    'zh': '正確完成 50 道 Python 題目',
                },
            },
            {
                'code': 'DJANGO_MASTER',
                'requirement_type': 'CATEGORY_MASTER',
                'name': {'en': 'Django Master', 'zh': 'Django 大師'},
                'description': {
                    'en': 'Complete 50 Django questions correctly',
                    'zh': '正確完成 50 道 Django 題目',
                },
            },
            {
                'code': 'JS_MASTER',
                'requirement_type': 'CATEGORY_MASTER',
                'name': {'en': 'JavaScript Master', 'zh': 'JavaScript 大師'},
                'description': {
                    'en': 'Complete 50 JavaScript questions correctly',
                    'zh': '正確完成 50 道 JavaScript 題目',
                },
            },
            {
                'code': 'CSS_MASTER',
                'requirement_type': 'CATEGORY_MASTER',
                'name': {'en': 'CSS Master', 'zh': 'CSS 大師'},
                'description': {
                    'en': 'Complete 50 CSS questions correctly',
                    'zh': '正確完成 50 道 CSS 題目',
                },
            },
            # Special achievements
            {
                'code': 'FIRST_WIN',
                'requirement_type': 'LEVEL',
                'name': {'en': 'First Victory', 'zh': '首次勝利'},
                'description': {'en': 'Win your first game', 'zh': '贏得你的第一場遊戲'},
            },
            {
                'code': 'PERFECT_GAME',
                'requirement_type': 'LEVEL',
                'name': {'en': 'Perfect Game', 'zh': '完美遊戲'},
                'description': {
                    'en': 'Answer correctly on the first attempt',
                    'zh': '第一次嘗試就答對',
                },
            },
            {
                'code': 'SPEED_DEMON',
                'requirement_type': 'LEVEL',
                'name': {'en': 'Speed Demon', 'zh': '速度惡魔'},
                'description': {
                    'en': 'Complete a game in under 30 seconds',
                    'zh': '在 30 秒內完成遊戲',
                },
            },
            {
                'code': 'POLYGLOT',
                'requirement_type': 'CATEGORY_MASTER',
                'name': {'en': 'Polyglot Programmer', 'zh': '多語言程式員'},
                'description': {
                    'en': 'Master all programming categories',
                    'zh': '精通所有程式語言分類',
                },
            },
            {
                'code': 'NIGHT_OWL',
                'requirement_type': 'LEVEL',
                'name': {'en': 'Night Owl', 'zh': '夜貓子'},
                'description': {
                    'en': 'Play 10 games between midnight and 6 AM',
                    'zh': '在午夜至早上 6 點之間遊玩 10 場遊戲',
                },
            },
        ]

        for trophy_data in trophies:
            trophy, created = Trophy.objects.get_or_create(
                code=trophy_data['code'],
                defaults={
                    'requirement_type': trophy_data['requirement_type'],
                    'name': trophy_data['name'],
                    'description': trophy_data['description'],
                },
            )
            if created:
                self.stdout.write(f'  Created trophy: {trophy}')
