# Pokésim
## Programs that Emulate some of the RNG Present in Pokémon

## ShinySim

### Intro
This is a short and sweet lil program written in Python for the sake of showcasing just how... unfun,
shiny hunting can be. It first generates a random trainer ID (TID) and secret ID (SID), then allows you to
roll once for a shiny, roll until you get a shiny, and do some statistics around shinies.

### The Shiny Hunt (Math Included)
Pokemon is, functionally, data structures that also double as spreadsheets fighting each other with fancy bitgraphic
animations (in the older games). Because of the format of the original games on the original GameBoy, some nice
bit manipulation is used to cut down on memory used per Pokemon. One of those things is the **Personality Value** (PV),
a 32-bit unsigned integer used to hold... a lot of information about a Pokemon. Just in Gen III, the values held in the PV include the
gender, ability, nature, shininess, and some species-specific information. The PV is generated upon an encounter with the Pokemon in question,
and is controlled by a pesudorandom number generator. But, to calculate shininess, Pokemon takes advantage of four 16-bit unsigned integers: the TID, the SID, and the PV split into two 16-bit integers.

Now, I should note here that Gen II (the first games with shiny pokemon) actually does it completely differently than every other generation. In Gen II, shiny odds are determined by the IVs of a pokemon (IVs are a rabbit hole I'm not gonna go down here; look it up if you're curious). To get a shiny pokemon, the following conditions must be met:

1. The speed, defense, and special IVs _must_ be equal to 10.
2. The Attack IV must be one of these values: `{2, 3, 6, 7, 10, 11, 14, 15}`.

Since Gen II does some weird stuff with HP for the IV value and sp. def and sp. attack are both using the special IV, there are only 4 separate IVs (the aforementioned ones) with 16 possibilities `[0, 16)` and thus there are $16^4 = 65,536$ distinct combinations of IVs that can be generated. Since there is only one (1) way to fulfill condition 1 and eight (8) ways to fulfill condition 2, the probability of a shiny (assuming all combinations are equally likely) is $\frac{1 * 8}{65,536} \rightarrow \frac{8}{65,536} \rightarrow \frac{1}{8,192}$ which is a percentage of `0.01221%`. Yeesh.

From Gen III onwards, algorithmically it's quite a simple calculation. Firstly, take the PV and use bitwise `AND` to pull out bits 32-16 (then rightshift them 16 spots so that you end up with a `uint16_t`).
Next, take that same PV and use bitwise `AND` to pull out bits 15-0. Call the first result `a`, and the second `b`. Now, we calculate the result with the following equation:

$`\text{result} = \text{TID} \oplus \text{SID} \oplus a \oplus b`$

If `result` is less than 8, the pokemon is shiny.

So, what's the probability of this? A `uint16_t` can range between `[0, 65,536)`, so a shiny has a probability of $\frac{8}{65,536} \rightarrow \frac{1}{8,192}$ (look familiar?) which is a percentage of `0.01221%`.

Starting in Gen VI, shiny hunting became slightly more manageable due to the probabilty being changed to $\frac{1}{4,096}$ (percentage of `0.02441%`) which is exactly double the previous probability. The way they did this was by changing the check at the end to be less than 16 instead of less than 8. In fact, the way you could easily mod games to have boosted shiny odds is by just changing what number you check against at the end. The math is pretty basic so I won't bother writing it _all_ out, but if you check if the result is less than 128 you'll give $\frac{1}{512}$ odds (percentage of `0.1953%`) and checking if the result is less than 1,024 will give $\frac{1}{64}$ odds (percentage of `1.562%`).

Finally, let's talk about the Shiny Charm. This was added in Gen V and is in every gen since then, and the way it works is that if the player has it in their Bag the game will generate two extra personality values for a given Pokemon encounter, effectively tripling the chances of finding a shiny. For Gen V (first game where this is available), the probability goes from $\frac{1}{8,192}$ to $\frac{3}{8,192}$ (roughly `0.03662%`). From Gen VI onwards, since the shiny odds were boosted (as discussed earlier), the shiny charm makes the probability go from $\frac{1}{4096}$ to $\frac{3}{4096}$ (roughly `0.07324%`).

### This Program, Explained
This program is a way of visualizing just how rough the shiny hunt can be, minus the resetting and the mashing (so it's still even faster than a real shiny hunt). When you start it up, it'll generate a random TID and SID for you and using those will allow you to shiny hunt. The program options are to roll once for a shiny, keep rolling until you get a shiny, or do statistical analysis on trials. The first one is self-explanatory, rolling till shiny just runs the program until a shiny is found and reports back with the number of resets (smallest would be 0 if you manage to get a shiny immediately), and the last option allows you to input a number of trials to do. It will then roll until shiny, storing the number of resets to get to that shiny, for the number of trials you specify. Then, it will get the arithmetic mean, the median, the mode, the standard deviation, the lowest number of resets, and the highest number of resets.

Some features it includes are the ability to use Gen II-V probability vs Gen VI+ probability, the shiny charm, the option to provide your own trainer ID and secret ID, and the ability to reset your trainer and secret ID whenever you want.

## CatchSim

### Intro
This is another quick program that exist to emulate the experience of catching a Pokémon. If you've ever been curious about how the catch odds work, or want to try something out that you've
never tried in the game, this is the program to run. Like before, I'll start by explaining the underlying mechanics and the math that is going on.

### To Catch 'em All (With Math)
So, catching a Pokémon is one of those things which has changed a _lot_ through the generations and versions, and as Gen III is my favorite, that is the version I've implemented in this program. The first key point about the catch algorithm, is that the catch rate of a particular mon is just a portion of the story and nowhere _near_ the entire story. Thus, it makes the most sense to begin the explanation of the catch system with a chat about the **modified catch rate**.

Let's start with the catch rate. The catch rate of a mon will vary from generation to generation, but generally speaking, the more rare or more evolved a mon is, the lower the base catch rate will be. For early route bugs, the catch rate is quite high (caterpie in generation III has a catch rate of 255, which is a maximum value) while legendaries will have a catch rate of 3 (yes, 3). The other factors that are considered are the pokéball type being used, the status on the mon (paralyzed, burned, frozen, asleep, or nothing), the current HP of the mon, and the max HP of the mon at the level you're catching it. All of these factors combine in this equation:

$`\text{MCR} = \frac{(3 * \text{HP}_{\text{max}}) - (2 * \text{HP}_{\text{current}})}{(3 * \text{HP}_{\text{max}})} * \text{catch rate} * \text{ball multiplier} * \text{status multiplier}`$

The **ball multiplier** starts with normal/premier/luxury pokéballs (1x), great balls (1.5x), ultra balls (2x), net balls (3.5x when used on water or bug types, 1x otherwise), dive balls (3.5x when used underwater while using dive, 1x otherwise. This was changed after gen I to be 3.5x on water types in general), nest balls ((41 - pokémon's level) / 10 if pokemon's level is between 1 and 29, 1x otherwise), repeat balls (3.5x if used on a mon that was caught previously, 1x otherwise), and timer balls (which uses a multipler calculated by this equation: $min(\frac{\text{turns} * 10}{10}, 4)$). If you're wondering about master balls, we'll get to that later.

The **status multiplier** uses a system of sleeping/frozen having a multiplier of 2x, paralysis/poisoning/burning having a multiplier of 1.5x, and no status change having a multiplier of 1x.

Taking two examples: catching a Deoxys (legendary psychic type with a catch rate of 3) at level 30 with 1 HP (default it has at that level is 70 hp) that is paralyzed throwing ultra balls yields a modified catch rate:

$`\frac{(3 * 70) - (2 * 1)}{(3 * 70)} * 3 * 2 * 1.5 \rightarrow 8.914285714`$

While a level 3 Weedle (bug poison type with a catch rate of 255) at level 3 with full HP with no status changes throwing great balls yields a modified catch rate:

$`\frac{(3 * 15) - (2 * 15)}{(3 * 15)} * 255 * 1.5 * 1 \rightarrow 127.5`$

Now that we have the modified catch rate, the next thing we need is what I call the **shake probability threshold**. This is a number between [0, 65536) that will be used as a comparator, which is calculated like this:

$`\frac{1,048,560}{\sqrt{\sqrt{\frac{16,711,680}{MCR}}}}`$

In the calculation, the result of the divisions as well as the square roots are rounded down. Taking our two calculated modified catch rates, the comparator for the Deoxys is

$`\frac{1,048,560}{\sqrt{\sqrt{\frac{16,711,680}{8.914285714}}}} \rightarrow 28,339`$

and the comparator for the Weedle is:

$`\frac{1,048,560}{\sqrt{\sqrt{\frac{16,711,680}{127.5}}}} \rightarrow 55,187`$

Now, with those calculated, we have the actual catch algorithm. Pokémon considers a mon to be caught if the ball shakes 4 times, so to calculate a single shake, we generate a 16 bit unsigned integer and compare it to the comparator we calculated in the previous step. If the value we generate is strictly less than the comparator, the shake check passes. Pass 4 shake checks back to back to back to back, and the mon is caught. Otherwise, the ball will shake the number of times as shake checks passed.

Given the values we've calculated, the probability of catching a mon, given the `MCR` and `SPT` we calculated before, is $(\frac{\text{SPT}}{65,535})^4$ (or $\frac{\text{MCR}}{255}$). Therefore, the probability of catching that Deoxys in those conditions with that particular ball is $(\frac{28,339}{65,535})^4 \rightarrow 0.03497 \rightarrow 3.497\%$ and for the Weedle with that particular ball is $(\frac{55,187}{65,535})^4 \rightarrow 0.50287 \rightarrow 50.2868\%$

Let's revisit a question: what about the master ball? Well, it's a simple short circuit. All you need to do is check if the ball thrown is a master ball, and if so just return 4 shakes (aka a catch) and you're done. In python code, it's pretty straight forward:

```python
def run_full_catch(
    mon: Pokemon, ball: str, status: str, hp: int, turn_number: int = 1
) -> int:
    """
    Runs a full catch sequence. For a pokemon to be caught, 4 shake checks must pass in a row.
    """

    # short circuit for master ball
    if ball == "master":
        return 4

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
```

And that's it! At least in Gen III, not including the Safari Zone since that uses entirely different logic that I didn't want to implement.
