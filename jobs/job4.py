from home.models import VideoEventPoints
import pandas as pd

def AssigningRank():
    getting_movies_wiki_id_list = list(dict.fromkeys(list(pd.DataFrame(VideoEventPoints.objects.filter(type='movie').values('wiki_id')).wiki_id)))

    for one_by_one_movies in getting_movies_wiki_id_list:
        movie_dea = VideoEventPoints.objects.filter(type='movie', wiki_id=one_by_one_movies).order_by('-points', '-average_points')
        for id_vep_m in range(len(movie_dea)):
            VideoEventPoints.objects.filter(id=movie_dea[id_vep_m].id).update(previous_rank=id_vep_m+1)

    getting_series_wiki_id_list = list(dict.fromkeys(list(pd.DataFrame(VideoEventPoints.objects.filter(type='series').values('wiki_id')).wiki_id)))

    for one_by_one_series in getting_series_wiki_id_list:
        series_dea = VideoEventPoints.objects.filter(type='series', wiki_id=one_by_one_series).order_by('-points', '-average_points')
        for id_vep_s in range(len(series_dea)):
            VideoEventPoints.objects.filter(id=series_dea[id_vep_s].id).update(previous_rank=id_vep_s+1)

    