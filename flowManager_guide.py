        bundleData = self.stringToList(data)
        elif type(data) is tuple:
            bundleData = self.tupleToList(data)
        self.type = bundleData[0]
        self.seq = bundleData[1]

        if len(bundleData) < 3:
            bundleData[2] = ''
        if len(bundleData) < 4:
            bundleData[3] = ''

        self.sid = bundleData[2]
        self.payload = bundleData[3]


# Single flow matching
# bundleData=['a', 'b', 3, 'x']
# flowTable=['a', 'b', 3, 'x']

# Multiple flow matching na
# flowTable=[['a', 'b', 3, 'x'], ['a', 'b', 3, 'x']]

class FlowManager:

    def __init__(self, bundleData):
        self.bundleData = bundleData

    #Look up table ng rules and everything 
    def flowTable(self):
        # flowTable=[ruleNo, bundleElements, action]
        self.flowTable=[['a', 'b', 3, 'x']]

    def flowMatching(self, bundleData, flowTable):
        for index, bundleElement in enumerate(bundleData):
            # print(index, bundleElement)

            if bundleElement == flowTable[index]:
                # print "Bundle data: ", bundleElement
                # print "Flow field:", flowTable[index]
                # print "Match"

                # If huling bundleElement na and match pa rin
                # if index == (len(flowTable)-1):
                #     print "Bundle data: ", bundleElement
                #     print "Flow field:", flowTable[index]
                    result = "Match"
                    print "Match"
                    # Dapat rule number and action yung i-rereturn, then pasa sa lookup ng flow table?
                    # Research kung ano magandang implementation for this

            else:
                result = "Not Match"
                print "Not match"
                    #may default na action pag wala sa flowTable

                # print "Bundle data: ", bundleElement
                # print "Flow field:", flowTable[index]

        return result
    

    def createNewFlow(self, flow):
        pass
        # append/add an array

    def editFlow(self, rule):
        pass
        # pass rule number, then yung parameters na papalitan

    def deleteFlow(self):
        pass
        # pass rule number/numbers

        
fm = FlowManager(bd)

fm.createNewFlow(['a', 'b', 3, 'd'])
fm.deleteFlow(0)