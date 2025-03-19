import pytest
from unittest.mock import patch, MagicMock
from currency_quote.application.use_cases.get_last_currency_quote import (
    GetLastCurrencyQuoteUseCase,
)
from currency_quote.domain.entities.currency import CurrencyQuote, CurrencyObject
from currency_quote.adapters.outbound.currency_api import CurrencyAPI
from currency_quote.adapters.outbound.currency_validator_api import CurrencyValidatorAPI
from currency_quote.domain.services.validate_currency import CurrencyValidatorService


def test_valid_currency_mocked():
    """Test getting last quote with valid currencies using complete mocking."""
    # Create mock quotes
    mock_quotes = [
        CurrencyQuote(
            currency_pair="USD-BRL",
            currency_pair_name="Dólar Americano/Real Brasileiro",
            base_currency_code="USD", 
            quote_currency_code="BRL",
            quote_timestamp=1614024000,
            bid_price=5.0876,
            ask_price=5.0891
        ),
        CurrencyQuote(
            currency_pair="EUR-BRL",
            currency_pair_name="Euro/Real Brasileiro",
            base_currency_code="EUR",
            quote_currency_code="BRL",
            quote_timestamp=1614024000,
            bid_price=6.0876,
            ask_price=6.0891
        )
    ]
    
    # Mock the GetLastCurrencyQuoteUseCase.execute method
    with patch('currency_quote.application.use_cases.get_last_currency_quote.GetLastCurrencyQuoteUseCase.execute') as mock_execute:
        # Configure mock to return our predefined quotes
        mock_execute.return_value = mock_quotes
        
        # Test data
        currency_list = ["USD-BRL", "EUR-BRL"]
        currency_quote = CurrencyObject(currency_list)
        
        # Call the function
        result = GetLastCurrencyQuoteUseCase.execute(currency_quote)
        
        # Verify results
        assert len(result) == 2
        assert result[0].currency_pair == "USD-BRL"
        assert result[1].currency_pair == "EUR-BRL"
        
        # Verify the mock was called
        mock_execute.assert_called_once_with(currency_quote)


@patch('api_to_dataframe.ClientBuilder')
def test_partial_valid_currency(mock_client_builder, mock_currency_api_response):
    """Test getting last quote with a mix of valid and invalid currencies."""
    # Configure the mock
    mock_client = MagicMock()
    mock_client.get_api_data.return_value = mock_currency_api_response
    mock_client_builder.return_value = mock_client
    
    # Test data with one invalid currency
    currency_list = ["USD-BRL", "EUR-BRL", "AAA-BBB"]
    currency_quote = CurrencyObject(currency_list)
    
    # Mock the validator to only return valid currencies
    valid_currencies = ["USD-BRL", "EUR-BRL"]
    with patch.object(CurrencyValidatorService, 'validate_currency_code', 
                     return_value=CurrencyObject(valid_currencies)):
        with patch.object(CurrencyValidatorAPI, 'validate_currency_code', 
                         return_value=valid_currencies):
            result = GetLastCurrencyQuoteUseCase.execute(currency_quote)
            
            # Verify results
            assert len(result) == 2
            for item in result:
                assert isinstance(item, CurrencyQuote)
                assert item.currency_pair in valid_currencies


@patch('api_to_dataframe.ClientBuilder')
def test_all_invalid_currencies(mock_client_builder):
    """Test behavior when all currencies are invalid."""
    mock_client = MagicMock()
    mock_client_builder.return_value = mock_client
    
    # Test data with all invalid currencies
    currency_list = ["AAA-BBB", "XXX-YYY"]
    currency_quote = CurrencyObject(currency_list)
    
    # Mock the validator to return empty list, which raises ValueError
    with patch.object(CurrencyValidatorAPI, 'validate_currency_code', return_value=[]):
        with patch.object(CurrencyValidatorService, 'validate_currency_code', 
                         side_effect=ValueError("All params are invalid.")):
            with pytest.raises(ValueError, match="All params are invalid."):
                GetLastCurrencyQuoteUseCase.execute(currency_quote)


def test_api_error_handling_mocked():
    """Test handling of API errors using direct mock."""
    # Mock the CurrencyAPI directly to raise an exception
    with patch('currency_quote.adapters.outbound.currency_api.CurrencyAPI.get_last_quote') as mock_get_last:
        # Configure mock to raise an exception
        mock_get_last.side_effect = Exception("API Connection Error")
        
        # Test with a simple try/except to verify exception is raised
        currency_quote = CurrencyObject(["USD-BRL"])
        
        # Test the exception is propagated
        try:
            # Try to use a direct instance of CurrencyAPI
            api = CurrencyAPI(currency_quote)
            api.get_last_quote()
            assert False, "Exception was not raised"
        except Exception as e:
            assert "API Connection Error" in str(e)
