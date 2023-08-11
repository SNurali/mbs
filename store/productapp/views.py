from django.shortcuts import render
import json

from .models import Tag, Product, Review
from .serializers import TagsSerializer, ProductSerializer, ReviewSerializer

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status


class TagsView(APIView):
	def get(self, request: Request) -> Response:
		tags = Tag.objects.all()
		serialized = TagsSerializer(tags, many=True)

		return Response(data=serialized.data, status=status.HTTP_200_OK)


class ProductView(APIView):
	def get(self, request: Request, pk) -> Response:
		product = Product.objects.get(id=pk)
		serialized = ProductSerializer(product)

		return Response(data=serialized.data, status=status.HTTP_200_OK)


class ProductReviewView(APIView):
	def post(self, request: Request, pk) -> Response:
		product = Product.objects.get(id=pk)

		if product:
			data = json.loads(request.body)
			author = data['author']
			if not author:
				author = 'Без имени'
			email = data['email']
			text = data['text']
			rate = data['rate']

			Review.objects.create(
				product=product,
				author=author,
				email=email,
				text=text,
				rate=rate
			)
			reviews = Review.objects.filter(product=pk)
			serialized = ReviewSerializer(reviews, many=True)

			return Response(data=serialized.data, status=status.HTTP_200_OK)

		return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)