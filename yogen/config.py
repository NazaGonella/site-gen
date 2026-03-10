import tomllib
from pathlib import Path
from pydantic import BaseModel, Field


class Paths(BaseModel):
    static : str
    content : str
    templates : str
    build : str

class Author(BaseModel):
    name : str
    email : str

class Site(BaseModel):
    title : str
    description : str
    base_url : str
    languages : list[str]
    authors : list[Author]

class Deploy(BaseModel):
    page_repo : str = Field(min_length=1)
    remote : str = Field(min_length=1)

class Feed(BaseModel):
    title : str
    subtitle : str
    icon : str | None = None
    output : str
    sections : list[str] = []
    tags : list[str] = []

class Config(BaseModel):
    paths : Paths
    site : Site
    deploy : Deploy
    feed : Feed | None = None


def load_config(path : Path) -> Config:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    if not path.is_file():
        raise ValueError(f"Expected a file, got: {path}")

    with path.open("rb") as f:
        data = tomllib.load(f)

    return Config(**data)
