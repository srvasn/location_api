from rest_framework.authentication import BasicAuthentication, SessionAuthentication

# __author__ = 'Sourav Banerjee'
# __email__ = ' srvasn@gmail.com'

class QuietBasicAuthentication(BasicAuthentication):
    # Makes BasicAuthentication quieter :P
    def authenticate_header(self, request):
        return 'xBasic realm="%s"' % self.www_authenticate_realm
