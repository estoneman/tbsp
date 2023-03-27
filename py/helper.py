from dataclasses import dataclass

@dataclass
class PairsResponse:
    data: list[tuple]
    time_elapsed: float

@dataclass
class TopKResponse:
    topk_domains: list[tuple]
    mean: float

