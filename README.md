# SFS Engine Calculator
A Python command line tool to tell you the best combination of engines for every stage of a given rocket in the game Spaceflight Simulator.

# Python version isn't yet functional or close to being such
Being worked on (hopefully still will be when you read this). In the meantime, the Scratch version works.

# Links
[Development Scratch version](https://scratch.mit.edu/projects/440582854), [TurboWarp](https://turbowarp.org/440582854) (I edit it there online and commit releases to this repo with changelogs, but that version works most of the time and can be run in-browser).

[Calculator wiki](https://github.com/DroneBetter/SFS_Engine_Calculator/wiki) (explains important spaceflight equations (most used in the calculator), isn't finished).

Play Spaceflight Simulator itself: [Android](https://play.google.com/store/apps/details?id=com.StefMorojna.SpaceflightSimulator), [iOS](https://apps.apple.com/us/app/spaceflight-simulator/id1308057272).

# What's the difference between the Python and Scratch version?
The Scratch one was initially going to be the only version, when I didn't know much about rocketry, but in making it I realised the most efficient engine combination for a stage isn't the best for the entire rocket, if a lighter one's reduced efficiency in its stage is outweighed by its increase to the efficiency of lower stages from its reduced mass. The Python version will account for this; instead of analysing combinations in a stage, it will analyse all combinations of combinations across all stages.

The Scratch version calculates delta-v (its metric for comparing combinations) with the [Tsiolkovsky rocket equation](https://en.wikipedia.org/wiki/Tsiolkovsky_rocket_equation) but with gravity, meaning it assumes gravity is constant throughout operation (but can much more efficiently find maximum liftoff mass and optimal fuel tank mass and delta-v). The Python one will use altitude to calculate gravity as it simulates the rocket's flight frame-by-frame (though a faster Tsiolkovsky option for orbital stages will be added).

# TODO
## Python
Make constants calculation work, make documentation (explain what every function and variable does, possibly disambiguate variable names in the process) and finish the frame-by-frame delta-v calculation and output display, make more (possibly all) functions use return() for their outputs to be cleaner and use fewer lists and allow more concise abstraction.

## Scratch
Re-add temporarily-removed things (like angle and percentage of fuel expected to be used, buttons currently ineffectual), add more threshold options with the other Tsiolkovsky-derived equations (ie. a toggle of whether to change fuel tank mass to a combination's optimal and treat the inputted fuel tank mass as a maximum instead of a given) and non-1.5 engine statistics (though most wiki pages are unclear about the exact versions of statistic changes) (will also be in toggling submenu).

Eventually add mouse-only navigation (for mobile users, because they can use the buttons with touchscreens and input numbers with on-screen keyboards but can't toggle graphing mode or do the calculation because they can't press G or space), potentially keyboard-only mode (with QWERTY physical key positions corresponding with button positions).
