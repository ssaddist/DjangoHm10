def simulate_battle(character_1, character_2):
    c1_hp = character_1.hp
    c2_hp = character_2.hp
    battle_log = []
    rounds = 1

    while True:
        damage_1 = max(character_1.attack - character_2.defense, 1)
        c2_hp -= damage_1
        battle_log.append(f'Round {rounds}: {character_1.name} dealt {damage_1} damage')
        if c2_hp <= 0:
            winner = character_1
            break

        damage_2 = max(character_2.attack - character_1.defense, 1)
        c1_hp -= damage_2
        battle_log.append(f'Round {rounds}: {character_2.name} dealt {damage_2} damage')
        if c1_hp <= 0:
            winner = character_2
            break

        rounds += 1

    return {
        'winner': winner,
        'rounds': rounds,
        'battle_log': battle_log,
    }
