from __future__ import annotations

import warnings

import requests
import wikipedia
from bs4 import GuessedAtParserWarning

warnings.filterwarnings("ignore", category=GuessedAtParserWarning, module="wikipedia")

COMMON_TOPIC_ALIASES = {
    "ai": "artificial intelligence",
    "ml": "machine learning",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "llm": "large language model",
}


def _extract_topic(query: str) -> str:
    cleaned = query.strip()
    lowered = cleaned.lower()
    for prefix in ("who is", "what is", "tell me about", "wikipedia", "wiki"):
        if lowered.startswith(prefix):
            return cleaned[len(prefix):].strip(" ?")
    return cleaned.strip(" ?")


def _normalize_topic(topic: str) -> str:
    lowered = topic.strip().lower()
    return COMMON_TOPIC_ALIASES.get(lowered, topic.strip())


def _resolve_topic(topic: str) -> str:
    normalized = _normalize_topic(topic)

    if normalized != topic:
        return normalized

    if topic.isupper() and len(topic) <= 5:
        results = wikipedia.search(topic, results=5, suggestion=False)
        for result in results:
            if result.lower() == topic.lower():
                return result
        if results:
            return results[0]

    return normalized


def search_wikipedia(query: str) -> str:
    topic = _extract_topic(query)
    if not topic:
        return "Please tell me what topic you want to search on Wikipedia."

    resolved_topic = _resolve_topic(topic)

    try:
        return wikipedia.summary(resolved_topic, sentences=2, auto_suggest=False)
    except wikipedia.exceptions.DisambiguationError as exc:
        options = ", ".join(exc.options[:3])
        return f"I found multiple matches for {resolved_topic}. Try one of these: {options}."
    except wikipedia.exceptions.PageError:
        if resolved_topic != topic:
            try:
                return wikipedia.summary(topic, sentences=2, auto_suggest=True)
            except Exception:
                pass
        return f"I could not find a Wikipedia page for {topic}."
    except requests.RequestException:
        return "Wikipedia is unreachable right now. Please check your internet connection."
