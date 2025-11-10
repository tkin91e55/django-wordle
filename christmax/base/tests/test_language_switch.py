"""HTTP and template behaviour for language switching."""
import pytest


def _content(response) -> str:
    return response.content.decode('utf-8')


# Locale-prefixed routes -----------------------------------------------------

def test_home_uses_english_by_default(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.wsgi_request.LANGUAGE_CODE == 'en'


def test_home_zh_route_switches_language(client):
    response = client.get('/zh/')
    assert response.status_code == 200
    assert response.wsgi_request.LANGUAGE_CODE == 'zh'


# HTTP responses -------------------------------------------------------------

def test_english_page_content(client):
    response = client.get('/')
    html = _content(response)

    assert response.status_code == 200
    assert 'Home' in html
    assert 'Language' in html
    assert '首頁' not in html


def test_chinese_page_content(client):
    response = client.get('/zh/')
    html = _content(response)

    assert response.status_code == 200
    assert '首頁' in html
    assert '語言' in html
    assert 'Home' not in html


@pytest.mark.parametrize('url', ['/', '/zh/'])
def test_language_switcher_presence(client, url: str):
    response = client.get(url)
    html = _content(response)
    assert 'language-select' in html
    assert 'switchLanguage' in html


# JavaScript helper ----------------------------------------------------------

def test_switch_language_function_exists(client):
    html = _content(client.get('/'))
    assert 'function switchLanguage' in html


def test_javascript_redirect_logic(client):
    html = _content(client.get('/'))
    assert "window.location.href = '/zh/'" in html
    assert "window.location.href = '/'" in html


# User journey ---------------------------------------------------------------

def test_complete_language_switching_flow(client):
    response = client.get('/')
    assert response.context['LANGUAGE_CODE'] == 'en'

    response = client.get('/zh/')
    assert response.context['LANGUAGE_CODE'] == 'zh'

    response = client.get('/')
    assert response.context['LANGUAGE_CODE'] == 'en'


def test_navigation_preserves_language(client):
    assert 'href="/zh/"' in _content(client.get('/zh/'))
    assert 'href="/"' in _content(client.get('/'))
