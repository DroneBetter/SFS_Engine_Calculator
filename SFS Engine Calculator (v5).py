import math as m

'''From wolframclient.evaluation import WolframLanguageSession

from wolframclient.language import wl, wlexpr

session = WolframLanguageSession()''' #Not necessary, frame-by-frame version is better and WolframClient doesn't work with Python 3.9.

engineNames=["Titan","Frontier","Hawk","Valiant","Kolibri","Ion"]
engines=len(engineNames)
engineMasses=[12,6,3.5,2,0.5,0.5]
engineThrusts=[400,100,120,40,15,2]
engineEfficiencies=[240,290,240,280,260,1200]
engineConsumptions=[]
for i in range(len(engineEfficiencies)):
    engineConsumptions.append(engineThrusts[i]/engineEfficiencies[i])

#print("Engine fuel consumptions:",engineConsumptions)

def sumList(listSummed,l,n):
    sumRange=0
    for i in range(l, n+1, 1):
        sumRange+=listSummed[i]
    return sumRange

def directionAndDistance(inDirection,inDistance,x1,y1,x2,y2):
    xD=x2-x1
    yD=y2-y1
    if inDirection==1:
        global direction
        direction=atan(xD/yD)+180*int(y1>y2)
    if inDistance==1:
        global distance
        distance=sqrt(xD^2+yD^2)

def findCombinations(combinationEngines):
    #if engines>1:
        #findCombinations(engines-1)
    currentCombination=[0]*combinationEngines
    #print("Beginning combination:",currentCombination)
    target=combinationEngines-1
    while target>-1:
        if target==combinationEngines-1:
            combinations.append(list(currentCombination))
            #print("Changed last:",currentCombination)
            currentCombination[target]+=1
        #print("Dominoing:",(not(target==-1))and(currentCombination[target]==engines))
        while (not(target==-1))and(currentCombination[target]==engines):
            currentCombination[target-1]+=1
            for target2 in range(target,combinationEngines):
                currentCombination[target2]=currentCombination[target-1]
                #print("Dominoes:",currentCombination)
            target-=1
        if target>-1:
            target=combinationEngines-1
    print(combinations)
    stageCombinations.append(combinations)

def findCombinationsForAllStages():
    for stages:
        findCombinations(stageMasses[stage])
        craftStagesCombinations.append(stageCombinations)

def findCombinationStatistics(combination,constants,nonConstants,payloadMass,fuelMass,gravity):
    if constants == 1: #Constants mean regardless of external gravity, mass, thrust, specific impulse and fuel consumption. Constants can be calculated separately from non-constants, so criteria (ie. minimum TWR, maximum fuel consumption, maximum mass) can be checked before other things.
        global combinationMass
        global combinationThrust
        global combinationConsumption
        for target in range(len(combination)):
            combinationMass+=engineMasses[combination[target]]
            combinationThrust+=engineThrusts[combination[target]]
            combinationConsumption+=engineConsumptions[combination[target]]
        global combinationMasses
        combinationMasses.append(combinationMass)
        global combinationThrusts
        combinationThrusts.append(combinationThrust)
        global combinationConsumptions
        combinationConsumptions.append(combinationConsumption)
        global combinationImpulse
        combinationImpulse=combinationThrust/combinationConsumption
        global combinationImpulses
        combinationImpulses.append(combinationImpulse)
        global combinationCraftMass
        combinationCraftMass=craftMass+combinationMass
        global combinationCraftMasses
        combinationCraftMasses.append(combinationCraftMass)
        global combinationListingTWR
        combinationListingTWR=combinationThrust/combinationCraftMass
        global combinationListingTWRs
        combinationListingTWRs.append(combinationListingTWR)
    if nonConstants == 1:
        global combinationGravityForce
        combinationGravityForce=gravity*combinationCraftMass
        global combinationGravityForces
        combinationGravityForces.append(combinationGravityForce)
        global combinationLift
        combinationLift=cos(craftDirection)*combinationThrust
        global combinationLifts
        combinationLifts.append(combinationLift)
        global combinationAngularTWR
        combinationAngularTWR=combinationLift/combinationGravityForce
        global combinationAngularTWRs
        combinationAngularTWRs.append(combinationAngularTWR)
        global combinationEffectiveEfficiency
        combinationEffectiveEfficiency=(math.sqrt((combinationLift-combinationGravityForce)^2+(sin(craftDirection)*combinationThrust)^2))/combinationConsumption*payloadMass/(payloadMass+combinationMass)*(2-1*int(combinationAngularTWR>0))
        global combinationEffectiveEfficiencies
        combinationEffectiveEfficiencies.append(combinationEffectiveEfficiency)
    if tsiolkovsky==1:
        deprecatedFindDeltaV()
    else:
        deprecatedFindDeltaV(0)
        global deltaVoffset
        deltaVoffset=deltaV
        deprecatedFindDeltaV(1)
        global combinationDeltaV
        combinationDeltaV=(deltaV-deltaVOffset)*combinationImpulse*fuelMass 

def findStageCombinationStatistics(stage,constants,nonConstants,gravity,payloadWithEngines,prune):
    for c in range(len(stage)):
        findCombinationStatistics(stageCombinations[stage][c],constants,nonConstants,payloadWithEngines,stageFuelMasses[stage],gravity)
        if prune=1:
            pruneCombinations()
    if constants==1:
        global stageCombinationMasses
        stageCombinationMasses.append(list(combinationMasses))
        global stageCombinationThrusts
        stageCombinationThrusts.append(list(combinationThrusts))
        global stageCombinationConsumptions
        stageCombinationConsumptions.append(list(combinationConsumptions))
        global stageCombinationImpulses
        stageCombinationImpulses.append(list(combinationImpulses))
        global stageCombinationListingTWRs
        stageCombinationListingTWRs.append(list(combinationListingTWRs))
    if nonConstants==1:
        global stageCombinationGravityForces
        stageCombinationGravityForces.append(list(combinationGravityForces))
        global stageCombinationLifts
        stageCombinationGravityForces.append(list(combinationLifts))
        global stageCombinationAngularTWRs
        stageCombinationGravityForces.append(list(combinationAngularTWRs))
        global stageCombinationEffectiveEfficiencies
        stageCombinationEffectiveEfficiencies.append(list(combinationEffectiveEfficiencies))

def findPossibilityStatistics(possibility,constants,nonConstants,gravity,prune):
    global combinationsOfStages
    combinationsOfStages[possibility]
    global engineCumulativeMasses
    engineCumulativeMasses=[]
    global stageCumulativeMassesWithEngines
    stageCumulativeMassesWithEngines=[]
    for s in (stages-1,0,-1):
        engineCumulativeMasses.insert(0,stageCombinationMasses[s][combinationsOfStages[possibility][s]]+engineCumulativeMasses[0])
    for s in stages:
        stageCumulativeMassesWithEngines.append(stageCumulativeMasses[s]+engineCumulativeMasses[s])
        findStageCombinationStatistics(s,constants,stageCumulativeMassesWithEngines[s],1)
    for s in stages:
        findCombinationStatistics()
    pruneCombinations()

def greatIterator(): #Run once after using findCombinationsForAllStages. Outputs combinationsOfStages, first dimension is possibilities across the entire craft, nth position in second dimension is the position in craftStagesCombinations[n] that has this possibility's engines for this stage.
    global targets
    currentCombination=[0]*stages
    targets=[0]*stages
    target=stages-1
    while target>-1:
        if target==stages-1:
            combinationsOfStages.append(list(currentCombination)) #Don't replace combinationsOfStages with stageCombinations, not a mistake, they're themselves combinations of stage combinations.
            #print("Changed last:",currentCombination)
            currentCombination[target]+=1
        while (not(target==-1))and(currentCombination[target]==len(stageCombinations[target])):
            currentCombination[target-1]+=1
            for target2 in range(target,stages):
                currentCombination[target2]=0
                #print("Dominoes:",currentCombination)
            target-=1
        if target>-1:
            target=stages-1

def accelerate(x,y):
    global xVelocity
    global yVelocity
    xVelocity+=x
    yVelocity+=y

def vAccelerate(direction,magnitude): #Hey. I'm applying for a new villain loan. Go by the name of Vector. It's a mathematical term, a quantity represented by an arrow, with both direction and magnitude. Vector! That's me, 'cause I'm committing crimes with both direction and magnitude. Oh, yeah! Check out my new weapon. Piranha gun! Oh, yes! Fires live piranhas. Ever seen one before? No, you haven't. I invented it.
    global xVelocity
    global yVelocity
    xVelocity+=m.sin(direction)*magnitude
    yVelocity+=m.cos(direction)*magnitude

def calculatePerFrameDeltaV(possibility):
    findPossibilityStatistics(possibility,1,0,0,1)
    global xPosition #These are only marked global because it lets embedded functions also edit them, they aren't used outside of this function.
    xPosition=0
    global yPosition
    yPosition=315000
    global xVelocity
    xVelocity=0
    global yVelocity
    yVelocity=0
    global angle
    angle=0
    for s in stages:
        findCombinationStatistics(stageCombinations[s][combinationsOfStages[possibility][s]])
        for frames in stageFuelMasses[s]/stageEngineConsumptions[s]:
            directionAndDistance(1,1,xPosition,yPosition,0,0)
            vAccelerate(direction,(1/distance^2)*(9.8/(1/315000^2)))
            vAccelerate(angle,stageThrusts[s]/(stageCumulativeMassesWithEngines[stage])
            xPosition+=xVelocity
            yPosition+=yVelocity
            directionAndDistance(1,1,0,0,xVelocity,yVelocity)
            vAccelerate(direction,distance*(1-(stageAerodynamicDrags*atmosphericdensity/stageCumulativeMassesWithEngines[s])))

def deprecatedFindDeltaV(deltaVtime):
    if tsiolkovsky==1:
        deltaV=CombinationImpulse*gravity*log(craftMass/payloadMass)
    else:
        true #Stops indentation errors by filling the else statement.
        #deltaV=-1*(fuelMass*gravity*time+math.log(combinationCraftMass-fuelMass*time))/fuelMass
        #deltaV=session.evaluate(wlexpr('((combinationCraftMass - fuelMass deltaVtime) (combinationThrust ArcTan[(-combinationThrust + gravity (combinationCraftMass - fuelMass deltaVtime) Cos[craftDirection])/Sqrt[-t^2 - gravity^2 (combinationCraftMass - fuelMass deltaVtime)^2 + 2 gravity combinationThrust (combinationCraftMass - fuelMass deltaVtime) Cos[craftDirection]]] + combinationThrust ArcTan[(-(gravity combinationCraftMass) + fuelMass gravity deltaVtime + combinationThrust Cos[craftDirection])/Sqrt[-combinationThrust^2 - gravity^2 (combinationCraftMass - fuelMass deltaVtime)^2 + 2 gravity combinationThrust (combinationCraftMass - fuelMass deltaVtime) Cos[craftDirection]]] Cos[craftDirection] - Sqrt[-combinationThrust^2 - gravity^2 (combinationCraftMass - fuelMass deltaVtime)^2 + 2 gravity combinationThrust (combinationCraftMass - fuelMass deltaVtime) Cos[craftDirection]]) Sqrt[(combinationThrust/(combinationCraftMass - fuelMass deltaVtime) - gravity Cos[craftDirection])^2 + gravity^2 Sin[craftDirection]^2])/(fuelMass Sqrt[-combinationThrust ^2 - gravity^2 (combinationCraftMass - fuelMass deltaVtime)^2 + 2 gravity combinationThrust (combinationCraftMass - fuelMass deltaVtime) Cos[craftDirection]])'))
        #Not as complicated as it looks, is from WolframAlpha's output of 'integral of sqrt((cos(a)-g+t/(m-fx))^2+(sin(a)g)^2)' where t=thrust, m=total mass, f=fuel mass, x=time, g=gravity.

def findSuffix(number):
    global suffix
    if number[len(number)-2]==1:
        return 'th'
    elif number[len(number)-1]==1:
        return 'st'
    elif number[len(number)-1]==2:
        return 'nd'
    elif number[len(number)-1]==3:
        return 'rd'
    else:
        return 'th'

combinations=[]
stageCombinations=[]
tsiolkovsky=1
stages=input("How many stages would you like?")
stageMasses=[]
stageFuelMasses=[]
stageSeparationForces=[]
stageAerodynamicDrags=[]
for s in range(stages):
    stageMasses.append(input("What is your "+str(s)+findSuffix(s)+" stage's mass (excluding above stages)?"))
    stageFuelMasses.append(input("Of which how much is fuel?"))
    if s<stages-1:
        stageSeparationForces.append(input("How much separation force does this stage have from its successor?"))
    stageAerodynamicDrags.append(input("How much aerodynamic drag does the rocket have at this stage?"))
for s in range(stages-1,0,-1):
    stageCumulativeMasses.insert(0,sumList(stageMasses,s,stages))
print(stageCumulativeMasses)

payloadMass=input("Payload (non-engine) mass?")
fuelMass=input("Of which fuel mass available for this stage?")
#payloadMass=payloadMass-fuelMass
craftMass=payloadMass+fuelMass
gravity=input("Gravity?")
craftDirection=0

findAllCombinationStatistics(1,0,1)