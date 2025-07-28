from src.applications.settings.settings import Config


def test_config_validation(local_config_app):
    """Test that Config properly validates and loads all required settings.

    Args:
        local_config_app: Fixture providing application configuration for
        testing.
    """
    config = Config(**local_config_app)
    assert config.url_prefix.startswith("/")
    assert config.logger is not None
    assert config.aws is not None
    assert config.account_id
    assert config.sns_error_arn
    assert config.rds_secret
    assert config.openai_secret
    assert config.jwt_secret
