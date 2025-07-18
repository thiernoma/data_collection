import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cleaning import clean_text


def scrape_dakar_auto(pages):
    base_url = 'https://dakar-auto.com/senegal/voitures-4?&page='
    all_data = []
    driver = webdriver.Chrome()

    try:
        for page in range(1, pages + 1):
            print(f"Scraping page {page}...")
            driver.get(base_url + str(page))
            time.sleep(2)

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.listing-card"))
                )
            except:
                print(f"Timeout page {page}")
                continue

            containers = driver.find_elements(By.CSS_SELECTOR, "div.listing-card")

            for container in containers:
                try:
                    description = container.find_element(By.CSS_SELECTOR, 'h2.listing-card__header__title.mb-md-2.mb-0').text
                    attributes = container.find_elements(By.CSS_SELECTOR, 'li.listing-card__attribute.list-inline-item')
                    desc_parts = clean_text(description).split()
                    brand = desc_parts[0] if len(desc_parts) > 0 else ""
                    year = desc_parts[-1] if len(desc_parts) > 0 else ""
                    price = container.find_element(By.CSS_SELECTOR, 'h3.listing-card__header__price.font-weight-bold.text-uppercase.mb-0').text
                    address = container.find_element(By.CSS_SELECTOR, 'span.town-suburb.d-inline-block').text
                    kms_driven = attributes[1].text.strip() if len(attributes) > 1 else "valeur manquante"
                    transmission = attributes[2].text.strip() if len(attributes) > 2 else "valeur manquante"
                    fuel = attributes[3].text.strip() if len(attributes) > 3 else "valeur manquante"
                    owner_element = container.find_element(By.CSS_SELECTOR, 'div.author-meta a[href*="dakar-auto.com"]')
                    owner = owner_element.text.replace("Par ", "").strip()
                    
                    all_data.append({
                        'brand': brand,
                        'year': year,
                        'price': clean_text(price),
                        'address': clean_text(address),
                        'kms_driven': clean_text(kms_driven),
                        'transmission': clean_text(transmission),
                        'fuel': clean_text(fuel),
                        'owner': owner
                    })

                except Exception as e:
                    print(f"Erreur produit: {str(e)[:50]}...")

    finally:
        driver.quit()

    df = pd.DataFrame(all_data)
    print(f"{len(df)} produits scrapés au total")
    return df

def scrape_dakar_moto(pages):
    base_url = 'https://dakar-auto.com/senegal/motos-and-scooters-3?&page='
    all_data = []
    driver = webdriver.Chrome()

    try:
        for page in range(1, pages + 1):
            print(f"Scraping page {page}...")
            driver.get(base_url + str(page))
            time.sleep(2)

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.listing-card"))
                )
            except:
                print(f"Timeout page {page}")
                continue

            containers = driver.find_elements(By.CSS_SELECTOR, "div.listing-card")

            for container in containers:
                try:
                    description = container.find_element(By.CSS_SELECTOR, 'h2.listing-card__header__title.mb-md-2.mb-0').text
                    attributes = container.find_elements(By.CSS_SELECTOR, 'li.listing-card__attribute.list-inline-item')
                    desc_parts = clean_text(description).split()
                    brand = desc_parts[0] if len(desc_parts) > 0 else ""
                    year = desc_parts[-1] if len(desc_parts) > 0 else ""
                    price = container.find_element(By.CSS_SELECTOR, 'h3.listing-card__header__price.font-weight-bold.text-uppercase.mb-0').text
                    address = container.find_element(By.CSS_SELECTOR, 'span.town-suburb.d-inline-block').text
                    kms_driven = attributes[1].text.strip() if len(attributes) > 1 else "valeur manquante"
                    owner_element = container.find_element(By.CSS_SELECTOR, 'div.author-meta a[href*="dakar-auto.com"]')
                    owner = owner_element.text.replace("Par ", "").strip()
                    
                    all_data.append({
                        'brand': brand,
                        'year': year,
                        'price': clean_text(price),
                        'address': clean_text(address),
                        'kms_driven': clean_text(kms_driven),
                        'owner': owner
                    })

                except Exception as e:
                    print(f"Erreur produit: {str(e)[:50]}...")

    finally:
        driver.quit()

    df = pd.DataFrame(all_data)
    print(f"{len(df)} produits scrapés au total")
    return df

def scrape_dakar_location(pages):
    base_url = 'https://dakar-auto.com/senegal/location-de-voitures-19?&page='
    all_data = []
    driver = webdriver.Chrome()

    try:
        for page in range(1, pages + 1):
            print(f"Scraping page {page}...")
            driver.get(base_url + str(page))
            time.sleep(2)

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.listing-card"))
                )
            except:
                print(f"Timeout page {page}")
                continue

            containers = driver.find_elements(By.CSS_SELECTOR, "div.listing-card")

            for container in containers:
                try:
                    description = container.find_element(By.CSS_SELECTOR, 'h2.listing-card__header__title.mb-md-2.mb-0').text
                    desc_parts = clean_text(description).split()
                    brand = desc_parts[0] if len(desc_parts) > 0 else ""
                    year = desc_parts[-1] if len(desc_parts) > 0 else ""
                    price = container.find_element(By.CSS_SELECTOR, 'h3.listing-card__header__price.font-weight-bold.text-uppercase.mb-0').text
                    address = container.find_element(By.CSS_SELECTOR, 'span.town-suburb.d-inline-block').text
                    owner_element = container.find_element(By.CSS_SELECTOR, 'div.author-meta a[href*="dakar-auto.com"]')
                    owner = owner_element.text.replace("Par ", "").strip()
                    
                    all_data.append({
                        'brand': brand,
                        'year': year,
                        'price': clean_text(price),
                        'address': clean_text(address),
                        'owner': owner
                    })

                except Exception as e:
                    print(f"Erreur produit: {str(e)[:50]}...")

    finally:
        driver.quit()

    df = pd.DataFrame(all_data)
    print(f"{len(df)} produits scrapés au total")
    return df
