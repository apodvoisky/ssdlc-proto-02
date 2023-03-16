from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from typing import Optional, List, Set


class Customer:
    def __init__(self, first_name: str, sur_name: str, second_name: str, cell_phone: str, email: str):
        self.first_name = first_name
        self.sur_name = sur_name
        self.second_name = second_name
        self.cell_phone = cell_phone
        self.email = email