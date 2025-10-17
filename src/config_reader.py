from dataclasses import dataclass
from dataclass_binder import Binder
import tomllib as toml
import datetime
from enum import Enum, auto
from typing import final


@dataclass()
class StyleConfig:
    bg_color: str
    title_color: str
    text_color: str
    critical_color: str
    high_color: str
    medium_color: str
    low_color: str
    info_color: str


@dataclass
class Config:
    org_name: str
    org_logo_path: str | None
    date: datetime.date
    style_config: StyleConfig


@dataclass
class Page:
    pass


class SpecialPageType(Enum):
    Title = auto()
    Blank = auto()
    Contents = auto()


class Impact(Enum):
    Critical = auto()
    High = auto()
    Medum = auto()
    Low = auto()
    Info = auto()


@dataclass
class Specialpage:
    special_page_type: SpecialPageType


@dataclass
class MarkdownPage(Page):
    text: str


@dataclass
class CVEVuln:
    id: str
    score: float
    desc: str
    impact: str
    affected_resources: str
    remidation: str
    cve_affected: str


@dataclass
class VulnPage(Page):
    vuln: CVEVuln
    impact: Impact
    evidence: list[str]


# Creates a Config obj from a given filename by parsing the toml file.
def load_config_from_file(filename: str) -> Config:
    if ".toml" not in filename:
        raise ValueError("File must end in .toml")
    binder = Binder(Config)
    config = binder.parse_toml(filename)
    return config
