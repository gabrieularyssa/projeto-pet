from rest_framework import serializers
from animals.models import Animal, Sex
from groups.serializers import GroupSerializer
from traits.serializers import TraitSerializer
from groups.models import Group
from traits.models import Trait

class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField(max_length = 50)
    age = serializers.IntegerField()
    weight = serializers.FloatField()
    sex = serializers.ChoiceField(
        choices=Sex.choices,
        default=Sex.DEFAULT,
    )

    age_in_human_year = serializers.SerializerMethodField()

    group = GroupSerializer()
    traits = TraitSerializer(many = True)

    def get_age(self, obj: Animal)->str:
        return obj.convert_dog_age_to_human_years()

    def create(self, validated_data):

        group_data = validated_data.pop("group")
        group_obj, _ = Group.objects.get_or_create(**group_data)

        traits_list = []
        traits = validated_data.pop("traits")
        for trait in traits:
            trait_obj, _ = Trait.objects.get_or_create(**trait)
            traits_list.append(trait_obj)

        animal_obj = Animal.objects.create(**validated_data, group=group_obj)
        animal_obj.traits.set(traits_list)

        return animal_obj

    def update(self, instance, validated_data):
        unauthorized = ["group", "traits", "sex"]
        err = {}

        for key, value in validated_data.items():
            if key in unauthorized:
                err.update({f"{key}": f"You can not update {key} property."})
            else:
                setattr(instance, key, value)

        if len(err):
            raise KeyError(err, 422)

        instance.save()

        return  instance

