
import os
import requests
import time

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)

def fetch_skinbid_deals():
    url = "https://api.skinbid.com/api/items/listings"
    params = {"sort": "endingSoon", "page": 1, "limit": 100}
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        return []

    try:
        items = response.json()["items"]
    except:
        return []

    results = []
    for item in items:
        try:
            title = item["title"]
            discount = item.get("discountPercent", 0)
            price = item.get("price", {}).get("eur", "N/A")
            link = f"https://skinbid.com/lot/{item['slug']}"
            if discount >= 11:
                results.append(f"✅ {title} — {discount}% off — €{price}\n{link}")
        except:
            continue
    return results

def main():
    while True:
        deals = fetch_skinbid_deals()
        if deals:
            for deal in deals:
                send_telegram_message(deal)
        else:
            send_telegram_message("🔎 Nicio reducere peste 11% găsită momentan.")
        time.sleep(900)  # 15 minute

if __name__ == "__main__":
    main()
