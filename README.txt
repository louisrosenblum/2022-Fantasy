---------------------------------------------------------------------------------------
Root directory is for flex players

Qb directory is for QBs

Advanced directory includes advanced stats but reduces sample years to 2018-present

---------------------------------------------------------------------------------------

Running main.py will generate a csv named 'flex.csv' or 'qb.csv'

Train and test data is stored in 'test.csv' and 'train.csv'

Feature coefficients are stored in 'coefficients.csv'

---------------------------------------------------------------------------------------

Set scoring settings in main.py:

FLEX
-----------------------------------
ppr = 1 # Points per reception
ppfd = 0 # Pointers per first down

QB
-----------------------------------
ppptd = 6 # Points per passing touchdown

---------------------------------------------------------------------------------------
Stats scraped from PFR (https://www.pro-football-reference.com/)