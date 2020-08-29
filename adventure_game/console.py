"""
Methods for writing out to the console or getting user input.
"""
import random


def draw_hud(characters):
    """
    Helper function to print out the HUD during fights. This should display the two
    characters involved in the fight and all relevant attributes.

    :param list characters: List of character objects to display. Must only be 2 in length.
    """
    # Start
    print(f'# {"-" * 50} #')

    # Name
    print('\t{:29s} {}'.format(*[char.name for char in characters]))

    # Iterating over all the float attributes and printing them out.
    for attribute in ['health', 'stamina']:
        attribute_strings = ['{} : {:5.2f}'.format(attribute.upper(), getattr(char, attribute)) for char in characters]
        print('\t{:28s}  {}'.format(*attribute_strings))

    # End
    print(f'# {"-" * 50} #')


def choose_action(header, actions_dict, tries=10):
    """
    Format the options for a player's input, present them to the player and return the result of the decision.

    :param str header: Header for the action to take.
    :param dict actions_dict: dictionary of actions to perform. Given as such:
                              > {1: {'type': 'light_attack', 'stamina': 10, 'damage_multiplier': 1 }}
                              NOTE: Index should begin at 1. If a value of 0 is returned the player has not been
                              able to make a choice.
    :param int tries: Number of tries the player gets before exiting the loop.
    :return: The resulting decision index from the actions_dict.
    :rtype: int
    """
    input_string = f'> {header}:\n'

    for index, action in actions_dict.items():
        input_string += '{}. {:30s} [{}]\n'.format(index, action['attack_type'], action['stamina_cost'])

    # Present the player with the options
    print(input_string)

    # Obtain the answer from the player
    tries_count = 0
    while True:
        result = input()

        # If the result is a digit and in the actions' dict.
        if result.isdigit() and int(result) in actions_dict.keys():
            return int(result)
        else:
            print(f'Please choose a number between 1 and {len(actions_dict.keys())}')

        # If the player can't make a choice, return zero.
        tries_count += 1
        if tries_count >= tries:
            return 0


def format_item_name(item_name):
    """
    Helper function to format item names neatly for better representation.

    :param str item_name: The item's name
    :return: Capitalised and separated name.
    :rtype: str
    """
    return ' '.join([x.capitalize() for x in item_name.split('_')])


def get_damage_verb(victim, damage):
    """
    Using the damage amount, and the character's health it was dealt to find the damage bracket 0-4.
    From there pick a random word in that bracket and return it.

    :param class victim: The class that received the attack.
    :param float damage: The amount of damage dealt.
    """
    # Verbs to be used to describe damage amounts in order of severity.
    damage_verbs_dict = {0: ['measly', 'frail', 'feeble', 'weakly', 'shaky', 'decrepit', 'faint', 'poor'],
                         1: ['brawny', 'sturdy', 'hefty', 'sharp', 'strong'],
                         2: ['mighty', 'tremendous', 'heavy', 'enormous', 'hefty', 'powerful'],
                         3: ['crippling', 'crushing', 'mammoth', 'massive'],
                         4: ['bone crushing', 'obliterating', 'annihilating', 'blackout', 'ravaging', 'paralyzing']}

    # Calculate the damage % from current health and damage dealt
    damage_percent = round((damage / victim.health * 100))

    # for each index of the damage dict, multiply it by 20
    damage_index = [x * 20 for x in damage_verbs_dict.keys()]

    # Using the indexes find the closest one to the damage percent
    closest_index = min(damage_index, key=lambda x: abs(x - damage_percent))

    # Using the best damage percent index get the damage verb list.
    damage_verbs_list = damage_verbs_dict[damage_index.index(closest_index)]

    # Grab a random verb from the list.
    random_damage_verb = (damage_verbs_list[random.randint(0, len(damage_verbs_list)-1)])
    return random_damage_verb.capitalize()


def attack_update(item, attacker, victim, damage):
    """
    Helper function to inform the user of what happened during an attack.
    Who took damage from what and how much was dished out.

    :param dict item: The weapon item that was used in the attack.
    :param class attacker: The class that performed the attack.
    :param class victim: The class that received the attack.
    :param float damage: The amount of damage dealt.
    """
    # Get a damage verb to spice things up.
    verb = get_damage_verb(victim, damage)

    # Getting the item's name
    item_name = format_item_name(item["item_name"])

    # Updating the player on what happened.
    print(f'{attacker.name} Attacks {victim.name} using {item_name} for a {verb} {damage} Damage !')
