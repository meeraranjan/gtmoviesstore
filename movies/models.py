from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    def __str__(self):
        return str(self.id) + ' - ' + self.name
    
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name
    
class Petition(models.Model):
    title= models.CharField(max_length=255)
    description= models.TextField(blank=True)
    created_by= models.ForeignKey(User, on_delete=models.CASCADE,related_name="petitions")
    created_at= models.DateTimeField(auto_now_add=True)

    def up_votes(self):
        return self.votes.filter(value=True).count()
    
    def down_votes(self):
        return self.votes.filter(value=False).count()
    
    def __str__(self):
        return self.title
    
class PetitionVote(models.Model):
    petition= models.ForeignKey(Petition, on_delete=models.CASCADE, related_name="votes")
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    value= models.BooleanField()

    class Meta:
        unique_together= ("petition", "user")