
# Tetris in Python

This is a simple tetris game written in python using python arcade library. 
the aim of this project is to learn python and by having some fun. 

### Install poetry and dependencies

From the home directory of the project run `poetry install` to install the dependencies.

### Run the tests

 * `poetry run pytest` to run all tests in the project once. 
 * `poetry run ptw` to run all tests in the project and watch for changes.
 * `poetry run pytest --cov=pytetris --cov-branch tests/` to run all tests in the project and get a coverage report.
 * `poetry run pytest --cov=pytetris --cov-branch --cov-report html tests/` to run all tests in the project and get a coverage report in html format.

### Run the Game 

`poetry run python pytetris/tetris.py` 

### Run the tetrimino display

`poetry run python pytetris/tetrimino_display.py`
