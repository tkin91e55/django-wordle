# Django Translation Management Makefile
# 
# This Makefile provides convenient commands for managing modular translations.
# 
# Source files:
#   - manual.po      : Manual overrides and fixes (highest priority)
#   - app.po         : Custom project translations
#   - allauth.po     : Django-allauth translations
#   - django-core.po : Django core translations (lowest priority)
#
# Generated files:
#   - django.po      : Merged result from source files
#   - django.mo      : Compiled binary for production use
#   - djangojs.po    : JavaScript translations (managed separately)
#   - djangojs.mo    : Compiled JS translations

.PHONY: help
help:
	@echo "Django Translation Management"
	@echo ""
	@echo "Available commands:"
	@echo "  make compile          - Compile all translation files (merge + build .mo files)"
	@echo "  make compile-verbose  - Compile with detailed file listing"
	@echo "  make update           - Extract new translatable strings to app.po"
	@echo "  make update-js        - Extract JavaScript translatable strings to djangojs.po"
	@echo "  make clean            - Remove auto-generated translation files"
	@echo "  make stats            - Show translation statistics"
	@echo ""
	@echo "Workflow:"
	@echo "  1. Add {% trans %} or gettext() calls to your code"
	@echo "  2. Run 'make update' to extract new strings"
	@echo "  3. Edit base/locale/zh/LC_MESSAGES/app.po to add translations"
	@echo "  4. Run 'make compile' to merge and build"
	@echo "  5. Restart Django dev server to see changes"

.PHONY: compile
compile:
	@echo "Compiling translations..."
	@poetry run python manage.py compile_translations
	@echo ""
	@echo "✓ Translations compiled successfully!"
	@echo "  Remember to restart your Django dev server for changes to take effect."

.PHONY: compile-verbose
compile-verbose:
	@echo "Compiling translations (verbose mode)..."
	@poetry run python manage.py compile_translations --show-files

.PHONY: update
update:
	@echo "Extracting translatable strings from Python and templates..."
	@poetry run python manage.py makemessages -l zh --no-location
	@if [ -f base/locale/zh/LC_MESSAGES/django.po ]; then \
		echo "Moving extracted strings to app.po..."; \
		mv base/locale/zh/LC_MESSAGES/django.po base/locale/zh/LC_MESSAGES/app.po; \
		echo "✓ New strings extracted to base/locale/zh/LC_MESSAGES/app.po"; \
		echo ""; \
		echo "Next steps:"; \
		echo "  1. Edit app.po to add Chinese translations"; \
		echo "  2. Run 'make compile' to build"; \
	else \
		echo "✗ No django.po file generated"; \
	fi

.PHONY: update-js
update-js:
	@echo "Extracting JavaScript translatable strings..."
	@poetry run python manage.py makemessages -d djangojs -l zh --no-location
	@echo "✓ JavaScript strings extracted to base/locale/zh/LC_MESSAGES/djangojs.po"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Edit djangojs.po to add Chinese translations"
	@echo "  2. Run 'make compile' to build"

.PHONY: clean
clean:
	@echo "Cleaning auto-generated translation files..."
	@find base/locale -name "django.po" -type f -delete
	@find base/locale -name "django.mo" -type f -delete
	@find base/locale -name "djangojs.mo" -type f -delete
	@echo "✓ Cleaned auto-generated files"
	@echo "  Kept source files: app.po, allauth.po, django-core.po, manual.po, djangojs.po"

.PHONY: stats
stats:
	@echo "Translation Statistics"
	@echo "======================"
	@echo ""
	@for lang in zh en; do \
		if [ -d base/locale/$$lang/LC_MESSAGES ]; then \
			echo "Language: $$lang"; \
			echo "-------------------"; \
			for file in manual.po app.po allauth.po django-core.po djangojs.po; do \
				if [ -f base/locale/$$lang/LC_MESSAGES/$$file ]; then \
					count=$$(grep -c "^msgid " base/locale/$$lang/LC_MESSAGES/$$file 2>/dev/null || echo 0); \
					printf "  %-15s: %4d translations\n" "$$file" "$$count"; \
				fi; \
			done; \
			if [ -f base/locale/$$lang/LC_MESSAGES/django.po ]; then \
				count=$$(grep -c "^msgid " base/locale/$$lang/LC_MESSAGES/django.po 2>/dev/null || echo 0); \
				printf "  %-15s: %4d translations (merged)\n" "django.po" "$$count"; \
			fi; \
			echo ""; \
		fi; \
	done

.PHONY: check
check:
	@echo "Checking translation file integrity..."
	@for lang in zh en; do \
		for file in app.po allauth.po django-core.po manual.po; do \
			if [ -f base/locale/$$lang/LC_MESSAGES/$$file ]; then \
				msgfmt --check --verbose base/locale/$$lang/LC_MESSAGES/$$file -o /dev/null 2>&1 || echo "✗ Error in $$lang/$$file"; \
			fi; \
		done; \
	done
	@echo "✓ Check complete"

# Development helpers
.PHONY: backup
backup:
	@echo "Creating backup of translation files..."
	@timestamp=$$(date +%Y%m%d_%H%M%S); \
	for file in app.po manual.po; do \
		if [ -f base/locale/zh/LC_MESSAGES/$$file ]; then \
			cp base/locale/zh/LC_MESSAGES/$$file base/locale/zh/LC_MESSAGES/$$file.backup_$$timestamp; \
			echo "✓ Backed up $$file"; \
		fi; \
	done

.PHONY: restore-allauth
restore-allauth:
	@echo "Restoring allauth.po from package..."
	@poetry run python -c "import allauth, os; print(os.path.dirname(allauth.__file__))" | \
		xargs -I {} cat {}/locale/zh_Hant/LC_MESSAGES/django.po > base/locale/zh/LC_MESSAGES/allauth.po
	@echo "✓ Restored allauth.po from django-allauth package"

.PHONY: restore-django-core
restore-django-core:
	@echo "Restoring django-core.po from package..."
	@poetry run python -c "import django, os; print(os.path.dirname(django.__file__))" | \
		xargs -I {} cat {}/conf/locale/zh_Hant/LC_MESSAGES/django.po > base/locale/zh/LC_MESSAGES/django-core.po
	@echo "✓ Restored django-core.po from Django package"
