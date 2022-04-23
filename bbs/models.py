from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):

    name    = models.CharField(verbose_name="カテゴリ名",max_length=20)

    #category検索時、requestオブジェクト内の値とidの型が不一致でselectedされないので、str型を返すメソッドで判定する
    def str_id(self):
        return str(self.id)

    """
    def __str__(self):
        return self.name
    """



class Topic(models.Model):

    category    = models.ForeignKey(Category,verbose_name="カテゴリ",on_delete=models.CASCADE)
    comment     = models.CharField(verbose_name="コメント",max_length=2000)

    #defaultありのモデルのフィールド追加
    #→テンプレートに表示だけさせれば良い {{ topic.dt }}
    dt = models.DateTimeField(verbose_name="投稿日時", default=timezone.now)

    image = models.ImageField(verbose_name="画像",upload_to="bbs/topic/image/",null=True,blank=True)


    #defaultなしのモデルのフィールド追加(Null禁止、default無しなので、マイグレーション時に警告が出る)
    #→フォーム(バリデーション対象のフィールド)とテンプレート(入力欄、{{ topic.name }})も追加する
    #name = models.CharField(verbose_name="名前", max_length=100)

    #TODO:↑のnameは廃止、userと紐付ける(1対多のリレーションを組む)フィールドをここに作る
    #https://noauto-nolife.com/post/django-models-foreignkey/

    user = models.ForeignKey(User, verbose_name="投稿者", on_delete=models.CASCADE, null=True,blank=True)


    def reply_amount(self):
        return Reply.objects.filter(topic=self.id).count()

    def __str__(self):
        return self.comment


class Reply(models.Model):

    topic   = models.ForeignKey(Topic,verbose_name="リプライ対象のトピック",on_delete=models.CASCADE)
    comment = models.CharField(verbose_name="コメント",max_length=2000)
    user    = models.ForeignKey(User, verbose_name="投稿者", on_delete=models.CASCADE, null=True,blank=True)

    def __str__(self):
        return self.comment