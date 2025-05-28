import pandas as pd
import pytest

from src.utils.xlsx_reader import load_transactions


def test_load_transactions():
    df = load_transactions("data/operations.xlsx")
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
