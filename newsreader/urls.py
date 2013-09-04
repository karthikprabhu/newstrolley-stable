from django.conf.urls import patterns, include, url

from newsreader import views

urlpatterns = patterns('newsreader.views',
	url(r'^$', views.index, name='index'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^login/', views.login, name='login'),
    url(r'^home/(?P<tab_id>\d+)', views.home, name='home'),
    url(r'^home/', views.home, name='home'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^add_tab/', views.add_tab, name='add_tab'),
    url(r'^confirm-email/', views.confirm_email, name='confirm_email'),
    url(r'^reset-password/', views.reset_password, name='reset_password'),
    url(r'^change-password/', views.change_password, name='change_password'),
	url(r'^article/(?P<article_no>\d+)', views.article, name='article'),
)
