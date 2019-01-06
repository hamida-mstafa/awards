from . import views
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings


urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(r'^signup/',views.signup,name='signup'),
    url(r'^profile/',views.profile,name='profile'),
    url(r'^post/',views.posts,name='posts'),
    url(r'^one/(?P<id>\d+)',views.get_post_by_id,name='one'),
    url(r'^comment/(\d+)',views.comment,name='comment'),
    url(r'^profiles/(\d+)',views.profiles,name='profiles'),
    url(r'^api/posts',views.PostList.as_view()),
    url(r'^api/profiles',views.ProfilesList.as_view()),
    url(r'^api/profile/profile-id/(?P<pk>[0-9]+)/$',
        views.ProfileData.as_view()),
    url(r'^search',views.search,name='search'),
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
