#!/usr/bin/env python3

import random
import statistics
from sys import exit
from typing import Tuple
from math import floor, sqrt

from utils import Pokemon, BALLS, STATUS, POKEMON_NUMBER_MAP, RESULTS_STR

OPT_STR = "(t)hrow one ball, throw (u)ntil caught, (s)tatistical analysis, (p)robabilty of a catch: "


def calculate_modified_catch_rate(
    mon: Pokemon, ball: str, status: str, hp: int, turns: int
) -> float:

    if ball == "timer":
        br = min((turns * 10 // 10), 4)
    else:
        br = BALLS[ball]

    sr = STATUS[status]

    return (((3 * mon.hp) - (2 * hp)) / (3 * mon.hp)) * mon.catch_rate * br * sr


def calculate_shake_probability(mod_catch_rate: float) -> int:
    return 1048560 // floor(sqrt(sqrt(16711680 // mod_catch_rate)))


def shake_check(shake_probability_threshold: int) -> bool:
    val = random.getrandbits(16)
    return val < shake_probability_threshold


def run_full_catch(
    mon: Pokemon, ball: str, status: str, hp: int, turn_number: int = 1
) -> int:
    shake_probability_threshold = calculate_shake_probability(
        calculate_modified_catch_rate(mon, ball, status, hp, turn_number)
    )

    shakes = 0
    while True:
        if shake_check(shake_probability_threshold):
            shakes += 1
            if shakes == 4:
                break
        else:
            break
    return shakes


def statistical_analysis(mon: Pokemon, status: str, hp: int) -> None:
    ball = grab_ball()

    try:
        trials = int(
            input(
                "Enter number of trials (minimum 100). Larger numbers will slow down your machine: "
            )
        )
    except (KeyboardInterrupt, EOFError):
        print("Exiting.")
        exit(0)

    results = []

    for _ in range(trials):
        results.append(throw_until_caught(mon, status, hp, ball))

    mean = statistics.mean(results)
    median = statistics.median(results)
    mode = statistics.mode(results)
    count = results.count(mode)
    sd = statistics.pstdev(results)
    low = min(results)
    high = max(results)

    print("Runs complete. Statistics:\n")
    print(RESULTS_STR.format(mean, median, mode, count, sd, low, high))


def grab_ball() -> str:
    for ball in BALLS.keys():
        print(f"{ball}")

    try:
        ball = input("Enter the full name of the ball you want to use: ")
    except (KeyboardInterrupt, EOFError):
        print("Exiting")
        exit(0)

    if ball not in BALLS.keys():
        raise ValueError(f"Value {ball} not in list of viable balls")
    return ball


def throw_until_caught(mon: Pokemon, status: str, hp: int, ball: str) -> int:

    counter = 1
    while True:
        shakes = run_full_catch(mon, ball, status, hp)

        if shakes == 4:
            print("Pokemon caught!")
            break
        print(f"Pokemon not caught. Number of shakes: {shakes}")
        counter += 1
    return counter


def throw_one_ball(mon: Pokemon, status: str, hp: int):

    ball = grab_ball()

    shakes = run_full_catch(mon, ball, status, hp)

    if shakes == 4:
        print("Pokemon caught!")
    else:
        print(f"Pokemon not caught. Number of shakes: {shakes}")


def calculate_catch_probability(mon: Pokemon, status: str, hp: int):

    ball = grab_ball()

    turn_number = int(
        input(
            "Enter number of turns of this catch. Must be <= 1. This really only matters if you're using a timer ball: "
        )
    )

    a = calculate_modified_catch_rate(mon, ball, status, hp, turn_number)

    print(f"Probability of catching {mon.name} at hp {hp}: {(a / 255) * 100}%")


def grab_values() -> Tuple[Pokemon, str, int]:

    # First, list out the pokemon to catch
    for key, mon in POKEMON_NUMBER_MAP.items():
        print(f"{key}: {mon.name}")

    try:
        mon = input("Pick a mon (enter the number): ")
    except (KeyboardInterrupt, EOFError):
        print("Exiting")
        exit(0)

    if mon not in POKEMON_NUMBER_MAP.keys():
        raise ValueError(f"Value {mon} not in list of viable balls")

    mon = POKEMON_NUMBER_MAP[mon]

    for status in STATUS.keys():
        print(f"{status}")

    try:
        status = input("Enter the full name of the status you want to use: ")
    except (KeyboardInterrupt, EOFError):
        print("Exiting")
        exit(0)

    if status not in STATUS.keys():
        raise ValueError(f"Value {status} not in list of viable balls")

    print(f"Your pokemon {mon.name} has a default HP of {mon.hp}")
    try:
        hp = int(input(f"Enter a value for the HP you want to catch (1, {mon.hp}): "))
    except (KeyboardInterrupt, EOFError):
        print("Exiting")
        exit(0)

    if not 1 <= hp <= mon.hp:
        raise ValueError(f"Value {hp} out of range")

    return mon, status, hp


if __name__ == "__main__":

    random.seed(None)

    mon, status, hp = grab_values()

    while True:
        try:
            cmd = input(OPT_STR).upper()
        except (KeyboardInterrupt, EOFError):
            print("Exiting")
            exit(0)

        match cmd:
            case "T":
                throw_one_ball(mon, status, hp)
            case "U":
                balls_thrown = throw_until_caught(mon, status, hp, grab_ball())
                print(f"Number of balls thrown: {balls_thrown}")
            case "S":
                statistical_analysis(mon, status, hp)
            case "P":
                calculate_catch_probability(mon, status, hp)
            case _:
                print(f"Command {cmd} not valid.")
