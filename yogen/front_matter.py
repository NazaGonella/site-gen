from pathlib import Path
from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import date as Date

class FrontMatter(BaseModel):
    model_config = ConfigDict(extra="allow")

    title : str | None = None
    authors : list[str] = Field(default_factory=list)
    date : Date = Field(default_factory=Date.today)
    template : Path | None = None
    section : str = "global"
    tags: list[str] = Field(default_factory=list)

    @field_validator("authors", mode="before")
    @classmethod
    def normalize_authors(cls, v):
        if isinstance(v, str):
            return [v]
        return v

    @field_validator("date", mode="before")
    @classmethod
    def normalize_date(cls, v):
        if v is None:
            return Date.today()

        try:
            return Date.fromisoformat(v) if isinstance(v, str) else v
        except Exception:
            return Date.today()

    @field_validator("tags", mode="before")
    @classmethod
    def normalize_tags(cls, v):
        if isinstance(v, str):
            return [v]
        return v
