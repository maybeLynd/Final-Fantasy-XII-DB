[Home](../../README.md) / Movement and pathfinding

# Movement and pathfinding

How characters and enemies move, turn, follow, avoid obstacles and find paths.

Jump to: [How actors move](#how-actors-move) · [Collision, bodies and pathfinding](#collision-bodies-and-pathfinding)

## Start here

Start with these pages, in this order:

1. [Player movement](player-movement.md): starts with the stick
2. [Movement step](heading-speed-to-position-delta.md): turns that request into a step
3. [Facing and steering](facing-and-steering.md): adds the turning
4. [Collision-mesh movement](collision-mesh-movement.md): shows what the map does to that step
5. [Movement bodies and separation](movement-bodies-and-separation.md): shows what other bodies do to it

## How actors move

How a stick, a battle order or an attack animation turns into motion and facing.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Player movement](player-movement.md) | Explanation | How the stick, dead zone and speed bands move the one controlled actor. |
| [Movement step](heading-speed-to-position-delta.md) | Explanation | The per-frame step that runs steering, computes the move and updates position. |
| [Facing and steering](facing-and-steering.md) | Explanation | How actors turn: their three angles, the facing writer and steering requests. |
| [Animation-driven movement](animation-driven-movement.md) | Explanation | The lunge and swing-round an attack animation asks for. |
| [Battle locomotion](battle-locomotion.md) | Explanation | The solver that moves a battle unit each step toward where it is going. |

## Collision, bodies and pathfinding

How moving bodies meet the map, keep apart and find routes, and the geometry tests underneath.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Collision-mesh movement](collision-mesh-movement.md) | Explanation | How a moving body crosses the map's collision and gets pushed out of walls. |
| [Movement bodies and separation](movement-bodies-and-separation.md) | Explanation | The pool of movement bodies, how they are sized and how they keep apart. |
| [Geometry primitives](geometry-primitives.md) | Explanation | The small shape and intersection tests under movement and collision. |
| [Navigation mesh and pathfinding](navigation-mesh-and-pathfinding.md) | Explanation | How a battle unit finds a route across an area. |
