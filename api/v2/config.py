"""
    Define the configuration params for various environments
"""
import os


class DefaultConfig:
    """
        Base config class with all the common and default config
        values
    """
    SECRET_KEY = "this-is-obviously-not-a-secret"
    DEBUG = False
    CSRF_ENABLED = True
    TEST = False


class DevelopmentConfig(DefaultConfig):
    """
        Overrides some of the default params for development-specific
        configs
    """
    DEBUG = True


class TestingConfig(DefaultConfig):
    """
        Overrides some of the default params for development-specific
        configs
    """
    TEST = True
    DEBUG = True


CONFIGS = {
    'development_config': DevelopmentConfig,
    'testing_config': TestingConfig,
    'db_url': os.getenv("DATABASE_URL"),
    'test_db_url': os.getenv("TEST_DATABASE_URL")
}
