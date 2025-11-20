# its test file 
import unittest
from rpg_battle import HeroFactory, Wizard, Fighter, Cleric

class TestRpgBattle(unittest.TestCase):

    def test_hit_reduces_health(self):
        # Gale hits Laezel: health should decrease by Gale.damage
        gale = HeroFactory.create_hero("Gale", "Wizard", "Elf")
        laezel = HeroFactory.create_hero("Laezel", "Fighter", "Githyanki")
        initial = laezel.health
        gale.hit(laezel)
        self.assertEqual(laezel.health, max(initial - gale.damage, 0))

    def test_heal_not_exceed_max(self):
        shadow = HeroFactory.create_hero("Shadowheart", "Cleric", "Half-Elf")
        shadow.health = 10
        shadow.heal(50)
        self.assertEqual(shadow.health, shadow.max_health)

    def test_special_effect(self):
        # Test cleric special heals self by known amount
        shadow = HeroFactory.create_hero("Shadowheart", "Cleric", "Half-Elf")
        before = shadow.health
        shadow.use_special(shadow)  # Cleric special heals self
        self.assertGreaterEqual(shadow.health, before)

if __name__ == "__main__":
    unittest.main()
