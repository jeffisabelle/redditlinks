try:
    # Import local settings to override existing values
    from settings_local import *  # noqa
except ImportError:
    from settings_default import *  # noqa
