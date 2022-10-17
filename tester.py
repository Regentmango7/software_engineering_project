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

#create the class object we are t=using to set values directly
testData = miner_game.classes.Data()


#function to test sellOre
def testSellOre():

    #setup for testSellOre
    testData.getOre("Copper").setAmount(10)
    testData.coin.setAmount(0)

    #testing
    #beginning
    print("Ore amount to start should be: ", 10)
    print("Ore amount to start is: ", testData.getOre("Copper"))
    print("coin amount to start should be: ,", 0)
    print("coin amount to start is: ,", testData.coin.getAmount())
    #test
    miner_game.sellOre(testData.getOre("Copper"), 1)
    #ending
    print("Ore amount at end should be: ", 0)
    print("Ore amount at end is: ", testData.getOre("Copper"))
    print("coin amount at end should be: ,", 20)
    print("coin amount at end is: ,", testData.coin.getAmount())
    print("")
    print("")
    print("")
    return

#function to test mineAction (JD)
def testMineAction():
    pass

#function to test buyWorker
"""
def buyWorker():
    cost = pow(10, gameData.minersTotal.getValue() + 1)
    if gameData.coin.getAmount() >= cost:
        gameData.minersTotal.value += 1
        gameData.minersAvailable.value += 1
        gameData.coin.addOre(-cost)
"""
def testBuyWorker():

    #setup for buyWorker
    testData.coin.setAmount(0)
    
    #testing buying with no money
    #beginning
    print("worker amount to start should be: ", 0)
    print("worker amount to start is: ", testData.getMine("Copper").getMinerCount())
    print("coin amount to start should be: ,", 0)
    print("coin amount to start is: ,", testData.coin.getAmount())
    #test
    miner_game.buyWorker()
    #ending
    print("worker amount at end should be: ", 0)
    print("worker amount at end is: ", testData.getMine("Copper").getMinerCount())
    print("coin amount at end should be: ,", 0)
    print("coin amount at end is: ,", testData.coin.getAmount())

    #setup again
    testData.coin.setAmount(1001)
    #testing buying with enough money
    #beginning
    print("worker amount to start should be: ", 0)
    print("worker amount to start is: ", testData.getMine("Copper").getMinerCount())
    print("coin amount to start should be: ,", 0)
    print("coin amount to start is: ,", testData.coin.getAmount())
    #test
    miner_game.buyWorker()
    #middle
    print("worker amount at middle should be: ", 1)
    print("worker amount at middle is: ", testData.getMine("Copper").getMinerCount())
    print("coin amount at middle should be: ,", 991)
    print("coin amount at middle is: ,", testData.coin.getAmount())
    #test
    miner_game.buyWorker()
    #end
    print("worker amount at end should be: ", 2)
    print("worker amount at end is: ", testData.getMine("Copper").getMinerCount())
    print("coin amount at end should be: ,", 891)
    print("coin amount at end is: ,", testData.coin.getAmount())
    print("")
    print("")
    print("")
    return

#function to test assignMiner
def testAssignMiner():
    pass

#function to test work
def testWork():

    #setup for work
    testData.getOre("Copper").setAmount(0)
    testData.coin.setAmount(0)
    
    #testing
    #beginning
    print("Ore amount to start should be: ", 0)
    print("Ore amount to start is: ", testData.getOre("Copper"))
    print("worker amount to start should be: ", 0)
    print("worker amount to start is: ", testData.getMine("Copper").getMinerCount())
    print("coin amount to start should be: ,", 0)
    print("coin amount to start is: ,", testData.coin.getAmount())
    #test

    #middle

    #test

    #ending

    print("")
    print("")
    print("")
    return

#function to test getCost
def testGetCost():
    pass

#function to test getCostString
def testGetCostString():
    pass

#function to test canAfford
def testCanAfford():
    pass

#function to test buyUpgrade
def testBuyUpgrade():
    pass

#main method to run the test functions
def main():
    testSellOre()
    #testMineAction()
    #testBuyWorker()
    #testAssignMiner()
    #testWork()
    #testGetCost()
    #testGetCostString()
    #testCanAfford()
    #testBuyUpgrade()

main()

