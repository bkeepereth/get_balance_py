#!/usr/bin/env python
import requests
import os
import sys
import traceback
import logging
import datetime
import getopt
import json

import xml.etree.ElementTree as ET
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

def get_config(file_name):
    if (file_name=="" or file_name==None):
        raise Exception(str(datetime.datetime.now())+"|get_config|file_name is invalid|file_name="+str(file_name))

    result=dict()
    root=ET.parse(file_name).getroot()
    for prop in root.findall('property'):
        result[prop.find('name').text]=prop.find('value').text

    return result

def get_balance(log, config, address, network):
    log.info(str(datetime.datetime.now())+"|get_balance|starting")

    provider_url=""
    if (network=="mainnet"):
        provider_url=config.get("ALCHEMY_MAINNET_URL")
    elif (network=="ropsten"):
        provider_url=config.get("ALCHEMY_ROPSTEN_URL")
    elif (network=="rinkeby"):
        provider_url=config.get("ALCHEMY_RINKEBY_URL")
    else:
        raise Exception(str(datetime.datetime.now)+"|get_balance|network not supported")
   
    if (network=="rinkeby"):
        w3=Web3(HTTPProvider(provider_url))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    else:
        w3=Web3(HTTPProvider(provider_url))

    last_block=""
    chain_id=""
    balance=0.0

    try:
        last_block=w3.eth.get_block('latest')['number']
        chain_id=w3.eth.chain_id
        balance=w3.eth.getBalance(address)/pow(10,18)
    except:
        pass

    output=('''
    last_block : '''+str(last_block)+'''
    chain_id : '''+str(chain_id)+'''
    network : '''+str(network)+'''
    balance : '''+str(balance)+'''
    address : '''+str(address))

    print(output)
    log.info(output)

    log.info(str(datetime.datetime.now())+"|get_balance|completed")

def get_balance_etherscan(log, config, address, network):
    log.info(str(datetime.datetime.now())+"|get_balance_etherscan|starting")

    #test="https://api-ropsten.etherscan.io/api
    #?module=proxy
    #&action=eth_blockNumber
    #&apikey=YourApiKeyToken"

    network_prefix=""
    if (network=="mainnet"):
        network_prefix="https://api.etherscan.io"
    elif (network=="ropsten"):
        network_prefix="https://api-ropsten.etherscan.io"
    elif (network=="rinkeby"):
        network_prefix="https://api-rinkeby.etherscan.io"
    else:
        raise Exception(str(datetime.datetime.now()+"|get_balance_etherscan|network not supported"))

    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, ''like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    block_url="/api?module=proxy&action=eth_blockNumber&apikey="
    url=network_prefix+block_url+str(config.get("ES_KEY"))

    last_block=0
    try:
        response=requests.get(url,headers=headers)

        if (response!=None):
            data=json.loads(response.text).get("result")
            last_block=int(data,16)
    except:
        #pass
        traceback.print_exc()

    balance_url="/api?module=account&action=balance&address="+str(address)+"&tag=latest&apikey="+str(config.get("ES_KEY"))
    url=network_prefix+balance_url

    balance=0
    try:
        response=requests.get(url,headers=headers)

        if (response!=None):
            data=json.loads(response.text).get("result")
            balance=int(data)/pow(10,18)
    except:
        #pass
        traceback.print_exc()

    output=('''
    last_block : '''+str(last_block)+'''
    network : '''+str(network)+'''
    balance : '''+str(balance)+'''
    address : '''+str(address))

    print(output)
    log.info(output)

    log.info(str(datetime.datetime.now())+"|get_balance_etherscan|completed")


def usage():
    print('''Usage: ./get_balance.py -c config_path -a address -n network -i api
    -n [mainnet, ropsten, rinkeby, all]
    -i [web3, es], web3.py by default, es enables etherscan api querying''')

def main(argv):
    try:
        (opts,args)=getopt.getopt(argv, "hc:a:n:i:",["help"])
        address=""
        network=""
        config=""
        api="web3"

        for (opt,arg) in opts:
            if (opt in ("-h","-help")):
                usage()
                sys.exit()
            elif (opt=="-c"):
                config=str(arg)
            elif (opt=="-a"):
                address=str(arg)
            elif (opt=="-n"):
                network=str(arg)
            elif (opt=="-i"):
                api=str(arg)
            else:
                usage()
                sys.exit()

        if (config==None or config==""):
            raise Exception(str(datetime.datetime.now())+"|main|-config option is invalid|config="+str(config))
        if (address==None or address==""):
            raise Exception(str(datetime.datetime.now())+"|main|-address option is invalid|address="+str(config))
        if (network==None or network==""):
            raise Exception(str(datetime.datetime.now())+"|main|-network option is invalid|network="+str(network))

        config=get_config(config)        
       
        logging.basicConfig(filename=config.get("LOG_DIR")+"/"+str(datetime.datetime.now()).replace(" ","_")+"_get_balance_py.log",filemode="w")
        log=logging.getLogger()
        log.setLevel(logging.INFO)
        log.info(str(datetime.datetime.now())+"|main|starting")
     
        if (api=="es" and network=="all"):
            get_balance_etherscan(log,config,address,"mainnet")
            get_balance_etherscan(log,config,address,"ropsten")
            get_balance_etherscan(log,config,address,"rinkeby")
        elif (api=="es" and network in ("mainnet","ropsten","rinkeby")):
            get_balance_etherscan(log,config,address,network)
        elif (api=="web3" and network=="all"):
            get_balance(log,config,address,"mainnet")
            get_balance(log,config,address,"ropsten")
            get_balance(log,config,address,"rinkeby")
        elif (api=="web3" and network in ("mainnet","ropsten","rinkeby")):
            get_balance(log,config,address,network)

        log.info(str(datetime.datetime.now())+"|main|completed")
    except:
        pass

if __name__=="__main__":
    main(sys.argv[1:])
