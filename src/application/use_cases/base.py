"""Base use case."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

InputDTO = TypeVar("InputDTO")
OutputDTO = TypeVar("OutputDTO")


class BaseUseCase(ABC, Generic[InputDTO, OutputDTO]):
    """Base use case interface."""

    @abstractmethod
    async def execute(self, input_dto: InputDTO) -> OutputDTO:
        """Execute the use case."""
        pass

