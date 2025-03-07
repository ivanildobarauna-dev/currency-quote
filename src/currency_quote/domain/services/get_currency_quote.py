from typing import Type, List
from currency_quote.application.ports.outbound.currency_repository import (
    ICurrencyRepository,
)
from currency_quote.application.use_cases.validate_currency import (
    ValidateCurrencyUseCase,
)
from currency_quote.domain.entities.currency import CurrencyQuote, CurrencyObject
from currency_quote.utils.open_observability import increment_metric


class GetCurrencyQuoteService:
    def __init__(
        self, currency: CurrencyObject, currency_repository: Type[ICurrencyRepository]
    ):
        self.currency = currency
        self.currency_repository = currency_repository

    @increment_metric
    def last(self) -> List[CurrencyQuote]:
        valid_currency = self.validate_currency_code()
        last_quote = self.currency_repository(valid_currency).get_last_quote()
        return last_quote

    @increment_metric
    def history(self, reference_date: int) -> List[CurrencyQuote]:
        return self.currency_repository(
            self.validate_currency_code()
        ).get_history_quote(reference_date=reference_date)

    @increment_metric
    def validate_currency_code(self) -> CurrencyObject:
        currency_valid_obj = ValidateCurrencyUseCase.execute(self.currency)
        return currency_valid_obj
