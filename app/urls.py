from django.urls import path,reverse_lazy
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm,PwdchangeForm

urlpatterns = [
    path('', views.HomeView.as_view()),
    path('product-detail/<int:pk>/', views.Product_detailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('showcart/',views.showCart,name='showcart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    
    path('mobile/<slug:data>', views.mobile, name='mobile'),
    path('mobile/', views.mobile, name='mobile'),
    path('laptop/',views.Laptop,name='laptop'),
    path('laptop/<slug:data>',views.Laptop, name='laptop'),
    path('topwear/',views.topwear,name='topwear'),
    path('topwear/<slug:data>',views.topwear, name='topwear'),
    path('bottomwear/',views.Bottomwear,name='bottomwear'),
    path('bottomwear/<slug:data>',views.Bottomwear, name='bottomwear'),
    path('accounts/login/',auth_view.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm), name='login'),
    path('logout/',auth_view.LogoutView.as_view(), name='logout'),
    path('registration/', views.customerregistrationView.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),

    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=PwdchangeForm,success_url='/passwordchangedone'),name='changepassword'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html',), name='passwordchangedone'),

    path('password-reset/', auth_view.PasswordResetView.as_view(template_name='app/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset/complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'), name='password_reset_complete'),

    path('edit_address/<int:pk>/',views.EditAddressView.as_view(),name='edit_address'),
    path('edit_address/',views.EditAddressView.as_view(),name='edit_address'),
    path('delate_address/<int:pk>/',views.deleteAddressView,name='delete_address'),
    path('remove_cart/<int:id>/',views.Removeitem_cart,name='removecart'),
    path('pluscart/',views.Plus_cart),
    path('minuscart/',views.Minus_cart),
    path('paymentdone/',views.payment_done,name="paymentdone"),

] + static (settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
