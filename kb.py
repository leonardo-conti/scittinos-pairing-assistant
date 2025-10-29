# kb.py
from typing import Dict, List

PairingKB: Dict[str, Dict] = {
    # Casual / Everyday
    "pizza night": {
        "food": {
            "appetizers": [
                "Garlic knots",
                "Arancini (Sicilian rice balls)",
                "House salad"
            ],
            "mains": [
                "12–16\" Pizzas (Cheese, Pepperoni, Margherita)",
                "Stromboli",
                "Calzone"
            ],
            "sides": [
                "Fried mozzarella",
                "Roasted veggies"
            ],
            "desserts": [
                "Cannoli (plain or chocolate-dipped)",
                "Assorted Italian cookies"
            ],
        },
        "drinks": {
            "alcoholic": ["Light lager", "Italian pilsner", "Chianti (red)"],
            "non_alcoholic": ["Cola", "Lemonade", "Sparkling water"],
            "coffee": ["Espresso", "Cappuccino"]
        },
        "tags": ["casual", "shareable", "family-friendly", "pizza"],
        "notes": "Pizzas & house specialties like Calzone/Stromboli are Scittino’s staples."
    },

    "italian family dinner": {
        "food": {
            "appetizers": [
                "Burrata with prosciutto & tomatoes",
                "Scittino’s homemade meatballs",
                "Tomato & fresh mozzarella platter"
            ],
            "mains": [
                "Lasagna (house)",
                "Chicken Parmigiana",
                "Penne alla Vodka or Bolognese"
            ],
            "sides": [
                "Garlic bread",
                "Caesar or Italian chopped salad"
            ],
            "desserts": [
                "Tiramisu",
                "Sfogliatelle",
                "Cheesecake"
            ],
        },
        "drinks": {
            "alcoholic": ["Sangiovese", "Montepulciano d’Abruzzo"],
            "non_alcoholic": ["Italian sodas", "Iced tea"],
            "coffee": ["Espresso", "Macchiato"]
        },
        "tags": ["family-style", "comfort", "classic-italian"]
    },

    "game day / tailgate": {
        "food": {
            "appetizers": [
                "Lascari wings (garlic lemon herb)",
                "Frito Misto (fried calamari & shrimp)",
                "Pepperoni rolls or Sausage Roll"
            ],
            "mains": [
                "Stromboli (salami, mortadella, mozzarella)",
                "The Sicilian sandwich (salumi, provolone, roasted peppers)",
                "Meatball subs"
            ],
            "sides": [
                "Potato wedges",
                "Coleslaw"
            ],
            "desserts": [
                "Brownies",
                "Cookie tray"
            ],
        },
        "drinks": {
            "alcoholic": ["Pale ale", "Amber lager"],
            "non_alcoholic": ["Cola", "Sports drinks", "Lemonade"]
        },
        "tags": ["casual", "shareable", "game-day"]
    },

    "office lunch / team meeting": {
        "food": {
            "appetizers": [
                "Gourmet marinated antipasto platter",
                "Tomato & fresh mozzarella platter"
            ],
            "mains": [
                "Assorted Classic Italian cold cut sandwiches",
                "Chicken Parm sandwich",
                "Pasta tray (Baked ziti or Penne alla Vodka)"
            ],
            "sides": [
                "House salad",
                "Chips"
            ],
            "desserts": [
                "Assorted Italian cookies",
                "Mini cannoli"
            ],
        },
        "drinks": {
            "non_alcoholic": ["Bottled water", "Iced tea", "Lemonade"],
            "coffee": ["Coffee urn", "Cappuccino (on request)"]
        },
        "tags": ["catering", "platter", "office-friendly"]
    },

    "kids birthday": {
        "food": {
            "appetizers": [
                "Cheesy garlic bread",
                "Fruit platter"
            ],
            "mains": [
                "Cheese pizza",
                "Chicken tenders",
                "Mini meatball sliders"
            ],
            "sides": [
                "Mac & cheese",
                "Carrot sticks & ranch"
            ],
            "desserts": [
                "Chocolate chip cookies",
                "Mini cannoli",
                "Cupcakes"
            ],
        },
        "drinks": {
            "non_alcoholic": ["Fruit punch", "Lemonade", "Water"],
        },
        "tags": ["kid-friendly", "nut-free-option", "shareable"]
    },

    "date night (italian)": {
        "food": {
            "appetizers": [
                "Burrata with balsamic & EVOO",
                "Arancini"
            ],
            "mains": [
                "Chicken or Eggplant Parmigiana",
                "Herb-crusted salmon (if featured) or Shrimp Fra Diavolo",
                "Wild mushroom risotto (veg option)"
            ],
            "sides": [
                "Grilled asparagus",
                "Truffle mashed potatoes"
            ],
            "desserts": [
                "Tiramisu",
                "Chocolate cannoli"
            ],
        },
        "drinks": {
            "alcoholic": ["Pinot Noir", "Barbera", "Prosecco"],
            "coffee": ["Espresso", "Cappuccino"]
        },
        "tags": ["elegant", "date-night"]
    },

    # Catering & Holidays
    "holiday antipasto & dessert trays": {
        "food": {
            "appetizers": [
                "Gourmet meat antipasto (prosciutto, sopressata, imported provolone)",
                "Marinated artichokes, olives, mushrooms"
            ],
            "mains": [],
            "sides": [],
            "desserts": [
                "Assorted biscotti & cookies",
                "Pignoli & almond macaroons",
                "Italian rum cake or Cannoli cake"
            ],
        },
        "drinks": {
            "alcoholic": ["Prosecco", "Moscato d’Asti"],
            "coffee": ["Espresso", "Americano"]
        },
        "tags": ["holiday", "platter", "bakery"]
    },

    # Market / Butcher / DIY
    "butcher grill pack": {
        "food": {
            "appetizers": [
                "Caprese skewers"
            ],
            "mains": [
                "House Italian sausage links (hot/sweet/fennel)",
                "Marinated chicken cutlets",
                "Homemade beef meatballs (for subs)"
            ],
            "sides": [
                "Deli salads (pasta salad, potato salad)"
            ],
            "desserts": [
                "Cookie tray"
            ],
        },
        "drinks": {
            "alcoholic": ["Italian lager", "Chianti for meatball subs"],
            "non_alcoholic": ["Sparkling water", "Iced tea"]
        },
        "tags": ["butcher", "grill", "cook-at-home"]
    },

    "build-your-own pasta kit": {
        "food": {
            "appetizers": [
                "Garlic bread",
                "Antipasto cup (olives, artichokes)"
            ],
            "mains": [
                "Fresh pasta (spaghetti/rigatoni/penne)",
                "House sauces (marinara, vodka, pesto, bolognese)",
                "Add-ons: meatballs, sausage, grilled chicken"
            ],
            "sides": [
                "Caesar or house salad"
            ],
            "desserts": [
                "Sfogliatelle",
                "Biscotti assortment"
            ],
        },
        "drinks": {
            "alcoholic": ["Chianti", "Nero d’Avola"],
            "coffee": ["Cappuccino"]
        },
        "tags": ["market", "DIY", "family-style"]
    },

    "coffee & pastry break": {
        "food": {
            "appetizers": [],
            "mains": [],
            "sides": [],
            "desserts": [
                "Cannoli (plain/chocolate/mini)",
                "Eclairs",
                "Cuccidati (fig cookies)",
                "Bread pudding (Panettone-based, seasonal)"
            ],
        },
        "drinks": {
            "coffee": ["Espresso", "Cappuccino", "Latte"],
            "non_alcoholic": ["Hot chocolate", "Bottled water"]
        },
        "tags": ["bakery", "coffee", "afternoon"]
    },

    # Sandwiches / Subs focus
    "italian sub platter": {
        "food": {
            "appetizers": [
                "Tomato & fresh mozzarella platter"
            ],
            "mains": [
                "Scittino’s Classic Italian Cold Cut subs",
                "The Sicilian sandwich",
                "Chicken cutlet & eggplant parm subs (mix)"
            ],
            "sides": [
                "Chips",
                "Italian chopped salad"
            ],
            "desserts": [
                "Mini cannoli",
                "Assorted cookies"
            ]
        },
        "drinks": {
            "non_alcoholic": ["Soda cans", "Iced tea", "Water"]
        },
        "tags": ["catering", "sandwich", "office-friendly"]
    }
}


def lookup_pairings(event: str) -> Dict:
    key = event.strip().lower()
    return PairingKB.get(key, {})
