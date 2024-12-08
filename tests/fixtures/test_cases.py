from contextlib import nullcontext as does_not_raise

import pytest
from fastapi import HTTPException

# url, params, expected_status_code, expected_payload, expectation
PARAMS_TEST_TRADING_DATES_HANDLER = [
    # positive case with custom params
    (
        "/v1/instrument/get_last_trading_days",
        {"num_dates": 5},
        200,
        [
            {"date": "2024-02-20"},
            {"date": "2024-02-19"},
            {"date": "2024-02-18"},
            {"date": "2024-02-17"},
            {"date": "2024-02-16"},
        ],
        does_not_raise(),
    ),
    # no input case
    (
        "/v1/instrument/get_last_trading_days",
        {},
        422,
        {
            "detail": [
                {
                    "input": None,
                    "loc": ["query", "num_dates"],
                    "msg": "Field required",
                    "type": "missing",
                }
            ]
        },
        does_not_raise(),
    ),
    # negative case with num_dates less than 1
    (
        "v1/instrument/get_last_trading_days",
        {"num_dates": -5},
        400,
        {"detail": "Number of days must be a positive integer"},
        pytest.raises(HTTPException),
    ),
]

# url, params, expected_status_code, expectation
PARAMS_TEST_DYNAMICS_HANDLER = [
    # positive case with custom params
    (
        "v1/instrument/get_dynamics",
        {
            "oil_id": "A10K",
            "delivery_type_id": "W",
            "delivery_basis_id": "ZLY",
            "start_date": "2024-02-10",
            "end_date": "2024-02-11",
        },
        200,
        does_not_raise(),
    ),
    # negative case with no params
    (
        "v1/instrument/get_dynamics",
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["query", "start_date"],
                    "msg": "Field required",
                    "input": "{}",
                },
                {
                    "type": "missing",
                    "loc": ["query", "end_date"],
                    "msg": "Field required",
                    "input": "{}",
                },
            ]
        },
        422,
        does_not_raise(),
    ),
    # negative case without params
    ("v1/instrument/get_dynamics", {}, 422, does_not_raise()),
    # negative case with start_date greater than end_date
    (
        "v1/instrument/get_dynamics",
        {
            "oil_id": "A10K",
            "delivery_type_id": "W",
            "delivery_basis_id": "ZLY",
            "start_date": "2024-02-12",
            "end_date": "2024-02-11",
        },
        422,
        does_not_raise(),
    ),
]

# url, params, expected_status_code, expectation
PARAMS_TEST_TRADING_RESULTS_HANDLER = [
    # positive case with custom params
    (
        "v1/instrument/get_trading_results",
        {
            "oil_id": "A10K",
            "delivery_type_id": "W",
            "delivery_basis_id": "ZLY",
        },
        200,
        does_not_raise(),
    ),
    # positive case with default params
    ("v1/instrument/get_trading_results", {}, 200, does_not_raise()),
]
