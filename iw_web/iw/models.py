from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from .utils import get_now_time


class WordManager(models.Manager):
    def save(self, user, fromLang, toLang, definition, phonetic, word, audio, sentence, trans):
        Word(
            user=user,
            fromLang=fromLang,
            toLang=toLang,
            definition=definition,
            phonetic=phonetic,
            word=word,
            audio=audio,
            sentence=sentence,
            trans=trans,
        ).save()

    def get_user_word_count(self, user):
        return self.filter(user=user).count()

    def get_user_word_list(self, user):
        return self.filter(user=user).all()

    def get_word_list(self):
        return self.all()

    def get_random_user_words(self, user, count):
        return self.get_user_word_list(user).order_by('?')[:count]

    def get_random_user_words_except_word(self, user, word_id, count):
        return self.get_user_word_list(user).exclude(id=word_id).order_by('?')[:count]

    def get_word(self, word_id):
        return self.get(id=word_id)

    def update_word_is_known(self, word_id, is_known):
        if int(is_known) > 2 or int(is_known) < 0:
            raise Exception("is_know must be 0,1,2")
        return self.filter(id=word_id).update(is_known=is_known, mark_time=get_now_time())

    def delete_all(self, user):
        self.get_user_word_list(user).delete()


    def dump_ml_training_log(self, user, max_record_size):
        word_list = self.get_word_list()
        dump_log_list = []
        for word in word_list:
            is_known = word.is_known
            if is_known is not 0:
                mark_time = word.mark_time
                ques_list = QuesRecord.objects.get_user_ques_record_list(user, word, mark_time)[:max_record_size]
                if ques_list:
                    dump_log = {}
                    dump_log["word_id"] = word.id
                    dump_log["is_known"] = is_known
                    dump_log["mark_time"] = mark_time
                    ques_record_log = []
                    for ques_record in ques_list:
                        ques_record_log.append({
                            "ques_type": ques_record.ques_type,
                            "record_time": ques_record.record_time,
                            "is_right": ques_record.is_right
                        })
                    dump_log["ques_record_log"] = ques_record_log
                    dump_log_list.append(dump_log)
        return dump_log_list


    def dump_ml_forecast_log(self, user, max_record_size):
        word_list = self.get_word_list()
        dump_log_list = []
        for word in word_list:
            is_known = word.is_known
            if is_known is not 0:
                ques_list = QuesRecord.objects.get_user_ques_record_list(user, word)[:max_record_size]
                if ques_list:
                    dump_log = {}
                    dump_log["word_id"] = word.id
                    dump_log["is_known"] = is_known
                    dump_log["mark_time"] = get_now_time()
                    ques_record_log = []
                    for ques_record in ques_list:
                        ques_record_log.append({
                            "ques_type": ques_record.ques_type,
                            "record_time": ques_record.record_time,
                            "is_right": ques_record.is_right
                        })
                    dump_log["ques_record_log"] = ques_record_log
                    dump_log_list.append(dump_log)
        return dump_log_list

class Word(models.Model):
    user = models.ForeignKey(User)
    fromLang = models.CharField(max_length=5)
    toLang = models.CharField(max_length=5)
    definition = models.CharField(max_length=100, blank=True, default='')
    phonetic = models.CharField(max_length=100, blank=True, default='')
    word = models.CharField(max_length=100, blank=True, default='')
    audio = models.CharField(max_length=100, blank=True, default='')

    sentence = models.CharField(max_length=200, blank=True, default='')
    trans = models.CharField(max_length=200, blank=True, default='')

    # 0 默认值 1 认识 2 不认识
    is_known = models.IntegerField(default=0)
    # 标记是否认识的时间
    mark_time = models.FloatField(max_length=20, default=get_now_time())

    objects = WordManager()

    class Meta:
        ordering = ('word',)

    def save(self, *args, **kwargs):
        super(Word, self).save(*args, **kwargs)

    def __str__(self):
        return self.word


class QuesRecordManager(models.Manager):
    def save(self, user, word_id, ques_type, is_right):
        word = Word.objects.get_word(word_id)
        QuesRecord(user=user, word=word, ques_type=ques_type, record_time=get_now_time(), is_right=is_right).save()

    def delete_all(self,user):
        self.filter(user=user).all().delete()

    def get_user_ques_record_list(self, user, word, before_time=get_now_time()):
        return self.order_by("-record_time").filter(user=user, word=word, record_time__lt=before_time)


class QuesRecord(models.Model):
    user = models.ForeignKey(User)
    word = models.ForeignKey(Word)
    ques_type = models.CharField(max_length=10, blank=True, default='')
    record_time = models.FloatField(max_length=20, default=get_now_time())
    is_right = models.BooleanField(default=True)

    objects = QuesRecordManager()

    class Meta:
        ordering = ('record_time',)
