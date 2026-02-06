from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Film, Review, Genre

def home(request):
    """Главная страница с поиском"""
    films = Film.objects.all()
    
    # Поиск
    search = request.GET.get('search', '').strip()
    if search:
        words = search.split()
        query = Q()
        for word in words:
            query |= Q(title__icontains=word) | Q(director__icontains=word) | Q(description__icontains=word)
        films = films.filter(query)
    
    # Фильтр по жанрам (несколько жанров)
    genre_ids = request.GET.getlist('genre')
    if genre_ids:
        films = films.filter(genres__id__in=genre_ids).distinct()
    
    genres = Genre.objects.all()
    
    context = {
        'films': films,
        'genres': genres,
        'search': search,
        'selected_genres': genre_ids,
    }
    return render(request, 'main.html', context)

def film_detail(request, film_id):
    """Страница деталей фильма"""
    film = get_object_or_404(Film, id=film_id)
    reviews = film.reviews.all().order_by('-created_at')
    
    # Добавление отзыва
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        rating = request.POST.get('rating', '')
        comment = request.POST.get('comment', '').strip()
        
        if name and email and rating and comment:
            Review.objects.create(
                film=film,
                name=name,
                email=email,
                rating=int(rating),
                comment=comment
            )
            messages.success(request, 'Ваш отзыв успешно добавлен!')
            return redirect('film_detail', film_id=film.id)
        else:
            messages.error(request, 'Пожалуйста, заполните все поля!')
    
    genres = Genre.objects.all()
    selected_genres = request.GET.getlist('genre')
    
    context = {
        'film': film,
        'reviews': reviews,
        'genres': genres,
        'selected_genres': selected_genres,
        'search': request.GET.get('search', ''),
    }
    return render(request, 'film_detail.html', context)