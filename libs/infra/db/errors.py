from typing import Optional


class SQLError(Exception):
    """
    SQL Error base exception
    """

    def __init__(self, message: Optional[str] = None):
        super().__init__(message)


class SQLModelError(SQLError):
    """
    SQL Model error
    """

    pass


class CannotResolveStatementError(SQLError):
    """
    Cannot Resolve Query Error
    """

    pass


class UnsupportedPythonTypeForFieldError(SQLModelError):
    """
    Unsupported Python Type For Field Error
    """

    pass


class FieldNotMappedWithColumnError(SQLModelError):
    """
    Field Not Mapped With Column Error
    """

    pass
