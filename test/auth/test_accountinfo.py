"""
    Tests for the AccountInfo module
"""
import pytest
from factiva.analytics import AccountInfo
from factiva.analytics.common import config

GITHUB_CI = config.load_environment_value('CI', False)
FACTIVA_USERKEY = config.load_environment_value("FACTIVA_USERKEY")
DUMMY_KEY = 'abcd1234abcd1234abcd1234abcd1234'

# API Response sample with the most complete set of attributes
# {
#     "data": {
#         "id": "abcd1234abcd1234abcd1234abcd1234",
#         "attributes": {
#             "cnt_curr_ext": 1,
#             "current_downloaded_amount": 427567508,
#             "max_allowed_concurrent_extracts": 10,
#             "max_allowed_document_extracts": 2500000,
#             "max_allowed_extracts": 5,
#             "name": "Company Corp",
#             "products": "DNA",
#             "tot_document_extracts": 1595383,
#             "tot_extracts": 4,
#             "tot_subscriptions": 0,
#             "tot_topics": 0,
#             "licensed_company_ids": [
#                 4,
#                 3,
#                 1,
#                 5
#             ],
#             "enabled_company_identifiers": [
#                 {
#                     "id": 4,
#                     "name": "isin"
#                 },
#                 {
#                     "id": 3,
#                     "name": "cusip"
#                 },
#                 {
#                     "id": 1,
#                     "name": "sedol"
#                 },
#                 {
#                     "id": 5,
#                     "name": "ticker_exchange"
#                 }
#             ]
#         },
#         "type": "account_with_contract_limits"
#     }
# }


def _test_userkey_types(usr):
    """"
    Checks the correct types were returned.
    """
    if isinstance(usr, str):
        usr = AccountInfo(stats=True)
    assert isinstance(usr.user_key.key, str)
    assert isinstance(usr.user_key.cloud_token, dict)
    assert isinstance(usr.account_name, str)
    assert isinstance(usr.active_product, str)
    assert isinstance(usr.max_allowed_concurrent_extractions, int)
    assert isinstance(usr.max_allowed_extracted_documents, int)
    assert isinstance(usr.max_allowed_extractions, int)
    assert isinstance(usr.remaining_documents, int)
    assert isinstance(usr.remaining_extractions, int)
    assert isinstance(usr.total_downloaded_bytes, int)
    assert isinstance(usr.total_extracted_documents, int)
    assert isinstance(usr.total_extractions, int)
    assert isinstance(usr.total_stream_instances, int)
    assert isinstance(usr.total_stream_subscriptions, int)
    assert isinstance(usr.enabled_company_identifiers, list)
    # Assert streams
    # Assert extractions


def _test_userkey_values(usr):
    """
    Checks if values within the expected lengths and ranges
    were returned
    """
    if isinstance(usr, str):
        usr = AccountInfo(stats=True)
    assert usr.user_key.key == FACTIVA_USERKEY
    assert len(usr.account_name) >= 0
    assert len(usr.active_product) >= 0
    assert usr.max_allowed_concurrent_extractions >= 0
    assert usr.max_allowed_extracted_documents >= 0
    assert usr.max_allowed_extractions >= 0
    assert usr.total_downloaded_bytes >= 0
    assert usr.total_extracted_documents >= 0
    assert usr.total_extractions >= 0
    assert usr.total_stream_instances >= 0
    assert usr.total_stream_subscriptions >= 0
    assert len(usr.enabled_company_identifiers) >= 0

def test_invalid_key():
    """
    Creates an object from the provided string and request the usage details to the API service
    The key is invalid and this should validate how the error is processed
    """
    with pytest.raises(ValueError, match=r'Factiva User-Key does not exist or inactive.'):
        AccountInfo(DUMMY_KEY)


def test_invald_lenght_key():
    """
    Attempts to create an object with malformed keys. This requires assert the raised exception.
    """
    with pytest.raises(ValueError, match=r'Factiva User-Key has the wrong length'):
        AccountInfo('abc')

def test_userkey_with_stats():
    """"
    Creates the object using the ENV variable and request the usage details to the API service
    """
    if GITHUB_CI:
        pytest.skip("Not to be tested in GitHub Actions")
    usr = AccountInfo()
    _test_userkey_types(usr)
    _test_userkey_values(usr)


def test_user_with_parameter_and_stats():
    """
    API Key is passed as a string
    """
    if GITHUB_CI:
        pytest.skip("Not to be tested in GitHub Actions")
    usr = AccountInfo(FACTIVA_USERKEY)
    _test_userkey_types(usr)
    _test_userkey_values(usr)



