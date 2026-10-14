from django.core.validators import MinValueValidator
from django.db import models


class Character(models.Model):
    name = models.CharField(max_length=255)
    hp = models.IntegerField(validators=[MinValueValidator(1)])
    attack = models.IntegerField(validators=[MinValueValidator(1)])
    defense = models.IntegerField(validators=[MinValueValidator(0)])

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(hp__gt=0),
                name='character_hp_gt_0',
            ),
            models.CheckConstraint(
                condition=models.Q(attack__gt=0),
                name='character_attack_gt_0',
            ),
            models.CheckConstraint(
                condition=models.Q(defense__gte=0),
                name='character_defense_gte_0',
            ),
        ]

    def __str__(self):
        return self.name


class Battle(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    character_1 = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='battles_as_character_1',
    )
    character_2 = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='battles_as_character_2',
    )
    winner = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='battles_won',
    )
    rounds = models.PositiveIntegerField()
    battle_log = models.JSONField(default=list)

    def __str__(self):
        return f'{self.character_1.name} vs {self.character_2.name}'
