from dataclasses import dataclass


@dataclass
class SearchQuery:
    tags_positional: list[str]
    tags_keywords: dict
