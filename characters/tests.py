from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Character, Battle


class CharacterAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.character = Character.objects.create(
            name='Knight',
            hp=100,
            attack=20,
            defense=5,
        )

    def test_list_characters(self):
        response = self.client.get('/api/characters/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Knight')

    def test_get_single_character(self):
        response = self.client.get(f'/api/characters/{self.character.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.character.id)
        self.assertEqual(response.data['name'], 'Knight')
        self.assertEqual(response.data['hp'], 100)
        self.assertEqual(response.data['attack'], 20)
        self.assertEqual(response.data['defense'], 5)

    def test_create_character(self):
        payload = {
            'name': 'Orc',
            'hp': 80,
            'attack': 15,
            'defense': 3,
        }
        response = self.client.post('/api/characters/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Orc')
        self.assertTrue(Character.objects.filter(name='Orc').exists())

    def test_create_character_invalid_hp(self):
        payload = {
            'name': 'Ghost',
            'hp': 0,
            'attack': 10,
            'defense': 2,
        }
        response = self.client.post('/api/characters/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_character_invalid_attack(self):
        payload = {
            'name': 'Peasant',
            'hp': 50,
            'attack': 0,
            'defense': 2,
        }
        response = self.client.post('/api/characters/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_character_invalid_defense(self):
        payload = {
            'name': 'Mage',
            'hp': 50,
            'attack': 10,
            'defense': -1,
        }
        response = self.client.post('/api/characters/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_character_defense_zero_allowed(self):
        payload = {
            'name': 'Glass Cannon',
            'hp': 50,
            'attack': 30,
            'defense': 0,
        }
        response = self.client.post('/api/characters/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['defense'], 0)

    def test_update_character(self):
        payload = {
            'name': 'Paladin',
            'hp': 120,
            'attack': 25,
            'defense': 8,
        }
        response = self.client.put(f'/api/characters/{self.character.id}/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.character.refresh_from_db()
        self.assertEqual(self.character.name, 'Paladin')
        self.assertEqual(self.character.hp, 120)

    def test_delete_character(self):
        response = self.client.delete(f'/api/characters/{self.character.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Character.objects.filter(id=self.character.id).exists())


class BattleSimulationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.c1 = Character.objects.create(
            name='Knight',
            hp=100,
            attack=20,
            defense=5,
        )
        self.c2 = Character.objects.create(
            name='Orc',
            hp=50,
            attack=15,
            defense=5,
        )

    def test_successful_battle_simulation(self):
        payload = {
            'character_1': self.c1.id,
            'character_2': self.c2.id,
        }
        response = self.client.post('/api/battle/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('winner', response.data)
        self.assertIn('rounds', response.data)
        self.assertIn('battle_log', response.data)
        self.assertEqual(response.data['winner'], 'Knight')
        self.assertEqual(response.data['rounds'], 4)

        expected_log = [
            'Round 1: Knight dealt 15 damage',
            'Round 1: Orc dealt 10 damage',
            'Round 2: Knight dealt 15 damage',
            'Round 2: Orc dealt 10 damage',
            'Round 3: Knight dealt 15 damage',
            'Round 3: Orc dealt 10 damage',
            'Round 4: Knight dealt 15 damage',
        ]
        self.assertEqual(response.data['battle_log'], expected_log)

        self.assertEqual(Battle.objects.count(), 1)
        saved_battle = Battle.objects.first()
        self.assertEqual(saved_battle.winner, self.c1)
        self.assertEqual(saved_battle.rounds, 4)

    def test_minimum_damage_applied(self):
        tank = Character.objects.create(
            name='Tank',
            hp=10,
            attack=1,
            defense=100,
        )
        weakling = Character.objects.create(
            name='Weakling',
            hp=2,
            attack=2,
            defense=100,
        )
        payload = {
            'character_1': weakling.id,
            'character_2': tank.id,
        }
        response = self.client.post('/api/battle/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['battle_log'][0], 'Round 1: Weakling dealt 1 damage')
        self.assertEqual(response.data['battle_log'][1], 'Round 1: Tank dealt 1 damage')

    def test_character_cannot_fight_themselves(self):
        payload = {
            'character_1': self.c1.id,
            'character_2': self.c1.id,
        }
        response = self.client.post('/api/battle/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_battle_nonexistent_character(self):
        payload = {
            'character_1': self.c1.id,
            'character_2': 9999,
        }
        response = self.client.post('/api/battle/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_battle_history_api(self):
        payload = {
            'character_1': self.c1.id,
            'character_2': self.c2.id,
        }
        self.client.post('/api/battle/', payload, format='json')

        response = self.client.get('/api/battles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['winner'], 'Knight')
        self.assertEqual(response.data[0]['rounds'], 4)

        get_battle_response = self.client.get('/api/battle/')
        self.assertEqual(get_battle_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(get_battle_response.data), 1)
