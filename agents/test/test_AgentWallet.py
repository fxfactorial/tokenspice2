import enforce
import pytest

from agents.AgentWallet import *
from agents.test.conftest import _DT_INIT, _DT_STAKE 
from web3engine import bfactory, bpool, dtfactory, datatoken

#=======================================================================
#__init__ related
@enforce.runtime_validation
def test_initFromPrivateKey():
    private_key = '0xbbfbee4961061d506ffbb11dfea64eba16355cbf1d9c29613126ba7fec0aed5d'
    address = '0x66aB6D9362d4F35596279692F0251Db635165871'
    
    w = AgentWallet(private_key=private_key)
    assert w._address == address
    assert w._web3wallet.address == address
    assert w._web3wallet.private_key == private_key

@enforce.runtime_validation
def test_initRandomPrivateKey():
    w1 = AgentWallet()
    w2 = AgentWallet()
    assert w1._address != w2._address
    assert w1._web3wallet.private_key != w2._web3wallet.private_key

@enforce.runtime_validation
def test_gotSomeETHforGas():
    w = AgentWallet()
    assert w.ETH() > 0.0    

@enforce.runtime_validation
def testStr():
    w = AgentWallet()        
    assert "AgentWallet" in str(w)

@enforce.runtime_validation
def testInitiallyEmpty():
    w = AgentWallet()

    assert w.USD() == 0.0
    assert w.OCEAN() == 0.0

@enforce.runtime_validation
def testInitiallyFilled():
    w = AgentWallet(USD=1.2, OCEAN=3.4)

    assert w.USD() == 1.2
    assert w.OCEAN() == 3.4

#=======================================================================
#USD-related
@enforce.runtime_validation
def testUSD():
    w = AgentWallet()

    w.depositUSD(13.25)
    assert w.USD() == 13.25

    w.depositUSD(1.00)
    assert w.USD() == 14.25

    w.withdrawUSD(2.10)
    assert w.USD() == 12.15

    w.depositUSD(0.0)
    w.withdrawUSD(0.0)
    assert w.USD() == 12.15

    assert w.totalUSDin() == (13.25+1.0)

    with pytest.raises(AssertionError):
        w.depositUSD(-5.0)

    with pytest.raises(AssertionError):
        w.withdrawUSD(-5.0)

    with pytest.raises(ValueError):
        w.withdrawUSD(1000.0)

@enforce.runtime_validation
def testFloatingPointRoundoff_USD():
    w = AgentWallet(USD=2.4)
    w.withdrawUSD(2.4000000000000004) #should not get ValueError
    assert w.USD() == 0.0
    assert w.OCEAN() == 0.0

@enforce.runtime_validation
def test_transferUSD():
    w1 = AgentWallet(USD=10.0)
    w2 = AgentWallet(USD=1.0)

    w1.transferUSD(w2, 2.0)

    assert w1.USD() == 10.0-2.0
    assert w2.USD() == 1.0+2.0
    
#=======================================================================
#OCEAN-related
@enforce.runtime_validation
def testOCEAN():
    w = AgentWallet()

    w.depositOCEAN(13.25)
    assert w.OCEAN() == 13.25

    w.depositOCEAN(1.00)
    assert w.OCEAN() == 14.25

    w.withdrawOCEAN(2.10)
    assert w.OCEAN() == 12.15

    w.depositOCEAN(0.0)
    w.withdrawOCEAN(0.0)
    assert w.OCEAN() == 12.15

    assert w.totalOCEANin() == (13.25+1.0)

    with pytest.raises(AssertionError):
        w.depositOCEAN(-5.0)

    with pytest.raises(AssertionError):
        w.withdrawOCEAN(-5.0)

    with pytest.raises(ValueError):
        w.withdrawOCEAN(1000.0)
        
@enforce.runtime_validation
def testFloatingPointRoundoff_OCEAN():
    w = AgentWallet(OCEAN=2.4)
    w.withdrawOCEAN(2.4000000000000004) #should not get ValueError
    assert w.USD() == 0.0
    assert w.OCEAN() == 0.0

@enforce.runtime_validation
def test_transferOCEAN():
    w1 = AgentWallet(OCEAN=10.0)
    w2 = AgentWallet(OCEAN=1.0)

    w1.transferOCEAN(w2, 2.0)

    assert w1.OCEAN() == (10.0-2.0)
    assert w2.OCEAN() == (1.0+2.0)
    
#===================================================================
#ETH-related
@enforce.runtime_validation
def testETH1():
    #super-basic test for ETH
    w = AgentWallet()
    assert isinstance(w.ETH(), float)
    
@enforce.runtime_validation
def testETH2():
    #TEST_PRIVATE_KEY1 should get initialized with ETH when ganache starts
    network = web3util.get_network()
    private_key = web3util.confFileValue(network, 'TEST_PRIVATE_KEY1')
    w = AgentWallet(private_key=private_key)
    assert w.ETH() > 1.0

#===================================================================
#datatoken and pool-related
@enforce.runtime_validation
def test_DT(alice_agent_wallet:AgentWallet, alice_DT:datatoken.Datatoken):
    alice_DT_amt:float = alice_agent_wallet.DT(alice_DT)
    assert alice_DT_amt == (_DT_INIT - _DT_STAKE)

def test_BPT(alice_agent_wallet:AgentWallet, alice_pool:bpool.BPool):
    assert alice_agent_wallet.BPT(alice_pool) == 100.0
    
@pytest.mark.skip(reason="TODO FIXME")
def test_stakeOCEAN():
    raise NotImplementedError()

@pytest.mark.skip(reason="TODO FIXME")
def test_unstakeOCEAN():
    raise NotImplementedError()

    
#===================================================================
#str-related
@enforce.runtime_validation
def testStr():
    w = AgentWallet()        
    assert "AgentWallet" in str(w)

#===================================================================
#burn-related
@enforce.runtime_validation
def testBurnWallet():
    w = BurnWallet()
    assert w._address == constants.BURN_ADDRESS
