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
import sys
from cli import CarRentalCLI


def _project_root() -> Path:
    """Return the folder that should hold the writable data directory."""

    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


# The main logic is contained in the cli module, and this script simply serves as the entry point to launch the application.
if __name__ == "__main__":
    current_dir = _project_root()
    db_path = current_dir / "data" / "car_rental.db"
    CarRentalCLI(db_path).run()
