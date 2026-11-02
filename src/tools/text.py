from pathlib import Path

_ESCAPE_MAP = (
    ("\\n", "\n"),
    ("\\t", "\t"),
    ("\\r", "\r"),
    ("\\b", "\b"),
    ("\\f", "\f"),
)

_HTML_ENTITIES = (
    ("&lt;", "<"),
    ("&gt;", ">"),
    ("&lpar;", "("),
    ("&rpar;", ")"),
    ("&amp;", "&"),
    ("&quot;", '"'),
    ("&apos;", "'"),
    ("&nbsp;", " "),
    ("&copy;", "©"),
    ("&reg;", "®"),
    ("&trade;", "™")
)

_MARKDOWN_SUFFIXES = {".md", ".markdown", ".mdx"}
_MARKUP_SUFFIXES = {".html", ".xml", ".xhtml", ".svg"}


def looks_like_escaped_source(text: str) -> bool:
    """True when the payload is one logical line stuffed with \\n sequences. """

    if "\\n" not in text:
        return False
    
    return text.count("\\n") >= 1


def normalized_source_text(text: str) -> str:
    """Turn double escaped new lines into real ones."""

    if not looks_like_escaped_source(text):
        return text

    normalized = text
    for escaped, raw in _ESCAPE_MAP:
        normalized = normalized.replace(escaped, raw)
    return normalized


def unespace_html_entities(text: str) -> str:
    """Unescape the HTML entities, for ex &gt to >"""
    if "&" not in text:
        return text

    normalized = text
    for html_entity, raw in _HTML_ENTITIES:
        normalized = normalized.replace(html_entity, raw)
    
    return normalized


def strip_markdown_fence(text: str) -> str:
    """Drop a wrapping ```lang... ```fence"""

    if "```" not in text:
        return text
    
    lines = text.split("\n")
    if lines and lines[0].lstrip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].rstrip().endswith("```"):
        lines = lines[:-1]
    return ("\n").join(lines)


def prepare_file_content(path: str, text: str) -> str:
    """
    Normalize a tool payload text into file bytes, independent of languages

    1. Normalize newlines/tabs
    2. Drop markdown fences
    3. Unescape HTML entities
    """
    suffix = Path(path).suffix.lower()
    prepared = normalized_source_text(text)
    if suffix not in _MARKDOWN_SUFFIXES:
        prepared = strip_markdown_fence(prepared)
    if suffix not in _MARKUP_SUFFIXES:
        prepared = unespace_html_entities(prepared)
        
    return prepared


