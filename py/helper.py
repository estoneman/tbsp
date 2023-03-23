from dataclasses import dataclass

@dataclass
class AlgResponse:
    data: list[tuple]
    time_elapsed: float

