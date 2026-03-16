from __future__ import annotations

import re
from dataclasses import dataclass

from modules.system_control import (
    open_application,
    open_google,
    open_url,
    open_youtube,
    play_on_youtube,
    search_web,
    take_screenshot,
)
from modules.web_tasks import search_wikipedia


@dataclass(slots=True)
class RouteResult:
    handled: bool
    response: str = ""


class TaskRouter:
    def route(self, command: str) -> RouteResult:
        original = command.strip()
        cleaned = original.lower()
        if not cleaned:
            return RouteResult(handled=True, response="Please say or type a command.")

        youtube_query = self._extract_youtube_query(original)
        if youtube_query is not None:
            if youtube_query:
                direct_opened = play_on_youtube(youtube_query)
                if direct_opened:
                    return RouteResult(True, f"Playing {youtube_query} on YouTube.")
                return RouteResult(True, f"Opening YouTube results for {youtube_query}.")
            open_youtube()
            return RouteResult(True, "Opening YouTube.")

        google_query = self._extract_google_query(original)
        if google_query is not None:
            if google_query:
                open_google(google_query)
                return RouteResult(True, f"Searching Google for {google_query}.")
            open_google()
            return RouteResult(True, "Opening Google.")

        if any(phrase in cleaned for phrase in ("take screenshot", "capture screenshot", "take a screenshot")):
            path = take_screenshot()
            return RouteResult(True, f"Screenshot captured at {path}.")

        if cleaned.startswith(("open ", "launch ", "start ")):
            target = re.sub(r"^(open|launch|start)\s+", "", original, flags=re.IGNORECASE).strip()
            if open_application(target):
                return RouteResult(True, f"Opening {target}.")
            if open_url(target):
                return RouteResult(True, f"Opening {target} in your browser.")
            return RouteResult(True, f"I could not find an application or website for {target}.")

        if cleaned.startswith(("search for ", "search ")):
            topic = re.sub(r"^search( for)?\s+", "", original, flags=re.IGNORECASE).strip()
            if not topic:
                return RouteResult(True, "Tell me what you want to search for.")
            search_web(topic)
            return RouteResult(True, f"Searching the web for {topic}.")

        if cleaned.startswith(("wikipedia ", "wiki ")):
            return RouteResult(True, search_wikipedia(original))

        return RouteResult(False, "")

    def _extract_youtube_query(self, command: str) -> str | None:
        patterns = (
            r"^open youtube(?: and)? play (.+)$",
            r"^open youtube(?: and)? search (?:for )?(.+)$",
            r"^play (.+) on youtube$",
            r"^search youtube for (.+)$",
            r"^youtube (.+)$",
            r"^open youtube$",
        )
        for pattern in patterns:
            match = re.match(pattern, command, flags=re.IGNORECASE)
            if match:
                return match.group(1).strip() if match.groups() else ""
        return None

    def _extract_google_query(self, command: str) -> str | None:
        patterns = (
            r"^open google(?: and)? search (?:for )?(.+)$",
            r"^google (.+)$",
            r"^search google for (.+)$",
            r"^open google$",
        )
        for pattern in patterns:
            match = re.match(pattern, command, flags=re.IGNORECASE)
            if match:
                return match.group(1).strip() if match.groups() else ""
        return None


_ROUTER = TaskRouter()


def route_task(command: str) -> str | None:
    result = _ROUTER.route(command)
    return result.response if result.handled else None
