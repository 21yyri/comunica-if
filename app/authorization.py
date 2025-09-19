from rest_framework.authentication import TokenAuthentication

class BearerTokenAuth(TokenAuthentication):
    keyword = 'Bearer'