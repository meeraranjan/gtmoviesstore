from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Petition, PetitionVote
from django.contrib.auth.decorators import login_required
from .forms import PetitionForm
from django.db.models import Count, Q



def petition_list(request):
    petitions= (Petition.objects.annotate(
        up_count= Count("votes", filter=Q(votes__value=True)),
        down_count= Count("votes", filter=Q(votes__value=False)),
        score= Count("votes", filter=Q(votes__value=True)) - Count("votes", filter=Q(votes__value=False))
    ).order_by("-score"))
    return render(request, "movies/petition_list.html", {"petitions":petitions})

@login_required
def petition_create(request):
    if request.method == 'POST':
        form = PetitionForm(request.POST)
        if form.is_valid():
            petition = form.save(commit=False)
            petition.created_by = request.user
            petition.save()
            return redirect("petition_list")
    else:
        form = PetitionForm()

    return render(request, "movies/petition_create.html", {"form": form})

@login_required
def petition_vote(request, petition_id, value):
    petition = get_object_or_404(Petition, id=petition_id)
    if value.lower()== "true":
        bool_value = True
    elif value.lower() =="false":
        bool_value = False
    else:
        return redirect("petition_list")
    vote, created= PetitionVote.objects.get_or_create(
        petition= petition,
        user= request.user,
        defaults={"value": bool_value }
    )
    if not created:
        vote.value= bool_value
        vote.save()
    return redirect("petition_list")


def index(request):
    search_term = request.GET.get('search')
    if search_term: 
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html',
    {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment']!= '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
    
@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
    user=request.user)
    review.delete()
    return redirect('movies.show', id=id)