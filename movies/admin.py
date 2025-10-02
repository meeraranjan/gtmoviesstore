from django.contrib import admin

# Register your models here.
from .models import Movie, Review, Petition, PetitionVote

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

class PetitionAdmin(admin.ModelAdmin):
    list_display=  ("id", "title", "created_by", "created_at", "up_votes", "down_votes")
    search_fields = ("title", "description", "created_by__username")
    list_filter = ("created_at", "created_by")

class PetitionVoteAdmin(admin.ModelAdmin):
    list_display=  ("id", "petition", "user", "value")
    search_fields = ("value",)
    list_filter = ("petition__title", "user__username")


admin.site.register(Petition, PetitionAdmin)
admin.site.register(PetitionVote, PetitionVoteAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)