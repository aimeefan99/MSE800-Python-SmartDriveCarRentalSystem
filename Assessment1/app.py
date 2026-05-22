"""
File: app.py
Purpose:
    Start the Assessment 1 Car Rental System from a single entry point.

Usage:
    Run this file in the terminal with:
    python3 app.py

Contents:
    - Finds the current project folder
    - Builds the database path
    - Starts the command-line interface

Author:
    fanfan

Change History:
    2026-05-13 - Created initial version for Assessment 1.
"""
# This file is intentionally left simple to avoid import issues when running the app.
from pathlib import Path
from cli import CarRentalCLI

# The main logic is contained in the cli module, and this script simply serves as the entry point to launch the application.
if __name__ == "__main__":
    # Get the directory of this script
    CURRENT_DIR = Path(__file__).resolve().parent 
    # Construct the path to the database file
    db_path = CURRENT_DIR / "data" / "car_rental.db" 
    # Create an instance of the CLI and run it
    CarRentalCLI(db_path).run() 
