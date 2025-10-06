ManBall — Tiny 2D Football Game (Pygame)

### Overview
ManBall is a compact 2D top‑down football game built with Pygame. It features basic player movement, kicking, simple physics (Euler integration, restitution, clamping) and role‑based AI with tunable “nerfs” to feel more human. The project is small, readable, and easy to modify for learning or prototyping.

### Demo Features
- Player movement with acceleration, damping, and speed clamp
- Ball physics with wall bounces and air drag
- Kicking with impulse, plus carry‑over from player velocity
- Simple circle‑vs‑circle collision resolution (player↔player, player↔ball)
- Role‑based AI: Attacking and Defensive bots with jitter/hesitation/avoidance
- HUD score and countdown timer
- Start screen and result screen (replay/quit)
- Sprite animations and crowd background

---

## Quick Start

### Prerequisites
- Python 3.10+ recommended
- Pygame (2.5+ recommended)

Install dependencies:
```bash
pip install pygame
```

### Run the game
```bash
python main.py
```

If you see any mixer/audio issues, check the Troubleshooting section.

---

## Controls

- Team 1 (Left, blue):
  - Move: W A S D
  - Kick: Space
  - Switch active player: Q

- Team 2 (Right, red):
  - Move: Arrow keys
  - Kick: Right Ctrl or Right Shift
  - Switch active player: P

The active player for each team is marked by an indicator icon above their head.

---

## Project Structure

```text
assets/
  audio/           # mp3 sound effects
  fonts/           # "Retroville NC.TTF" font
  sprites/         # field, goalpost, players, crowd, indicators
controller/
  AI.py            # SimpleSoccerAI, AttackingAI, DefensiveAI
GameObject/
  ball.py          # Ball entity + physics, collisions
  player.py        # Player entity + movement, animation, kicking
Physics/
  physics.py       # Vec2, Euler integration, collision, clamp helpers
ui/
  hud.py           # Score + timer HUD
  start_screen.py  # Start screen flow
  overlay.py       # (not used for result screen; kept for reference)
  button.py, ui.py, timer.py
main.py            # Game loop, rendering, input handling
Readme.md
```

---

## Gameplay Loop
1. Start screen is shown.
2. The match runs with a countdown timer and score HUD.
3. Players and AIs move, kick, and collide with the ball and each other.
4. A goal is detected when the ball crosses into the goal mouth rectangle.
5. When the timer reaches zero, the result screen displays the winner and score, with Replay and Quit options.

---

## Configuration & Tuning

Most tunables are small constants in code. Suggested entry points:

- `main.py`
  - `SCREEN_SIZE` and `PITCH_RECT`: overall canvas and play area
  - `goal_width`, `goal_height`: size of each goal mouth
  - Countdown timer duration: `CountdownTimer(6000)` uses milliseconds; e.g. `600000` = 10 minutes

- `GameObject/player.py`
  - `max_speed`: clamp magnitude of velocity
  - `accel`: acceleration magnitude when input is held
  - `linear_damping`: simple linear drag to reduce speed over time
  - Kick parameters: `kick_power`, `kick_extra_range`, `kick_cooldown`

- `GameObject/ball.py`
  - `radius`: visual size and collision radius
  - `restitution_wall`: bounciness on pitch bounds
  - `linear_damping`: simple air drag (reduces speed each frame)

- `controller/AI.py` (via `SimpleSoccerAI` and subclasses)
  - `dead_zone`: ignores tiny movements to avoid jitter
  - `avoid_radius`, `avoid_strength`: avoid crowding teammates
  - `hold_off_distance`: distance at which AI may strafe/retreat instead of charging
  - `hesitation_prob`, `wrong_axis_prob`: imperfect decisions for human‑like feel
  - `wander_jitter`: random noise magnitude added to movement vector
  - `kick_chance`: probability to kick when in range and off cooldown

---

## Physics Summary

- Vectors: magnitude, normalization, angle are provided by `Vec2` in `Physics/physics.py`.
- Integration: Euler method
  - `v(t + dt) = v(t) + a * dt`
  - `x(t + dt) = x(t) + v(t + dt) * dt`
  - optional linear damping: `v *= (1 - c * dt)`
- Collisions: circle‑vs‑circle with simple impulse resolution and positional de‑penetration (equal mass = 1)
- Bounds: clamping to a rectangle with per‑axis bounce using restitution
- A vertical helper `integrate_height` exists for simple 1D gravity/bounce if you extend gameplay

---

## AI Summary

- Desired movement vector aims at the ball, then applies:
  - Teammate avoidance (pushes away within a radius)
  - Optional strafe or retreat when too close to the ball
  - Random jitter and axis‑choice imperfections
- Attacking AI: blends toward an attack target (goal center)
- Defensive AI: balances covering a defend position vs. ball proximity

---

## Assets & Attributions

- Fonts: `Retroville NC.TTF`
- Sprites: in `assets/sprites/` (players, ball, field, crowd, indicators, goalpost)
- Audio: `assets/audio/*.mp3` (ball hit, miss, goal, run, stadium, match end)

All assets are included for local development. Please verify licensing before redistribution.

---

## Troubleshooting

- Pygame mixer fails to init or no audio
  - Ensure `pg.mixer.init()` is after `pg.init()`
  - On some systems, MP3 support can be limited; converting audio to `.ogg` often helps
  - Check the device volume and Pygame music/effect volume levels

- Font not found
  - Verify `assets/fonts/Retroville NC.TTF` exists and path case matches

- Black window or crash on start
  - Confirm Python and Pygame versions
  - Run from repository root so relative asset paths resolve

- Performance
  - Reduce window size `SCREEN_SIZE`
  - Decrease crowd animation rate (`crowd_interval`)
  - Lower sprite scale in `GameObject/player.py` if you add new art

---

## Extending the Game

- Add passing, shooting accuracy, stamina, fouls, or goalkeeper logic
- Add camera panning/zoom and parallax
- Swap sprites/animations by updating the player sprite paths in `player.py`
- Introduce formations and role switching strategies in AI

---

## Development Tips

- Run with a terminal open to see logs and exceptions
- Tweak constants one at a time; keep notes of good values
- Keep `Vec2` operations and helper physics functions centralized in `Physics/physics.py`

---

## License

This repository currently has no explicit license. If you plan to distribute, add a `LICENSE` file (e.g., MIT/Apache‑2.0) and ensure third‑party assets are compatible.

---

## Acknowledgements

Thanks to the Pygame community and open art/audio resources used for prototyping and learning.
