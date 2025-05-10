def hello_world(name: str = "world") -> None:
    """Prints a greeting message.
    Args:
        name: Name to greet (default: world)
    """
    print(f"Hello, {name}!")  # noqa: T201
