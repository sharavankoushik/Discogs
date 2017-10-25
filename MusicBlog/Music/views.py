from django.http import Http404
# serialize to Iterate over model column names and values in template
from django.shortcuts import get_object_or_404, render

from .models import Album, Songs


# Create your views here.
def index(request):
    #to iterate over all columns in the model
    Avail_albums =  Album.objects.all()
    meta_names = Album._meta.fields
    #to iterate over selected column names
    #Avail_albums = serializers.serialize( "python", Album.objects.all(),fields = ('album_title','album_artist))
    context = {
        'avail_albums' : Avail_albums,
        'columns_name' : meta_names
    }
    return render(request,'Music/index.html',context)

#details of particular album when selected
def details(request,album_id):
    try:
        returned_album = Album.objects.get(pk=album_id)
        song_columns = Songs._meta.fields
        title = Songs._meta.get_field('song_title')
        artist =Songs._meta.get_field('song_artist')
        length = Songs._meta.get_field('song_length')
        stype =Songs._meta.get_field('song_type')
        indi_cols = [title,artist,length,stype]
        #serializers.serialize( "python", Songs.objects.all(),fields = ('song_title','song_artist','song_length'))
        context = {
        'album': returned_album,
        'song_columns':song_columns,
        'indi_cols':indi_cols
        }
    except Album.DoesNotExist:
        raise Http404("Album No longer exists")
    return render(request,'Music\Details.html',context)

def favorite(request,album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        selected_song = album.songs_set.get(pk = request.POST['song'])
    except (KeyError, Songs.DoesNotExist):
        return render(request,'Music\Details.html',
                        {'album':album,
                        'error_message':"Please select a valid option (Song)"}
                        )
    else:
        selected_song.is_favorite = True
        selected_song.save()
        return render(request, 'Music\Details.html', {'album':album})
