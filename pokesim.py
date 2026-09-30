#!/usr/bin/env python3

import random
import statistics
from sys import exit

BOTTOM_SIXTEEN_MASK = 0x0000FFFF
TOP_SIXTEEN_MASK = 0xFFFF0000

RESULTS_STR = "Arithmetic Mean: {}, Median: {}, Mode: {}, Standard Deviation: {}, Lowest: {}, Highest: {}"


def generate_pokemon_personality_value() -> int:
    """
    Returns a 32 bit unsigned int representing a pokemon's personality value (PV).
    In Gen III, PV is used to determine the gender, ability, nature, shininess (for all pokemon)
    as well as some speciality attributes like spinda's spot pattern, unown's letter, wumple's evolution,
    the gender-counterpart species, and the size of the pokemon. The PV is generated with the pokemon is first
    encountered.
    """
    return random.getrandbits(32)


def generate_trainer_secret_id() -> int:
    """
    Returns a 16 bit unsigned integer representing the trainer/secret ID. This is generated as soon as a save file is created.
    The secret ID is never shown to the player, while the trainer ID is visible on the trainer card.
    """
    return random.getrandbits(16)


def extract_bits(target: int, mask: int) -> int:
    """
    Bitwise manipulation to extract target bits from the PV
    """
    return target & mask


def is_pokemon_shiny(PV: int, TID: int, SID: int, gen3odds: bool) -> bool:
    """
    Given a PV, TID, and SID, figure out if the pokemon is shiny or not. The calculation is a 4-way
    exclusive OR between the TID, SID, first 16 bits of the PV, and last 16 bits of the PV which results in a
    uint16_t. In Gen II-V, if that result is less than 8, the pokemon is shiny. In Gen VI+, if the result is less than 16, the pokemon is shiny.
    The resulting odds end up being 1/8,192 in Gen II-V (0.01221%) and 1/4096 in Gen VI+ (0.02441%)
    """
    first_16 = extract_bits(PV, TOP_SIXTEEN_MASK) >> 16
    last_16 = extract_bits(PV, BOTTOM_SIXTEEN_MASK)

    result = TID ^ SID ^ first_16 ^ last_16

    return (result < 8) if gen3odds else (result < 16)


def run_until_shiny(TID: int, SID: int, gen3odds: bool) -> int:
    """
    Given a TID and SID, roll the dice over and over until a shiny is hit. Once we do, report how
    many tries it took.
    """
    counter = 0

    while True:
        result = is_pokemon_shiny(
            generate_pokemon_personality_value(), TID, SID, gen3odds
        )
        if result:
            break
        counter += 1

    return counter


def statistical_trials(TID: int, SID: int, gen3odds: bool) -> None:
    """
    Let's do some statistics! Grab a number of trials, then do `run_until_shiny` for the set number of trials
    and grab some basic stats from it.
    """
    results = []
    trials = int(
        input(
            "\nEnter number of trials to do. Recommend at least 250, but doing too many _will_ slow down your machine: "
        )
    )

    print("Starting runs...")

    for _ in range(trials):
        results.append(run_until_shiny(TID, SID, gen3odds))

    mean = statistics.mean(results)
    median = statistics.median(results)
    mode = statistics.mode(results)
    sd = statistics.pstdev(results)
    low = min(results)
    high = max(results)

    print("Runs complete. Statistics:\n")
    print(RESULTS_STR.format(mean, median, mode, sd, low, high))


if __name__ == "__main__":
    TID = generate_trainer_secret_id()
    SID = generate_trainer_secret_id()
    print(f"\nSave file started. TID: {TID}, SID: {SID}")

    try:
        odds = input("Gen (2)-5 odds or gen (6)+ odds? ")
    except (KeyboardInterrupt, EOFError):
        print("Exiting...")
        exit(0)

    gen3odds = True if odds == "2" else False

    while True:
        try:
            opt = input(
                "\nRoll (o)nce for shiny, roll (u)ntil shiny, do (s)tatistics about shinies, (r)eset IDs, (q)uit: "
            ).upper()
        except (KeyboardInterrupt, EOFError):
            print("Exiting...")
            exit(0)

        match opt:
            case "O":
                print(
                    f"\nPokemon {"is" if is_pokemon_shiny(generate_pokemon_personality_value(), TID, SID, gen3odds) else "is not"} shiny"
                )
            case "U":
                print("\nRunning until shiny...")
                count = run_until_shiny(TID, SID, gen3odds)
                print(f"Complete. Number of resets before shiny: {count}")
            case "S":
                statistical_trials(TID, SID, gen3odds)
            case "R":
                TID = generate_trainer_secret_id()
                SID = generate_trainer_secret_id()

                print(f"\nIDs reset. New TID: {TID}, new SID: {SID}")
            case "Q":
                break
            case _:
                print("\nInvalid option provided.")
