from dataclasses import dataclass
from environs import Env


@dataclass
class Config:
    token: str
    interests: list


def load_config(path: str) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        token=env.str('TOKEN'),
        interests=env.str('INTERESTS').split(',')
    )
