from datetime import datetime
from typing import List
from api_to_dataframe import ClientBuilder, RetryStrategies

from currency_quote.application.ports.outbound.currency_repository import (
    ICurrencyRepository,
)
from currency_quote.config.endpoints import API
from currency_quote.domain.entities.currency import CurrencyQuote, CurrencyObject
from currency_quote.utils.open_observability import inject_context_into_headers, trace_span


class CurrencyAPI(ICurrencyRepository):
    def __init__(self, currency_obj: CurrencyObject):
        self.currency_list = currency_obj.get_currency_list()

    @trace_span
    def get_last_quote(self) -> List[CurrencyQuote]:
        url = f"{API.ENDPOINT_LAST_COTATION}{','.join(self.currency_list)}"
        headers = {}
        inject_context_into_headers(headers)
        
        client = ClientBuilder(
            endpoint=url, 
            retry_strategy=RetryStrategies.EXPONENTIAL_RETRY_STRATEGY,
            headers=headers
        )

        response = client.get_api_data()

        quote_list = []

        for item in self.currency_list:
            parsed_item = item.replace("-", "")
            currency_quote = CurrencyQuote(
                currency_pair=item,
                currency_pair_name=response[parsed_item]["name"],
                base_currency_code=response[parsed_item]["code"],
                quote_currency_code=response[parsed_item]["codein"],
                quote_timestamp=int(response[parsed_item]["timestamp"]),
                bid_price=response[parsed_item]["bid"],
                ask_price=response[parsed_item]["ask"],
            )

            quote_list.append(currency_quote)

        return quote_list

    @trace_span
    def get_history_quote(self, reference_date: int) -> List[CurrencyQuote]:
        today = int(datetime.today().strftime("%Y%m%d"))

        if (
            reference_date > today
            or reference_date == today
            or len(str(reference_date)) != 8
        ):
            print("[currency-quote] Invalid reference date")
            return []

        quote_list = []

        for item in self.currency_list:
            url = (
                f"{API.ENDPOINT_HISTORY_COTATION}{item}"
                f"?start_date={reference_date}&end_date={reference_date}"
            )

            headers = {}
            inject_context_into_headers(headers)
            
            client = ClientBuilder(
                endpoint=url, 
                retry_strategy=RetryStrategies.EXPONENTIAL_RETRY_STRATEGY,
                headers=headers
            )

            response = client.get_api_data()

            currency_quote = CurrencyQuote(
                currency_pair=item,
                currency_pair_name=response[0]["name"],
                base_currency_code=response[0]["code"],
                quote_currency_code=response[0]["codein"],
                quote_timestamp=int(response[0]["timestamp"]),
                bid_price=float(response[0]["bid"]),
                ask_price=float(response[0]["ask"]),
            )

            quote_list.append(currency_quote)

        return quote_list
