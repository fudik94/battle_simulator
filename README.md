# ⚔️ RPG Battle Simulator
🎓 **Academic Project** | Author: Fuad Ismayilbayli | Language: Python 3

A small RPG battle simulator demonstrating OOP principles (Abstraction, Inheritance, Polymorphism, Encapsulation) and Factory pattern.

---

## Project Structure

```
rpg_battle.py        ← main code (Hero base class, classes, factory, battle logic)
tests/
  test_rpg.py        ← pytest unit tests (50+ tests)
requirements.txt     ← dependencies (pytest)
```

## What the Code Demonstrates

- **Abstraction** — `Hero(ABC)` abstract base class with abstract method `use_special`
- **Inheritance** — `Wizard`, `Fighter`, `Cleric`, `Barbarian`, `Druid`, `Warlock` inherit from `Hero`
- **Polymorphism** — each subclass implements its own `use_special`
- **Encapsulation** — health changed only via `take_damage`, `heal`, `hit`, `set_damage`
- **Factory Pattern** — `HeroFactory` centralizes hero creation

---

## Unit Tests (50+ tests)

Tests cover:
- Hero creation and base stats for all 6 classes
- Race bonuses (Elf, Human, Tiefling, Half-Elf, Githyanki)
- `take_damage` — normal, zero, negative (error), overflow
- `heal` — normal, max health cap
- `is_alive` — alive, dead, edge cases
- Special abilities for all classes
- `HeroFactory` — all classes + unknown class error
- Battle logic — deterministic with monkeypatching
