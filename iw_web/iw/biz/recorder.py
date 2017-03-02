from ..models import QuesRecord
from ..utils import get_user

def record(requset,ques, is_right):
    print(">>>>做题记录")
    print(ques)
    print(">>>>结果:" + str(is_right))
    user = get_user(requset)
    QuesRecord.objects.save(user=user,word_id=ques['word_id'], ques_type=ques['ques_type'], is_right=is_right)
