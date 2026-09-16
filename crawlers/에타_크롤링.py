"""Archived Selenium collector used during the project.

Run only when the account owner has permission to access and collect the target
board, and after checking the platform terms and research-ethics requirements.
Credentials are entered manually in the browser and are never read by this file.
"""

from __future__ import annotations

import argparse
import random
import time
from pathlib import Path

import chromedriver_autoinstaller
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Collect authorized Everytime board posts")
    parser.add_argument("--board-id", required=True, help="Board identifier visible in its URL")
    parser.add_argument("--max-pages", type=int, default=10, help="Maximum pages to visit")
    parser.add_argument("--output", type=Path, default=Path("data/raw/everytime_crawling.csv"))
    parser.add_argument("--min-delay", type=float, default=1.0)
    parser.add_argument("--max-delay", type=float, default=2.0)
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()
    if args.max_pages < 1:
        parser.error("--max-pages must be at least 1")
    if args.min_delay < 0 or args.max_delay < args.min_delay:
        parser.error("delay values must satisfy 0 <= min <= max")
    return args


def build_driver(headless: bool) -> webdriver.Chrome:
    chromedriver_autoinstaller.install()
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("lang=ko_KR")
    if headless:
        options.add_argument("--headless=new")
    return webdriver.Chrome(options=options)


def collect(args: argparse.Namespace) -> pd.DataFrame:
    driver = build_driver(args.headless)
    rows: list[dict[str, object]] = []
    wait = WebDriverWait(driver, 10)
    try:
        driver.get("https://everytime.kr/login")
        print("브라우저에서 직접 로그인한 뒤 이 콘솔로 돌아오세요.")
        input("로그인과 수집 권한 확인을 마쳤으면 엔터를 누르세요: ")

        for page in range(1, args.max_pages + 1):
            driver.get(f"https://everytime.kr/{args.board_id}/p/{page}")
            time.sleep(random.uniform(args.min_delay, args.max_delay))
            links = [
                element.get_attribute("href")
                for element in driver.find_elements(By.CSS_SELECTOR, "article > a.article")
            ]
            for link in filter(None, links):
                driver.get(link)
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "article")))
                time.sleep(random.uniform(args.min_delay, args.max_delay))

                post = driver.find_element(By.TAG_NAME, "article")
                status = post.find_element(By.CSS_SELECTOR, "ul.status.left")
                paragraphs = post.find_elements(By.CSS_SELECTOR, "p.large")
                title = post.find_element(By.CSS_SELECTOR, "h2.large").text
                rows.append(
                    {
                        "content": f"{title} {paragraphs[0].text}" if paragraphs else title,
                        "comment": [paragraph.text for paragraph in paragraphs[1:]],
                        "like": status.find_element(By.CSS_SELECTOR, "li.vote").text,
                        "comment_count": status.find_element(By.CSS_SELECTOR, "li.comment").text,
                        "scrap": status.find_element(By.CSS_SELECTOR, "li.scrap").text,
                        "date": post.find_element(By.CSS_SELECTOR, "time.large").text,
                    }
                )
            print(f"page {page}: {len(rows)} posts collected")
    finally:
        driver.quit()
    return pd.DataFrame(rows)


def main() -> None:
    args = parse_args()
    frame = collect(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(args.output, index=False, encoding="utf-8-sig")
    print(f"Saved {len(frame)} rows to {args.output}")


if __name__ == "__main__":
    main()
