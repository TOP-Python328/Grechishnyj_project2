from core.kind import Kind, MaturePhase, Creature
from core.parameters import *
from core.actions import *  

cube = Kind(
    'Кубик', 
    MaturePhase(
        5, 
        Parameters(Health).value(50, 0, 50),
        Parameters(Satiety).value(50, 0, 50),
        Parameters(Fatigue).value(50, 0, 50),
        Parameters(Hygiene).value(50, 0, 50),
        Parameters(Mood).value(50, 0, 50),
        Parameters(Stamina).value(50, 0, 50),
        player_actions=[
            Feed(3)
        ],
        creature_actions=[
            ChaseTail(0.7),
        ]
    ),
    MaturePhase(
        20,
        Parameters(Health).value(0, 0, 75),
        Parameters(Satiety).value(0, 0, 75),
        Parameters(Fatigue).value(0, 0, 75),
        Parameters(Hygiene).value(0, 0, 75),
        Parameters(Mood).value(0, 0, 75),
        Parameters(Stamina).value(0, 0, 75),
        player_actions=[
            Feed(5)
        ],
        creature_actions=[
            ChaseTail(0.1),
        ]
    ), 
    MaturePhase(
        50, 
        Parameters(Health).value(0, 0, 100),
        Parameters(Satiety).value(0, 0, 100),
        Parameters(Fatigue).value(0, 0, 100),
        Parameters(Hygiene).value(0, 0, 100),
        Parameters(Mood).value(0, 0, 100),
        Parameters(Stamina).value(0, 0, 100),
        player_actions=[
            Feed(7)
        ],
        creature_actions=[]
    )
)
