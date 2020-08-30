"""
Main gameplay methods for the game.
"""
import time
import character
import console


def combat_attack(player, enemy):
    """

    """
    attack_action = console.choose_action(header='Choose an Attack',
                                          actions_dict=player.attack_actions,
                                          attack=True,
                                          back=True)

    if attack_action == 0:
        return False
    else:
        # Perform the attack.
        player.perform_attack(enemy, attack_action)
        return True


def combat(player, enemy):
    # Player to attack
    # console.draw_hud([player, enemy])

    while player.alive and enemy.alive:
        console.draw_hud([player, enemy])

        # Get an action from the player
        combat_action = console.choose_action('Choose an Action', player.combat_actions)

        # ATTACK
        if combat_action == 1:
            combat_result = combat_attack(player, enemy)
            if not combat_result:
                continue

        # BLOCK
        if combat_action == 2:
            continue

        # REST
        if combat_action == 3:
            continue

        # INVENTORY
        if combat_action == 4:
            continue

        # If the monster is alive, play its turn.
        if enemy.alive:
            # print(f'{enemy.name} turn to attack')
            enemy.perform_attack(player, 3)

    print('-' * 20)
    print(f'{enemy.name} : {enemy.alive}')
    print(f'{player.name} : {player.alive}')


def main():
    monster = character.Monster('Wolf')
    hero = character.Character('Sheep')

    # Entering combat
    combat(hero, monster)


if __name__ == '__main__':
    main()
