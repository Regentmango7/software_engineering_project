'''tester.py

Unit testing for miner_game
'''

#import the file we are testing
import pytest
import click_miners
import classes
import pygame
import coverage
pygame.init()

#create the class object we are t=using to set values directly


#function to test sellOre
def testSellOre():
    testSellData = classes.Data()

    #setup for testSellOre
    testSellData.getOre("Copper").setAmount(10)
    testSellData.coin.setAmount(0)

    #testing
    #beginning
    assert 10 == testSellData.getOre("Copper").getAmount()  #is copper amount 10 after setup?
    assert 0 == testSellData.coin.getAmount()  #is coin amount 0 after setup?

    #test
    testSellData.sellOre(testSellData.getOre("Copper"), 1)
    #ending
    assert 0 == testSellData.getOre("Copper").getAmount() #is copper all gone after sell?
    assert 20 == testSellData.coin.getAmount()  #is coin 20 after selling 10 copper?

    #setup again for testSellOre
    testSellData.getOre("Copper").setAmount(10)
    testSellData.coin.setAmount(0)

    #testing
    #beginning
    assert 10 == testSellData.getOre("Copper").getAmount()  #is copper amount 10 after setup?
    assert 0 == testSellData.coin.getAmount()  #is coin amount 0 after setup?

    #test
    testSellData.sellOre(testSellData.getOre("Copper"), .5)
    #ending
    assert 5 == testSellData.getOre("Copper").getAmount() #is copper all gone after sell?
    assert 10 == testSellData.coin.getAmount()  #is coin 20 after selling 10 copper?

    return

#function to test buyMiner
def testBuyMiner():
    testBuyMinerData = classes.Data()
    #setup for buyMiner
    testBuyMinerData.coin.setAmount(0)
    
    #testing buying with no money
    #beginning
    assert 0 == testBuyMinerData.getStat("Total Miners").getValue()  #is minersTotal 0 at beginning?
    assert 0 == testBuyMinerData.coin.getAmount()  #is coin count 0 at beginning?
    #test
    testBuyMinerData.buyMiner()
    #ending
    assert 0 == testBuyMinerData.getStat("Total Miners").getValue()  #is minersTotal 0 after buyMiner()?
    assert 0 == testBuyMinerData.coin.getAmount()  #is coin count 0 after buyMiner()?

    #setup again
    testBuyMinerData.coin.setAmount(1001)
    #testing buying with enough money
    #beginning
    assert 0 == testBuyMinerData.getStat("Total Miners").getValue()  #is minersTotal 0 after initialization?
    assert 1001 == testBuyMinerData.coin.getAmount()  #is coin count 1001 after initialization?
    #test
    testBuyMinerData.buyMiner()
    #middle
    assert 1 == testBuyMinerData.getStat("Total Miners").getValue()  #is minersTotal 1 after successful buyMiner()?
    assert 991 == testBuyMinerData.coin.getAmount()  #is coin 991 after successful buyMiner()?
    #test
    testBuyMinerData.buyMiner()
    #end
    assert 2 == testBuyMinerData.getStat("Total Miners").getValue()  #is minersTotal 2 after second successful buyMiner()?
    assert 891 == testBuyMinerData.coin.getAmount()  #is coin 891 after second successful buyMiner()?
    return

#function to test work
def testWork():
    
    testWorkData = classes.Data()

    #setup for work
    testWorkData.getOre("Copper").setAmount(0)
    testWorkData.coin.setAmount(1001)
    testWorkData.buyMiner()
    testWorkData.assignMiners(testWorkData.activeMine)
    store = 0
    firstRun = False
    timer = pygame.time.Clock()
    framerate = 60
    
    #testing
    #beginning
    assert 0 == testWorkData.getOre("Copper").getAmount()  #Copper ore starts at 0
    assert 1 == testWorkData.getStat("Total Miners").getValue()  #one worker has been purchased
    assert 1 == testWorkData.getMine("Copper").getMinerCount() #one worker is assigned to Copper mine
    assert 991 == testWorkData.coin.getAmount()  #coin os 991 to start
    #test
    running = True
    while running and testWorkData.getOre("Copper").getAmount() == 0:
        timer.tick(framerate)
        testWorkData.work()

    assert testWorkData.getOre("Copper").getAmount() == 1  #Ore should be one after work is run
    #ending
    return

#function to test getCost
def testGetCost():
    testGetCostData = classes.Data()

    #setup for "Add" upgrade

    #testing for "Add" upgrade
    #begining
    clickBase = testGetCostData.getUpgrade("Click_Base_Count")

    baseList = clickBase.getCost()
    #TESTING BASE CLICK UPGRADE
    assert "Copper" == baseList[0].getOre().getName()  #First ore is Copper
    assert 1.2 == baseList[0].getRate() # Copper cost is 1.2 initially

    testGetCostData.getOre("Copper").setAmount(5)

    clickBase.buyUpgrade()

    #COPPER COST SHOULD BE 2.4 after 1 upgrade
    baseList = clickBase.getCost()
    assert "Copper" == baseList[0].getOre().getName()  #First ore is Copper
    assert 2.4 == baseList[0].getRate() # Copper cost is 2.4 after first upgrade


    #end


    #setup for "Multiply" upgrade

    #testing for "Multiply" upgrade
    #begining
    
    
    
    multUp = testGetCostData.getUpgrade("Click_Multiplier")

    baseList = multUp.getCost()
    #TESTING CLICK MULTIPLIER UPGRADE\n COPPER COST SHOULD BE 10
    assert "Copper" == baseList[0].getOre().getName()  #First ore is Copper
    assert 10 == baseList[0].getRate() # Copper cost is 10

    testGetCostData.getOre("Copper").setAmount(10)

    multUp.buyUpgrade()

    baseList = multUp.getCost()
    assert "Copper" == baseList[0].getOre().getName()  #First ore is Copper
    assert 100 == baseList[0].getRate() # Copper cost is 100

    #end


    #setup for "worker speed" upgrade

    #testing for "worker speed" upgrade
    #begining

    mineSpeed = testGetCostData.getUpgrade("Miner_Speed")

    baseList = mineSpeed.getCost()
    #TESTING Miner_Speed UPGRADE
    assert "Copper" == baseList[0].getOre().getName()  #First ore is Copper
    assert 1.2 == baseList[0].getRate() # Copper cost is 1.2 initially

    testGetCostData.getOre("Copper").setAmount(5)

    mineSpeed.buyUpgrade()

    #COPPER COST SHOULD BE 2.4 after 1 upgrade
    baseList = mineSpeed.getCost()
    assert "Copper" == baseList[0].getOre().getName()  #First ore is Copper
    assert 2.4 == baseList[0].getRate() # Copper cost is 2.4 after first upgrade


    #end
    return

#function to test canAfford
def testCanAfford():
    testAffordData = classes.Data()

    # TESTING FOR Click_Base_Count:

    #setup for no money
    testAffordData.getOre("Copper").setAmount(0)
    #TESTING WITH NO ORE
    #beginning
    assert 0 == testAffordData.getOre("Copper").getAmount()
    #end
    assert False == testAffordData.getUpgrade("Click_Base_Count").canAfford()
    #setup for enough money
    testAffordData.getOre("Copper").setAmount(1001)
    #TESTING WITH ENOUGH ORE
    #beginning
    assert 1001 == testAffordData.getOre("Copper").getAmount()
    #end
    assert True == testAffordData.getUpgrade("Click_Base_Count").canAfford()
    

    #TESTING FOR Click_Multiplier

    #setup for no money
    testAffordData.getOre("Copper").setAmount(0)
    #TESTING WITH NO ORE
    #beginning
    assert 0 == testAffordData.getOre("Copper").getAmount()
    #end
    assert False == testAffordData.getUpgrade("Click_Multiplier").canAfford()
    #setup for enough money
    testAffordData.getOre("Copper").setAmount(1001)
    #TESTING WITH ENOUGH ORE
    #beginning
    assert 1001 == testAffordData.getOre("Copper").getAmount()
    #end
    assert True == testAffordData.getUpgrade("Click_Multiplier").canAfford()

    # TESTING FOR Miner_Speed:

    #setup for no money
    testAffordData.getOre("Copper").setAmount(0)
    #TESTING WITH NO ORE
    #beginning
    assert 0 == testAffordData.getOre("Copper").getAmount()
    #end
    assert False == testAffordData.getUpgrade("Miner_Speed").canAfford()
    #setup for enough money
    testAffordData.getOre("Copper").setAmount(1001)
    #TESTING WITH ENOUGH ORE
    #beginning
    assert 1001 == testAffordData.getOre("Copper").getAmount()
    #end
    assert True == testAffordData.getUpgrade("Miner_Speed").canAfford()

     # TESTING FOR Miner_Cost:

    #setup for no money
    testAffordData.getOre("Copper").setAmount(0)
    #TESTING WITH NO ORE
    #beginning
    assert 0 == testAffordData.getOre("Copper").getAmount()
    #end
    assert False == testAffordData.getUpgrade("Miner_Cost").canAfford()
    #setup for enough money
    testAffordData.getOre("Copper").setAmount(1001)
    #TESTING WITH ENOUGH ORE
    #beginning
    assert 1001 == testAffordData.getOre("Copper").getAmount()
    #end
    assert True == testAffordData.getUpgrade("Miner_Cost").canAfford()

    return 

#function to test buyUpgrade
def testBuyUpgrade():
    testBuyUpData = classes.Data()

    #TESTING FOR Click_Base_Count:

    #setup for no money
    testBuyUpData.getOre("Copper").setAmount(0)
    #TESTING WITH NO ORE
    #beginning
    assert 0 == testBuyUpData.getOre("Copper").getAmount()
    assert 1 == testBuyUpData.getStat("Base Click Value").getValue()
    #test
    testBuyUpData.getUpgrade("Click_Base_Count").buyUpgrade()
    #end
    assert 0 == testBuyUpData.getOre("Copper").getAmount()
    assert 1 == testBuyUpData.getStat("Base Click Value").getValue()

    #setup for enough money
    testBuyUpData.getOre("Copper").setAmount(1001)
    #TESTING WITH ENOUGH ORE
    #beginning
    assert 1001 == testBuyUpData.getOre("Copper").getAmount()
    assert 1 == testBuyUpData.getStat("Base Click Value").getValue()
    #test
    testBuyUpData.getUpgrade("Click_Base_Count").buyUpgrade()
    #end
    assert 999.8 == testBuyUpData.getOre("Copper").getAmount()
    assert 2 == testBuyUpData.getStat("Base Click Value").getValue()
    

    #TESTING FOR Click_Multiplier

    #setup for no money
    testBuyUpData.getOre("Copper").setAmount(0)
    #TESTING WITH NO ORE
    #beginning
    assert 0 == testBuyUpData.getOre("Copper").getAmount()
    assert 1 == testBuyUpData.getStat("Click Multiplier").getValue()
    #test
    testBuyUpData.getUpgrade("Click_Multiplier").buyUpgrade()
    #end
    assert 0 == testBuyUpData.getOre("Copper").getAmount()
    assert 1 == testBuyUpData.getStat("Click Multiplier").getValue()

    #setup for enough money
    testBuyUpData.getOre("Copper").setAmount(1001)
    #TESTING WITH ENOUGH ORE
    #beginning
    assert 1001 == testBuyUpData.getOre("Copper").getAmount()
    assert 1 == testBuyUpData.getStat("Click Multiplier").getValue()
    #test
    testBuyUpData.getUpgrade("Click_Multiplier").buyUpgrade()
    #end
    assert 991 == testBuyUpData.getOre("Copper").getAmount()
    assert 10 == testBuyUpData.getStat("Click Multiplier").getValue()


    #TESTING FOR Miner_Speed:

    #setup for no money
    testBuyUpData.getOre("Copper").setAmount(0)
    #TESTING WITH NO ORE
    #beginning
    assert 0 == testBuyUpData.getOre("Copper").getAmount()
    assert 100 == testBuyUpData.getStat("Miner Speed").getValue()
    #test
    testBuyUpData.getUpgrade("Miner_Speed").buyUpgrade()
    #end
    assert 0 == testBuyUpData.getOre("Copper").getAmount()
    assert 100 == testBuyUpData.getStat("Miner Speed").getValue()

    #setup for enough money
    testBuyUpData.getOre("Copper").setAmount(1001)
    #TESTING WITH ENOUGH ORE
    #beginning
    assert 1001 == testBuyUpData.getOre("Copper").getAmount()
    assert 100 == testBuyUpData.getStat("Miner Speed").getValue()
    #test
    testBuyUpData.getUpgrade("Miner_Speed").buyUpgrade()
    #end
    assert 999.8 == testBuyUpData.getOre("Copper").getAmount()
    assert 95 == testBuyUpData.getStat("Miner Speed").getValue()


    #TESTING FOR Miner_Cost:

    #setup for no money
    testBuyUpData.getOre("Copper").setAmount(0)
    #TESTING WITH NO ORE
    #beginning
    assert 0 == testBuyUpData.getOre("Copper").getAmount()
    assert 1.0 == testBuyUpData.getStat("Miner Cost Reduce").getValue()
    #test
    testBuyUpData.getUpgrade("Miner_Cost").buyUpgrade()
    #end
    assert 0 == testBuyUpData.getOre("Copper").getAmount()
    assert 1.0 == testBuyUpData.getStat("Miner Cost Reduce").getValue()

    #setup for enough money
    testBuyUpData.getOre("Copper").setAmount(1001)
    #TESTING WITH ENOUGH ORE
    #beginning
    assert 1001 == testBuyUpData.getOre("Copper").getAmount()
    assert 1.0 == testBuyUpData.getStat("Miner Cost Reduce").getValue()
    #test
    testBuyUpData.getUpgrade("Miner_Cost").buyUpgrade()
    #end
    assert 999.8 == testBuyUpData.getOre("Copper").getAmount()
    assert 0.5 == testBuyUpData.getStat("Miner Cost Reduce").getValue()
    return

def testNumScaling():
    #test for zero
    assert "0" == classes.numberScaling(0)
    #test for 1
    assert "1" == classes.numberScaling(1)
    #test for many (both positive and negative)
    assert "10.0K" == classes.numberScaling(10000)
    assert "-10.0K" == classes.numberScaling(-10000)
    assert "1.0B" == classes.numberScaling(1000000000)
    return

#main method to run the test functions
def main():
    testNumScaling()
    testSellOre() #working!
    testBuyMiner() #working!
    testWork() #working!
    testGetCost() #working!
    testCanAfford() #working!
    testBuyUpgrade() #working!
    return

main()

