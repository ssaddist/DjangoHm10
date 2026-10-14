from rest_framework import serializers
from .models import Character, Battle


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ['id', 'name', 'hp', 'attack', 'defense']

    def validate_hp(self, value):
        if value <= 0:
            raise serializers.ValidationError('HP must be greater than 0.')
        return value

    def validate_attack(self, value):
        if value <= 0:
            raise serializers.ValidationError('Attack must be greater than 0.')
        return value

    def validate_defense(self, value):
        if value < 0:
            raise serializers.ValidationError('Defense must be greater than or equal to 0.')
        return value


class BattleSimulationSerializer(serializers.Serializer):
    character_1 = serializers.PrimaryKeyRelatedField(queryset=Character.objects.all())
    character_2 = serializers.PrimaryKeyRelatedField(queryset=Character.objects.all())

    def validate(self, attrs):
        if attrs['character_1'] == attrs['character_2']:
            raise serializers.ValidationError('Characters must be different.')
        return attrs


class BattleSerializer(serializers.ModelSerializer):
    character_1 = serializers.CharField(source='character_1.name', read_only=True)
    character_2 = serializers.CharField(source='character_2.name', read_only=True)
    winner = serializers.CharField(source='winner.name', read_only=True)
    character_1_id = serializers.IntegerField(source='character_1.id', read_only=True)
    character_2_id = serializers.IntegerField(source='character_2.id', read_only=True)
    winner_id = serializers.IntegerField(source='winner.id', read_only=True)

    class Meta:
        model = Battle
        fields = [
            'id',
            'created_at',
            'character_1',
            'character_1_id',
            'character_2',
            'character_2_id',
            'winner',
            'winner_id',
            'rounds',
            'battle_log',
        ]
