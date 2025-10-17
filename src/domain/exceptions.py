"""Domain exceptions."""


class DomainException(Exception):
    """Base domain exception."""

    pass


class EntityNotFoundException(DomainException):
    """Entity not found exception."""

    def __init__(self, entity_name: str, entity_id: str) -> None:
        """Initialize exception."""
        self.entity_name = entity_name
        self.entity_id = entity_id
        super().__init__(f"{entity_name} with id {entity_id} not found")


class EntityAlreadyExistsException(DomainException):
    """Entity already exists exception."""

    def __init__(self, entity_name: str, field: str, value: str) -> None:
        """Initialize exception."""
        self.entity_name = entity_name
        self.field = field
        self.value = value
        super().__init__(
            f"{entity_name} with {field}={value} already exists"
        )


class ValidationException(DomainException):
    """Validation exception."""

    def __init__(self, message: str) -> None:
        """Initialize exception."""
        super().__init__(message)

