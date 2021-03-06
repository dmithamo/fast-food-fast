"""
    Define the configuration params for various environments
"""
import os


class DefaultConfig:
    """
        Base config class with all the common and default config
        values
    """
    SECRET_KEY = os.getenv('SECRET_KEY')
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


CONFIGS = {
    'development_config': DevelopmentConfig,
    'testing_config': TestingConfig
}
