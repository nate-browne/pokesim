from typing import List, Dict


class Pokemon(object):
    def __init__(self, name: str, hp: int, types: List[str], catch_rate: int):
        self.name = name
        self.hp = hp
        self.types = types
        self.catch_rate = catch_rate


RESULTS_STR = "Arithmetic Mean: {}, Median: {}, Mode: {} (count {}), Standard Deviation: {}, Lowest: {}, Highest: {}"
POKEMON_NUMBER_MAP: Dict[str, Pokemon] = {
    "1": Pokemon("Charmander", 20, ["fire"], 45),
    "2": Pokemon("Totodile", 20, ["water"], 45),
    "3": Pokemon("Weedle", 15, ["bug", "poison"], 255),
    "4": Pokemon("Abra", 28, ["psychic"], 200),
    "5": Pokemon("Psyduck", 76, ["water"], 190),
    "6": Pokemon("Golduck", 98, ["water"], 75),
    "7": Pokemon("Electabuzz", 90, ["electric"], 45),
    "8": Pokemon("Gyrados", 82, ["water", "flying"], 45),
    "9": Pokemon("Rapidash", 102, ["fire"], 60),
    "10": Pokemon("Skarmory", 79, ["steel", "flying"], 25),
    "11": Pokemon("Deoxys", 70, ["psychic"], 3),
    "12": Pokemon("Latios", 140, ["dragon", "psychic"], 3),
    "13": Pokemon("Rayquaza", 227, ["dragon", "flyging"], 3),
}


BALLS = {
    "master": 0,
    "regular": 1,
    "great": 1.5,
    "ultra": 2,
    "net": 3,
    "timer": 0,
}

STATUS = {
    "sleep": 2,
    "freeze": 2,
    "paralysis": 1.5,
    "poison": 1.5,
    "burn": 1.5,
    "none": 1,
}
