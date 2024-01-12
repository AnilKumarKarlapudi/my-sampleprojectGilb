# Errors
class ResolverError(Exception):
    pass


class MissingResolverError(ResolverError):
    pass


class CannotBeResolvedError(ResolverError):
    def __init__(self, name: str):
        super().__init__(f"Cannot be resolved: {name}")


class UnrecognizedConfigurationError(ResolverError):
    def __init__(self, name: str):
        super().__init__(f"Unrecognized configuration: {name}")


class SkipConfiguration(RuntimeError):
    pass
