from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Character, Battle
from .serializers import CharacterSerializer, BattleSimulationSerializer, BattleSerializer
from .services import simulate_battle


class CharacterViewSet(viewsets.ModelViewSet):
    queryset = Character.objects.all()
    serializer_class = CharacterSerializer


class BattleSimulationView(APIView):
    def post(self, request):
        serializer = BattleSimulationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        char_1 = serializer.validated_data['character_1']
        char_2 = serializer.validated_data['character_2']

        result = simulate_battle(char_1, char_2)

        Battle.objects.create(
            character_1=char_1,
            character_2=char_2,
            winner=result['winner'],
            rounds=result['rounds'],
            battle_log=result['battle_log'],
        )

        return Response(
            {
                'winner': result['winner'].name,
                'rounds': result['rounds'],
                'battle_log': result['battle_log'],
            },
            status=status.HTTP_200_OK,
        )

    def get(self, request):
        battles = Battle.objects.all().order_by('-created_at')
        serializer = BattleSerializer(battles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BattleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Battle.objects.all().order_by('-created_at')
    serializer_class = BattleSerializer
