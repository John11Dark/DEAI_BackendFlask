#!/bin/bash

# ? *--> Creating virtual environment
python3 -m venv myenv
source myenv/bin/activate

# ? *--> Installing dependencies
pip install -r requirements.txt

# ? *--> Run the main script
python main.py