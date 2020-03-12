from django.shortcuts import render
from rest_framework.pagination import LimitOffsetPagination

from .models import MyUser
# from .serializers import MyUserSerializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.db.models import Q
from django.core.mail import EmailMessage
from rest_framework import pagination
from .services import prepare_activation_link, verifyOtpOrHash

from .enums import TokenType
from .models import Token
# Create your views here.
from .serializers import MyUserSerializers
#
# from utils.utils import convert_date


########################  User Sign Up (Mail send to admin when new user signed up##################################33
class CreateUser(APIView):

    def post(self, request):
        try:
            params = request.data
            print(params)
            serializer = MyUserSerializers(data=params)
            print(serializer, 'user_detail')
            # admin=MyUser.objects.get(pk=1)
            # print(admin,'adminnn')
            # email = EmailMessage('Hello', 'New User Signed Up', to=[admin])

            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                user.set_password(params['password'])
                user.save()
                # prepare_activation_link(user, TokenType.EMAIL_VERIFICATION)
                # print(prepare_activation_link(),'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

                #             # email.send()
                # print(email_obj,'email_objjjj')

                return Response({
                    "message": "signup successfully, Activation link has been sent to your email Please confirm Your Email."},
                    status=status.HTTP_200_OK, content_type='application/json')
        except Exception as e:
            print(e)
            return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

#######################Login using JWT#############################

class UserLogin(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        try:
            params = request.data
            user_exist = MyUser.objects.get(email=params['email'])
            print(user_exist, 'user_exist')

            if not user_exist:
                return Response({"message": "Signup First"}, status=400)
            user = authenticate(email=params['email'], password=params['password'])
            if user:
                serializer = MyUserSerializers(user)
                login(request, user)
                return Response(
                    {"message": "Logged in successfully.", "data": serializer.data, "token": user.create_jwt()},
                    status=status.HTTP_200_OK)
            else:
                return Response({"message": "Please enter correct credentials"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)



#############################  Get all user  ###########################################
class Get_all_user(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            userobj = MyUser.objects.all()
            paginator = LimitOffsetPagination()
            result_page = paginator.paginate_queryset(userobj, request)

            serializer = MyUserSerializers(result_page, many=True)
            return Response({"message": "All user data", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

########################## user logout ##################################

class UserLogout(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            logout(request)
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

###################### search user acc. to name email #############################

class Search(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            SearchKeyword = request.GET['SearchKeyword']
            query = MyUser.objects.filter(Q(email__icontains=SearchKeyword) | Q(first_name__icontains=SearchKeyword))
            serializer = MyUserSerializers(query, many=True)
            return Response({"message": "All user data", "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

######################### send mail (smtp) ######################################

class SendMail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        params = request.GET['email']
        print(params, 'emaillll')
        try:
            user_exist = MyUser.objects.get(email=params)
            print(user_exist, 'user_exist')
            if user_exist:
                email = EmailMessage('Hello', 'World', to=[params])
                print(email, 'emaillllll')
                return Response(email.send(), status=status.HTTP_200_OK)

        except MyUser.DoesNotExist as e:
            print(e)
            return Response({'message': "not found"}, status=status.HTTP_200_OK)


########################## Reset Password of current user #############################

class UserChangePassword(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        try:
            user_email = request.user.email
            params = request.data
            current_password = params['current_password']
            new_password = params['new_password']
            confirm_new_password = params['confirm_new_password']

            if not new_password == confirm_new_password:
                return Response({"message": "New password and Confirm password is not matching."},
                                status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(email=user_email, password=current_password)
            if user == None:
                return Response({"message": "Current password dosen't match with old password"},
                                status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password changed successfuly"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
        return Response({"message": "Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
