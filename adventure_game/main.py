"""
Main gameplay methods for the game.
"""
import time
import character
import console


def main():
    monster = character.Monster('Wolf')
    hero = character.Character('Sheep')

    while hero.alive and monster.alive:
        # Player to attack
        console.draw_hud([hero, monster])

        result = console.choose_action('Choose an attack', hero.attack_actions)

        #
        if result:
            hero.perform_attack(monster, result)
        else:
            hero.kill()

        # If the monster is dead, end the fight
        if not monster.alive:
            break

        monster.perform_attack(hero, 3)

    print('-' * 20)
    print(f'{monster.name} : {monster.alive}')
    print(f'{hero.name} : {hero.alive}')


if __name__ == '__main__':
    main()
