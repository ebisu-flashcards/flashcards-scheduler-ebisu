from collections import namedtuple

from flashcards_core.database import Card


EbisuPrior = namedtuple("EbisuPrior", ["alpha", "beta", "t"])


def get_prior(card: Card):
    pass

def update_prior(card: Card, new_prior: EbisuPrior):
    pass


