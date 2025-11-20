# Quiz Seed Data

This document describes the seed data system for the Django Wordle quiz application.

## Overview

The quiz app includes a management command to load initial data including:
- **6 Categories**: HTML, Python, Django, JavaScript, CSS, Random
- **Sample Questions**: 23+ bilingual questions across multiple difficulty levels
- **15 Achievement Trophies**: Level-based and category mastery achievements

## Loading Seed Data

### Basic Usage

Load seed data into the database:

```bash
python manage.py load_seed_data
```

### Clear and Reload

Clear existing data and load fresh seed data:

```bash
python manage.py load_seed_data --clear
```

⚠️ **Warning**: The `--clear` flag will delete all existing questions, categories, and trophies.

## Seed Data Structure

### Categories

| Category | Icon | Prism Language | Questions |
|----------|------|----------------|-----------|
| HTML | fa-html5 | html | 4 |
| Python | fa-python | python | 4 |
| Django | fa-d | python | 4 |
| JavaScript | fa-js | javascript | 4 |
| CSS | fa-css3-alt | css | 4 |
| Random | fa-shuffle | - | 3 |

### Question Difficulty Distribution

- **Beginner**: 11 questions
- **Intermediate**: 6 questions
- **Advanced**: 6 questions
- **Expert**: 0 questions (to be added)

### Sample Questions

Each question includes:
- **Bilingual content** (English + Traditional Chinese)
  - Question text
  - Hint text
  - Explanation
- **Code snippet** (syntax highlighted using Prism.js)
- **Answer** (5-6 characters for Wordle gameplay)

#### Example Question Structure

```python
{
    'category': 'PYTHON',
    'difficulty': 'BEGINNER',
    'question_text': {
        'en': 'What keyword defines a function?',
        'zh': '哪個關鍵字定義函數？',
    },
    'code_snippet': 'def greet():\n    print("Hello")',
    'answer': 'def',
    'hint_text': {
        'en': 'Short for "define"',
        'zh': '「定義」的縮寫',
    },
    'explanation': {
        'en': 'The def keyword is used to define functions in Python',
        'zh': 'def 關鍵字用於在 Python 中定義函數',
    },
}
```

### Achievements/Trophies

#### Level-Based Achievements
- **Level 5**: Beginner Graduate
- **Level 10**: Rising Star
- **Level 25**: Expert Coder
- **Level 50**: Master Developer
- **Level 100**: Coding Legend

#### Category Mastery
- **HTML Master**: Complete 50 HTML questions
- **Python Master**: Complete 50 Python questions
- **Django Master**: Complete 50 Django questions
- **JavaScript Master**: Complete 50 JavaScript questions
- **CSS Master**: Complete 50 CSS questions
- **Polyglot Programmer**: Master all programming categories

#### Special Achievements
- **First Victory**: Win your first game
- **Perfect Game**: Answer correctly on the first attempt
- **Speed Demon**: Complete a game in under 30 seconds
- **Night Owl**: Play 10 games between midnight and 6 AM

## Extending Seed Data

### Adding More Questions

Edit `/christmax/quiz/management/commands/load_seed_data.py` and add questions to the `questions` list in the `load_questions()` method:

```python
{
    'category': 'PYTHON',  # HTML, PYTHON, DJANGO, JS, CSS, RANDOM
    'difficulty': 'EXPERT',  # BEGINNER, INTERMEDIATE, ADVANCED, EXPERT
    'question_text': {
        'en': 'Your English question here',
        'zh': '你的中文問題在這裡',
    },
    'code_snippet': '# Optional code example',
    'answer': 'answer',  # 5-6 characters recommended
    'hint_text': {
        'en': 'English hint',
        'zh': '中文提示',
    },
    'explanation': {
        'en': 'English explanation',
        'zh': '中文解釋',
    },
}
```

### Adding Custom Trophies

Add to the `trophies` list in the `load_trophies()` method:

```python
{
    'code': 'UNIQUE_CODE',  # Unique identifier
    'requirement_type': 'LEVEL',  # LEVEL or CATEGORY_MASTER
    'name': 'Trophy Name',
    'description': 'How to unlock this trophy',
}
```

## Verifying Loaded Data

Check what data was loaded:

```bash
python manage.py shell -c "
from quiz.models import Category, Question, Trophy
print(f'Categories: {Category.objects.count()}')
print(f'Questions: {Question.objects.count()}')
print(f'Trophies: {Trophy.objects.count()}')
"
```

Test bilingual content:

```bash
python manage.py shell -c "
from quiz.models import Question
q = Question.objects.first()
print(f'EN: {q.get_question_text(\"en\")}')
print(f'ZH: {q.get_question_text(\"zh\")}')
"
```

## Data Requirements for Production

For a full production deployment, consider adding:

1. **More Questions**: Target ~10 questions per category/difficulty combo (240 total)
2. **Expert-Level Questions**: Add challenging questions for advanced users
3. **More Categories**: Consider adding SQL, Git, Docker, etc.
4. **Seasonal Content**: Holiday-themed questions or events
5. **Community Questions**: User-submitted questions system

## Notes

- All questions use **case-insensitive** answer matching
- Answers should be **5-6 characters** for optimal Wordle gameplay
- Code snippets use **Prism.js** for syntax highlighting
- Categories have **FontAwesome icons** for visual appeal
- Questions support **multiple languages** via JSONField

## Related Documentation

- [Quiz Models](./quiz-models.md) - Database schema and relationships
- [Translation System](./translation-system.md) - i18n implementation
- [Quiz Models ERD](./quiz-models-erd.svg) - Visual database diagram
