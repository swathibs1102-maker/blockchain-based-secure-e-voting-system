from django.urls import path

from . import views



urlpatterns = [path("index.html", views.index, name="index"),
		   path('Login.html', views.Login, name="Login"), 
	       path('Register.html', views.Register, name="Register"),
		   path('Signup', views.Signup, name="Signup"),
	       path('UserLogin', views.UserLogin, name="UserLogin"),
	       path("AdminLogin", views.AdminLogin, name="AdminLogin"),
	       path("Admin.html", views.Admin, name="Admin"),
	       path("Vote.html", views.Vote, name="Vote"),
		   path('trainmodel',views.trainmodel,name="trainmodel"),
	       path("ViewCount", views.ViewCount, name="ViewCount"),	
	       path("CastVote", views.CastVote, name="CastVote"),
	       path("CastVoteAction", views.CastVoteAction, name="CastVoteAction"),
	       path("ViewCountAction", views.ViewCountAction, name="ViewCountAction"),
		   path("Addcand", views.Addcand, name="Addcand"),
		   path("addcanditate", views.addcanditate, name="addcanditate"),
		   path("regotpverify", views.regotpverify, name="regotpverify"),
		   path("otpverify", views.otpverify, name="otpverify"),
		   path("ViewCountes", views.ViewCountes, name="ViewCountes"),
]
