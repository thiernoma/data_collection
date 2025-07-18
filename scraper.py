import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from cleaning import clean_text


def scrape_dakar_auto(pages):
    base_url = 'https://dakar-auto.com/senegal/voitures-4?&page='
    all_data = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for page in range(1, pages + 1):
        print(f"Scraping page {page}...")
        try:
            response = requests.get(base_url + str(page), headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            time.sleep(2)  # Respectful delay between requests

            containers = soup.select("div.listing-card")

            for container in containers:
                try:
                    # Extract data
                    title_elem = container.select_one('h2.listing-card__header__title.mb-md-2.mb-0')
                    description = title_elem.text if title_elem else ""
                    desc_parts = clean_text(description).split()
                    brand = desc_parts[0] if len(desc_parts) > 0 else ""
                    year = desc_parts[-1] if len(desc_parts) > 0 else ""

                    price_elem = container.select_one('h3.listing-card__header__price.font-weight-bold.text-uppercase.mb-0')
                    price = price_elem.text if price_elem else ""

                    address_elem = container.select_one('span.town-suburb.d-inline-block')
                    address = address_elem.text if address_elem else ""

                    attributes = container.select('li.listing-card__attribute.list-inline-item')
                    kms_driven = attributes[1].text.strip() if len(attributes) > 1 else "valeur manquante"
                    transmission = attributes[2].text.strip() if len(attributes) > 2 else "valeur manquante"
                    fuel = attributes[3].text.strip() if len(attributes) > 3 else "valeur manquante"

                    owner_elem = container.select_one('div.author-meta a[href*="dakar-auto.com"]')
                    owner = owner_elem.text.replace("Par ", "").strip() if owner_elem else ""

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

        except Exception as e:
            print(f"Erreur page {page}: {str(e)[:50]}...")
            continue

    df = pd.DataFrame(all_data)
    print(f"{len(df)} produits scrapés au total")
    return df


def scrape_dakar_moto(pages):
    base_url = 'https://dakar-auto.com/senegal/motos-and-scooters-3?&page='
    all_data = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for page in range(1, pages + 1):
        print(f"Scraping page {page}...")
        try:
            response = requests.get(base_url + str(page), headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            time.sleep(2)

            containers = soup.select("div.listing-card")

            for container in containers:
                try:
                    title_elem = container.select_one('h2.listing-card__header__title.mb-md-2.mb-0')
                    description = title_elem.text if title_elem else ""
                    desc_parts = clean_text(description).split()
                    brand = desc_parts[0] if len(desc_parts) > 0 else ""
                    year = desc_parts[-1] if len(desc_parts) > 0 else ""

                    price_elem = container.select_one('h3.listing-card__header__price.font-weight-bold.text-uppercase.mb-0')
                    price = price_elem.text if price_elem else ""

                    address_elem = container.select_one('span.town-suburb.d-inline-block')
                    address = address_elem.text if address_elem else ""

                    attributes = container.select('li.listing-card__attribute.list-inline-item')
                    kms_driven = attributes[1].text.strip() if len(attributes) > 1 else "valeur manquante"

                    owner_elem = container.select_one('div.author-meta a[href*="dakar-auto.com"]')
                    owner = owner_elem.text.replace("Par ", "").strip() if owner_elem else ""

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

        except Exception as e:
            print(f"Erreur page {page}: {str(e)[:50]}...")
            continue

    df = pd.DataFrame(all_data)
    print(f"{len(df)} produits scrapés au total")
    return df


def scrape_dakar_location(pages):
    base_url = 'https://dakar-auto.com/senegal/location-de-voitures-19?&page='
    all_data = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for page in range(1, pages + 1):
        print(f"Scraping page {page}...")
        try:
            response = requests.get(base_url + str(page), headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            time.sleep(2)

            containers = soup.select("div.listing-card")

            for container in containers:
                try:
                    title_elem = container.select_one('h2.listing-card__header__title.mb-md-2.mb-0')
                    description = title_elem.text if title_elem else ""
                    desc_parts = clean_text(description).split()
                    brand = desc_parts[0] if len(desc_parts) > 0 else ""
                    year = desc_parts[-1] if len(desc_parts) > 0 else ""

                    price_elem = container.select_one('h3.listing-card__header__price.font-weight-bold.text-uppercase.mb-0')
                    price = price_elem.text if price_elem else ""

                    address_elem = container.select_one('span.town-suburb.d-inline-block')
                    address = address_elem.text if address_elem else ""

                    owner_elem = container.select_one('div.author-meta a[href*="dakar-auto.com"]')
                    owner = owner_elem.text.replace("Par ", "").strip() if owner_elem else ""

                    all_data.append({
                        'brand': brand,
                        'year': year,
                        'price': clean_text(price),
                        'address': clean_text(address),
                        'owner': owner
                    })

                except Exception as e:
                    print(f"Erreur produit: {str(e)[:50]}...")

        except Exception as e:
            print(f"Erreur page {page}: {str(e)[:50]}...")
            continue

    df = pd.DataFrame(all_data)
    print(f"{len(df)} produits scrapés au total")
    return df