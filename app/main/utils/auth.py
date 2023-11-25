from typing import Optional

from flask import Request


def get_bearer_token(request: Request) -> Optional[str]:
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return

    header_parts = auth_header.split()

    if len(header_parts) != 2:
        return

    return header_parts[1]
