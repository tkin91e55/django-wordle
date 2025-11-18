"""
Django management command to compile translations from modular .po files.

This command merges multiple translation source files into a single django.po file
and then compiles it to django.mo for use by Django's translation system.

Source files (in priority order - first has highest priority):
1. manual.po      - Manual overrides and fixes
2. app.po         - Custom project translations
3. allauth.po     - Django-allauth translations
4. django-core.po - Django core translations

Usage:
    python manage.py compile_translations
    python manage.py compile_translations --locale zh
    python manage.py compile_translations --verbose
"""

import subprocess
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """Compile translations by merging multiple .po files."""

    help = "Compile translations by merging modular .po files into django.po"

    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            "--locale",
            "-l",
            action="append",
            dest="locales",
            help="Locale(s) to process (e.g. zh, en). Default is to process all.",
        )
        parser.add_argument(
            "--show-files",
            action="store_true",
            help="Show detailed list of files being merged",
        )

    def handle(self, *args, **options):
        """Execute the command."""
        verbosity = options.get("verbosity", 1)
        show_files = options.get("show_files", False)
        locales = options.get("locales", None)

        # Get the base locale directory
        locale_dir = Path(settings.BASE_DIR) / "base" / "locale"

        if not locale_dir.exists():
            raise CommandError(f"Locale directory not found: {locale_dir}")

        # Get list of locales to process
        if locales:
            locale_codes = locales
        else:
            # Process all locale directories
            locale_codes = [
                d.name
                for d in locale_dir.iterdir()
                if d.is_dir() and not d.name.startswith(".")
            ]

        if not locale_codes:
            self.stdout.write(self.style.WARNING("No locales found to process"))
            return

        total_compiled = 0

        for lang_code in locale_codes:
            lang_dir = locale_dir / lang_code / "LC_MESSAGES"

            if not lang_dir.exists():
                if show_files or verbosity > 1:
                    self.stdout.write(
                        self.style.WARNING(f"Skipping {lang_code}: No LC_MESSAGES directory")
                    )
                continue

            # Define source files in priority order (first = highest priority)
            source_files = [
                lang_dir / "manual.po",  # Highest priority
                lang_dir / "app.po",  # Custom project strings
                lang_dir / "allauth.po",  # Allauth translations
                lang_dir / "django-core.po",  # Django core (lowest priority)
            ]

            # Filter to existing files
            existing_files = [f for f in source_files if f.exists()]

            if not existing_files:
                if show_files or verbosity > 1:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Skipping {lang_code}: No source .po files found"
                        )
                    )
                continue

            # Output file
            output_file = lang_dir / "django.po"

            # Merge using msgcat (--use-first gives priority to first file)
            try:
                if show_files or verbosity > 1:
                    self.stdout.write(
                        f"\nMerging {len(existing_files)} files for {lang_code}:"
                    )
                    for f in existing_files:
                        self.stdout.write(f"  - {f.name}")

                cmd = [
                    "msgcat",
                    "--use-first",  # First occurrence wins
                    "--sort-output",  # Alphabetical order
                    "-o",
                    str(output_file),
                ] + [str(f) for f in existing_files]

                result = subprocess.run(
                    cmd,
                    check=True,
                    capture_output=True,
                    text=True,
                )

                if show_files and result.stdout:
                    self.stdout.write(result.stdout)

            except subprocess.CalledProcessError as e:
                raise CommandError(
                    f"Failed to merge .po files for {lang_code}: {e.stderr}"
                )
            except FileNotFoundError:
                raise CommandError(
                    "msgcat command not found. Please install gettext utilities:\n"
                    "  macOS: brew install gettext\n"
                    "  Ubuntu/Debian: apt-get install gettext\n"
                    "  Windows: https://mlocati.github.io/articles/gettext-iconv-windows.html"
                )

            # Compile to .mo using msgfmt
            try:
                mo_file = lang_dir / "django.mo"
                compile_cmd = [
                    "msgfmt",
                    "-o",
                    str(mo_file),
                    str(output_file),
                ]

                result = subprocess.run(
                    compile_cmd,
                    check=True,
                    capture_output=True,
                    text=True,
                )

                if show_files and result.stdout:
                    self.stdout.write(result.stdout)

                total_compiled += 1
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Compiled {lang_code}/LC_MESSAGES/django.mo")
                )

            except subprocess.CalledProcessError as e:
                raise CommandError(
                    f"Failed to compile .mo file for {lang_code}: {e.stderr}"
                )

        # Also compile JavaScript translations if they exist
        self._compile_js_translations(locale_dir, locales, show_files, verbosity)

        # Summary
        if total_compiled > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    f"\n✓ Successfully compiled {total_compiled} locale(s)"
                )
            )
        else:
            self.stdout.write(self.style.WARNING("No translations were compiled"))

    def _compile_js_translations(self, locale_dir, locales, show_files, verbosity):
        """Compile JavaScript translation files (djangojs.po -> djangojs.mo)."""
        if locales:
            locale_codes = locales
        else:
            locale_codes = [
                d.name
                for d in locale_dir.iterdir()
                if d.is_dir() and not d.name.startswith(".")
            ]

        for lang_code in locale_codes:
            lang_dir = locale_dir / lang_code / "LC_MESSAGES"
            js_po_file = lang_dir / "djangojs.po"
            js_mo_file = lang_dir / "djangojs.mo"

            if not js_po_file.exists():
                continue

            try:
                compile_cmd = [
                    "msgfmt",
                    "-o",
                    str(js_mo_file),
                    str(js_po_file),
                ]

                result = subprocess.run(
                    compile_cmd,
                    check=True,
                    capture_output=True,
                    text=True,
                )

                if show_files and result.stdout:
                    self.stdout.write(result.stdout)

                self.stdout.write(
                    self.style.SUCCESS(f"✓ Compiled {lang_code}/LC_MESSAGES/djangojs.mo")
                )

            except subprocess.CalledProcessError as e:
                self.stdout.write(
                    self.style.WARNING(
                        f"Failed to compile JS translations for {lang_code}: {e.stderr}"
                    )
                )
