"""
All character classes to defined here
"""
import random


class Character(object):
    """
    Base Class for all characters to inherit from
    """

    def __init__(self, name):
        self.name = name
        self.alive = True
        self.health = 100.0
        self.strength = 50.0
        self.stamina = 50

        self.attack_actions = {1: {'type': 'light_attack',
                                   'stamina': 10,
                                   'damage_multiplier': 1
                                   },
                               2: {'type': 'medium_attack',
                                   'stamina': 20,
                                   'damage_multiplier': 1.5
                                   },
                               3: {'type': 'heavy_attack',
                                   'stamina': 30,
                                   'damage_multiplier': 2
                                   }}

    @staticmethod
    def random_value(min_value=0, max_value=1, multiplier=1):
        """
        :param int|optional min_value: Minimum value to generate.
        :param int|optional max_value: Maximum value to generate.
        :param float|optional multiplier: Multiplier for the result.
        :return: Calculate a random value given the start and end points with a multiplier applied.
        :rtype: float
        """
        return random.randint(min_value, max_value) * multiplier

    def __deal_damage(self, target_character, multiplier=1):
        """
        Primary method for attacking and dealing damage.

        :param object target_character: The character to attack.
        :param float|optional multiplier: The multiplier for the final result of the attack. 1 by Default.
        """
        # Calculate the damage + apply it.
        damage = self.random_value(0, self.strength, multiplier)
        target_character.health -= damage

        # If health drops below 0, the character will die.
        if target_character.health <= 0:
            target_character.alive = False

    def _attack(self, target_character, stamina_cost, damage_multiplier):
        """
        Base method for attacks. Attacks cost stamina and will drain it as they happen. If the character has
        enough stamina to perform the attack they will, if they have less than the required amount but more than
        zero, they can still perform the action but its effectiveness will be diminished and after its been performed
        the character will have their stamina zero'd.

        :param target_character: The character to attack.
        :param stamina_cost: Cost to the character's stamina bar.
        :param damage_multiplier: How much the damage is amplified.
        """
        if self.stamina >= stamina_cost:
            self.__deal_damage(target_character, multiplier=damage_multiplier)
            self.stamina -= stamina_cost

        # Last stand, will zero stamina and be less effective.
        elif stamina_cost > self.stamina > 0:
            self.__deal_damage(target_character, multiplier=damage_multiplier / 2)
            self.stamina = 0
        else:
            print('Not enough stamina to attack!')

    def perform_attack(self, target_character, attack_index):
        """
        Perform a light attack onto a target character.

        :param int attack_index: Index number of the attack from self.attack_actions
        :param object target_character: The character to target.
        """
        self._attack(target_character=target_character,
                     stamina_cost=self.attack_actions[attack_index]['stamina'],
                     damage_multiplier=self.attack_actions[attack_index]['damage_multiplier'])

    def heal(self, heal_amount, target_character=None, multiplier=1):
        """
        Primary method for healing. By default, healing will be applied to self.

        :param float heal_amount: The amount to heal by.
        :param object|optional target_character: The character to heal.
        :param multiplier: The multiplier for the final result for healing. 1 by Default.
        """
        target_character = self if not target_character else target_character
        target_character.health += heal_amount * multiplier

    def rest(self):
        """
        TODO: Create a method for regeneration of stamina during a fight.
        """

    def kill(self):
        """
        Kill the current entity.
        """
        self.health = 0
        self.alive = False
        print(f'{self.name} has died.')


class Monster(Character):
    def __init__(self, name):
        super().__init__(name)
        self.health = 120.0
        self.stamina = 30
