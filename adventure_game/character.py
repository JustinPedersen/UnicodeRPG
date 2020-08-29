"""
All character classes defined here
"""
import random
import console


class Character(object):
    """
    Base Class for all characters to inherit from
    TODO:
        self.luck - Chance for a critical hit
    """

    def __init__(self, name):
        self.name = name

        # basic attributes
        self.alive = True
        self.health = 100.0
        self.strength = 50.0
        self.stamina = 50
        self.luck = 10

        # Inventory and equipped items.
        self.inventory = {'weapons': {0: {'item_name': 'bare_fists',
                                          'damage_bonus': 10,
                                          'durability': 0}}
                          }

        self.equipped = [self.inventory['weapons'][0]]

        # Basic attack actions that are picked up and used by the console and actions methods.
        self.attack_actions = {1: {'attack_type': 'light_attack',
                                   'stamina_cost': 10,
                                   'damage_multiplier': 1
                                   },
                               2: {'attack_type': 'medium_attack',
                                   'stamina_cost': 20,
                                   'damage_multiplier': 1.5
                                   },
                               3: {'attack_type': 'heavy_attack',
                                   'stamina_cost': 30,
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

    def __deal_damage(self, target_character, attack_index, multiplier=1):
        """
        Primary method for attacking and dealing damage. An attack will be performed for each item currently
        equipped in the player's inventory. The damage is calculated by using the character's strength + the
        weapon damage bonus to form the upper limit of damage possible.

        :param class target_character: The character to attack.
        :param int attack_index: Index number of the attack from self.attack_actions
        :param float|optional multiplier: The multiplier for the final result of the attack. 1 by Default.
        """
        # Get the attack type so that it can be used later.
        attack_type = self.attack_actions[attack_index]['attack_type']

        # Perform an attack for each item that is currently equipped.
        for item in self.equipped:
            # Calculate the damage + apply it.
            upper_damage_limit = item['damage_bonus'] + self.strength
            damage = self.random_value(0, upper_damage_limit, multiplier)

            if target_character.health > 0:
                # Update the user on what happened + remove the health
                console.attack_update(self, target_character, item, damage, attack_type)

                # If health drops below 0, the character will die.
                if damage >= target_character.health:
                    target_character.kill(killer=self)
                else:
                    target_character.health -= damage

    def perform_attack(self, target_character, attack_index):
        """
        Base method for attacks. Attacks cost stamina and will drain it as they happen. If the character has
        enough stamina to perform the attack they will, if they have less than the required amount but more than
        zero, they can still perform the action but its effectiveness will be diminished and after it's been performed
        the character will have their stamina zero'd.

        :param target_character: The character to attack.
        :param int attack_index: Index number of the attack from self.attack_actions
        """
        stamina_cost = self.attack_actions[attack_index]['stamina_cost']
        damage_multiplier = self.attack_actions[attack_index]['damage_multiplier']

        if self.stamina >= stamina_cost:
            self.__deal_damage(target_character,
                               attack_index=attack_index,
                               multiplier=damage_multiplier)
            self.stamina -= stamina_cost

        # Last stand, will zero stamina and be less effective.
        elif stamina_cost > self.stamina > 0:
            self.__deal_damage(target_character,
                               attack_index=attack_index,
                               multiplier=damage_multiplier / 2)
            self.stamina = 0
        else:
            print(f'{self.name} does not have enough stamina to attack!')

    def heal(self, heal_amount, target_character=None, multiplier=1):
        """
        Primary method for healing. By default, healing will be applied to self.

        :param float heal_amount: The amount to heal by.
        :param class|optional target_character: The character to heal.
        :param multiplier: The multiplier for the final result for healing. 1 by Default.
        """
        target_character = self if not target_character else target_character
        target_character.health += heal_amount * multiplier

    def rest(self):
        """
        TODO: Create a method for regeneration of stamina during a fight.
        """

    def kill(self, killer=None):
        """
        Kill the current entity and pass the events to the console to inform the player.

        :param class|optional killer: If a killer is specified it will appear in the death message.
        """
        self.health = 0
        self.alive = False
        console.death_message(self, killer)


class Monster(Character):
    def __init__(self, name):
        super().__init__(name)

        # basic attributes
        self.health = 120.0
        self.strength = 50.0
        self.stamina = 30
        self.luck = 10

        # Inventory and equipped items.
        self.inventory = {'weapons': {0: {'item_name': 'razor_claws',
                                          'damage_bonus': 20,
                                          'durability': 0}}
                          }

        self.equipped = [self.inventory['weapons'][0]]
