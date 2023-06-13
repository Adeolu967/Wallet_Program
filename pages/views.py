from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from .models import UserProfile
import requests
from web3 import Web3

# Create your views here.

def home(request):
    return render(request, "index.html")


def register(request):
    if request.method == 'POST':
        uname = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']

        if password==password2:       
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=uname).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=uname, email=email, password=password)
                user.save();
                print('User Created')
                return redirect('login')

        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
        
        return redirect('wallet')

    else:
        return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')

        print(username)
        print(password)

        user = auth.authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('wallet')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    else:
        return render(request, 'login.html')

# def Login(request):
#     if request.method=='POST':
#         username =request.POST.get('username')
#         pass1 = request.POST.get('password1')
#         user = authenticate(request, username=username, password=pass1)

#         if user is not None:
#             login(request, user)
#             return redirect('wallet')
#         else:
#             messages.info(request, 'Invalid Credentials')
#             return redirect('login')        
#     return render(request, 'login.html')

def get_crypto_prices():
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': 'bitcoin,ethereum,tether,sandbox,bnb,elrond,polkadot,litecoin,uniswap,shiba-inu,cardano,solana',  # Add the desired cryptocurrency symbols separated by commas
        'vs_currencies': 'usd',
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    return {}


@login_required(login_url='login')
def wallet(request):
    prices = get_crypto_prices()
    return render(request, "wallet.html", {'prices': prices})



@login_required(login_url='login')
def about(request):
    return render(request, "about.html")


@login_required(login_url='login')
def buy(request):
    return render(request, "buy.html")


@login_required(login_url='login')
def detail(request):
    return render(request, "details.html")


@login_required(login_url='login')
def sell(request):
    return render(request, "sell.html")


@login_required(login_url='login')
def user_profile(request):
    return render(request, "user-profile.html")


@login_required(login_url='login')
def transfer(request):
    return render(request, "transfer.html")


@login_required(login_url='login')
def contact(request):
    return render(request, "contact.html")


@login_required(login_url='login')
def list(request):
    prices = get_crypto_prices()
    return render(request, "list.html", {'prices': prices})


@login_required(login_url='login')
def main(request):
    prices = get_crypto_prices()
    return render(request, "main.html", {'prices': prices})


# Trust Wallet Payment Integration
def trust_wallet_integration(request):
    # Connect to the Ethereum network using Infura's HTTP provider
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/a2dfb0a97549491a8264f29dd6a707d3'))

    # Define the contract address and ABI
    contract_address = '0x123456789abcdef...'
    contract_abi = [
        # Contract ABI definitions
        # ...
    ]

    # Create an instance of the contract
    contract = w3.eth.contract(address=contract_address, abi=contract_abi)

    # Get the account balance
    account_address = '0xabcde...'
    account_balance = w3.eth.get_balance(account_address)

    # Simulate sending a transaction
    destination_address = '0x987654321abcdef...'
    transaction = contract.functions.transfer(destination_address, 1).buildTransaction({
        'from': account_address,
        'gas': 200000,
        'gasPrice': w3.toWei('50', 'gwei'),
        'nonce': w3.eth.getTransactionCount(account_address),
    })

    # Sign the transaction with the account's private key
    private_key = '0x123456789abcdef...'
    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)

    # Send the signed transaction to the Ethereum network
    transaction_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction).hex()

    # Render the response
    return render(request, 'trust_wallet_integration.html', {
        'account_balance': account_balance,
        'transaction_hash': transaction_hash,
    })
