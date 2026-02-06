from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Genre(models.Model):
    """Модель жанра фильма"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Название жанра")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ['name']

class Film(models.Model):
    """Модель фильма"""
    title = models.CharField(max_length=200, verbose_name="Название фильма")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    year = models.IntegerField(verbose_name="Год выпуска")
    genres = models.ManyToManyField(Genre, verbose_name="Жанры", blank=True)
    director = models.CharField(max_length=200, verbose_name="Режиссёр", blank=True, null=True)
    
    # Загрузка постера
    poster = models.ImageField(
        upload_to='posters/', 
        verbose_name="Постер фильма", 
        blank=True, 
        null=True,
        help_text="Загрузите постер фильма (JPG, PNG)"
    )
    
    # Загрузка видео файла трейлера
    trailer_file = models.FileField(
        upload_to='trailers/',
        verbose_name="Видеофайл трейлера",
        blank=True,
        null=True,
        help_text="Загрузите видеофайл трейлера в формате MP4"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    
    def get_poster_url(self):
        """Возвращает URL постера"""
        if self.poster:
            return self.poster.url
        return ''
    
    def get_trailer_url(self):
        """Возвращает URL видеофайла трейлера"""
        if self.trailer_file:
            return self.trailer_file.url
        return ''
    
    def get_average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            total = sum([review.rating for review in reviews])
            return round(total / reviews.count(), 1)
        return 0.0
    
    def __str__(self):
        return f"{self.title} ({self.year})"
    
    def display_genres(self):
        """Возвращает строку с жанрами для админки"""
        return ", ".join([genre.name for genre in self.genres.all()])
    display_genres.short_description = 'Жанры'
    
    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
        ordering = ['-created_at']

class Review(models.Model):
    """Модель отзыва к фильму"""
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='reviews', verbose_name="Фильм")
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    rating = models.IntegerField(
        verbose_name="Оценка",
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Оценка от 1 до 10"
    )
    comment = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    def __str__(self):
        return f"Отзыв от {self.name} на {self.film.title}"
    
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_at']