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
never tried in the game, this is the program to run.
