#import
from django.core.paginator import Paginator
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from .models import Article, Comment
from .forms import CommentForm
from django.db.models import Q
from django.views import generic
from django.views.generic import ListView
 
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
##############################################################

#一覧
class IndexView(generic.ListView):
    model = Article

    paginate_by = 10

    #検索
    def get_queryset(self):
        q_word = self.request.GET.get('query')
 
        # チェックボックスにチェックが入っている項目だけを検索対象とする
        selected_title = self.request.GET.get('title')
        selected_article = self.request.GET.get('article')
 
        if q_word:
            if selected_title and selected_article:
                object_list = Article.objects.filter(
                    Q(title__icontains=q_word) | Q(content__icontains=q_word))
            elif selected_title:
                object_list = Article.objects.filter(Q(title__icontains=q_word))
            else: # 投稿内容のみ、または両方ともチェックされていない場合は投稿内容のみを検索する
                object_list = Article.objects.filter(Q(content__icontains=q_word))
        else:
            object_list = Article.objects.all()
 
        return object_list
 
#詳細
class DetailView(generic.DetailView):
    model = Article

    #返信機能部分
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # テンプレートにコメント作成フォームを渡す
        context['comment_form'] = CommentForm
 
        return context

#投稿
class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Article
    fields = ['content', 'title', ]
 
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)

#編集
class UpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Article
    fields = ['content', 'title', ]
 
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
 
        if obj.author != self.request.user:
            raise PermissionDenied('You do not have permission to edit.')
 
        return super(UpdateView, self).dispatch(request, *args, **kwargs)

#削除
class DeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Article
    success_url = reverse_lazy('bbs:index')

#返信
class CommentView(LoginRequiredMixin, generic.edit.CreateView):
    model = Comment
    form_class = CommentForm
 
    #格納する値をチェック
    def form_valid(self, form):
        form.instance.author = self.request.user
        article_pk = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_pk)
 
        comment = form.save(commit=False)
        comment.target = article
        comment.save()
 
        return redirect('bbs:detail', pk=article_pk)