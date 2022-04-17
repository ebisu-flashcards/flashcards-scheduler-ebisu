from typing import Any
from datetime import datetime

from ebisu import updateRecall as ebisu_update, predictRecall as ebisu_predict
from sqlalchemy.orm import Session

from flashcards_core.errors import NoCardsToStudyException
from flashcards_core.schedulers import BaseScheduler
from flashcards_core.database import Deck, Card

from flashcards_scheduler_ebisu.data_model import get_prior, update_prior


class EbisuScheduler(BaseScheduler):

    def __init__(self, session: Session, deck: Deck):
        super().__init__(session=session, deck=deck)

    def next_card(self) -> Card:
        """
        :return: the next card to review
        """
        try:
            return sorted(self.deck.cards, key=lambda card: ebisu_predict(get_prior(card)), reverse=True)[0]
        except KeyError:
            return NoCardsToStudyException("Seems like you have no cards to study.")

    def process_test_result(self, card: Card, result: bool):
        """
        Creates a Review for the card, storing the test result.

        :param card: the card that was reviewed
        :param result: the results of the test
        :return: None
        """
        update_prior(card=card, new_prior=ebisu_update(prior=get_prior(card), success=1 if result else 0, total=1, tnow=datetime.now()))