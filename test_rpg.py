import pytest
import random
from rpg_battle import (
    Hero, HeroFactory, Wizard, Fighter, Cleric,
    Barbarian, Druid, Warlock, battle, race_bonus
)


# HERO CREATION & RACE BONUSES


def test_wizard_base_stats():
    w = Wizard("Gale", "Human")
    assert w.health == 85   # 80 + 5 human bonus
    assert w.damage == 13   # 12 + 1 human bonus
    assert w.hero_class == "Wizard"

def test_fighter_base_stats():
    f = Fighter("Laezel", "Githyanki")
    assert f.health == 120
    assert f.damage == 15
    assert f.hero_class == "Fighter"

def test_cleric_base_stats():
    c = Cleric("Shadowheart", "Human")
    assert c.health == 105  # 100 + 5
    assert c.damage == 11   # 10 + 1

def test_barbarian_base_stats():
    b = Barbarian("Karlach", "Human")
    assert b.health == 135  # 130 + 5
    assert b.damage == 19   # 18 + 1

def test_druid_base_stats():
    d = Druid("Halsin", "Human")
    assert d.health == 105  # 100 + 5
    assert d.damage == 12   # 11 + 1

def test_warlock_base_stats():
    w = Warlock("Wyll", "Human")
    assert w.health == 95   # 90 + 5
    assert w.damage == 14   # 13 + 1

def test_elf_race_bonus_damage():
    w = Wizard("Gale", "Elf")
    assert w.damage == 14  # 12 base + 2 elf bonus

def test_human_race_bonus():
    f = Fighter("Hero", "Human")
    assert f.health == 125  # 120 + 5
    assert f.damage == 16   # 15 + 1

def test_tiefling_race_bonus():
    b = Barbarian("Karlach", "Tiefling")
    assert b.damage == 20  # 18 + 2

def test_half_elf_race_bonus():
    c = Cleric("Shadowheart", "Half-Elf")
    assert c.damage == 11  # 10 + 1

def test_githyanki_no_bonus():
    f = Fighter("Laezel", "Githyanki")
    assert f.health == 120
    assert f.damage == 15


# TAKE DAMAGE


def test_take_damage_normal():
    f = Fighter("Test", "Human")
    f.take_damage(30)
    assert f.health == 95  # 125 - 30

def test_take_damage_does_not_go_below_zero():
    f = Fighter("Test", "Human")
    f.take_damage(9999)
    assert f.health == 0

def test_take_damage_exact_zero():
    f = Fighter("Test", "Githyanki")
    f.take_damage(120)
    assert f.health == 0

def test_take_damage_negative_raises_error():
    f = Fighter("Test", "Human")
    with pytest.raises(ValueError):
        f.take_damage(-10)

def test_take_zero_damage():
    f = Fighter("Test", "Human")
    hp = f.health
    f.take_damage(0)
    assert f.health == hp


# HEAL


def test_heal_normal():
    f = Fighter("Test", "Githyanki")
    f.take_damage(50)
    f.heal(20)
    assert f.health == 90  # 120 - 50 + 20

def test_heal_does_not_exceed_max():
    f = Fighter("Test", "Githyanki")
    f.take_damage(10)
    f.heal(9999)
    assert f.health == f.max_health

def test_heal_at_full_health():
    f = Fighter("Test", "Githyanki")
    hp = f.health
    f.heal(50)
    assert f.health == hp  # stays at max


# IS ALIVE


def test_is_alive_true():
    f = Fighter("Test", "Human")
    assert f.is_alive() is True

def test_is_alive_false_after_death():
    f = Fighter("Test", "Human")
    f.take_damage(9999)
    assert f.is_alive() is False

def test_is_alive_exactly_one_hp():
    f = Fighter("Test", "Githyanki")
    f.take_damage(119)
    assert f.is_alive() is True


# HIT (NORMAL ATTACK)


def test_hit_deals_damage():
    attacker = Wizard("Gale", "Human")
    defender = Fighter("Laezel", "Githyanki")
    hp_before = defender.health
    attacker.hit(defender)
    assert defender.health == hp_before - attacker.damage

def test_hit_does_not_affect_attacker():
    attacker = Wizard("Gale", "Human")
    defender = Fighter("Laezel", "Githyanki")
    hp_before = attacker.health
    attacker.hit(defender)
    assert attacker.health == hp_before


# SPECIAL ABILITIES


def test_wizard_fireball():
    wiz = Wizard("Gale", "Human")
    target = Fighter("Laezel", "Githyanki")
    hp_before = target.health
    wiz.use_special(target)
    assert target.health == hp_before - 25

def test_fighter_power_strike():
    f = Fighter("Laezel", "Githyanki")
    target = Wizard("Gale", "Human")
    hp_before = target.health
    f.use_special(target)
    assert target.health == hp_before - 20

def test_barbarian_rage():
    b = Barbarian("Karlach", "Human")
    target = Fighter("Laezel", "Githyanki")
    hp_before = target.health
    b.use_special(target)
    assert target.health == hp_before - 30

def test_warlock_eldritch_blast():
    w = Warlock("Wyll", "Human")
    target = Fighter("Laezel", "Githyanki")
    hp_before = target.health
    w.use_special(target)
    assert target.health == hp_before - 22

def test_cleric_heals_self():
    c = Cleric("Shadowheart", "Human")
    c.take_damage(40)
    hp_before = c.health
    c.use_special(c)
    assert c.health == min(c.max_health, hp_before + 25)

def test_druid_heals_self():
    d = Druid("Halsin", "Human")
    d.take_damage(30)
    hp_before = d.health
    d.use_special(d)
    assert d.health == min(d.max_health, hp_before + 20)

def test_special_does_not_go_below_zero():
    b = Barbarian("Karlach", "Human")
    target = Wizard("Gale", "Human")
    target.take_damage(9999)
    b.use_special(target)
    assert target.health == 0


# HERO FACTORY


def test_factory_creates_wizard():
    h = HeroFactory.create_hero("Gale", "Wizard", "Elf")
    assert isinstance(h, Wizard)

def test_factory_creates_fighter():
    h = HeroFactory.create_hero("Laezel", "Fighter", "Githyanki")
    assert isinstance(h, Fighter)

def test_factory_creates_cleric():
    h = HeroFactory.create_hero("Shadowheart", "Cleric", "Half-Elf")
    assert isinstance(h, Cleric)

def test_factory_creates_barbarian():
    h = HeroFactory.create_hero("Karlach", "Barbarian", "Tiefling")
    assert isinstance(h, Barbarian)

def test_factory_creates_druid():
    h = HeroFactory.create_hero("Halsin", "Druid", "Elf")
    assert isinstance(h, Druid)

def test_factory_creates_warlock():
    h = HeroFactory.create_hero("Wyll", "Warlock", "Human")
    assert isinstance(h, Warlock)

def test_factory_unknown_class_raises_error():
    with pytest.raises(ValueError):
        HeroFactory.create_hero("Test", "Rogue", "Human")


# BATTLE


def test_battle_ends_with_one_winner(monkeypatch):
    monkeypatch.setattr("random.random", lambda: 0.0)
    hero1 = HeroFactory.create_hero("Karlach", "Barbarian", "Tiefling")
    hero2 = HeroFactory.create_hero("Gale", "Wizard", "Elf")
    battle(hero1, hero2)
    assert (hero1.is_alive() and not hero2.is_alive()) or \
           (hero2.is_alive() and not hero1.is_alive())

def test_battle_with_special_attacks(monkeypatch):
    monkeypatch.setattr("random.random", lambda: 1.0)
    hero1 = HeroFactory.create_hero("Karlach", "Barbarian", "Tiefling")
    hero2 = HeroFactory.create_hero("Gale", "Wizard", "Elf")
    battle(hero1, hero2)
    assert (hero1.is_alive() and not hero2.is_alive()) or \
           (hero2.is_alive() and not hero1.is_alive())

def test_set_damage():
    f = Fighter("Test", "Human")
    f.set_damage(50)
    assert f.damage == 50

def test_repr_contains_name():
    f = Fighter("Laezel", "Githyanki")
    assert "Laezel" in repr(f)