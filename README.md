# get_balance_py

utility script to get balance by request of a fren. <br><br>

Setup and Run:   <br>
- Bootstrap paths for bin, etc, log <br>
- Bootstrap configuration.xml with alchemy http keys, required <br>
- Bootstrap configuration.xml with etherscan key, optional <br>

Usage:   <br>
./get_balance.py -c config_path -a address -n network [-i api].  <br><br>

  -n [mainnet, ropsten, rinkeby, all]  <br><br>

  -i [web3, es], web3.py by default, es enables etherscan api querying<br><br><br>
  
  
Tests: <br>
./get_balance.py -c ../etc/configuration.xml -a 0xB07626Bc2fF18d680ec886c3109e9BF6ee05E6b7 -n mainnet <br>
./get_balance.py -c ../etc/configuration.xml -a 0xB07626Bc2fF18d680ec886c3109e9BF6ee05E6b7 -n ropsten <br>
./get_balance.py -c ../etc/configuration.xml -a 0xB07626Bc2fF18d680ec886c3109e9BF6ee05E6b7 -n rinkeby <br><br>

./get_balance.py -c ../etc/configuration.xml -a 0xB07626Bc2fF18d680ec886c3109e9BF6ee05E6b7 -n mainnet -i es <br>
./get_balance.py -c ../etc/configuration.xml -a 0xB07626Bc2fF18d680ec886c3109e9BF6ee05E6b7 -n ropsten -i es <br>
./get_balance.py -c ../etc/configuration.xml -a 0xB07626Bc2fF18d680ec886c3109e9BF6ee05E6b7 -n rinkeby -i es <br><br>

./get_balance.py -c ../etc/configuration.xml -a 0xB07626Bc2fF18d680ec886c3109e9BF6ee05E6b7 -n all  <br>
./get_balance.py -c ../etc/configuration.xml -a 0xB07626Bc2fF18d680ec886c3109e9BF6ee05E6b7 -n all -i es <br>
./get_balance.py -c ../etc/configuration.xml -a 0xB07626Bc2fF18d680ec886c3109e9BF6ee05E6b7 -n all -i web3 <br>




