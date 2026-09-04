import json
import re
from html.parser import HTMLParser
from urllib.parse import quote, unquote, urlencode
from urllib.request import Request, urlopen

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


TRAVEL_RECORDS = [
    {"city": "Kochi", "place": "Fort Kochi", "text": "Fort Kochi has Chinese fishing nets, St. Francis Church, Santa Cruz Basilica, heritage streets, cafes, and relaxed seaside walks. Hotel examples include Brunton Boatyard, Forte Kochi, and Old Harbour Hotel. Restaurant examples include Kashi Art Cafe, Fort House Restaurant, and Oceanos."},
    {"city": "Kochi", "place": "Mattancherry and Jew Town", "text": "Mattancherry and Jew Town are known for Mattancherry Palace, the Paradesi Synagogue area, antique shops, markets, and heritage streets. Restaurant examples include Rahumaniya Biriyani, Kayees Rahmathulla Cafe, and Ginger House Restaurant."},
    {"city": "Kochi", "place": "Kumbalangi", "text": "Kumbalangi near Kochi offers village, fishing, and backwater experiences. Activity availability and operator details should be verified."},
    {"city": "Munnar", "place": "Munnar tea country", "text": "Munnar is known for tea plantations, rolling hills, viewpoints, Eravikulam National Park, and cool mountain weather. Hotel examples include The Paniperuma, Fragrant Nature Munnar, and Tea County. Restaurant examples include Rasa Gurukulam, Saravana Bhavan, and Hotel Hill View."},
    {"city": "Alappuzha", "place": "Alappuzha backwaters", "text": "Alappuzha, also called Alleppey, is known for Kerala backwaters, houseboats, canals, coconut palms, and village scenery. Hotel examples include Raheem Residency, Punnamada Resort, and Marari Beach Resort. Restaurant examples include Thaff Restaurant, Mushroom, and Harbour Restaurant."},
    {"city": "Wayanad", "place": "Wayanad nature", "text": "Wayanad offers hills, forests, waterfalls, Edakkal Caves, wildlife areas, and quieter nature-focused experiences. Hotel examples include Vythiri Resort, Wayanad Wild, and Arayal Resort. Restaurant examples include Wilton Restaurant, Jubilee Restaurant, and 1980's A Nostalgic Restaurant."},
    {"city": "Bengaluru", "place": "Bengaluru city", "text": "Bengaluru is known for Lalbagh Botanical Garden, Cubbon Park, Bengaluru Palace, museums, cafes, breweries, and technology culture. Hotel examples include The Oberoi Bengaluru, ITC Gardenia, and The Leela Palace. Restaurant examples include MTR, Nagarjuna, Karavalli, and Vidyarthi Bhavan."},
    {"city": "Mysuru", "place": "Mysuru Palace and heritage", "text": "Mysuru is known for Mysuru Palace, Devaraja Market, Chamundi Hill, St. Philomena's Church, yoga, and traditional food. Hotel examples include Radisson Blu Plaza Hotel, Lalitha Mahal Palace Hotel, and Hotel Ruchi the Prince. Restaurant examples include RRR Restaurant, Mylari, and Hotel Vinayaka Mylari."},
    {"city": "Coorg", "place": "Coorg coffee country", "text": "Coorg, also called Kodagu, is known for coffee plantations, Madikeri, Abbey Falls, viewpoints, forests, and Kodava cuisine. Hotel examples include Evolve Back Coorg, The Tamara Coorg, and Taj Madikeri Resort & Spa. Restaurant examples include Raintree Restaurant, Coorg Cuisine, and Taste of Coorg."},
    {"city": "Ooty", "place": "Ooty hill station", "text": "Ooty is known for Nilgiri mountain scenery, the botanical garden, Ooty Lake, tea estates, and the heritage toy train route. Hotel examples include Savoy Ooty, Sterling Ooty Fern Hill, and Gem Park Ooty. Restaurant examples include Earl's Secret, Hyderabad Biryani House, and Adyar Ananda Bhavan."},
    {"city": "Kodaikanal", "place": "Kodaikanal hills", "text": "Kodaikanal offers a cool hill climate, Kodaikanal Lake, Coaker's Walk, Pillar Rocks, pine forests, and scenic viewpoints. Hotel examples include The Carlton, The Tamara Kodai, and Sterling Kodai Lake. Restaurant examples include Cloud Street, Ten Degrees, and Tava."},
    {"city": "Chennai", "place": "Chennai culture and coast", "text": "Chennai is known for Marina Beach, Kapaleeshwarar Temple, Fort St. George, museums, classical music, Bharatanatyam, and South Indian food. Hotel examples include Taj Coromandel, The Leela Palace Chennai, and ITC Grand Chola. Restaurant examples include Murugan Idli Shop, Dakshin, Ratna Cafe, and Sangeetha."},
    {"city": "Mahabalipuram", "place": "Mahabalipuram shore temples", "text": "Mahabalipuram is known for Shore Temple, rock-cut monuments, Arjuna's Penance, sculpture workshops, and the Bay of Bengal coast. Hotel examples include Radisson Blu Resort Temple Bay, InterContinental Chennai Mahabalipuram Resort, and Chariot Beach Resort. Restaurant examples include Moonrakers, Le Yogi, and Nautilus."},
    {"city": "Madurai", "place": "Madurai heritage", "text": "Madurai is known for Meenakshi Amman Temple, historic markets, Tamil cuisine, evening temple rituals, and the Thirumalai Nayakkar Palace. Hotel examples include Heritage Madurai, The Gateway Hotel Pasumalai, and Courtyard by Marriott Madurai. Restaurant examples include Murugan Idli Shop, Kumar Mess, and Konar Mess."},
    {"city": "Hyderabad", "place": "Hyderabad heritage and food", "text": "Hyderabad is known for Charminar, Golconda Fort, Qutb Shahi Tombs, museums, biryani, Irani chai, and lively old-city markets. Hotel examples include Taj Falaknuma Palace, Park Hyatt Hyderabad, and ITC Kohenur. Restaurant examples include Paradise Biryani, Shah Ghouse, Bawarchi, and Cafe Niloufer."},
    {"city": "Hampi", "place": "Hampi ruins", "text": "Hampi has UNESCO-listed Vijayanagara ruins, Virupaksha Temple, stone monuments, boulder landscapes, river scenery, and cycling routes. Stay examples include Evolve Back Hampi, Hampi's Boulder Resort, and guesthouses around Hampi Bazaar. Restaurant examples include Mango Tree, The Goan Corner, and Taste of Brahmins."},
    {"city": "Puducherry", "place": "Puducherry", "text": "Puducherry is known for the French Quarter, seaside promenade, cafes, Sri Aurobindo Ashram, Auroville nearby, and Tamil-French culture. Hotel examples include Palais de Mahe, Le Dupleix, and The Promenade. Restaurant examples include Villa Shanti, Cafe des Arts, Surguru Spot Restaurant, and La Villa."},
    {"city": "Goa", "place": "Goa beaches and heritage", "text": "Goa offers beaches, Portuguese heritage in Old Goa, local seafood, markets, churches, nature areas, and varied nightlife. Hotel examples include Taj Exotica Resort, ITC Grand Goa, and Alila Diwa Goa. Restaurant examples include Gunpowder, Ritz Classic, Vinayak Family Restaurant, and Martin's Corner."},
]

SHORT_CITY_NAMES = {
    "blr": "Bengaluru",
    "b'lore": "Bengaluru",
    "cok": "Kochi",
    "maa": "Chennai",
    "mad": "Madurai",
    "hyd": "Hyderabad",
    "mys": "Mysuru",
    "pdy": "Puducherry",
    "pondy": "Puducherry",
    "hsn": "the full city name",
}

CITY_DAILY_BUDGETS = {
    "alappuzha": 9000,
    "bengaluru": 14000,
    "chennai": 13000,
    "coorg": 11000,
    "goa": 16000,
    "hampi": 8000,
    "hyderabad": 12000,
    "kodaikanal": 10000,
    "kochi": 12000,
    "madurai": 8000,
    "mahabalipuram": 11000,
    "munnar": 11000,
    "mysuru": 9000,
    "ooty": 10000,
    "puducherry": 12000,
    "wayanad": 10000,
}

_VECTOR_TEXTS = [f"{record['city']} {record['place']} {record['text']}" for record in TRAVEL_RECORDS]
_VECTOR_MODEL = TfidfVectorizer(stop_words="english")
_VECTOR_MATRIX = _VECTOR_MODEL.fit_transform(_VECTOR_TEXTS)


def supported_cities() -> list[str]:
    return sorted({record["city"] for record in TRAVEL_RECORDS})


def short_city_name_error(city: str) -> str | None:
    cleaned_city = city.strip()
    suggestion = SHORT_CITY_NAMES.get(cleaned_city.casefold())
    if suggestion:
        if suggestion == "the full city name":
            return f"'{cleaned_city}' looks like a short code. Please enter the city's full name."
        return f"Please enter the full city name '{suggestion}' instead of '{cleaned_city}'."
    if cleaned_city.casefold() in {name.casefold() for name in supported_cities()}:
        return None
    if re.fullmatch(r"[A-Z]{2,5}", cleaned_city):
        return f"'{cleaned_city}' looks like an abbreviation. Please enter the city's full name."
    if re.fullmatch(r"[A-Za-z]{2,6}", cleaned_city) and not re.search(r"[aeiou]", cleaned_city.casefold()):
        return f"'{cleaned_city}' looks like a short code. Please enter the city's full name."
    return None


def estimate_daily_budget(city: str) -> tuple[int, bool]:
    normalized_city = city.strip().casefold()
    budget = CITY_DAILY_BUDGETS.get(normalized_city)
    if budget is not None:
        return budget, True
    return 10000, False


def retrieve_city_context(city: str, limit: int = 5) -> list[dict[str, str]]:
    normalized_city = city.strip().casefold()
    city_records = [record for record in TRAVEL_RECORDS if record["city"].casefold() == normalized_city]
    if not city_records:
        return []

    query_vector = _VECTOR_MODEL.transform([city])
    scores = cosine_similarity(query_vector, _VECTOR_MATRIX).ravel()
    ranked_indexes = scores.argsort()[::-1]
    return [
        TRAVEL_RECORDS[index]
        for index in ranked_indexes
        if TRAVEL_RECORDS[index]["city"].casefold() == normalized_city
    ][:limit]


def format_context(records: list[dict[str, str]]) -> str:
    return "\n\n".join(
        f"Source: built-in South India travel knowledge\nPlace: {record['place']} ({record['city']})\n{record['text']}"
        for record in records
    )


class _SearchResultParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.results: list[dict[str, str]] = []
        self._current: dict[str, str] | None = None
        self._field: str | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        classes = (attributes.get("class") or "").split()
        if tag == "a" and ("result__a" in classes or "result-link" in classes):
            self._current = {"url": unquote(attributes.get("href") or ""), "title": "", "content": ""}
            self._field = "title"
        elif tag in {"a", "div", "td"} and ("result__snippet" in classes or "result-snippet" in classes) and self._current:
            self._field = "content"

    def handle_data(self, data: str) -> None:
        if self._current and self._field:
            self._current[self._field] += data.strip() + " "

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._current and self._field == "title":
            self._field = None
        elif tag in {"a", "div", "td"} and self._current and self._field == "content":
            self.results.append({key: value.strip() for key, value in self._current.items()})
            self._current = None
            self._field = None


def search_web_context(city: str, limit: int = 6) -> tuple[str, list[str]]:
    queries = [
        f"{city} official tourism attractions",
        f"{city} hotels accommodation",
        f"{city} famous restaurants local food",
    ]
    results = []
    for query in queries:
        query_results = []
        for endpoint in ("https://html.duckduckgo.com/html/?q=", "https://lite.duckduckgo.com/lite/?q="):
            request = Request(
                endpoint + quote(query),
                headers={"User-Agent": "Mozilla/5.0 (Trip Advisor research)"},
            )
            with urlopen(request, timeout=20) as response:
                parser = _SearchResultParser()
                parser.feed(response.read().decode("utf-8", errors="ignore"))
            query_results = parser.results[:limit]
            if query_results:
                break
        results.extend(query_results)

    if not any(result.get("content") and result.get("url") for result in results):
        wikipedia_url = "https://en.wikipedia.org/w/rest.php/v1/search/page?" + urlencode({"q": city, "limit": limit})
        request = Request(
            wikipedia_url,
            headers={"User-Agent": "Wanderwise travel research/1.0"},
        )
        with urlopen(request, timeout=20) as response:
            pages = json.loads(response.read().decode("utf-8")).get("pages", [])
        results = [
            {
                "url": f"https://en.wikipedia.org/wiki/{quote(page.get('key', ''))}",
                "title": page.get("title", ""),
                "content": page.get("description", "") + " " + page.get("excerpt", ""),
            }
            for page in pages
        ]

    sources = [result["url"] for result in results if result.get("url")]
    context = "\n\n".join(
        f"Source URL: {result['url']}\nTitle: {result['title']}\n{result['content']}"
        for result in results
        if result.get("content") and result.get("url")
    )
    if not context:
        raise ValueError(f"Web search returned no useful sources for '{city}'.")
    return context, sources
