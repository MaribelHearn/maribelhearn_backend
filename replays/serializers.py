from rest_framework import serializers

from .models import Game, ShotType, Category, Replay


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = "__all__"


class ShotTypeSerializer(serializers.ModelSerializer):
    game = serializers.SlugRelatedField(slug_field="short_name", read_only=True)

    class Meta:
        model = ShotType
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    game = serializers.SlugRelatedField(
        slug_field="shot__game__short_name", read_only=True
    )
    shot = serializers.SlugRelatedField(slug_field="shot__name", read_only=True)

    class Meta:
        model = Category
        fields = "__all__"


class ReplaySerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Replay
        fields = "__all__"
