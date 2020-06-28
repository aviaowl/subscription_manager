CURRENCIES = ("USD", "GBP", "EUR", "RUB", "CNY")
FREQUENCIES = ("daily", "weekly", "monthly", "yearly")
DEFAULT_COLLECTION_NAME = "subscriptions"

"""Application messages"""
EMPTY_FIELD_MSG = "Field length should be more than one"
WRONG_TYPE_MSG = "Found wrong field type, expected: {expected}, received: {{{recieved_type}, {field}}}"
FUTURE_START_DATE_MSG = "Start dates in the future are not supported"
UNEXPECTED_FREQUENCY_MSG = (
    "Unexpected frequency: {frequency}, supported frequencies: " + " ".join(FREQUENCIES)
)
UNEXPECTED_CURRENCY_MSG = (
    "Unexpected currency: {currency}, supported currencies: " + " ".join(CURRENCIES)
)
MISSING_FIELDS_MSG = "Some fields in the taken subscription are missing"
