import math as m

'''From wolframclient.evaluation import WolframLanguageSession

from wolframclient.language import wl, wlexpr

session = WolframLanguageSession()''' #Not necessary, frame-by-frame version is better and WolframClient doesn't work with Python 3.9.

engineNames=["Titan","Frontier","Hawk","Valiant","Kolibri","Ion"]
engines=len(engineNames)
engineMasses=[12,6,3.5,2,0.5,0.5]
engineThrusts=[400,100,120,40,15,2]
engineImpulses=[240,290,240,280,260,1200]
engineConsumptions=[]
for i in range(len(engineImpulses)):
    engineConsumptions.append(engineThrusts[i]/engineImpulses[i])

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
        while not(target==-1) and currentCombination[target]==engines:
            currentCombination[target-1]+=1
            for target2 in range(target,combinationEngines):
                currentCombination[target2]=currentCombination[target-1]
                #print("Dominoes:",currentCombination)
            target-=1
        if target>-1:
            target=combinationEngines-1
    stageCombinations.append(combinations)

def findCombinationsForAllStages():
    for s in range(0,len(stages)):
        findCombinations(stageMasses[s])
        stageCombinations.append(stageCombinations)

def clearCombinationStatistics():
    combinationStatistics=[]

def clearStageStatistics():
    stageCombinationStatistics=[]

def findCombinationStatistics(combination,constants,nonConstants,payloadMass,fuelMass,gravity,accountForOwnMass):
    combinationStatistics=[] #Mass, thrust, consumption, impulse, craft mass, standard TWR, 
    if constants == 1: #Constants are regardless of external gravity; mass, thrust, specific impulse, fuel consumption, total mass, TWR under standard gravity. Constants can be calculated without non-constants, so criteria (ie. minimum TWR, maximum fuel consumption, maximum mass) can be checked before other things are calculated.
        combinationMass=0
        combinationThrust=0
        combinationConsumption=0
        for target in range(len(combination)):
            if accountForOwnMass == 1:
                combinationMass+=engineMasses[combination[target]]
            combinationThrust+=engineThrusts[combination[target]]
            combinationConsumption+=engineConsumptions[combination[target]]
        combinationStatistics.append(combinationMass)
        combinationStatistics.append(combinationThrust)
        combinationStatistics.append(combinationConsumption)
        combinationStatistics.append(combinationThrust/combinationConsumption)
        combinationStatistics.append(craftMass+combinationMass)
        combinationStatistics.append(combinationThrust/combinationCraftMass)
    if nonConstants == 1: #Non-constants regard external gravity and angle, etc.; Gravity force, lift (at angle), angular TWR,.
        combinationGravityForce=gravity*combinationCraftMass
        combinationStatistics.append(combinationGravityForce)
        combinationLift=m.cos(craftDirection)*combinationThrust
        combinationStatistics.append(combinationLift)
        combinationAngularTWR=combinationLift/combinationGravityForce
        combinationStatistics.append(combinationAngularTWR)
        combinationEffectiveEfficiency=(math.sqrt((combinationLift-combinationGravityForce)^2+(sin(craftDirection)*combinationThrust)^2))/combinationConsumption*payloadMass/(payloadMass+combinationMass)*(2-1*int(combinationAngularTWR>0))
        combinationStatistics.append(combinationEffectiveEfficiency)
        global combinationDeltaV
        if tsiolkovsky==1:
            combinationDeltaV=deprecatedFindDeltaV(1)
        else:
            deprecatedFindDeltaV(0,0)
            global deltaVoffset
            deltaVoffset=deltaV
            deprecatedFindDeltaV(0,1)
            combinationDeltaV=(deltaV-deltaVOffset)*combinationImpulse*fuelMass 
        combinationStatistics.append(combinationDeltaV)


def findStageCombinationStatistics(stage,constants,nonConstants,gravity,payloadWithEngines): #stage argument wants a list of the stage's combinations, not its identifier in the list.
    global stageCombinations
    global stageCombinationStatistics
    for c in range(len(stage)):
        clearCombinationStatistics()
        findCombinationStatistics(stage[c],constants,nonConstants,payloadWithEngines,stageFuelMasses[stage],gravity)
        stageCombinationStatistics.append(combinationStatistics)

def findCombinationStatisticsForAllStages(constants,nonConstants,prune):
    for s in range(len(stageCombinations)):
        findStageCombinationStatistics(stageCombinations[s],constants,nonConstants,gravity,payloadWithEngines)

def greatIterator(): #Run once after using findCombinationsForAllStages. Outputs combinationsOfStages, first dimension is possibilities across the entire craft, nth position in second dimension is the position in stageCombinations[n] that has this possibility's engines for this stage.
    global targets
    currentCombination=[0]*stages
    targets=[0]*stages
    target=stages-1
    while target>-1:
        if target==stages-1:
            combinationsOfStages.append(list(currentCombination)) #Don't replace combinationsOfStages with stageCombinations, not a mistake, they're themselves combinations of stage combinations.
            #print("Changed last:",currentCombination)
            currentCombination[target]+=1
        while not(target==-1) and currentCombination[target]==len(stageCombinations[target]):
            currentCombination[target-1]+=1
            for target2 in range(target,stages):
                currentCombination[target2]=0
                #print("Dominoes:",currentCombination)
            target-=1
        if target>-1:
            target=stages-1

def findPossibilityStatistics(possibility,constants,nonConstants,gravity):
    global combinationsOfStages
    global engineCumulativeMasses
    engineCumulativeMasses=[]
    global stageCumulativeMassesWithEngines
    stageCumulativeMassesWithEngines=[]
    for s in range(stages-1,-1,-1):
        engineCumulativeMasses.insert(0,stageCombinationStatistics[s][combinationsOfStages[possibility][s]][0]+engineCumulativeMasses[0])
    for s in stages:
        stageCumulativeMassesWithEngines.append(stageCumulativeMasses[s]+engineCumulativeMasses[s])
        findStageCombinationStatistics(stageCombinations[s],constants,stageCumulativeMassesWithEngines[s],1)
    for s in stages:
        findCombinationStatistics(stageCombinations[s][combinationsOfStages[possibility][s]],1,0,stageCumulativeMassesWithEngines[s],0,0,0)

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
        for frames in range(stageFuelMasses[s]/stageCombinationStatistics[s][2]):
            directionAndDistance(1,1,xPosition,yPosition,0,0)
            vAccelerate(direction,(1/distance^2)*(9.8/(1/315000^2)))
            vAccelerate(angle,stageThrusts[s]/(stageCumulativeMassesWithEngines[stage]))
            xPosition+=xVelocity
            yPosition+=yVelocity
            directionAndDistance(1,1,0,0,xVelocity,yVelocity)
            vAccelerate(direction,distance*(1-(stageAerodynamicDrags*atmosphericdensity/stageCumulativeMassesWithEngines[s])))

def deprecatedFindDeltaV(tsiolkovsky,deltaVtime):
    if tsiolkovsky==1:
        global craftMass
        global payloadMass
        global gravity
        global combinationConsumption
        deltaV=CombinationImpulse*m.ln(craftMass/payloadMass)-gravity*(fuelMass/combinationConsumption)
    else:
        true #Stops indentation errors by filling the else statement.
        #deltaV=-1*(fuelMass*gravity*time+math.log(combinationCraftMass-fuelMass*time))/fuelMass
        #deltaV=session.evaluate(wlexpr('((combinationCraftMass - fuelMass deltaVtime) (combinationThrust ArcTan[(-combinationThrust + gravity (combinationCraftMass - fuelMass deltaVtime) Cos[craftDirection])/Sqrt[-t^2 - gravity^2 (combinationCraftMass - fuelMass deltaVtime)^2 + 2 gravity combinationThrust (combinationCraftMass - fuelMass deltaVtime) Cos[craftDirection]]] + combinationThrust ArcTan[(-(gravity combinationCraftMass) + fuelMass gravity deltaVtime + combinationThrust Cos[craftDirection])/Sqrt[-combinationThrust^2 - gravity^2 (combinationCraftMass - fuelMass deltaVtime)^2 + 2 gravity combinationThrust (combinationCraftMass - fuelMass deltaVtime) Cos[craftDirection]]] Cos[craftDirection] - Sqrt[-combinationThrust^2 - gravity^2 (combinationCraftMass - fuelMass deltaVtime)^2 + 2 gravity combinationThrust (combinationCraftMass - fuelMass deltaVtime) Cos[craftDirection]]) Sqrt[(combinationThrust/(combinationCraftMass - fuelMass deltaVtime) - gravity Cos[craftDirection])^2 + gravity^2 Sin[craftDirection]^2])/(fuelMass Sqrt[-combinationThrust ^2 - gravity^2 (combinationCraftMass - fuelMass deltaVtime)^2 + 2 gravity combinationThrust (combinationCraftMass - fuelMass deltaVtime) Cos[craftDirection]])'))
        #Not as complicated as it looks, is from WolframAlpha's output of 'integral of sqrt((cos(a)-g+t/(m-fx))^2+(sin(a)g)^2)' where t=thrust, m=total mass, f=fuel mass, x=time, g=gravity.
        return deltaV

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

def pruneCombinations(prunes,pruneMasses,pruneThrusts,pruneImpulses,pruneDuplicates):
    output=prunes
    '''outputIDs=[]
    for ID in range(len(prunes)):
        outputIDs.append(ID)''' #Not necessary.
    c=0
    for _ in range(len(prunes)):
        uhOh=0
        d=0
        for _ in range(c+1,len(prunes)):
            ohUh=0
            if uhOh==0:
                if pruneMasses[d]==pruneMasses[c] and pruneThrusts[d]==pruneThrusts[c] and pruneImpulses[d]==pruneImpulses:
                        if pruneDuplicates==1:
                            del output[d]
                            #del outputIDs[d]
                            ohUh=1
                else:
                    if pruneMasses[d]<=pruneMasses[c] and pruneThrusts[d]>=pruneThrusts[c] and pruneImpulses[d]>=pruneImpulses[c]:
                            del output[c]
                            #del outputIDs[c]
                            uhOh=1
                    elif pruneMasses[c]<=pruneMasses[d] and pruneThrusts[c]>=pruneThrusts[d] and pruneImpulses[c]>=pruneImpulses[d]:
                            del output[d]
                            #del outputIDs[d]
                            ohUh=1
            if ohUh==0:
                d+=1
        if uhOh==0:
            c+=1
    return output

def pruneAllStages(pruneDuplicates):
    for s in range(len(stageCombinations)):
        stageCombinations[s]=pruneCombinations(stageCombinations[s],stageCombinationStatistics[s][0],stageCombinationStatistics[s][1],stageCombinationStatistics[s][3],pruneDuplicates)
    clearCombinationStatistics()
    findCombinationStatisticsForAllStages(1,0,1)

def findSuffix(number,append):
    strumber=str(number)
    global suffix
    if strumber[len(strumber)-2]==1:
        output='th'
    elif strumber[len(strumber)-1]==1:
        output='st'
    elif strumber[len(strumber)-1]==2:
        output='nd'
    elif strumber[len(strumber)-1]==3:
        output='rd'
    else:
        output='th'
    if append==1:
        output=strumber+output
    return output

combinations=[]
stageCombinations=[]
tsiolkovsky=1
stages=input("How many stages would you like?")
stageMasses=[]
stageFuelMasses=[]
stageSeparationForces=[]
stageAerodynamicDrags=[]
for s in range(stages):
    stageMasses.append(input("What is your "+findSuffix(s,1)+" stage's mass (excluding above stages)?"))
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
findCombinationsForAllStages()
findCombinationStatisticsForAllStages(1,0,1)
pruneAllStages(0)
greatIterator()
