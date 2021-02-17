# SFS_Engine_Calculator
A Python command line tool to tell you the best combination of engines for every stage of a given rocket in the game Spaceflight Simulator.

# Python version isn't yet functional or close to being such
Being worked on (hopefully still will be when you read this). In the meantime, the Scratch version works.

# Links
[Development Scratch version](https://scratch.mit.edu/projects/440582854), [TurboWarp](https://turbowarp.org/440582854) (I edit it there online and commit releases to this repo with changelogs, but that version works most of the time and can be run in-browser).
[Wiki](https://github.com/DroneBetter/SFS_Engine_Calculator/wiki) (explains some equations used, isn't finished).
Play Spaceflight Simulator itself: [Android](https://play.google.com/store/apps/details?id=com.StefMorojna.SpaceflightSimulator), [iOS](https://apps.apple.com/us/app/spaceflight-simulator/id1308057272).

# TODO
## Python
Make constants calculation work, make documentation (explain what every function and variable does, possibly disambiguate variable names in the process), clean up earlier functions (ie. findCombinations()) and finish the delta-v calculation and output display, eventually make most functions use return() to be cleaner and use fewer lists.

## Scratch
Add sub-menu system for >15 buttons (ie. a 'Thresholds' button for minimum TWR and maximum consumption and mass, possibly add pruning toggle there (not enabled by default because a combination could be pruned because it's inferior to another which doesn't fit in the given area)). I like graphing having its own row in the main menu as an indicator when enabled, though, will keep it.

Add option for whether craft lifts off from the ground or the air. If it's from the ground, use optimal fuel mass instead of actual if it's lower than actual (because all fuel above optimal will be burned while stationary). (Option only applies if gravity > 0, otherwise hide option when inapplicable (also make minimum TWR hide at 0 gravity).)

Make optimal fuel mass equation also account for fuel tank mass only being 90% fuel.

Eventually add mouse-only navigation (for mobile users, because they can use the buttons and input parameters with on-screen keyboards but can't toggle graphing mode or do the calculation because they can't press G or space).
