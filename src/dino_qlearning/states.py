"""Convert game measurements into a small, discrete Q-table state."""

from typing import TypeAlias

State: TypeAlias = tuple[int, int, int, int]

DISTANCE_STEP = 50
MAX_DISTANCE = 300


def make_state(
    distance: float | None,
    obstacle_type: str | None,
    is_jumping: bool,
    speed: float,
) -> State:
    """Bucket continuous game values so they can be dictionary keys."""
    if distance is None:
        distance_bucket = MAX_DISTANCE // DISTANCE_STEP
        obstacle_bucket = 0
    else:
        distance_bucket = min(int(max(distance, 0) // DISTANCE_STEP), MAX_DISTANCE // DISTANCE_STEP)
        obstacle_bucket = 2 if obstacle_type == "PTERODACTYL" else 1

    jumping_bucket = int(is_jumping)
    speed_bucket = int(speed >= 10)
    return distance_bucket, obstacle_bucket, jumping_bucket, speed_bucket