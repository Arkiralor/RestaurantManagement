#!/bin/bash
python -m pip install pip-tools
pip-compile --resolver=backtracking --output-file=requirements.dev.txt requirements.dev.in
python -m pip install -r requirements.dev.txt