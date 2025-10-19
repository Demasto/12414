# -*- coding: utf-8 -*-


import os
import re
import csv
import time
import base64
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://economy.gov.ru/material/directions/vneshneekonomicheskaya_deyatelnost/tamozhenno_tarifnoe_regulirovanie/"

OUT_DIR = r"C:\Users\dmelnikov\Desktop\Работа\Хакатон\knowledge\pdf"
LOG_PATH = os.path.join(OUT_DIR, "news_log.csv")

# ручной режим — окно открыто
HEADLESS = False
PAGE_LOAD_TIMEOUT = 60
OPEN_ARTICLE_WAIT = 25

AJAX_PAUSE = 0.9
APPLY_WAIT_TIMEOUT = 40

CARD_SELECTORS = [
    "article.e-info__item header a[href]",
    "article header a[href]",
    ".e-list article header a[href]",
    ".e-cards article header a[href]"
]

SHOW_MORE_SELECTORS = [
    "button.js-list-load-more",
    "a.js-list-load-more",
    "button.e-more",
    "a.e-more"
]

def ensure_outdir():
    os.makedirs(OUT_DIR, exist_ok=True)

def init_driver():
    opts = Options()
    if HEADLESS:
        opts.add_argument("--headless=new")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--window-size=1500,1100")
    opts.add_argument("--lang=ru-RU")
    opts.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=opts)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    return driver

def try_close_overlays(driver):
    js = """
    (function(){
      var sel = [
        '.cookie','.cookies','.cookie-banner','#cookie',
        '.modal','.overlay','.e-headline__shares','.e-headline__actions','.popup','.sharer'
      ];
      sel.forEach(function(s){
        document.querySelectorAll(s).forEach(function(el){
          try{ var b=el.querySelector('button,.btn,.close,[aria-label=\"Закрыть\"],[aria-label=\"Принять\"]'); if(b) b.click(); }catch(e){}
          el.style.display='none'; el.setAttribute('aria-hidden','true');
        });
      });
    })();
    """
    try:
        driver.execute_script(js)
    except Exception:
        pass

def wait_cards_present(driver, timeout=APPLY_WAIT_TIMEOUT):
    end = time.time() + timeout
    while time.time() < end:
        try_close_overlays(driver)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        for sel in CARD_SELECTORS:
            if soup.select_one(sel):
                return True
        time.sleep(0.5)
    return False

def click_show_more_until_end(driver, max_rounds=60):
    """
    Жмём «Показать ещё», если есть. Параллельно скроллим вниз — у них подгрузка через swiper/reachEnd.
    """
    rounds = 0
    prev_count = 0
    while rounds < max_rounds:
        rounds += 1
        try_close_overlays(driver)
        # текущий счётчик карточек
        soup = BeautifulSoup(driver.page_source, "html.parser")
        count_before = 0
        for sel in CARD_SELECTORS:
            count_before = max(count_before, len(soup.select(sel)))

        # пробуем нажать кнопку
        clicked = False
        for sel in SHOW_MORE_SELECTORS:
            try:
                btn = driver.find_element(By.CSS_SELECTOR, sel)
                if btn.is_displayed() and btn.is_enabled():
                    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
                    time.sleep(0.3)
                    try:
                        btn.click()
                    except Exception:
                        driver.execute_script("arguments[0].click();", btn)
                    time.sleep(1.2)
                    clicked = True
                    break
            except Exception:
                pass

        # Скроллим вниз несколько раз
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.7)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.7)

        # Пробуем дёрнуть их функцию догрузки (если есть)
        try:
            driver.execute_script("try{ if (typeof loadMoreSubmaterials==='function') loadMoreSubmaterials(); }catch(e){}")
        except Exception:
            pass

        time.sleep(0.7)

        # проверим, стало ли больше
        soup2 = BeautifulSoup(driver.page_source, "html.parser")
        count_after = 0
        for sel in CARD_SELECTORS:
            count_after = max(count_after, len(soup2.select(sel)))

        # если не растёт и кнопку не нашли — похоже, всё
        if count_after <= count_before and not clicked:
            break

        prev_count = count_after

def collect_cards_from_dom(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    cards = []
    seen = set()
    for sel in CARD_SELECTORS:
        for a in soup.select(sel):
            href = a.get("href")
            if not href:
                continue
            if href in seen:
                continue
            seen.add(href)
            title = (a.select_one(".e-title") or a).get_text(strip=True)
            date = (a.select_one(".e-date").get_text(strip=True)
                    if a.select_one(".e-date") else "")
            url = urljoin(BASE_URL, href)
            cards.append((url, title, date))
    return cards

def inject_print_css(driver):
    css = """
    var style = document.createElement('style');
    style.textContent = `
      header, footer, .e-headline__actions, .e-headline__shares, .e-breadcrumbs,
      .e-headline__share, .e-sidebar, .e-aside { display: none !important; }
      body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
      table { border-collapse: collapse; }
      table, th, td { border: 1px solid #777; }
      th, td { padding: 6px 8px; }
      img { max-width: 100%; height: auto; }
    `;
    document.head.appendChild(style);
    """
    driver.execute_script(css)

def print_current_page_to_pdf(driver, out_pdf_path):
    driver.execute_cdp_cmd("Page.enable", {})
    # прогрузим ленивое
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(0.2)
    inject_print_css(driver)
    pdf = driver.execute_cdp_cmd("Page.printToPDF", {
        "landscape": False,
        "printBackground": True,
        "paperWidth": 8.27,
        "paperHeight": 11.69,
        "marginTop": 0.4, "marginBottom": 0.4, "marginLeft": 0.4, "marginRight": 0.4,
        "scale": 1.0
    })
    with open(out_pdf_path, "wb") as f:
        f.write(base64.b64decode(pdf["data"]))

def slugify(text, maxlen=160):
    text = (text or "").strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[\\/:*?\"<>|]", " ", text)
    return text[:maxlen].rstrip()

def append_log(row):
    exists = os.path.exists(LOG_PATH)
    with open(LOG_PATH, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        if not exists:
            w.writerow(["title", "date", "url", "pdf_path", "status", "error"])
        w.writerow(row)

def run():
    ensure_outdir()
    driver = init_driver()
    try:
        driver.get(BASE_URL)
        time.sleep(1.5)
        try_close_overlays(driver)

        print("✅ В окне браузера вручную выбери ГОД (и при желании месяц). Дождись, пока список обновится.")
        input("Когда на странице видны карточки — нажми Enter в консоли... ")

        # Ждём появления карточек (если пользователь не дождался)
        if not wait_cards_present(driver, timeout=APPLY_WAIT_TIMEOUT):
            print("[WARN] Карточки не появились сами — пробую догрузить...")
        click_show_more_until_end(driver, max_rounds=60)

        # Собираем карточки
        cards = collect_cards_from_dom(driver)
        print(f"Найдено карточек: {len(cards)}")

        # Отладка, если пусто
        if len(cards) == 0:
            # дамп HTML и скрин
            with open("debug_html.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            try:
                driver.save_screenshot("debug_screen.png")
            except Exception:
                pass
            # ещё попытка: скролл + ещё раз собрать
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.0)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.6)
            cards = collect_cards_from_dom(driver)
            print(f"[retry] Найдено карточек: {len(cards)}")
            if len(cards) == 0:
                print("Окно оставлю открытым на 60 секунд для визуальной проверки...")
                time.sleep(60)
                return

        for url, title, date in cards:
            try:
                driver.get(url)
                try:
                    WebDriverWait(driver, OPEN_ARTICLE_WAIT).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".e-material__content, .e-main"))
                    )
                except Exception:
                    pass
                try_close_overlays(driver)
                # имя файла
                # сначала нормализуем дату к красивому префиксу, если в тексте есть "27 декабря 2024"
                m = re.search(r"(\d{1,2}\s+[А-Яа-яA-Za-z\.]+\s+\d{4})", date or "")
                prefix = m.group(1) if m else date or ""
                fname = (prefix + " - " if prefix else "") + slugify(title) + ".pdf"
                pdf_path = os.path.join(OUT_DIR, fname)
                # печать
                print_current_page_to_pdf(driver, pdf_path)
                append_log([title, date, url, pdf_path, "OK", ""])
                print("  [+]", pdf_path)
            except Exception as e:
                append_log([title, date, url, "", "ERROR", repr(e)])
                print("  [ERR]", url, "::", e)

        print("Готово. PDF в папке:", OUT_DIR)
        print("Лог:", LOG_PATH)

    finally:
        try:
            driver.quit()
        except Exception:
            pass

if __name__ == "__main__":
    run()
