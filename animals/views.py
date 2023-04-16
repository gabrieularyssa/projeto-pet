from .models import Animal
from .serializers import AnimalSerializer
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.views import APIView, Response, Request, status

class AnimalView(APIView):
    def get(self, request: Request) -> Response:

        animals = Animal.objects.all()

        serializer = AnimalSerializer(animals, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:

        serializer = AnimalSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        # if not serializer.is_valid():
        #     return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        # animal = Animal.objects.create(**serializer.validated_data)

        # serializer = AnimalSerializer(animal)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


    class AnimalDetailView(APIView):
        # def get(self, request: Request, animal_id: int) -> Response:
        #     animal = get_object_or_404(Animal, id=animal_id)
        #     serializer = AnimalSerializer(animal)

        def patch(self, request: Request, animal_id: int) -> Response:
            animal = get_object_or_404(Animal, id=animal_id)
            serializer = AnimalSerializer(animal, request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            try:
                serializer.save()
            except KeyError as err:
                return Response(*err.args)

            return Response(serializer.data)