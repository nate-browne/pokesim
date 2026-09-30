#!/usr/bin/env python3

import random
import statistics
from sys import exit
from typing import List

BOTTOM_SIXTEEN_MASK = 0x0000FFFF
TOP_SIXTEEN_MASK = 0xFFFF0000

RESULTS_STR = "Arithmetic Mean: {}, Median: {}, Mode: {} (count {}), Standard Deviation: {}, Lowest: {}, Highest: {}"


def generate_pokemon_personality_value() -> int:
    """
    Returns a 32 bit unsigned int representing a pokemon's personality value (PV).
    See the README for an explanation of why this matters.
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


def is_pokemon_shiny(
    PV: int, TID: int, SID: int, gen3odds: bool, shiny_charm: bool
) -> bool:
    """
    Given a PV, TID, and SID, figure out if the pokemon is shiny or not. See the README for an explanation on the procedure and the math.
    If shiny charm is applied, we do the calculation 3 times. Once on the provided PV, then we generate a second and see if shiny, then we generate a third and
    see if shiny. The real version of this in the games has to account for setting bits on the nature and gender (and other fields) to ensure that the encounter is the
    "same" (at least in Gen V), but everything else it uses PRNG and sees if we get a shiny.
    """

    # shift 16 slots to ignore the 16 0s in spots 0-15 and get the number as a short (16bit) instead of an int (32bit)
    first_16 = extract_bits(PV, TOP_SIXTEEN_MASK) >> 16
    last_16 = extract_bits(PV, BOTTOM_SIXTEEN_MASK)

    result = TID ^ SID ^ first_16 ^ last_16

    shiny = (result < 8) if gen3odds else (result < 16)

    if not shiny:
        if shiny_charm:
            for _ in range(2):
                PV = generate_pokemon_personality_value()
                first_16 = extract_bits(PV, TOP_SIXTEEN_MASK) >> 16
                last_16 = extract_bits(PV, BOTTOM_SIXTEEN_MASK)

                result = TID ^ SID ^ first_16 ^ last_16
                shiny = (result < 8) if gen3odds else (result < 16)

                if shiny:
                    break
    return shiny


def run_until_shiny(TID: int, SID: int, gen3odds: bool, shiny_charm: bool) -> int:
    """
    Given a TID and SID, roll the dice over and over until a shiny is hit. Once we do, report how
    many tries it took.
    """
    counter = 0

    while True:
        result = is_pokemon_shiny(
            generate_pokemon_personality_value(), TID, SID, gen3odds, shiny_charm
        )
        if result:
            break
        counter += 1

    return counter


def statistical_trials(TID: int, SID: int, gen3odds: bool, shiny_charm: bool) -> None:
    """
    Let's do some statistics! Grab a number of trials, then do `run_until_shiny` for the set number of trials
    and grab some basic stats from it.
    """
    results: List[int] = []
    trials = int(
        input(
            "\nEnter number of trials to do. Recommend at least 250, but doing too many _will_ slow down your machine: "
        )
    )

    print("Starting runs...")

    for _ in range(trials):
        results.append(run_until_shiny(TID, SID, gen3odds, shiny_charm))

    mean = statistics.mean(results)
    median = statistics.median(results)
    mode = statistics.mode(results)
    count = results.count(mode)
    sd = statistics.pstdev(results)
    low = min(results)
    high = max(results)

    print("Runs complete. Statistics:\n")
    print(RESULTS_STR.format(mean, median, mode, count, sd, low, high))


if __name__ == "__main__":

    random.seed(None)

    TID = generate_trainer_secret_id()
    SID = generate_trainer_secret_id()
    print(f"\nSave file started. TID: {TID}, SID: {SID}")

    try:
        odds = input("Gen (2)-5 odds or gen (6)+ odds? ")
    except (KeyboardInterrupt, EOFError):
        print("Exiting...")
        exit(0)

    gen3odds = True if odds == "2" else False

    try:
        charm = input("Use shiny charm (y/n)? ").upper()
    except (KeyboardInterrupt, EOFError):
        print("Exiting...")
        exit(0)

    shiny_charm = True if charm == "Y" else False

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
                    f"\nPokemon {"is" if is_pokemon_shiny(generate_pokemon_personality_value(), TID, SID, gen3odds, shiny_charm) else "is not"} shiny"
                )
            case "U":
                print("\nRunning until shiny...")
                count = run_until_shiny(TID, SID, gen3odds, shiny_charm)
                print(f"Complete. Number of resets before shiny: {count}")
            case "S":
                statistical_trials(TID, SID, gen3odds, shiny_charm)
            case "R":
                TID = generate_trainer_secret_id()
                SID = generate_trainer_secret_id()

                print(f"\nIDs reset. New TID: {TID}, new SID: {SID}")
            case "Q":
                break
            case _:
                print("\nInvalid option provided.")
