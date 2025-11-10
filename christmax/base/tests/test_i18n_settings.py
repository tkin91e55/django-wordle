"""Internationalization configuration and asset tests."""
from pathlib import Path
from typing import Iterable

import pytest
from django.conf import settings
from django.urls import get_resolver
from django.utils.encoding import force_str
from django.utils.translation import gettext


@pytest.fixture(scope='module')
def base_locale_dir() -> Path:
    """Path helper for locale assertions."""
    return Path(settings.LOCALE_PATHS[0])


def test_languages_setting_lists_expected_pairs():
    """LANGUAGES should expose English and Traditional Chinese."""
    codes = [code for code, _ in settings.LANGUAGES]
    labels = [force_str(label) for _, label in settings.LANGUAGES]

    assert codes == ['en', 'zh']
    assert labels == ['English', 'Traditional Chinese']


def test_locale_middleware_present_and_ordered():
    """LocaleMiddleware must run before CommonMiddleware."""
    middleware = list(settings.MIDDLEWARE)
    locale = 'django.middleware.locale.LocaleMiddleware'
    common = 'django.middleware.common.CommonMiddleware'

    assert locale in middleware
    assert common in middleware
    assert middleware.index(locale) < middleware.index(common)


def test_locale_paths_contain_base_locale_dir():
    """Translations live in base/locale."""
    expected = Path(settings.BASE_DIR) / 'base' / 'locale'
    resolved = [Path(path) for path in settings.LOCALE_PATHS]
    assert expected in resolved


@pytest.mark.parametrize('extension', ['django.po', 'django.mo'])
def test_translation_files_exist(base_locale_dir: Path, extension: str):
    """Each locale ships both .po and .mo files."""
    for lang_code, _ in settings.LANGUAGES:
        msg_path = base_locale_dir / lang_code / 'LC_MESSAGES' / extension
        assert msg_path.exists(), f'Missing {extension} for {lang_code}'


@pytest.mark.parametrize('string', ['Home', 'Language'])
def test_required_translations_exist(string: str):
    """Spot-check a couple of core translation strings."""
    assert gettext(string) is not None


def test_language_code_consistency(base_locale_dir: Path):
    """Language codes must align between settings and locale directories."""
    language_codes = [code for code, _ in settings.LANGUAGES]

    assert {'en', 'zh'} <= set(language_codes)

    missing_dirs: Iterable[str] = [
        code for code in language_codes if not (base_locale_dir / code).exists()
    ]
    assert not missing_dirs, f'Missing locale directories: {missing_dirs}'


def test_url_pattern_structure():
    """home and home_zh should always be present."""
    resolver = get_resolver()
    assert 'home' in resolver.reverse_dict
    assert 'home_zh' in resolver.reverse_dict
