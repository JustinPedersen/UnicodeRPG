"""
Methods for writing out to the console or getting user input.
"""
import re
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


def format_attack_actions(index, attack_type, stamina_cost):
    """
    Attacks are formatted a bit differently display more info to the player.

    :param int index: The index of the actions' dict to use.
    :param str attack_type: Type of attack to perform.
    :param int stamina_cost: Stamina cost of the action to display.
    """
    return '{}. {:30s} [{}]\n'.format(index, attack_type, stamina_cost)


def choose_action(header, actions_dict, attack=False, back=False):
    """
    Format the options for a player's input, present them to the player and return the result of the decision.

    :param str header: Header for the action to take.
    :param dict actions_dict: dictionary of actions to perform. Given as such:
                              > {1: {'type': 'light_attack', 'stamina': 10, 'damage_multiplier': 1 }}
                              NOTE: Index should begin at 1. If a value of 0 is returned the player has not been
                              able to make a choice.
    :param bool attack: If True format this action as an attack.
    :param bool back: If True will add an extra item to the end for going back in the menus.
    :return: The resulting decision index from the actions_dict.
    :rtype: int
    """
    options_string = f'> {header}:\n'

    for index, action in actions_dict.items():
        if attack:
            options_string += format_attack_actions(index,
                                                    action['type'],
                                                    action['stamina_cost'])

        else:
            options_string += f'{index}. {action["type"]}\n'

    if back:
        options_string += f'{len(actions_dict.items())+1}. Back\n'

    # Present the player with the options, excluding the last new line.
    print(options_string[:-1])

    # Obtain the answer from the player
    num_actions = len(actions_dict.keys()) if not back else len(actions_dict.keys()) + 1

    while True:
        result = input()

        if result.isdigit() and int(result) in actions_dict.keys():
            # If the result is a digit and in the actions' dict.
            return int(result)

        elif back and result.isdigit() and result == str(num_actions):
            # If the result is the back option
            return 0

        else:
            # The user has input the wrong answer.
            print(f'Please choose a number between 1 and {num_actions}')


def format_name(name):
    """
    Helper function to format item names neatly for better representation.

    :param str name: Name to be formatted.
    :return: Capitalised and separated name.
    :rtype: str
    """
    return ' '.join([x.capitalize() for x in name.split('_')])


def correct_vowels(sentence):
    """
    Scan the input sentence and if it contains an 'a' followed by a letter beginning with a vowel, replace
    the 'a' for 'an'

    :param str sentence: The sentence to scan.
    :returns: The grammatically correct sentence:
    :rtype: str
    """
    regular_expression = r'( [aA] )([aAeEiIoOuU])'
    return re.sub(regular_expression, r' an \2', sentence)


def get_random_index(iterable):
    """
    :return: From all available indexes in iterable, choose one at random and return it.
    :rtype: int
    """
    return random.randint(0, len(iterable) - 1)


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
    random_damage_verb = (damage_verbs_list[random.randint(0, len(damage_verbs_list) - 1)])
    return random_damage_verb.capitalize()


def attack_update(attacker, victim, item, damage, attack_type):
    """
    Helper function to inform the user of what happened during an attack.
    Who took damage from what and how much was dished out.

    :param class attacker: The class that performed the attack.
    :param class victim: The class that received the attack
    :param dict item: The weapon item that was used in the attack..
    :param float damage: The amount of damage dealt.
    :param str attack_type: The type of attack used.
    """

    verb = get_damage_verb(victim, damage)
    item_name = format_name(item["item_name"])
    attack = format_name(attack_type)

    # Some more random sentence structures to add further spice.
    sentence_dict = {0: f'{attacker.name} performs a {attack}, charging {victim.name} with '
                        f'{item_name} and deals a {verb} {damage} Damage!',
                     1: f'{attacker.name} {attack}\'s {victim.name} using {item_name}, for a {verb} {damage} Damage!',
                     2: f'{attacker.name} {attack}\'s {victim.name} with {item_name}, '
                        f'inflicting a {verb} {damage} Damage!',
                     3: f'{attacker.name} assaults {victim.name} with their {attack} wielding {item_name}, '
                        f'administering a {verb} {damage} Damage in the process!',
                     4: f'{victim.name} receives a {verb} {damage} Damage from {attacker.name}\'s {attack}'
                        f'wielding their {item_name}, lowering {victim.name}\'s health to {victim.health-damage}!'}

    # Updating the player on what happened.
    random_index = random.randint(0, len(sentence_dict) - 1)
    print(correct_vowels(sentence_dict[random_index]))


def death_message(deceased_character, killer=None):
    """
    Display a death message to the player informing them that a character has died.

    :param class deceased_character: Class of the deceased_character
    :param class|optional killer: If there was a killer.
    """
    deceased_name = deceased_character.name
    killer_name = killer.name if killer else ''

    # 0 - No killer, 1 - NPC killer, 2 - NonNPC killer
    death_msg_dict = {0: [f'{deceased_name} has died'],
                      1: [f'{deceased_name} has been slain by {killer_name}',
                          f'{deceased_name} has fallen in battle to {killer_name}',
                          f'Bloodied and broken, {deceased_name} falls to the ground at the hands of {killer_name}',
                          f'{deceased_name} draws their last breath as {killer_name} emerges victorious.',
                          f'{killer_name} has bested {deceased_name} in battle.'],
                      2: []}

    index = 1 if killer else 0
    random_index = random.randint(0, len(death_msg_dict[index]) - 1)
    print(death_msg_dict[index][random_index])


def rest_message(character, info):
    """
    Inform the player of who rested and by how much.

    :param class character: Class of the character who rested.
    :param dict info: dictionary of info given as such:
                    {'attribute name': amount regenerated}

    """
    rest_msg_list = [f'{character.name} takes a knee to regenerate',
                     f'{character.name} steps back from battle for a moment to regenerate',
                     f'Knowing that time is precious, {character.name} takes a moment to rest, replenishing',
                     f'The wise {character.name} pauses to rejuvenating',
                     f'Short of breath, {character.name} pulls back to refresh',
                     f'Noticing that they have only {character.stamina} Stamina and {character.health} Health, '
                     f'{character.name} steps back momentarily restoring']

    # Choosing a random base sentence
    message = rest_msg_list[random.randint(0, len(rest_msg_list) - 1)]

    # Adding the updates to it.
    for i, (attribute, value) in enumerate(info.items()):

        # Deciding how to join the sentence together.
        if i == 0:
            joiner = ''
        elif i == len(info) - 1:
            joiner = ' and'
        else:
            joiner = ','

        message += f'{joiner} {value} {attribute}'

    print(message)
