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
