#! /bin/bash

rm dist/*
echo '[]' > space_escape/data/highscores.json
.venv/bin/python setup.py sdist bdist_wheel
.venv/bin/python -m twine upload dist/*
