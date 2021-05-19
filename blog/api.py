from django.http import HttpResponse, JsonResponse
from django.http.response import Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, mixins, generics, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, action
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Comment, Category, PostSetting
from .serializer import PostSerializer, CommentSerializer, CategorySerializer, PostSetSerializer


class PostViewModel(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # authentication_classes = [ BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["GET"])
    def comments(self, request, pk=None):
        posts = self.get_object()
        comments = posts.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["POST"])
    def publish(self, request, pk=None):
        posts = self.get_object()
        posts.draft = False
        posts.save()
        serializer = self.get_serializer(posts)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def get_published(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(draft=False)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewModel(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @action(detail=False, methods=["GET"])
    def not_confirm(self, request):
        comments = Comment.objects.filter(is_confirmed=False)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["GET"])
    def confirm(self, request):
        comments = Comment.objects.filter(is_confirmed=True)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    


class CategoryViewModel(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=False, methods=["GET"])
    def main_category(self, request):
        mc = Category.objects.filter(parent=None)
        serializer = CategorySerializer(mc, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["GET"])
    def sub_category(self, request):
        subcat = Category.objects.exclude(parent=None)
        serializer = CategorySerializer(subcat, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=["GET"])
    def all_category(self, request):
        cat = Category.objects.all()
        serializer = CategorySerializer(cat, many=True)
        return Response(serializer.data)


class PostSetViewModel(viewsets.ModelViewSet):
    queryset = PostSetting.objects.all()
    serializer_class = PostSetSerializer












































# class PostList1(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

# class PostDetail1(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#
# class PostList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class PostDetail(mixins.RetrieveModelMixin,
#                  mixins.UpdateModelMixin,
#                  mixins.DestroyModelMixin,
#                  generics.GenericAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
#
#
# class PostView(APIView):
#     def get(self, request, format=None):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class PostDetailView(APIView):
#     def get_object(self, pk):
#         try:
#             return Post.objects.get(pk=pk)
#         except Post.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         post = self.get_object(pk)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# @csrf_exempt
# @api_view(['GET', 'POST'])
# def post_list(request):
#     if request.method == "GET":
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @csrf_exempt
# @api_view(['GET', 'PUT', 'DELETE'])
# def post_detail(request, pk):
#     try:
#         post = Post.objects.get(pk=pk)
#     except Post.DoesNotExist:
#         return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == 'GET':
#         serializer = PostSerializer(post)
#         return JsonResponse(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# @csrf_exempt
# def comment_list(request):
#     if request.method == "GET":
#         comments = Comment.objects.all()
#         seriallizer = CommentSerializer(comments, many=True)
#         return JsonResponse(seriallizer.data, safe=False)
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = CommentSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)
#
#
# @csrf_exempt
# def comment_detail(request, pk):
#     try:
#         comment = Comment.objects.get(pk=pk)
#     except Comment.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = CommentSerializer(comment)
#         return JsonResponse(serializer.data)
#
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = CommentSerializer(comment, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         comment.delete()
#         return HttpResponse(status=204)
