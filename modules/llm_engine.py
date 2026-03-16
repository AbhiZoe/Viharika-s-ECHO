from __future__ import annotations

from typing import Any

from config.config import GROQ_API_KEY, GROQ_MODEL, LLM_PROVIDER, LLM_TIMEOUT_SECONDS, OPENAI_API_KEY, OPENAI_MODEL
from utils.helpers import append_memory, load_memory

SYSTEM_PROMPT = (
    "You are Echo-Mind, a modern desktop AI voice assistant. "
    "Be concise, helpful, and safe. If a local task already handled the request, do not invent extra actions."
)

try:
    from groq import Groq
except Exception:
    Groq = None

try:
    from openai import OpenAI
except Exception:
    OpenAI = None


class LLMEngine:
    def __init__(self) -> None:
        self.provider = LLM_PROVIDER

    def _build_messages(self, prompt: str) -> list[dict[str, str]]:
        return [{"role": "system", "content": SYSTEM_PROMPT}, *load_memory(), {"role": "user", "content": prompt}]

    def _get_client(self) -> tuple[Any, str]:
        try:
            if self.provider == "openai":
                if not OPENAI_API_KEY:
                    return None, "OpenAI API key is missing. Add OPENAI_API_KEY in .env."
                if OpenAI is None:
                    return None, "The openai package is not installed yet. Install requirements and restart Echo-Mind."
                return OpenAI(api_key=OPENAI_API_KEY, timeout=LLM_TIMEOUT_SECONDS), OPENAI_MODEL

            if not GROQ_API_KEY:
                return None, "Groq API key is missing. Add GROQ_API_KEY in .env."
            if Groq is None:
                return None, "The groq package is not installed yet. Install requirements and restart Echo-Mind."
            return Groq(api_key=GROQ_API_KEY, timeout=LLM_TIMEOUT_SECONDS), GROQ_MODEL
        except TypeError as exc:
            if "proxies" in str(exc):
                return None, "Groq dependency mismatch detected. Install compatible packages with: venv\\Scripts\\python.exe -m pip install setuptools httpx==0.27.2"
            return None, f"LLM client setup failed: {exc}"
        except Exception as exc:
            return None, f"LLM client setup failed: {exc}"

    def ask(self, prompt: str) -> str:
        clean_prompt = prompt.strip()
        if not clean_prompt:
            return "Please say or type a command."

        client, model_or_error = self._get_client()
        if client is None:
            return model_or_error

        try:
            response = client.chat.completions.create(
                model=model_or_error,
                messages=self._build_messages(clean_prompt),
                temperature=0.5,
                max_tokens=450,
            )
            answer = (response.choices[0].message.content or "").strip()
        except Exception:
            return "I could not reach the language model right now. Please check your connection and try again."

        if not answer:
            return "I understood the request, but the model returned an empty response."

        append_memory("user", clean_prompt)
        append_memory("assistant", answer)
        return answer


_ENGINE = LLMEngine()


def ask_llm(prompt: str) -> str:
    return _ENGINE.ask(prompt)
