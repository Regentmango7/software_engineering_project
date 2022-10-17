'''tester.py


sellOre
mineAction
buyWorker
assignMiner
work
getCost?
getCostString?
canAfford?
buyUpgrade

'''

#import the file we are testing
import miner_game
import pygame
pygame.init()

#create the class object we are t=using to set values directly
testData = miner_game.classes.Data()

#function to test sellOre
def testSellOre():
    print("testSellOre")

    #setup for testSellOre
    testData.getOre("Copper").setAmount(10)
    testData.coin.setAmount(0)

    #testing
    #beginning
    print("Ore amount to start should be: ", 10)
    print("Ore amount to start is: ", testData.getOre("Copper").getAmount())
    print("coin amount to start should be: ,", 0)
    print("coin amount to start is: ,", testData.coin.getAmount())
    #test
    miner_game.sellOre(testData.getOre("Copper"), 1)
    #ending
    print("Ore amount at end should be: ", 0)
    print("Ore amount at end is: ", testData.getOre("Copper").getAmount())
    print("coin amount at end should be: ,", 20)
    print("coin amount at end is: ,", testData.coin.getAmount())
    print("")
    print("")
    print("")
    return

#function to test mineAction (JD)
def testMineAction():
    print("testMineAction")

    #setup for mineAction

    pass #change to return

#function to test buyWorker
def testBuyWorker():
    print("testBuyWorker")
    #setup for buyWorker
    testData.coin.setAmount(0)
    
    #testing buying with no money
    #beginning
    print("worker amount to start should be: ", 0)
    print("worker amount to start is: ", testData.minersTotal.getValue())
    print("coin amount to start should be: ,", 0)
    print("coin amount to start is: ,", testData.coin.getAmount())
    #test
    miner_game.buyWorker()
    #ending
    print("worker amount at end should be: ", 0)
    print("worker amount at end is: ", testData.minersTotal.getValue())
    print("coin amount at end should be: ,", 0)
    print("coin amount at end is: ,", testData.coin.getAmount())

    #setup again
    testData.coin.setAmount(1001)
    #testing buying with enough money
    #beginning
    print("worker amount to start should be: ", 1001)
    print("worker amount to start is: ", testData.minersTotal.getValue())
    print("coin amount to start should be: ,", 0)
    print("coin amount to start is: ,", testData.coin.getAmount())
    #test
    miner_game.buyWorker()
    #middle
    print("worker amount at middle should be: ", 1)
    print("worker amount at middle is: ", testData.minersTotal.getValue())
    print("coin amount at middle should be: ,", 991)
    print("coin amount at middle is: ,", testData.coin.getAmount())
    #test
    miner_game.buyWorker()
    #end
    print("worker amount at end should be: ", 2)
    print("worker amount at end is: ", testData.minersTotal.getValue())
    print("coin amount at end should be: ,", 891)
    print("coin amount at end is: ,", testData.coin.getAmount())
    print("")
    print("")
    print("")
    return

#function to test assignMiner
def testAssignMiner():
    print("testAssignMiner")
    pass #change to return

#function to test work
def testWork():
    print("testWork")

    #setup for work
    testData.getOre("Copper").setAmount(0)
    testData.coin.setAmount(1001)
    miner_game.buyWorker()
    miner_game.assignMiner()
    store = 0
    firstRun = False
    timer = pygame.time.Clock()
    framerate = 60
    
    #testing
    #beginning
    print("Ore amount to start should be: ", 0)
    print("Ore amount to start is: ", testData.getOre("Copper").getAmount())
    print("worker amount to start should be: ", 1)
    print("total worker amount to start is: ", testData.minersTotal.getValue())
    print("assigned worker amount to start is: ", testData.getMine("Copper").getMinerCount())
    print("coin amount to start should be: ,", 991)
    print("coin amount to start is: ,", testData.coin.getAmount())
    #test
    running = True
    while running and testData.getOre("Copper").getAmount() == 0:
        timer.tick(framerate)
        store, firstRun = miner_game.work(store, firstRun)
    #ending
    print("Ore amount to end should be: ", 1)
    print("Ore amount to end is: ", testData.getOre("Copper").getAmount())
    print("")
    print("")
    print("")
    return

#function to test getCost
def testGetCost():
    print("testGetCost")
    
    

    #setup for "Add" upgrade

    #testing for "Add" upgrade
    #begining
    clickBase = testData.getUpgrade("Click_Base_Count")

    baseList = clickBase.getCost()
    print("TESTING BASE CLICK UPGRADE")
    print("COPPER COST SHOULD BE 1.2")

    for rate in baseList:
        print("ORE: " + rate.getOre().getName() + ", COST: " + str(rate.getRate()))

    testData.getOre("Copper").setAmount(5)

    clickBase.buyUpgrade()
    print("Upgraded successfully")

    print("COPPER COST SHOULD BE 2.4 after 1 upgrade")
    baseList = clickBase.getCost()
    for rate in baseList:
        print("ORE: " + rate.getOre().getName() + ", COST: " + str(rate.getRate()))


    #end


    #setup for "Multiply" upgrade

    #testing for "Multiply" upgrade
    #begining
    
    
    
    multUp = testData.getUpgrade("Click_Multiplier")

    baseList = multUp.getCost()
    print("TESTING CLICK MULTIPLIER UPGRADE\n COPPER COST SHOULD BE 10")

    for rate in baseList:
        print("ORE: " + rate.getOre().getName() + ", COST: " + str(rate.getRate()))

    testData.getOre("Copper").setAmount(10)

    multUp.buyUpgrade()
    print("Upgraded successfully")

    print("COPPER COST SHOULD BE 100 after 1 upgrade")
    baseList = multUp.getCost()
    for rate in baseList:
        print("ORE: " + rate.getOre().getName() + ", COST: " + str(rate.getRate()))

    #end
    print("")
    print("")
    print("")
    return

#function to test getCostString
def testGetCostString():
    print("testGetCostString")
    pass #change to return

#function to test canAfford
def testCanAfford():
    print("testCanAfford")
    pass #change to return

#function to test buyUpgrade
def testBuyUpgrade():
    print("testBuyUpgrade")
    pass #change to return

#main method to run the test functions
def main():
    #testSellOre() #working!
    #testMineAction() #writing (JD)
    #testBuyWorker() #working!
    #testAssignMiner() #writing (JD)
    #testWork() #working!
    testGetCost() #working!
    #testGetCostString() #writing
    #testCanAfford() #writing
    #testBuyUpgrade() #writing
    return

main()

