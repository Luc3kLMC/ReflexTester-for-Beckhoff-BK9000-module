*** Beckhoff module reflex game ***

1. INTRODUCTION

    Written when I was learning basics of communication with Beckhoff BK9000 module 
    in Python. 
    Because almost everything can be used to make a game, even if the simpliest one.

2. WHAT IS THIS DOING?

    In "Stoper version" module will turn on one of six coils randomly, then start counting time.
    Press corresponding number (1-6) on your keyboard to turn it off and Beckhoff will light on 
    aother one. After several tries you will be informed of your average response time.

    In "Speed version", after each correct button press, the module starts to light coils on 
    faster and faster. You lose when all lights are on (this version need some serious tweaking still).

3. REQUIREMENTS

    You need to have Beckhoff BK9000 and some (6 as for now) coils to switch. Module must be 
    configured first, I recommend using ARP table or using the defaults.
    Install pygame and pymodbus, update SERVER_HOST and SERVER_PORT to match your module settings.
    This should be enough.

Thanks for reading,
Luc3k