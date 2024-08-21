from kavenegar import *
from django.contrib.auth.mixins import UserPassesTestMixin


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('6D352B436531784A4B4D7751526438483930714E58495655317255776737526C767057674E2B35687678413D')
        params = {
            'sender': '',  #optional
            'receptor': f'{phone_number}',  # multiple mobile number, split by comma
            'message': f'کد تایید شما : {code}',
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


class UserIsAdmin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin
