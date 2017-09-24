# api/views.py

from rest_framework import generics
from .serializers import TopTokenHolderSerializer,TopTokenTransactionsSerializer
from polls.models import TopTokenHolder,TopTokenTransaction,Account,Token
from polls.views import get_all_transaction_data_for_a_token
from dateutil import parser
from django.http import JsonResponse,HttpResponse
import requests
from polls.tasks import get_ether_delta_inout_for_zrx

class RetriveTopTokenHolderView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = TopTokenHolder.objects.all()
    serializer_class = TopTokenHolderSerializer
    lookup_url_kwarg_time = "time"
    lookup_url_kwarg_token = "token"

    def get_queryset(self):
        timestamp_s = self.kwargs.get(self.lookup_url_kwarg_time)
        timestamp = parser.parse(timestamp_s)
        token_contract_address = self.kwargs.get(self.lookup_url_kwarg_token)
        token_obj = Token.objects.get(contract_address=token_contract_address)
        holders = TopTokenHolder.objects.filter(timestsamp=timestamp,token_name=token_obj)
        return holders

class RetriveTopTokenTransactionView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = TopTokenTransaction.objects.all()
    serializer_class = TopTokenTransactionsSerializer
    lookup_url_kwarg_time = "time"
    lookup_url_kwarg_token = "token"

    def get_queryset(self):
        timestamp_s = self.kwargs.get(self.lookup_url_kwarg_time)
        timestamp = parser.parse(timestamp_s)
        token_contract_address = self.kwargs.get(self.lookup_url_kwarg_token)
        token_obj = Token.objects.get(contract_address=token_contract_address)
        transactions = TopTokenTransaction.objects.filter(timestsamp=timestamp,token_name=token_obj)
        return transactions
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_account(request,account):
    memo = request.POST.get("memo",None)
    if memo is None:
        response = JsonResponse({'status':'false'}, status=400)
        return response
    account_obj = Account.objects.get(account_address=account)
    account_obj.gussed_name = memo
    account_obj.save()
    return JsonResponse({"status":"okay"})

from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
def add_token(request,token,token_name):
    if token is None or token == "":
        return JsonResponse({'status':'false','reason':'token not specified'},status=400)
    if token_name is None or token_name == "":
        return JsonResponse({'status': 'false', 'reason': 'token_name wrong'}, status=400)
    etherscan_api_url = "https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress={}&apikey=B4IFQIJ88Z36UYYRUHVRPTZ46HZ2S3FCCV".format(token)
    r = requests.get(etherscan_api_url)
    json_result = r.json()
    if json_result['result'] == "0":
        return JsonResponse({'status': 'false','reason':'token not found on etherscan'}, status=400)

    error = False
    try:
        dummy = Token.objects.get(contract_address=token)
        error = True
    except ObjectDoesNotExist:
        token_obj = Token(coin_name=token_name,contract_address=token)
        token_obj.status = "fetching_all_data"
        token_obj.save()
        get_all_transaction_data_for_a_token(token_name,token)

    if error:
        return JsonResponse({"status": "false", 'reason': 'token already exists'})
    else:
        return JsonResponse({"status": "okay"})
def get_all_tokens(request):
    tokens = Token.objects.all()
    results = []
    for token in tokens:
        results.append({"coin_name":token.coin_name,"contract_address":token.contract_address})
    return JsonResponse({'results': results})

from web3 import Web3, HTTPProvider, IPCProvider
web3 = Web3(HTTPProvider('http://localhost:8545'))

def get_etherdelta_input_for_zerox(request):
    first_block = 4306700
    last_block = web3.eth.blockNumber
    for block_number in range(first_block,last_block+1):
        print(block_number)
        get_ether_delta_inout_for_zrx.apply_async([block_number])
    return JsonResponse({"status": "okay"})
