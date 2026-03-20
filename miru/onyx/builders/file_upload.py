"""Fluent builder for FileUpload components."""

from typing import Self
from miru.onyx.components.file_upload import FileUpload

__all__ = ["FileUploadBuilder"]


class FileUploadBuilder:
    """Fluent builder for FileUpload components."""

    def __init__(self) -> None:
        self._custom_id: str | None = None
        self._min_values: int = 1
        self._max_values: int = 1
        self._required: bool = True
        self._id: int | None = None

    def set_custom_id(self, custom_id: str) -> Self:
        self._custom_id = custom_id
        return self

    def set_min_values(self, min_values: int) -> Self:
        self._min_values = min_values
        return self

    def set_max_values(self, max_values: int) -> Self:
        self._max_values = max_values
        return self

    def set_required(self, required: bool) -> Self:
        self._required = required
        return self

    def set_id(self, id: int) -> Self:
        self._id = id
        return self

    def build(self) -> FileUpload:
        if self._custom_id is None:
            raise ValueError("custom_id is required")
        return FileUpload(
            custom_id=self._custom_id,
            min_values=self._min_values,
            max_values=self._max_values,
            required=self._required,
            id=self._id,
        )
