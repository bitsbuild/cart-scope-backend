from rest_framework.decorators import api_view,authentication_classes
from user.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
@api_view(['POST'])
def create_user(request):
    user_data = request.data
    srlzr = UserSerializer(data=user_data)
    if srlzr.is_valid():
        user = srlzr.save()
        token,_ = Token.objects.get_or_create(user=user)
        return Response({
            "Status":"Account Creation Successful",
            "Username":str(request.data['username']),
            "Email":str(request.data['email']),
            "Token":str(token.key)
        },status=status.HTTP_200_OK)
    else:
        return Response({
            "Status":"Error",
            "Error":""
        },status=status.HTTP_400_BAD_REQUEST)
@api_view(['DELETE'])
@authentication_classes([IsAuthenticated])
def delete_user(request):
    try:
        request.user.delete()
        return Response(
            {
                "Status":"Account Deletion Successful"
            },status=status.HTTP_200_OK
        )
    except Exception as error:
        return Response({
            "Status":"Account Deletion Failed",
            "Error":str(error)
            },status=status.HTTP_400_BAD_REQUEST)