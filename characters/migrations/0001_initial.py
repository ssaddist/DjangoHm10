
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('hp', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('attack', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('defense', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'constraints': [models.CheckConstraint(condition=models.Q(('hp__gt', 0)), name='character_hp_gt_0'), models.CheckConstraint(condition=models.Q(('attack__gt', 0)), name='character_attack_gt_0'), models.CheckConstraint(condition=models.Q(('defense__gte', 0)), name='character_defense_gte_0')],
            },
        ),
        migrations.CreateModel(
            name='Battle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('rounds', models.PositiveIntegerField()),
                ('battle_log', models.JSONField(default=list)),
                ('character_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='battles_as_character_1', to='characters.character')),
                ('character_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='battles_as_character_2', to='characters.character')),
                ('winner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='battles_won', to='characters.character')),
            ],
        ),
    ]
