from src.infraestructure.driven_adapters.sns_repository.error.\
    sns_repository_error import SnsRepositoryError


def test_sns_repository_error_with_message():
    """Test SnsRepositoryError with a custom message."""
    error = SnsRepositoryError(message="Custom error message")
    assert str(error) == "[Model Error] Custom error message"


def test_sns_repository_error_without_message():
    """Test SnsRepositoryError without a custom message."""
    error = SnsRepositoryError()
    assert str(error) == "[Model Error] No details."
