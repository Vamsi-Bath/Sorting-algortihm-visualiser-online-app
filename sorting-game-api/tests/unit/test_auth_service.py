import pytest
from fastapi import HTTPException
from app.auth import create_token, hash_password, read_token, verify_password


def test_password_hash_verifies_correct_password():
    stored = hash_password("Password123")
    assert verify_password("Password123", stored) is True


def test_password_hash_rejects_wrong_password_branch():
    stored = hash_password("Password123")
    assert verify_password("WrongPassword", stored) is False


def test_password_hash_rejects_bad_format_branch():
    assert verify_password("Password123", "not-a-real-hash") is False


def test_token_round_trip():
    token = create_token(123)
    assert read_token(token) == 123


def test_token_rejects_tampered_signature_branch():
    token = create_token(123)
    bad_token = token + "tampered"
    with pytest.raises(HTTPException):
        read_token(bad_token)
