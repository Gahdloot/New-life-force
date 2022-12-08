import requests

# for verification, we use identitypass Api for verifying users data

class Verify:
    URL = 'https://sandbox.myidentitypass.com/api/v2/biometrics/merchant/data/verification/bvn_validation'
    HEADERS = {
    'Accepts': 'application/json',
    'x-api-key': 'test_ucc8c5fyl6rl78idn3lqjp:ogINip3R6hrzzARkTI42vv13ybY',
    'app-id': 'e9265dad-9424-420c-8290-e0b19a7944d7'
}

    def bvn_verification(self,**kwargs):
        response = requests.post(Verify.URL, data=kwargs, headers=Verify.HEADERS)

        if response.json()['status'] == True and response.json()['verification']["status"] == "VERIFIED":
            return True
        return False


    def nin_verification(self, **kwargs):
        response = requests.post(Verify.URL, data=kwargs, headers=Verify.HEADERS)

        if response.json()['status'] == True and response.json()['verification']["status"] == "VERIFIED":
            return True
        return response.json()

    def cac_verification(self, **kwargs):
        response = requests.post(Verify.URL, query=kwargs, headers=Verify.HEADERS)

        if response.json()['status'] == True and response.json()['verification']["status"] == "VERIFIED":
            return True
        return False



# vr = Verify()
# print(vr.nin_verification(number='AA1234567890123B', number_nin=2147483647))