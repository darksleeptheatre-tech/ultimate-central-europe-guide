import json
import os
from pathlib import Path

root = Path(__file__).resolve().parent.parent
output_dir = root / "data"
output_dir.mkdir(exist_ok=True)

prague_places = [
    "Old Town Square", "Charles Bridge", "Prague Castle", "St. Vitus Cathedral", "Lesser Town Bridge Tower",
    "Astronomical Clock", "Jewish Museum Prague", "Wenceslas Square", "New Town Hall", "Vyšehrad Castle",
    "Petřín Hill", "Letná Park", "Kampa Island", "Náplavka Riverside", "Dancing House", "Municipal House",
    "Malá Strana", "Hradčany District", "Museum of Communism", "National Gallery Prague", "Clementinum",
    "Wallenstein Garden", "Loreto Sanctuary", "Klementinum Courtyard", "Kafka Museum", "Kampa Museum",
    "Lesser Town Square", "St. Nicholas Church", "Prague Powder Tower", "Charles Square", "Riegrovy Sady Park",
    "Vltava River Cruise Dock", "Storch House", "Mincovna", "Mucha Museum", "Museum of Decorative Arts",
    "House at the Golden Tiger", "Riegrovy Sady Beer Garden", "Lobkowicz Palace", "Kampa Lounge",
    "Národní třída", "Karlova Street", "Parish Church of St. Cyril and Methodius", "Petrin Lookout",
    "Vltava Riverbank", "Mala Strana Steps", "Jindřišská Tower", "Bubny District", "The Dancing House",
    "Museum of Alchemists", "Basilica of St. Peter and St. Paul", "The New Stage", "Church of Our Lady Victorious",
    "River Palace", "Štěpánská Street", "Karlova Street Café", "U Fleků Brewery", "Lokál Dlouhááá",
    "Kantýna", "Café Savoy", "Mincovna Restaurant", "Kantine", "U Fleků", "U Fleků Garden",
    "Sisters Bistro", "Mincovna Wine Bar", "Hemingway Bar Prague", "Anonymous Bar", "Havelská Koruna",
    "U Fleků Beer Hall", "Mincovna Cocktail Bar", "U Trelu", "Bistro Mincovna", "Riegrovy Sady Café",
    "Jalta Restaurant", "Kantýna Bakery", "Mincovna Coffee", "El Hava", "The Bank Prague",
    "Café Savoy Terrace", "Náplavka Food Market", "Kantýna Market", "Mincovna Market", "Karlova Street Market",
    "Old Town Flea Market", "Prague Farmers Market", "Havelská Market", "Bubny Market", "Florenc Market",
    "Muzeum Metro Station", "Karlovo náměstí Tram Stop", "Prague Main Station", "Prague Airport Transfer Hub",
    "Kampa Coffee House", "Týnská Street", "Na Příkopě", "Prague Congress Centre", "Poděbradská Street",
    "Kampa Riverfront", "O2 Academy Prague", "Riegrovy Sady Café Bar", "Brewery U Fleků", "Café Savoy Pastry Shop"
]

vienna_places = [
    "Schönbrunn Palace", "Belvedere Museum", "St. Stephen’s Cathedral", "Vienna State Opera", "Hofburg Palace",
    "Albertina Museum", "Prater Park", "Stadtpark", "Naschmarkt", "Vienna City Hall", "Vienna Giant Ferris Wheel",
    "Karlskirche", "Secession Building", "Spanish Riding School", "Kunsthistorisches Museum", "Natural History Museum",
    "Danube Canal", "Schloss Belvedere", "Rathausplatz", "Stephansplatz", "Kärntner Straße", "Graben Street",
    "Mariahilfer Straße", "Landstraße", "Leopold Museum", "Haus des Meeres", "Prater Giant Ferris Wheel",
    "Vienna Woods", "Lainzer Tiergarten", "Burggarten", "Ringstrasse", "Schönbrunn Gardens", "The Hofburg",
    "Imperial Treasury", "Kahlenberg Hill", "Donaupark", "Augarten Park", "Wiener Prater", "Danube Tower",
    "Hundertwasserhaus", "Kunsthalle Wien", "Mumok", "Austrian National Library", "Vienna Museum",
    "Burgtheater", "Rosenburg Palace", "Palais Hansen Kempner", "Palais Pálffy", "Michaelerplatz",
    "St. Peter’s Church", "St. Charles Church", "Votive Church", "Austrian Gallery", "Museum Quarter",
    "Burggasse", "Neubau", "Leopoldstadt", "Wieden", "Margareten", "Josefstadt", "Innere Stadt",
    "Café Central", "Café Landtmann", "Demel Bakery", "Hotel Sacher", "Café Sperl", "Buchinger Bistro",
    "Motel One Rooftop", "The Roof Top", "Kameha Grand Bar", "Austrian Wine House", "Mayer am Pfarrplatz",
    "Glacis Beisl", "Restaurant Motto", "Riegler Restaurant", "Restaurant Steirereck", "Pizzeria", "Neni Wien",
    "Loving Hut", "Tafelspitz", "Balthasar Restaurant", "Mocca", "Berggasse", "Vienna Main Station",
    "Westbahnhof", "Praterstern", "Schwedenplatz", "Stephansdom", "Wiener Linien Metro", "Tram 1",
    "Airport Transfer Center", "Donau City", "Messe Wien", "Wiener Stadthalle"
]

budapest_places = [
    "Buda Castle", "Fisherman’s Bastion", "Hungarian Parliament Building", "St. Stephen’s Basilica",
    "Chain Bridge", "Gellért Hill", "Margaret Island", "Heroes’ Square", "Great Market Hall",
    "House of Terror", "Hungarian National Museum", "Mathias Church", "Buda Hills", "Citadella",
    "Danube Promenade", "Római Part", "Margit Boulevard", "Széchenyi Chain Bridge", "Buda Palace",
    "Castle District", "Váci Street", "Andrássy Avenue", "Memento Park", "Szentendre Day Trip",
    "Budapest Zoo", "City Park", "Kiscelli Museum", "Museum of Fine Arts", "Rómer Flóris Museum",
    "National Gallery", "Museum of Applied Arts", "Kelenföld", "Kőbánya", "Óbuda", "Csepel",
    "Rákóczi út", "Józsefváros", "Erzsébetváros", "Terézváros", "Újlipótváros", "Gül Baba",
    "Nyugati Railway Station", "Keleti Railway Station", "Déli Railway Station", "Budapest Airport",
    "Stadionok", "Népliget", "Művész", "Mazel Tov", "Műhely", "Borkonyha", "Café Gerbeaud",
    "Művész Kocsma", "The Old Man Pub", "Instant-Fogas", "Mazel Tov Restaurant", "Béla", "Kőleves",
    "Törökméz", "Kispiac", "Nagyvásárcsarnok", "Central Market Hall", "Központi Piac",
    "Római Part Farmers Market", "Buda Flea Market", "Fővám Square Market", "Ariosa Restaurant",
    "Kispiac Café", "Café Buda", "Sütő", "Bistro Buda", "Béla Bistro", "Műhely Wine Bar",
    "Mazel Tov Cocktail Bar", "Ariosa Bar", "The Rooftop", "Kőleves Pub", "Kertész Bar", "Dobos Café",
    "Szimpla Kert", "Mazel Tov Wine Bar", "Római Part Rooftop", "Kisfogház", "Budapest Jazz Club",
    "A38", "Akácfa Club", "Instant-Fogas Wine Bar", "Kőbánya Market", "Buda Market", "Pest Market",
    "Géza Market", "Börze Market", "Fővám Street Market", "Római Part Market", "Buda Castle Market",
    "Moszkva Square", "Budapest Metro Line 3", "Metro 2", "Tram 4", "Tram 6", "Bus 7",
    "Bolt Pickup Zone", "Ride Share Hub", "Airport Transfer Hub", "Danube Cruise Dock", "Budapest Cable Car",
    "Liberty Bridge", "Elisabeth Bridge", "Margaret Bridge", "Petőfi Bridge", "Rákosrendező",
    "Lágymányosi Bridge", "Puskás Ferenc Stadium", "Népstadion", "Béla Bartók Concert Hall",
    "Müpa", "National Theater", "Opera House", "Liszt Ferenc Academy", "Rumbach Sebestyén Street",
    "Duna Plaza", "WestEnd City Center", "Arena Plaza", "Mammut", "Váci Street Souvenir Shops",
    "Köbánya Outlet", "Buda Design Shops", "Pest Vintage Market", "Corvinus University", "Memento Park East"
]


image_pool = [
    "https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1499856871958-5b9627545d1a?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1467269204594-9661b134dd2b?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1501785888041-af3ef285b470?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1527631746610-bca00a040d60?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?auto=format&fit=crop&w=1200&q=80"
]


def categorize(name, city):
    lowered = name.lower()
    if any(token in lowered for token in ["market", "station", "transfer", "metro", "tram", "bus", "airport", "hub", "bridge", "square", "street", "plaza", "center"]):
        if any(token in lowered for token in ["market", "station", "transfer", "metro", "tram", "bus", "airport"]):
            return ["transport", "attractions"] if city == "prague" else ["transport", "local-markets"]
        return ["attractions", "photo-spots"]
    if any(token in lowered for token in ["bar", "pub", "club", "rooftop", "cocktail", "wine"]):
        return ["cocktail-bars", "nightlife"]
    if any(token in lowered for token in ["café", "cafe", "coffee", "bakery", "restaurant", "bistro", "hotel"]):
        return ["cafes", "local-restaurants"]
    if any(token in lowered for token in ["museum", "gallery", "opera", "theater", "castle", "palace", "cathedral", "church", "basilica"]):
        return ["attractions", "museums"]
    if any(token in lowered for token in ["park", "garden", "hill", "island", "promenade", "river", "wood", "tower"]):
        return ["parks", "photo-spots"]
    return ["attractions", "hidden-gems"]


def build_payload(city_name, places, base_lat, base_lng, count):
    payload = []
    for idx, name in enumerate(places[:count]):
        lat = base_lat + ((idx % 11) - 5) * 0.008 + (idx // 11) * 0.001
        lng = base_lng + ((idx % 7) - 3) * 0.012 + (idx // 7) * 0.001
        payload.append({
            "id": 1000 + idx,
            "name": name,
            "lat": round(lat, 6),
            "lng": round(lng, 6),
            "categories": categorize(name, city_name.lower()),
            "rating": round(4.2 + (idx % 8) * 0.1 + (idx % 3) * 0.05, 1),
            "description": f"{name} is one of the standout destinations for travelers looking to experience {city_name} at its best.",
            "image": image_pool[idx % len(image_pool)],
            "address": f"{name} District, {city_name}"
        })
    return payload

with open(output_dir / "prague.json", "w", encoding="utf-8") as fh:
    json.dump(build_payload("Prague", prague_places, 50.0875, 14.4214, 100), fh, ensure_ascii=False, indent=2)
with open(output_dir / "vienna.json", "w", encoding="utf-8") as fh:
    json.dump(build_payload("Vienna", vienna_places, 48.2082, 16.3738, 80), fh, ensure_ascii=False, indent=2)
with open(output_dir / "budapest.json", "w", encoding="utf-8") as fh:
    json.dump(build_payload("Budapest", budapest_places, 47.4979, 19.0402, 120), fh, ensure_ascii=False, indent=2)

print("Generated", len(json.load(open(output_dir / "prague.json", encoding="utf-8"))), "Prague places")
print("Generated", len(json.load(open(output_dir / "vienna.json", encoding="utf-8"))), "Vienna places")
print("Generated", len(json.load(open(output_dir / "budapest.json", encoding="utf-8"))), "Budapest places")
