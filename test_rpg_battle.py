#i dont really understand essence of how the test work , but its in cinditions

import random
import pytest
from rpg_battle import HeroFactory, Wizard, Fighter, Cleric, battle

def test_take_damage_and_heal():
    f = Fighter("TestF", "Githyanki")
    assert f.health == 120
    f.take_damage(30)
    assert f.health == 90
    f.heal(20)
    assert f.health == 110
    f.take_damage(200)
    assert f.health == 0

def test_victory_condition_deterministic(monkeypatch):
    # make randomness deterministic: always choose normal hit (random.random -> 0.0)
    monkeypatch.setattr("random.random", lambda: 0.0)
    gale = HeroFactory.create_hero("Gale", "Wizard", "Elf")
    laezel = HeroFactory.create_hero("Laezel", "Fighter", "Githyanki")
    battle(gale, laezel)
    # exactly one must be alive after battle
    assert (gale.is_alive() and not laezel.is_alive()) or (laezel.is_alive() and not gale.is_alive())

def test_specials_effects():
    wiz = Wizard("WizTest", "Human")
    f = Fighter("FightTest", "Human")
    start_hp = f.health
    wiz.use_special(f)
    assert f.health == max(0, start_hp - 25)
    cler = Cleric("Cler", "Human")
    cler.take_damage(30)
    hp_after_hit = cler.health
    cler.use_special(cler)
    assert cler.health == min(cler.max_health, hp_after_hit + 25)


   
