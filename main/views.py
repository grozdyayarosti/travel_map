import json

from django.shortcuts import render
from django.views.generic import View, ListView
from django.http import JsonResponse
from django.contrib.auth import get_user, get_user_model
from .models import *


class FetchHandler(View):

    def get(self, request):
        all_users = get_user_model()
        all_users = list(all_users.objects.values())
        print(all_users)
        user_context = request.user
        curr_user = request.user.id
        if request.GET.get('user_search') != "":
            user = get_user_model()
            user = list(user.objects.filter(username=request.GET.get('user_search')).values())
            if len(user) != 0:
                curr_user = user[0]['id']
                user_context = user[0]['username']

        content_list = list(Mark.objects.filter(user_id=curr_user).values('content_id'))
        content_indexes = [elem['content_id'] for elem in content_list]

        content = list(Content.objects.filter(id__in=content_indexes).values('id', 'title', 'description'))
        photos = list(Photo.objects.filter(content_id__in=content_indexes).values('id', 'photo', 'content_id'))

        marks = list(Mark.objects.filter(user_id=curr_user).values('latitude', 'longitude', 'content_id',
                                                                              'user_id'))
        context = {
            'marks': marks,
            'content': content,
            'photos': photos,
            'user_context': user_context,
            'users_list': all_users
        }

        # if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        #     return JsonResponse({'Uknown': 1})
        # #print(request.user.id)
        return render(request, 'main/index.html', context)

    def post(self, request):
        # Получаем значения из ответа
        values = json.loads(request.body.decode('utf-8'))

        user = get_user(request)
        #
        content = Content.objects.create(title=values['title'], description=values['description'])
        for source in values['sources']:
            Photo.objects.create(photo=source, content_id=content)
        Mark.objects.create(latitude=values['lat'], longitude=values['lng'], user_id=user, content_id=content)


        print('Выполнение POST-запроса')

        return JsonResponse({'val': 'data'}, status=200)
        # print(f)
        # return JsonResponse()


class Search(ListView):
    template_name = 'templates/index.html'
    def get_queryset(self):
        print(self.request.GET.get('user_search'))
        #user = get_user()
        return Mark.objects.filter(user_id=self.request.GET.get('user_search'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_search'] = Mark.objects.filter(user_id=self.request.GET.get('user_search'))
        print(context)
        return context

# def index(request):
#     # №context = {'marks': list(Mark.objects.values('latitude', 'longitude', 'content_id', 'user_id'))}
#     # print(context)
#     return render(request, 'main/index.html')


# def about(request):
#     return render(request, 'main/add.html')
