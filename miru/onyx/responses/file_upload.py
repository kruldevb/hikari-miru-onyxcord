"""Response data for FileUpload component."""

from dataclasses import dataclass
from typing import Literal

__all__ = ["FileUploadResponse", "AttachmentData"]


@dataclass
class AttachmentData:
    """Represents an uploaded file attachment.

    Attributes
    ----------
    id : str
        Snowflake ID of the attachment
    filename : str
        Name of the file
    size : int
        Size of the file in bytes
    url : str
        URL to download the file
    proxy_url : str
        Proxied URL to download the file
    content_type : str | None
        MIME type of the file
    """

    id: str
    filename: str
    size: int
    url: str
    proxy_url: str
    content_type: str | None = None


@dataclass
class FileUploadResponse:
    """Response data for FileUpload component.

    Attributes
    ----------
    id : int
        Component ID assigned by Discord
    custom_id : str
        Custom identifier for the component
    values : list[str]
        List of snowflake IDs of uploaded files
    attachments : list[AttachmentData]
        Resolved attachment objects with URLs and metadata
    type : Literal[19]
        Component type (always 19)
    """

    id: int
    custom_id: str
    values: list[str]
    attachments: list[AttachmentData]
    type: Literal[19] = 19
