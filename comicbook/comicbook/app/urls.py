from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm,MyPasswordChangeForm
from .views import CustomLoginView


urlpatterns = [
    path('',views.ProductView.as_view(),name="home"),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart,name='showcart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('superheros/', views.superheros, name='superheros'),
    path('nonfiction/', views.nonfiction, name='nonfiction'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('sciencefiction/', views.sciencefiction, name='sciencefiction'),
    path('horror/', views.horror, name='horror'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('search/', views.product_search, name='product-search'),
    path('superheros/<slug:data>', views.superheros, name='superherosdata'),
    path('nonfiction/<slug:data>', views.nonfiction, name='nonfictiondata'),
    path('sciencefiction/<slug:data>', views.sciencefiction, name='sciencefictiondata'),
    path('horror/<slug:data>', views.horror, name='horrordata'),
    path('accounts/login/', CustomLoginView.as_view(template_name="app/login.html"), name="login"),
    # path('accounts/login/',auth_views.LoginView.as_view(template_name="app/login.html",authentication_form=LoginForm),name="login"),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'),name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    #path('password-reset/',auth_views.PasswordResetView.as_view(template_name="app/password_reset.html")),
    path('registration/',views.CustomerRegistrationView.as_view(),name="customerregistration")
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
