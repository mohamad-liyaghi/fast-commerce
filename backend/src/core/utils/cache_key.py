async def format_key(key: str, **kwargs) -> str:
    """
    Generate a cache key and format with params
    """
    return key.format(**kwargs)
