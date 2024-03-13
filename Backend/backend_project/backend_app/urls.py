from django.urls import path 
from backend_app.views import * 

urlpatterns = [
    path('signup', RegisterAPI.as_view() , name='signup') , 
    path('verify', VerifyOTP.as_view() , name='verify') ,
    path('login', LoginAPI.as_view() , name='login') , 
    path('updateProfile' , updateProfile.as_view() , name='updateProfile') , 
    path('forgotPassword', ForgetPassword.as_view() , name='forgotPassword') ,
    path('changePassword', ResetPassword.as_view() , name='changePassword') ,
    path('testpin', TestPin.as_view() , name='testpin'),
    path('transaction', TransactionView.as_view() , name='transaction')  ,
    path('pending', PendingView.as_view() , name='pending') , 
    path('history', HistoryView.as_view() , name = 'history') ,
    path('execute', ExecuteView.as_view() , name = 'execute'),
    path('block', AllBlockView.as_view() , name = 'block') ,
    path('block/<block_id>/', BlockDetailView.as_view(), name='block_detail'),
]
