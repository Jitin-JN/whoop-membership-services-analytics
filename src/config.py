from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    seed: int = 42

    # Scale
    n_members: int = 200_000
    n_tickets: int = 10_000

    # Date ranges
    signup_start: str = "2022-01-01"
    signup_end: str = "2024-12-31"
    ticket_start: str = "2024-01-01"
    ticket_end: str = "2024-12-31"

    today: str = "2025-01-01"