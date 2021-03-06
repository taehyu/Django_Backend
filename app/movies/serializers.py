from django.db.models import Sum, Count
from rest_framework import serializers

from utils.custom_functions import reformat_duration
from .models import Movie, Rating, MovieLike


# 전체 영화 일반 정보
class MovieSerializer(serializers.ModelSerializer):
    average_point = serializers.SerializerMethodField('get_average_point')
    acc_favorite = serializers.SerializerMethodField('get_acc_favorite')

    class Meta:
        model = Movie
        fields = [
            'id',
            'rank',
            'name_kor',
            'name_eng',
            'poster',
            'grade',
            'description',
            'average_point',
            'reservation_rate',
            'acc_favorite',
            'open_date',
        ]

    def get_average_point(self, movie):
        point_sum = Movie.objects.filter(pk=movie.pk).values('ratings__score').aggregate(
            point_sum=Sum('ratings__score')
        )['point_sum']

        point_count = Movie.objects.filter(pk=movie.pk).values('ratings__score').aggregate(
            point_count=Count('ratings__score')
        )['point_count']

        return round(point_sum / point_count, 2) if point_count != 0 else 6.3

    def get_acc_favorite(self, movie):
        likes_count = movie.movie_likes.filter(liked=True).count()
        result = likes_count + 689 - (movie.pk * 24)
        return result if result >= 0 else likes_count + 11


class RatingsSerializer(serializers.ModelSerializer):
    rating_id = serializers.IntegerField(source='id', read_only=True)
    member = serializers.CharField(source='member.name', read_only=True)

    class Meta:
        model = Rating
        fields = [
            'rating_id',
            'member',
            'score',
            'key_point',
            'comment',
        ]


# 영화별 상세 정보
class MovieDetailSerializer(serializers.ModelSerializer):
    average_point = serializers.SerializerMethodField('get_average_point')
    acc_favorite = serializers.SerializerMethodField('get_acc_favorite')
    running_time = serializers.SerializerMethodField('get_running_time')
    directors = serializers.SerializerMethodField()
    actors = serializers.SerializerMethodField()
    genres = serializers.SerializerMethodField()
    key_point_count = serializers.SerializerMethodField('get_key_point_count')
    ratings = RatingsSerializer(many=True, source='ratings.all')

    class Meta:
        model = Movie
        fields = [
            'id',
            'rank',
            'name_kor',
            'name_eng',
            'poster',
            'trailer',
            'description',
            'average_point',
            'grade',
            'reservation_rate',
            'open_date',
            'close_date',
            'acc_audience',
            'acc_favorite',
            'running_time',
            'directors',
            'actors',
            'genres',
            'key_point_count',
            'ratings',
        ]

    def get_average_point(self, movie):
        point_sum = Movie.objects.filter(pk=movie.pk).values('ratings__score').aggregate(
            point_sum=Sum('ratings__score')
        )['point_sum']

        point_count = Movie.objects.filter(pk=movie.pk).values('ratings__score').aggregate(
            point_count=Count('ratings__score')
        )['point_count']
        return round(point_sum / point_count, 1) if point_count != 0 else 6.3

    def get_acc_favorite(self, movie):
        likes_count = movie.movie_likes.filter(liked=True).count()
        result = likes_count + 689 - (movie.pk * 24)
        return result if result >= 0 else likes_count + 11

    def get_running_time(self, obj):
        return reformat_duration(obj.running_time)

    def get_directors(self, movie):
        return movie.directors.values_list('name', flat=True)

    def get_actors(self, movie):
        return movie.actors.values_list('name', flat=True)

    def get_genres(self, movie):
        return movie.genres.values_list('name', flat=True)

    def get_key_point_count(self, movie):
        actor = movie.ratings.filter(key_point='actor').count()
        prod = movie.ratings.filter(key_point='prod').count()
        story = movie.ratings.filter(key_point='story').count()
        visual = movie.ratings.filter(key_point='visual').count()
        ost = movie.ratings.filter(key_point='ost').count()

        # 더 나은 데이터 그래프를 위해 임의로 수 올림
        return {
            'actors': (actor + 3) * 6,
            'prods': (prod + 3) * 4,
            'story': (story + 3) * 7,
            'visual': (visual + 3) * 5,
            'ost': (ost + 3) * 8
        }


class AgeBookingSerializer(serializers.Serializer):
    teens = serializers.IntegerField(source='teens__sum')
    twenties = serializers.IntegerField(source='twenties__sum')
    thirties = serializers.IntegerField(source='thirties__sum')
    fourties = serializers.IntegerField(source='fourties__sum')
    fifties = serializers.IntegerField(source='fifties__sum')


# 무비스토리 타임라인에 사용될 영화 정보
class MovieTimelineSerializer(serializers.ModelSerializer):
    movie_name = serializers.CharField(source='name_kor')
    acc_favorite = serializers.SerializerMethodField('get_acc_favorite')
    open_date = serializers.DateField(format='%Y-%m-%d')
    running_time = serializers.SerializerMethodField('get_running_time')
    directors = serializers.SerializerMethodField('get_directors')
    genres = serializers.SerializerMethodField('get_genres')

    class Meta:
        model = Movie
        fields = [
            'movie_name',
            'poster',
            'grade',
            'acc_favorite',
            'open_date',
            'running_time',
            'directors',
            'genres',
        ]

    def get_acc_favorite(self, movie):
        likes_count = movie.movie_likes.filter(liked=True).count()
        result = likes_count + 689 - (movie.pk * 24)
        return result if result >= 0 else likes_count + 11

    def get_running_time(self, obj):
        return reformat_duration(obj.running_time)

    def get_directors(self, movie):
        return movie.directors.values_list('name', flat=True)

    def get_genres(self, movie):
        return movie.genres.values_list('name', flat=True)


class MovieLikeSerializer(serializers.ModelSerializer):
    member = serializers.CharField(source='member.name')
    movie_name = serializers.CharField(source='movie.name_kor')

    class Meta:
        model = MovieLike
        fields = [
            'id',
            'member',
            'movie_name',
            'liked',
            'liked_at',
        ]
