from rest_framework import serializers

from .models import Game, ShotType, Category, Replay


class GameReplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Replay
        fields = ["date", "submitted_date", "player", "replay", "video"]


class GameCategorySerializer(serializers.ModelSerializer):
    replays = GameReplaySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["route", "difficulty", "type", "replays"]


class GameShotSerializer(serializers.ModelSerializer):
    categories = GameCategorySerializer(many=True, read_only=True)

    class Meta:
        model = ShotType
        fields = ["name", "categories"]


class GameSerializer(serializers.ModelSerializer):
    shots = GameShotSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        fields = ["full_name", "short_name", "shots"]


class ShotTypeSerializer(serializers.ModelSerializer):
    game = serializers.SlugRelatedField(slug_field="short_name", read_only=True)

    class Meta:
        model = ShotType
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    game = serializers.SerializerMethodField()
    shot = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Category
        fields = ["id", "game", "shot", "type", "route", "difficulty", "code"]

    def get_game(self, obj):
        return obj.shot.game.short_name


class ReplaySerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Replay
        fields = "__all__"
