from django.db import models

class Sex(models.TextChoices):
    MALE = "Macho"
    FEMALE = "Femea"
    DEFAULT = "Não informado"

class Animal(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()

    sex = models.CharField(
        max_length=15,
        choices=Sex.choices,
        default=Sex.DEFAULT,
    )

# 1:N groups
    group = models.ForeignKey(
        "groups.Group",
        on_delete=models.CASCADE,
        related_name="animals",
    )
    
# N:N traits
    traits = models.ManyToManyField(
        "traits.Trait",
        related_name="animals",
    )

    def convert_dog_age_to_human_years(self):
        age_h = 16 * log(self.age) + 31
        return age_h
