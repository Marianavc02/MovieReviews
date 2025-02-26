import matplotlib
import matplotlib.pyplot as plt
from django.http import HttpResponse
import io
import base64
from .models import Movie
from django.shortcuts import render
from django.http import HttpResponse

def statistics_view(request):
    matplotlib.use('Agg') # Para que no se muestre la gráfica en la ventana emergente
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year') # Obtener todos los años de las peliculas
    movie_counts_by_year = {} # Crear un diccionario para almacenar la cantidad de películas por año 
    for year in years: # Contar la cantidad de películas por año
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        count = movies_in_year.count()
        movie_counts_by_year[year] = count
    bar_width = 0.5 # Ancho de las barras
    bar_spacing = 0.5 # Separación entre las barras 
    bar_positions = range(len(movie_counts_by_year)) # Posiciones de las barras

    #Crear la gráfica de barras
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    # Personalizar la gráfica
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    # Ajustar el espaciado entre las barras
    plt.subplots_adjust(bottom=0.3)
    # Guardar la gráfica en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    # Renderizar la plantilla statistics.html con la gráfica
    return render(request, 'statistics.html', {'graphic': graphic})


def statistics_view(request):
    matplotlib.use('Agg')  # Para que no se muestre la gráfica en ventana emergente

    # Gráfico de cantidad de películas por año
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    movie_counts_by_year = {year: Movie.objects.filter(year=year).count() for year in years if year}
    
    bar_width = 0.5  # Ancho de las barras
    bar_positions = range(len(movie_counts_by_year))

    plt.figure(figsize=(10, 5))
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center', color='skyblue')
    plt.title('Movies per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    graphic_years = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # Gráfico de cantidad de películas por género (primer género de cada película)
    movies = Movie.objects.exclude(genre__isnull=True).exclude(genre='').values_list('genre', flat=True)
    genre_counts = {}
    for movie_genres in movies:
        first_genre = movie_genres.split(',')[0].strip()  # Tomar solo el primer género
        genre_counts[first_genre] = genre_counts.get(first_genre, 0) + 1

    plt.figure(figsize=(10, 5))
    plt.bar(genre_counts.keys(), genre_counts.values(), color='coral')
    plt.xlabel('Genre')
    plt.ylabel('Number of Movies')
    plt.title('Movies per Genre')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    graphic_genres = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    # Renderizar la plantilla con ambas gráficas
    return render(request, 'statistics.html', {'graphic_years': graphic_years, 'graphic_genres': graphic_genres})




# Create your views here.
def home(request):
    #return HttpResponse('<h1>Welcome to Home Page</h1>')
    #return render(request,'home.html')
    #return render(request, 'home.html',{'name':'mariana valderrama'})
    searchTerm= request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request,'home.html',{'searchTerm':searchTerm,'movies':movies})

def about(request):
    #return HttpResponse('<h1>Welcome to About Page</h1>')
    return render(request, 'about.html')

def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})

