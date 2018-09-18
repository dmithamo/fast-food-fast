"""
    Define the configuration params for various environments
"""


class DefaultConfig:
    """
        Base config class with all the common and default config
        values
    """
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = 'i-will-amend-later-this-8888'
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
