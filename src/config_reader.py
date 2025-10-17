from typing import Self
from pydantic import BaseModel, ValidationError, model_validator
from pydantic_extra_types.color import Color
import tomllib
import datetime
from enum import StrEnum, auto


class SpecialPageType(StrEnum):
    Title = auto()
    Blank = auto()
    Contents = auto()


class Impact(StrEnum):
    Critical = auto()
    High = auto()
    Medum = auto()
    Low = auto()
    Info = auto()


class SpecialPage(BaseModel):
    special_page_type: SpecialPageType


class MarkdownPage(BaseModel):
    text: str


class CVEVuln(BaseModel):
    id: str
    score: float
    desc: str
    impact: str
    affected_resources: str
    remidation: str
    cve_affected: str


class VulnPage(BaseModel):
    vuln: CVEVuln
    impact: int
    evidence: list[str]


class StyleConfig(BaseModel):
    bg_color: Color
    title_color: Color
    text_color: Color
    critical_color: Color
    high_color: Color
    medium_color: Color
    low_color: Color
    info_color: Color


class Page(BaseModel):
    markdown: MarkdownPage | None = None
    vuln: VulnPage | None = None
    special: SpecialPage | None = None

    @model_validator(mode="after")
    def check_at_least_one_field_used(self) -> Self:
        items = self.__dict__.items()

        null_fields = [field for field, value in items if value is None]
        if len(null_fields) != len(items) - 1:
            raise ValueError(f"You must have at least one active page type!")
        return self


class Config(BaseModel):
    org_name: str
    date: datetime.date
    style_config: StyleConfig
    page_order: list[str]
    pages: dict[str, Page]
    org_logo_path: str | None = None


# Creates a Config obj from a given filename by parsing the toml file.
def load_config_from_file(filename: str) -> Config:
    if ".toml" not in filename:
        raise ValueError("File must end in .toml")

    with open(filename, "rb") as file:
        toml = tomllib.load(file)
        try:
            m = Config.model_validate(toml)
            return m
        except ValidationError as e:
            print(e.errors())
