import json

from django.views import View
from django.http import JsonResponse

from .models import Post
from users.decorator import login_decorator

class PostView(View):
    @login_decorator
    def post(self, request):
        try:
            data    = json.loads(request.body)
            user    = request.user
            title   = data['title']
            content = data['content']

            post = Post.objects.create(
                username = user.name,
                title    = title,
                content  = content,
                user     = user
            )

            Result = {
                "title"     : post.title,
                "username"  : user.name,
                "content"   : post.content,
                "created_at": post.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }

            return JsonResponse({"MESSAGE":"CREATE", "data":Result}, status=201)
    
        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status=400)

    def get(self, request, post_id):
        if not Post.objects.filter(id=post_id).exists():
            return JsonResponse({"MESSAGE":"DOES_NOT_EXIST"}, status=404)
        
        post = Post.objects.get(id=post_id)

        Result = {
            "username"  : post.username,
            "title"     : post.title,
            "content"   : post.content,
            "created_at": post.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }

        return JsonResponse({"Result":Result}, status=200)

    @login_decorator
    def patch(self, request, post_id):
        try:
            if not Post.objects.filter(id=post_id).exists():
                return JsonResponse({"MESSAGE":"DOES_NOT_EXIST"}, status=404)
            if not request.user == Post.objects.get(id=post_id).user:
                return JsonResponse({"MESSAGE":"NOT_MATCHED_USER"}, status=400)

            data    = json.loads(request.body)
            content = data['content']
            post    = Post.objects.filter(id=post_id, username=request.user.name)
            post.update(content=content)
            
            return JsonResponse({"MESSAGE":"SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status=400)

    @login_decorator
    def delete(self, request, post_id):
        if not Post.objects.filter(id=post_id).exists():
            return JsonResponse({"MESSAGE":"DOES_NOT_EXIST"}, status=404)
        if not request.user == Post.objects.get(id=post_id).user:
            return JsonResponse({"MESSAGE":"NOT_MATCHED_USER"}, status=403)
        post = Post.objects.filter(id=post_id, username=request.user.name)
        post.delete()
        
        return JsonResponse({"MESSAGE":"DELETE"}, status=204)

class PostlistView(View):        
    def get(self, request):
        limit  = int(request.GET.get("limit",3))
        offset = int(request.GET.get("offset",0))
        posts  = Post.objects.all()

        Result = [{
            "username"  : post.username,
            "title"     : post.title,
            "content"   : post.content,
            "created_at": post.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }for post in posts]
        
        Result = Result[offset:offset+limit]
        count = len(Result)

        return JsonResponse({"count":count, "Result":Result}, status=200)