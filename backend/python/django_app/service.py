def generate_greetings(name):
    """
    A simple service function that generates a greeting message.
    """
    if not name:
        name = "World"
    return f"Hello, {name}!"