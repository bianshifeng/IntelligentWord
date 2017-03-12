from django.conf.urls import url, include
from .views import api, data_manager, ques, mark, test, index, regist, help
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title='Pastebin API')

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'words', api.WordViewSet)
router.register(r'ques_record', api.QuesRecordViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.

urlpatterns = [
    url('^schema/$', schema_view),
    url(r'^api/', include(router.urls)),
    url('', include('django.contrib.auth.urls')),

    url(r'^regist/$', regist.regist,name="regist"),
    url(r'^user_logout/$', regist.user_logout,name="user_logout"),

    url(r'^index/', index.index, name="index"),

    url(r'^data/$', data_manager.index, name="data_manager_index"),
    url(r'^init/data/', data_manager.init, name="init"),
    url(r'^clear_words/data/', data_manager.clear_words, name="clear_words"),
    url(r'^clear_records/data/', data_manager.clear_records, name="clear_records"),
    url(r'^dump_origin_data/data/(?P<max_record_size>[0-9]+)/', data_manager.dump_origin_data, name="dump_origin_data"),
    url(r'^dump_processed_data/data/(?P<max_record_size>[0-9]+)/', data_manager.dump_processed_data, name="dump_processed_data"),
    url(r'^dump_train_test_nparray_data/data/(?P<max_record_size>[0-9]+)/', data_manager.dump_train_test_nparray_data, name="dump_train_test_nparray_data"),
    url(r'^dump_forecate_nparray_data/data/(?P<max_record_size>[0-9]+)/', data_manager.dump_forecate_nparray_data, name="dump_forecate_nparray_data"),
    url(r'^training/data/(?P<max_record_size>[0-9]+)/', data_manager.training, name="training"),
    url(r'^ques/ques_list/(?P<size>[0-9]+)/', ques.ques_list, name="ques_list"),
    url(r'^ques/start_exercise/(?P<size>[0-9]+)/', ques.start_exercise, name="start_exercise"),
    url(r'^ques/end_exercise/', ques.end_exercise, name="end_exercise"),
    url(r'^ques/answer/(?P<option_pos>[0-9]+)/', ques.answer, name="answer"),
    url(r'^mark/word_list/', mark.word_list, name="word_list"),
    url(r'^mark/word_list_mark_is_known/(?P<word_id>[0-9]+)/(?P<is_known>[0-9]+)/', mark.word_list_mark_is_known, name="word_list_mark_is_known"),
    url(r'^mark/word_detail/(?P<word_id>[0-9]+)/', mark.word_detail, name="word_detail"),
    url(r'^mark/mark_is_known/(?P<word_id>[0-9]+)/(?P<is_known>[0-9]+)/', mark.mark_is_known, name="mark_is_known"),
    url(r'^help/', help.help, name="help"),

    url(r'^test/', test.test, name="test"),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
