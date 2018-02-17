from django.shortcuts import render
from api.models import DiGraph
from api.serializers import DiGraphSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from django.http import JsonResponse
import json
from django.contrib.auth.models import User


def home(request):
    return render(request, 'api/index.html')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None):
        if pk == 'i':
            return Response(UserSerializer(request.user,
                context={'request':request}).data)
        return super(UserViewSet, self).retrieve(request, pk)

class DiGraphList(APIView):

    def get(self, request, format=None):
        graphs = DiGraph.objects.all()
        serializer = DiGraphSerializer(graphs, many=True)
        return Response(serializer.data)


def add_node(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        name = data['name']
        graph = DiGraph.objects.get(pk=data['graph'])
        graph.add_node(name)
        graph.save()
        return JsonResponse({'message': 'success'})
    return JsonResponse({status: status.HTTP_400_BAD_REQUEST})


def delete_node(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        graph = DiGraph.objects.get(pk=data['graph'])
        node = graph.nodes.all().get(pk=data['node'])
        graph.delete_node(node)
        graph.save()
        return JsonResponse({'message': 'deleted'})
    return JsonResponse({status: status.HTTP_400_BAD_REQUEST})


def add_edge(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        graph = DiGraph.objects.get(pk=data['graph'])
        parent = graph.nodes.get(name=data['parent'])
        child = graph.nodes.get(name=data['child'])
        graph.add_edge(parent, child)
        graph.save()
        return JsonResponse({'message': 'success'})
    return JsonResponse({status: status.HTTP_400_BAD_REQUEST})


def delete_edge(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        graph = DiGraph.objects.get(pk=data['graph'])
        parent = graph.nodes.all().get(pk=data['parent'])
        child = graph.nodes.all().get(pk=data['child'])
        graph.remove_edge(parent, child)
        graph.save()
        return JsonResponse({'message': 'deleted'})
    return JsonResponse({status: status.HTTP_400_BAD_REQUEST})
