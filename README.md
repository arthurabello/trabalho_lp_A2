# Warbound 🏹⚔️

*"If you know the enemy and know yourself, you need not fear the results of a hundred battles."*
*-Sun Tzu*

## Introduction
Warbound is a turn-based strategy game, developed with [Python](https://www.python.org/) and [Pygame](https://www.pygame.org/). The main purpose of this is to simulate how ancient battles would have been fought, strategically and tactically. The player is induced to think as a general, and make strategic decisions to avoid failing in battle.

## About the Game
In Warbound, players control armies with diverse unit types including infantry, cavalry, and archers. Each player chooses a historical general with unique abilities before the battle begins. The game's core mechanics involve:

- Strategic unit movement [(source)](https://github.com/arthurabello/warbound/blob/main/src/classes/units/base/unit_movement.py)
- Tactical formations [(source)](https://github.com/arthurabello/warbound/blob/main/src/classes/units/base/unit_formation.py)
- Unit orientation on the battlefield [(source)](https://github.com/arthurabello/warbound/blob/main/src/classes/units/base/unit_formation.py)
- Army management [(source)](https://github.com/arthurabello/warbound/blob/main/src/classes/units/base/unit_formation.py)
- Terrain-based advantages [(source)](https://github.com/arthurabello/warbound/blob/main/src/classes/units/base/unit_formation.py)
- Unit-specific combat abilities [(source)](https://github.com/arthurabello/warbound/blob/main/src/classes/unit_combat_mixin.py)
- General-specific advantages (and disadvantages) [(source)](https://github.com/arthurabello/warbound/blob/main/src/classes/unit_combat_mixin.py)
- Realistic combat mechanics, with a probabilistic system [(source)](https://github.com/arthurabello/warbound/blob/main/src/classes/unit_combat_mixin.py)

The game includes a comprehensive in-game [tutorial](https://github.com/arthurabello/warbound/blob/main/src/classes/menu/tutorial/tutorial_manager.py) for new players.

## Objective
The victory condition is to defeat the enemy by either eliminating their general or destroying their entire army.

## Preview
![Warbound](assets/images/game.png)

## How to run the game
1. Clone the repository:
   ```bash
   git clone https://github.com/arthurabello/trabalho_lp_A1.git
   cd trabalho_lp_A1
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate 
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the game::
   ```bash
   cd src
   python3 main.py

## Unit Tests
We used [unittest](https://docs.python.org/3/library/unittest.html) to test our scripts and ensure their functionality. To run the tests:

1. Navigate to the tests directory:
```bash
cd tests
```

2. Run the tests for each script:
```bash
python3 -m unittest test_graph.py
...
```

## Developers
This game was developed by:
- [Arthur Rabello](https://github.com/arthurabello)
- [Rodrigo Severo](https://github.com/rodrisevero)

## License
The game is licensed under the [GNU License](https://github.com/arthurabello/warbound/blob/main/LICENSE).