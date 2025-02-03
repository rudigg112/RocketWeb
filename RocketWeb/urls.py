from django.contrib import admin
from django.urls import path, include

from RocketBuddy.views import save_profile_field
from RocketWebMain.views import login_page
from TeacherAssistant.views import check_client, create_draft, update_task_defense_field

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('RocketWebMain.urls'), name='home'),
    path('teacher-assistant/', include('TeacherAssistant.urls'), name='teacher_assistant'),

    path('login/', login_page, name='login'),

    path('check-client/', check_client, name='check_client'),

    path('save_profile_field/', save_profile_field, name='save_profile_field'),

    path('create-draft/', create_draft, name='create_draft'),

    path('update_task_defense_field/', update_task_defense_field, name='update_task_defense_field'),

]
