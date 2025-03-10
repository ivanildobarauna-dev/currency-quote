# src/currency_quote/adapters/outbound/currency_validator_api.py
from api_to_dataframe import ClientBuilder, RetryStrategies
from currency_quote.config.endpoints import API
from currency_quote.application.ports.outbound.currency_validator_repository import (
    ICurrencyValidator,
)
from currency_quote.domain.entities.currency import CurrencyObject
from currency_quote.utils.open_observability import inject_context_into_headers, trace_span


class CurrencyValidatorAPI(ICurrencyValidator):
    def __init__(self, currency_quote: CurrencyObject) -> None:
        self.currency_quote = currency_quote

    @trace_span
    def validate_currency_code(self) -> list:
        headers = {}
        inject_context_into_headers(headers)
        
        client = ClientBuilder(
            endpoint=API.ENDPOINT_AVALIABLE_PARITIES,
            retry_strategy=RetryStrategies.LINEAR_RETRY_STRATEGY,
            headers=headers
        )

        valid_list = client.get_api_data()

        validated_list = []

        for currency_code in self.currency_quote.get_currency_list():
            if currency_code in valid_list:
                validated_list.append(currency_code)

        return validated_list
