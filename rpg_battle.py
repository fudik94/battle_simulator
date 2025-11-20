# rpg_battle.py
# Simple RPG Battle Simulator inspired by Baldur's Gate 3
# Author: Fuad Ismayilbayli
# Language: Python 3

from abc import ABC, abstractmethod
import random
from typing import Dict

# Race bonuses (расовые бонусы)
race_bonus: Dict[str, Dict[str, int]] = {
    "Human": {"health": 5, "damage": 1},
    "Elf": {"health": 0, "damage": 2},
    "Half-Elf": {"health": 0, "damage": 1},
    "Tiefling": {"health": 0, "damage": 2},
    "Githyanki": {"health": 0, "damage": 0}
}

# Base Hero Class (Abstraction)
class Hero(ABC):
    """Abstract base class for all heroes."""

    def __init__(self, name: str, hero_class: str, race: str, damage: int, health: int = 100):
        self.name = name
        self.hero_class = hero_class
        self.race = race
        # we apply race bonuses during create personage ( применяем бонусы расы при создании персонажа)
        bonus = race_bonus.get(race, {"health": 0, "damage": 0})
        self.damage = damage + bonus.get("damage", 0)
        self.health = health + bonus.get("health", 0)
        self.max_health = self.health

    # Encapsulation: Attack Method ( инкапсуляция: метод атаки)
    def hit(self, target: 'Hero'):
        target.health -= self.damage
        if target.health < 0:
            target.health = 0
        print(f"{self.name} attacks {target.name} for {self.damage} damage. ({target.name} health: {target.health})")

    # Encapsulation: Restoring Health (инкапсуляция: восстановление здоровья)
    def heal(self, amount: int):
        old_health = self.health
        self.health = min(self.health + amount, self.max_health)
        print(f"{self.name} heals for {amount}. ({old_health} → {self.health})")

    # Damage ghance (изменить урон)
    def set_damage(self, value: int):
        if value > 0:
            self.damage = value
        print(f"{self.name}'s damage is now {self.damage}")

    @abstractmethod
    def use_special(self, target: 'Hero'):
        pass


# Subclasses (Inheritance + Polymorphism)

class Wizard(Hero):
    def __init__(self, name: str, race: str):
        super().__init__(name, "Wizard", race, damage=12, health=80)

    def use_special(self, target: Hero):
        dmg = 25
        target.health -= dmg
        if target.health < 0:
            target.health = 0
        print(f"{self.name} casts Fireball on {target.name} for {dmg} damage! ({target.name} health: {target.health})")


class Fighter(Hero):
    def __init__(self, name: str, race: str):
        super().__init__(name, "Fighter", race, damage=15, health=120)

    def use_special(self, target: Hero):
        dmg = 20
        target.health -= dmg
        if target.health < 0:
            target.health = 0
        print(f"{self.name} performs a Power Strike on {target.name} for {dmg} damage! ({target.name} health: {target.health})")


class Cleric(Hero):
    def __init__(self, name: str, race: str):
        super().__init__(name, "Cleric", race, damage=10, health=100)

    def use_special(self, target: Hero):
        heal_amount = 25
        self.heal(heal_amount)
        print(f"{self.name} uses Divine Blessing and heals self for {heal_amount} HP!")


class Barbarian(Hero):
    def __init__(self, name: str, race: str):
        super().__init__(name, "Barbarian", race, damage=18, health=130)

    def use_special(self, target: Hero):
        dmg = 30
        target.health -= dmg
        if target.health < 0:
            target.health = 0
        print(f"{self.name} goes into Rage and deals {dmg} damage to {target.name}! ({target.name} health: {target.health})")


class Druid(Hero):
    def __init__(self, name: str, race: str):
        super().__init__(name, "Druid", race, damage=11, health=100)

    def use_special(self, target: Hero):
        heal_amount = 20
        self.heal(heal_amount)
        print(f"{self.name} transforms and restores {heal_amount} HP!")


class Warlock(Hero):
    def __init__(self, name: str, race: str):
        super().__init__(name, "Warlock", race, damage=13, health=90)

    def use_special(self, target: Hero):
        dmg = 22
        target.health -= dmg
        if target.health < 0:
            target.health = 0
        print(f"{self.name} casts Eldritch Blast for {dmg} damage! ({target.name} health: {target.health})")


# Factory Pattern
class HeroFactory:
    """Factory to create heroes by name/class."""
    @staticmethod
    def create_hero(name: str, hero_class: str, race: str) -> Hero:
        if hero_class == "Wizard":
            return Wizard(name, race)
        elif hero_class == "Fighter":
            return Fighter(name, race)
        elif hero_class == "Cleric":
            return Cleric(name, race)
        elif hero_class == "Barbarian":
            return Barbarian(name, race)
        elif hero_class == "Druid":
            return Druid(name, race)
        elif hero_class == "Warlock":
            return Warlock(name, race)
        else:
            raise ValueError(f"Unknown hero class: {hero_class}")


# Example battle simulation
def battle(hero1: Hero, hero2: Hero):
    print(f"Battle starts: {hero1.name} ({hero1.hero_class}) vs {hero2.name} ({hero2.hero_class})\n")

    turn = 0
    while hero1.health > 0 and hero2.health > 0:
        attacker = hero1 if turn % 2 == 0 else hero2
        defender = hero2 if turn % 2 == 0 else hero1

        # randomly choose normal attack or special attack
        if random.random() < 0.7:
            attacker.hit(defender)
        else:
            attacker.use_special(defender)

        if defender.health <= 0:
            print(f"\n{attacker.name} wins! {defender.name} has fallen.")
            break

        turn += 1


# Main program (example heroes)
if __name__ == "__main__":
    gale = HeroFactory.create_hero("Gale", "Wizard", "Elf")
    laezel = HeroFactory.create_hero("Laezel", "Fighter", "Githyanki")

    shadowheart = HeroFactory.create_hero("Shadowheart", "Cleric", "Half-Elf")
    halsin = HeroFactory.create_hero("Halsin", "Druid", "Elf")

    wyll = HeroFactory.create_hero("Wyll", "Warlock", "Human")
    karlach = HeroFactory.create_hero("Karlach", "Barbarian", "Tiefling")

    # fight example
    battle(gale, laezel)
