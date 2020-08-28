"""
Methods for writing out to the console or getting user input.
"""


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
        input_string += '{}. {:30s} [{}]\n'.format(index, action['type'], action['stamina'])

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