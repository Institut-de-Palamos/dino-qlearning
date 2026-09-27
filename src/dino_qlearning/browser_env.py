"""Playwright adapter for the bundled Chrome Dino page."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from playwright.sync_api import Browser, Page, Playwright

from dino_qlearning.qlearning import DUCK, JUMP
from dino_qlearning.states import State, make_state

DEFAULT_GAME_URL = (Path(__file__).resolve().parents[2] / "dino" / "index.html").as_uri()


class BrowserDinoEnv:
    """Expose the browser game as reset() and step(action) operations."""

    def __init__(
        self,
        url: str = DEFAULT_GAME_URL,
        headless: bool = False,
        step_seconds: float = 0.1,
    ) -> None:
        self.url = url
        self.headless = headless
        self.step_milliseconds = int(step_seconds * 1000)
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.page: Page | None = None

    def __enter__(self) -> "BrowserDinoEnv":
        from playwright.sync_api import sync_playwright

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.page = self.browser.new_page()
        self.page.goto(self.url, wait_until="domcontentloaded")
        self.page.wait_for_function("window.Runner && window.Runner.instance_")
        return self

    def __exit__(self, *_: object) -> None:
        if self.browser is not None:
            self.browser.close()
        if self.playwright is not None:
            self.playwright.stop()

    def reset(self) -> State:
        page = self._require_page()
        if page.evaluate("window.Runner.instance_.crashed"):
            page.evaluate("window.Runner.instance_.restart()")
        elif page.evaluate("window.Runner.instance_.playing"):
            page.reload(wait_until="domcontentloaded")
            page.wait_for_function("window.Runner && window.Runner.instance_")
            page.keyboard.press("Space")
        else:
            page.keyboard.press("Space")

        page.wait_for_function(
            "window.Runner.instance_.playing && "
            "!window.Runner.instance_.crashed"
        )
        return self._observe()

    def step(self, action: int) -> tuple[State, float, bool, int]:
        page = self._require_page()
        if action == JUMP:
            page.keyboard.press("Space")
        elif action == DUCK:
            page.keyboard.down("ArrowDown")
        elif action != 0:
            raise ValueError(f"Unknown action: {action}")

        try:
            page.wait_for_timeout(self.step_milliseconds)
            observation = self._read_game_state()
        finally:
            if action == DUCK:
                page.keyboard.up("ArrowDown")

        state = self._make_state(observation)
        crashed = bool(observation["crashed"])
        reward = -100.0 if crashed else 1.0
        return state, reward, crashed, int(observation["score"])

    def _observe(self) -> State:
        return self._make_state(self._read_game_state())

    @staticmethod
    def _make_state(observation: dict[str, Any]) -> State:
        return make_state(
            distance=observation["distance"],
            obstacle_type=observation["obstacle_type"],
            is_jumping=observation["is_jumping"],
            is_ducking=observation["is_ducking"],
            speed=observation["speed"],
        )

    def _read_game_state(self) -> dict[str, Any]:
        page = self._require_page()
        return page.evaluate(
            """() => {
                const runner = window.Runner.instance_;
                const dino = runner.tRex;
                const obstacle = runner.horizon.obstacles.find(
                    item => item.xPos + item.width >= dino.xPos
                );
                return {
                    distance: obstacle ? obstacle.xPos - dino.xPos : null,
                    obstacle_type: obstacle ? obstacle.typeConfig.type : null,
                    is_jumping: dino.jumping,
                    is_ducking: dino.ducking,
                    speed: runner.currentSpeed,
                    crashed: runner.crashed,
                    score: runner.distanceMeter.getActualDistance(
                        Math.ceil(runner.distanceRan)
                    )
                };
            }"""
        )

    def _require_page(self) -> Page:
        if self.page is None:
            raise RuntimeError("Use BrowserDinoEnv inside a 'with' block.")
        return self.page