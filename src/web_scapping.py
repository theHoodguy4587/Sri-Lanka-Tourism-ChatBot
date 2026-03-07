import requests
from bs4 import BeautifulSoup
import os
import re

places = [
"Sigiriya",
"Kandy",
"Galle",
"Ella,_Sri_Lanka",
"Mirissa",
"Unawatuna",
"Arugam_Bay",
"Yala_National_Park",
"Udawalawe_National_Park",
"Dambulla_Cave_Temple",
"Anuradhapura",
"Polonnaruwa",
"Adam%27s_Peak",
"Horton_Plains_National_Park",
"Nuwara_Eliya"
]

headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

os.makedirs("tourism_data", exist_ok=True)

for place in places:

    url = f"https://en.wikipedia.org/wiki/{place}"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch {place} | Status: {response.status_code}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    paragraphs = soup.select("p")

    text = ""

    for p in paragraphs[:8]:
        text += p.get_text()

    text = re.sub(r"\[[0-9]+\]", "", text)

    filename = place.replace(",", "").replace("_", " ").replace("%27","")

    with open(f"tourism_data/{filename}.txt", "w", encoding="utf-8") as file:
        file.write(text)

    print(f"Saved: {filename}")