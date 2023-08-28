#import
from django.db import models
from django.urls import reverse
 
from django.conf import settings
from django.core.mail import EmailMessage
import asyncio
import os
 
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
##############################################################

#一次コメントモデル
class Article(models.Model):
    title = models.CharField(verbose_name='タイトル', max_length=200, null = True, )
    content = models.TextField(verbose_name='本文', max_length=1000, )
 
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        null = True
    )

    class Meta:
        ordering = ['-updated_at'] # 降順ソート
 
    created_at = models.DateTimeField(auto_now_add=True, null = True)
    updated_at = models.DateTimeField(auto_now=True, null = True)
 
    def __str__(self):
        return self.content
 
    def get_absolute_url(self):
        asyncio.run(self.send_email())
        return reverse('bbs:detail', kwargs={'pk': self.pk})
 
    #投稿内容のメール確認
    async def send_email(self):
        subject = '投稿通知'
        message = '【タイトル】：' + self.title + '\n'
        message += '【投稿者】：' + str(self.author) + '\n'
        message += '【本文】：' + '\n' + self.content
 
        email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, ['s21c1032@gmail.com'])
        email.send()

#返信機能
class Comment(models.Model):
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    target = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
    )
    content = models.TextField('コメント')
    created_at = models.DateTimeField(auto_now_add=True)