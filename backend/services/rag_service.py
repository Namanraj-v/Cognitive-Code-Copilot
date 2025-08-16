import os

def get_rag_context(smell: str) -> str:
    """Retrieves best practice text based on the identified code smell."""
    if not smell:
        return "General software engineering best practices recommend writing clean, readable, and maintainable code."

    filepath = os.path.join('backend', 'knowledge_base', f'{smell}.md')
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "No specific context found for this issue."