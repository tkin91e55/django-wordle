# Django Modular Translation System

## Overview

This project uses a **modular translation architecture** where translations are split into separate
source files and merged at compile time. This provides better maintainability, clear separation of
concerns, and easier updates.

## Architecture

### Source Files (Tracked in Git)

Located in: `christmax/base/locale/<lang>/LC_MESSAGES/`

1. **`manual.po`** (Highest Priority)
   - Manual translation overrides and fixes
   - Example: Password validator strings with curly apostrophes
   - Edited by: Developers
   - ~5 translations

2. **`app.po`** (Custom Project)
   - Custom project-specific translations
   - Generated from: `{% trans %}` tags in templates, `gettext()` in Python code
   - Edited by: Translators
   - ~149 translations

3. **`allauth.po`** (Django-allauth)
   - Django-allauth framework translations
   - Source: Copied from `django-allauth` package (`zh_Hant` locale)
   - Updated when: Upgrading django-allauth
   - ~370 translations

4. **`django-core.po`** (Django Core, Lowest Priority)
   - Django framework core translations
   - Source: Copied from Django package (`zh_Hant` locale)
   - Updated when: Upgrading Django
   - ~349 translations

5. **`djangojs.po`** (JavaScript)
   - JavaScript translation strings (separate domain)
   - Generated from: `gettext()` calls in `.js` files
   - Edited by: Translators
   - ~2 translations

### Generated Files (NOT Tracked in Git)

- **`django.po`** - Merged result from source files (auto-generated)
- **`django.mo`** - Compiled binary for Django (auto-generated)
- **`djangojs.mo`** - Compiled JS translations (auto-generated)

## Usage

### Quick Commands

```bash
# Show all available commands
make help

# Compile all translations (merge source files and build .mo files)
make compile

# Show translation statistics
make stats

# Extract new translatable strings from code
make update

# Extract JavaScript translatable strings
make update-js

# Clean auto-generated files
make clean
```

### Development Workflow

#### 1. Adding New Translations

1. Add translatable strings to your code:
   ```python
   # In Python
   from django.utils.translation import gettext as _
   message = _("Hello, world!")
   ```

   ```django
   {# In Templates #}
   {% load i18n %}
   <h1>{% trans "Welcome" %}</h1>
   ```

2. Extract new strings:
   ```bash
   make update
   ```

3. Edit `base/locale/zh/LC_MESSAGES/app.po` to add Chinese translations

4. Compile:
   ```bash
   make compile
   ```

5. Restart Django dev server to see changes

#### 2. Updating External Dependencies

When you upgrade Django or django-allauth:

```bash
# Update allauth translations
make restore-allauth

# Update Django core translations
make restore-django-core

# Recompile
make compile
```

#### 3. Manual Overrides

To override any translation (e.g., fixing character encoding issues):

1. Edit `base/locale/zh/LC_MESSAGES/manual.po`
2. Add your override (it has highest priority)
3. Run `make compile`

Example:
```po
# manual.po
msgid "Your password can't be too similar..."
msgstr "您的密碼不能與您的其他個人資訊太相似。"
```

**Note:** Use curly apostrophes (U+2019 `'`) not straight apostrophes (U+0027 `'`) to match Django's source strings.

## Management Command

The modular system is powered by a custom Django management command:

```bash
# Compile all locales
poetry run python manage.py compile_translations

# Compile specific locale
poetry run python manage.py compile_translations --locale zh

# Show detailed file listing
poetry run python manage.py compile_translations --show-files
```

### How It Works

1. Reads source files in priority order (manual → app → allauth → django-core)
2. Merges using `msgcat --use-first` (first occurrence wins)
3. Compiles merged `django.po` to `django.mo` using `msgfmt`
4. Also compiles `djangojs.po` to `djangojs.mo` if present

## File Structure

```
christmax/
├── Makefile                                    # Translation management commands
├── base/
│   ├── locale/
│   │   ├── zh/                                # Chinese (Traditional)
│   │   │   └── LC_MESSAGES/
│   │   │       ├── manual.po               ✓  # [SOURCE] Manual overrides
│   │   │       ├── app.po                  ✓  # [SOURCE] Custom translations
│   │   │       ├── allauth.po              ✓  # [SOURCE] Allauth translations
│   │   │       ├── django-core.po          ✓  # [SOURCE] Django core
│   │   │       ├── djangojs.po             ✓  # [SOURCE] JavaScript
│   │   │       ├── django.po               ✗  # [AUTO] Merged (gitignored)
│   │   │       ├── django.mo               ✗  # [AUTO] Compiled (gitignored)
│   │   │       └── djangojs.mo             ✗  # [AUTO] Compiled (gitignored)
│   │   └── en/                                # English
│   │       └── LC_MESSAGES/
│   │           └── ... (same structure)
│   └── management/
│       └── commands/
│           └── compile_translations.py        # Custom command
└── .gitignore                                 # Ignores auto-generated files
```

## Benefits

### ✅ Maintainability
- **Clear separation:** Know exactly where each translation comes from
- **Easy updates:** Update dependencies independently
- **Version control:** Track changes to each component separately

### ✅ Collaboration
- **No merge conflicts:** Developers work on `app.po`, translators on their own files
- **Clear ownership:** `app.po` = project, others = dependencies

### ✅ Consistency
- **Priority system:** Manual overrides always win
- **Reproducible builds:** Same source files = same output
- **Clean diffs:** Git shows only actual translation changes

### ✅ Upgrade Safety
- **Django upgrade:** Just update `django-core.po`
- **Allauth upgrade:** Just update `allauth.po`
- **No re-translation needed:** Custom work preserved in `app.po` and `manual.po`

## Troubleshooting

### Translations not showing up?

1. **Did you compile?**
   ```bash
   make compile
   ```

2. **Did you restart the Django dev server?**
   Django caches translations at startup. After compiling, restart the server.

3. **Check the source files:**
   ```bash
   make stats
   ```

4. **Verify .mo files exist:**
   ```bash
   ls -la base/locale/zh/LC_MESSAGES/*.mo
   ```

### Character encoding issues?

- Use UTF-8 encoding for all `.po` files
- For curly apostrophes in Django strings, use U+2019 (`'`) not U+0027 (`'`)
- Edit `manual.po` to override problematic strings

### msgcat not found?

Install gettext utilities:
```bash
# macOS
brew install gettext

# Ubuntu/Debian
sudo apt-get install gettext

# Windows
# Download from: https://mlocati.github.io/articles/gettext-iconv-windows.html
```

## Testing

Verify translations work correctly:

```bash
cd christmax
poetry run python manage.py shell
```

```python
from django.utils.translation import activate
from django.contrib.auth.password_validation import password_validators_help_texts

activate('zh')
for text in password_validators_help_texts():
    print(text)
```

Expected output (all in Chinese):
```
您的密碼不能與您的其他個人資訊太相似。
您的密碼必須包含至少 8 個字元。
您的密碼不能是常用密碼。
您的密碼不能完全是數字。
```

## Reference

- **Django i18n docs:** https://docs.djangoproject.com/en/stable/topics/i18n/
- **GNU gettext manual:** https://www.gnu.org/software/gettext/manual/
- **msgcat documentation:** `man msgcat`
