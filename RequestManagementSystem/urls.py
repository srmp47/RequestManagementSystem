from django.contrib import admin
from django.urls import path

from advertisements.views import SetExecutionDetailsView, ContractorDailyScheduleView
from comments.views import CommentListCreateView, CommentRetrieveUpdateDestroyView, ContractorReviewListView
from tickets import views as tickets_view
from users import views as users_view
from advertisements import views as advertisements_view
from comments import views as comments_view
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('user/login', users_view.LoginView.as_view(), name='login'),
    path('user/register', users_view.RegisterView.as_view(), name='register'),
    path('user/profile/', users_view.UserProfileView.as_view(), name='user-profile'),
    path('contractors/<int:pk>/profile/', users_view.ContractorProfileView.as_view(), name='contractor-profile'),
    path('contractors/', users_view.ContractorListView.as_view(), name='contractor-list'),
    path('contractor/<int:contractor_id>/reviews/', ContractorReviewListView.as_view(), name='contractor-reviews'),
    path('profile/<int:pk>/', users_view.PublicProfileView.as_view(), name='public-profile'),

    path('advertisement/', advertisements_view.RequestListCreateView.as_view(), name='ad-list-create'),
    path('advertisement/<int:pk>/', advertisements_view.RequestRetrieveUpdateDeleteView.as_view(), name='ad-detail'),
    path('advertisement/<int:pk>/allocate/', advertisements_view.AllocateContractorView.as_view(), name='ad-allocate'),
    path('advertisement/<int:pk>/done/', advertisements_view.MarkAsDoneView.as_view(), name='ad-done'),
    path('advertisement/<int:pk>/confirm/', advertisements_view.ConfirmDoneView.as_view(), name='ad-confirm-done'),
    path('advertisement/<int:pk>/cancel-ad/', advertisements_view.CancelAdvertisementView.as_view(), name='ad-cancel-owner'),
    path('advertisement/<int:pk>/apply/', advertisements_view.ApplyForAdvertisementView.as_view(), name='ad-apply'),
    path('advertisement/<int:pk>/cancel/', advertisements_view.CancelApplicationView.as_view(), name='ad-cancel'),
    path('advertisement/<int:pk>/review/', comments_view.SubmitReviewView.as_view(), name='ad-review'),

    path('my-schedule/', ContractorDailyScheduleView.as_view(), name='contractor-schedule'),
    path('advertisement/<int:pk>/set-details/', SetExecutionDetailsView.as_view(), name='set-execution-details'),

    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyView.as_view(), name='comment-detail'),

    path('tickets/', tickets_view.TicketListCreateView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/', tickets_view.TicketRetrieveUpdateDestroyView.as_view(), name='ticket-detail'),
    path('support/tickets/<int:pk>/answer/', tickets_view.TicketAnswerView.as_view(), name='ticket-answer-admin'),
    path('support/tickets/', tickets_view.AdminTicketListView.as_view(), name='admin-ticket-list'),
]