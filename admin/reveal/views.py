from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


import time
import datetime
import sys
import os

from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract

sys.path.append(os.path.abspath('..'))

from polls.models import Question, Choice 


def _pollActive(pubTime):
	now = timezone.now()
	return now <= pubTime

@csrf_exempt
def revealvote(request, poll_id, nounce, vote):
	# get question object
	question = get_object_or_404(Question, pk=poll_id)

	publishDate = question.pub_date

	if _pollActive(publishDate):
		return HttpResponse('poll is still active, '+
							'cannot reveal vote now.', content_type='text/plain')
	
	# need to send the poll to blockchain
	print(poll_id, nounce, vote)

	contract_abi = pickle.load(open("../conf/" + str(poll_id) + "contract_abi', 'rb'))
	contract_address = pickle.load(open("../conf/" + str(poll_id) + "contract_address', 'rb'))
	ConciseContract = pickle.load(open("../conf/" + str(poll_id) + "ConciseContract', 'rb'))

	contract_instance = eth_provider.contract(
		abi=contract_abi,
		address=contract_address,
		ContractFactoryClass=ConciseContract,
	)

	default_account = eth_provider.accounts[0]
	
	transaction_details = {
		'from': default_account,
	}

	nonce = nounce.encode().hex()
	hexvote = hex(vote)[2:]
	if (vote < 16):
		hexvote = '0' + hexvote
		
	revealval = '0x' + nonce + hexvote

	contract_instance.revealVote(revealval, transact=transaction_details)

	return HttpResponse('your vote has been reveal in blockchain, '+
							'hold back for results :)', content_type='text/plain')