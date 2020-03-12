from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import  PostSerializers,CommentSerializer
from .models import Post,Comment
# from blog.utils.utils import convert_date


################################ create post request for a user ###################################
from blog.utils.utils import convert_date


class Posts(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        try:
            params = request.data
            serializer = PostSerializers(data=params)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user)
                return Response({"message": "successfully created"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Bad Json"}, status=status.HTTP_400_BAD_REQUEST)



########################## List of data(post) of current user ###################################

    def get(self, request):
        try:
            user = request.user
            get_post = Post.objects.filter(user=user)
            serializer = PostSerializers(get_post, many=True)
            return Response({"message": "user data", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

########################## update specific post of current user ###################################

    def put(self, request, id):
        try:
            post = Post.objects.get(id=id)
            if post.user == request.user:
                '''Partial updates By default, serializers must be passed values for all required fields or they will raise validation errors'''
                serializer = PostSerializers(post, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"message":"updated successfuly","data": serializer.data}, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)



################# Filter acc. to particular dates for a current user else return all data(current user) #######################

class Filter_Post(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args):
        try:

            user=request.user
            post = Post.objects.filter(user=user)
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')

            if start_date and end_date:
                starting_dates = convert_date(start_date)
                ending_dates = convert_date(end_date)

                if starting_dates <= ending_dates:
                    date = Post.objects.filter(created_post__range=[starting_dates, ending_dates], user=request.user)
                    serializer = PostSerializers(date, many=True)
                    return Response({"message": "Post according to dates", "data": serializer.data},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({"message": "end date must be greater than start date"},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = PostSerializers(post, many=True)
                return Response({"message": "all Data", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


############################ Filter post(data) acc. to current week for a current user ####################################

import datetime

class week(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self,request):
        try:

            today = datetime.date.today()
            dates = [today + datetime.timedelta(days=i) for i in range(0 - today.weekday(), 7 - today.weekday())]
            start_date = dates[1]
            end_date =dates[len(dates)-1]
            post=Post.objects.filter(created_post__range=[start_date,end_date],user=request.user)
            serializer=PostSerializers(post,many=True)
            return Response({"message":"success","data":serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

##################################### Comment on other's post ###########################################

class Post_Comment(APIView):
    permission_classes = [IsAuthenticated,]
    def post(self,request):
        try:
            try:
                post_id=request.data.get('post')
                post_id_exist=Post.objects.get(id=post_id) #checking post exist then go further else no.
            except Exception as e:
                return Response({"message": "post doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)


            serializer=CommentSerializer(data=request.data,partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user)
                return Response({"message":"comment successfull"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": "something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

