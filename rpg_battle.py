# Simple RPG Battle Simulator 
# Author: Fuad Ismayilbayli 
# Language: Python 3
from abc import ABC, abstractmethod
import random
from typing import Dict

# Race bonuses 
race_bonus: Dict[str, Dict[str, int]] = {
    "Human": {"health": 5, "damage": 1},
    "Elf": {"health": 0, "damage": 2},
    "Half-Elf": {"health": 0, "damage": 1},
    "Tiefling": {"health": 0, "damage": 2},
    "Githyanki": {"health": 0, "damage": 0}
}

#  Abstraction: base class defines common interface/contract 
class Hero(ABC):
    """Abstract base class for all heroes.
    Demonstrates: Abstraction (common contract), Encapsulation (methods to change health).
    """

    def __init__(self, name: str, hero_class: str, race: str, damage: int, health: int = 100):
        self.name = name
        self.hero_class = hero_class
        self.race = race
        # apply race bonuses
        bonus = race_bonus.get(race, {"health": 0, "damage": 0})
        self.damage = damage + bonus.get("damage", 0)
        # store health and max_health
        self.health = health + bonus.get("health", 0)
        self.max_health = self.health

    # Encapsulation: change HP only via this method (central place)
    def take_damage(self, amount: int):
        """Apply damage; ensures health never below 0."""
        if amount < 0:
            # guard against incorrect usage
            raise ValueError("Damage must be non-negative")
        self.health = max(0, self.health - amount)
        #print(f"{self.name} takes {amount} damage. (HP: {self.health}/{self.max_health})")

    # Encapsulation: healing via method
    def heal(self, amount: int):
        old = self.health
        self.health = min(self.health + amount, self.max_health)
        print(f"{self.name} heals for {amount}. ({old} → {self.health})")

    # Encapsulation: attack uses take_damage of target (no direct writes to target.health)
    def hit(self, target: 'Hero'):
        """Normal attack: deal self.damage to target using its take_damage method."""
        target.take_damage(self.damage)
        print(f"{self.name} attacks {target.name} for {self.damage} damage. ({target.name} health: {target.health})")

    def set_damage(self, value: int):
        if value > 0:
            self.damage = value
        print(f"{self.name}'s damage is now {self.damage}")

    def is_alive(self) -> bool:
        return self.health > 0

    @abstractmethod
    def use_special(self, target: 'Hero'):
        """Each subclass defines a special ability (Polymorphism)."""
        pass

    def __repr__(self):
        return f"<{self.hero_class} {self.name} HP:{self.health}/{self.max_health} DMG:{self.damage}>"

# Subclasses: Inheritance + Polymorphism 
class Wizard(Hero):
    def __init__(self, name: str, race: str):
        super().__init__(name, "Wizard", race, damage=12, health=80)

    def use_special(self, target: Hero):
        dmg = 25
        target.take_damage(dmg)
        print(f"{self.name} casts Fireball on {target.name} for {dmg} damage! ({target.name} health: {target.health})")


class Fighter(Hero):
    def __init__(self, name: str, race: str):
        super().__init__(name, "Fighter", race, damage=15, health=120)

    def use_special(self, target: Hero):
        dmg = 20
        target.take_damage(dmg)
        print(f"{self.name} performs a Power Strike on {target.name} for {dmg} damage! ({target.name} health: {target.health})")


class Cleric(Hero):
    def __init__(self, name: str, race: str):
        super().__init__(name, "Cleric", race, damage=10, health=100)

    def use_special(self, target: Hero):
        # Cleric heals self (allowed). Using self.heal instead of touching health directly.
        heal_amount = 25
        self.heal(heal_amount)
        print(f"{self.name} uses Divine Blessing and heals self for {heal_amount} HP!")


class Barbarian(Hero):
    def __init__(self, name: str, race: str):
        super().__init__(name, "Barbarian", race, damage=18, health=130)

    def use_special(self, target: Hero):
        dmg = 30
        target.take_damage(dmg)
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
        target.take_damage(dmg)
        print(f"{self.name} casts Eldritch Blast for {dmg} damage! ({target.name} health: {target.health})")


# Simple Factory for creation 
class HeroFactory:
    """Create instances by class name (simple factory)."""
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

# Battle logic 
def battle(hero1: Hero, hero2: Hero):
    print(f"Battle starts: {hero1.name} ({hero1.hero_class}) vs {hero2.name} ({hero2.hero_class})\n")

    turn = 0
    while hero1.is_alive() and hero2.is_alive():
        attacker = hero1 if turn % 2 == 0 else hero2
        defender = hero2 if turn % 2 == 0 else hero1

        # randomly choose normal attack or special attack
        if random.random() < 0.7:
            attacker.hit(defender)
        else:
            attacker.use_special(defender)

        if not defender.is_alive():
            print(f"\n{attacker.name} wins! {defender.name} has fallen.")
            break

        turn += 1

#Main example usage
if __name__ == "__main__":
    gale = HeroFactory.create_hero("Gale", "Wizard", "Elf")
    laezel = HeroFactory.create_hero("Laezel", "Fighter", "Githyanki")

    shadowheart = HeroFactory.create_hero("Shadowheart", "Cleric", "Half-Elf")
    halsin = HeroFactory.create_hero("Halsin", "Druid", "Elf")

    wyll = HeroFactory.create_hero("Wyll", "Warlock", "Human")
    karlach = HeroFactory.create_hero("Karlach", "Barbarian", "Tiefling")

    # fight example
    battle(karlach, laezel)


   
