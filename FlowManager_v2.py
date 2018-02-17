# Use RegExp para sa mga wildcards!


#bundleData = [type, bundleSeq, sid, ipAddr, dataSummary (eto yung minMaxAve, etc)]
#flowTable = [ruleNo, type, bundleSeq, sid, ipAddr, dataSummary (eto yung minMaxAve, etc), action]
  
# ===========================================================================

#bundleData_updated = [type, bundleSeq, sid, ipAddr, d_ave_gt, d_ave_eq, d_ave_lt, d_min_gt, d_min_eq, d_min_lt, d_max_gt, d_max_eq, d_max_lt]
#15 fields in total
#flowTable_updated = [ruleNo, type, bundleSeq, sid, ipAddr, d_ave_gt, d_ave_eq, d_ave_lt, d_min_gt, d_min_eq, d_min_lt, d_max_gt, d_max_eq, d_max_lt, action]

#flowTable_updated = [ruleNo, type, bundleSeq, sid, ipAddr,
# d_ave_gt, d_ave_eq, d_ave_lt,
# d_min_gt, d_min_eq, d_min_lt,
# d_max_gt, d_max_eq, d_max_lt, action]

  
  # //RULES
  # //0 ip address ==
  # //1 sensor id ==
  # //2 data Ave >
  # //3 data Ave ==
  # //4 data Ave <
  # //5 smallest data >
  # //6 smallest data ==
  # //7 smallest data <
  # //8 largest data >
  # //9 largest data ==
  # //10 largest data <


# Multiple flow matching
# bundleData=['1', '4', '1', '172.24.1.1', '']
# flowTable=[['1', '1', '4', '1', '172.24.1.2', '', '1'], ['2', '1', '4', '1', '172.24.1.1', '', '0'], ['3', '1', '4', '1', '172.24.1.3', '', '5']]
# print "flowTable", flowTable
# print "bundleData", bundleData
# flowTableLength= len(flowTable)

# Compares bundleData against all flows in the flow tables,
# Gets list of probable matched flows

class FlowManager:

    def __init__(self, bundleData, flowTable):
        self.bundleData = bundleData
        self.flowTable = flowTable

        self.type = bundleData[0]
        self.seq = bundleData[1]
        self.sid = bundleData[2]
        self.ipAddr = bundleData[3]
        self.dataSummary = bundleData[4]

    # def getBundleData(bundleData):
    #     self.bundleData = bundleData
    #     self.type = bundleData[0]
    #     self.seq = bundleData[1]
    #     self.sid = bundleData[2]
    #     self.ipAddr = bundleData[3]
    #     self.dataSummary = bundleData[4]

    def getType(self):
        return self.type

    def getSeq(self):
        return self.seq

    def getSID(self):
        return self.sid

    def getIPaddr(self):
        return self.ipAddr

    def getDataSummary(self):
        return self.dataSummary

    def parseDataSummary(self):
        pass


    def getFlowTableLength(self):
        # Define flow table here?
        # flowTable = [[ruleNo(int), ipAddr(str ), field2, field3, action(int)]]
        # flowTable = flowTable=[[1, 'b', 3, 'x', 'action'], [2, 'c', 3, 'y', 'action']]
        self.flowTableLength = len(self.flowTable)
        return self.flowTableLength

    def getFlowTable(self):
        # Define flow table here?
        # flowTable = [[ruleNo(int), ipAddr(str ), field2, field3, action(int)]]
        # flowTable = flowTable=[[1, 'b', 3, 'x', 'action'], [2, 'c', 3, 'y', 'action']]
        # print self.flowTable
        return self.flowTable

    # def getMiniFlowTable(self):

    #     self.Mini = self.getFlowTable()
    #     lenz = len(self.Mini)+1
    #     for index_x, x in enumerate(self.Mini):
    #         for index_y, y in enumerate(x):
    #             self.Mini[index_x][index_y] = self.Mini[index_x][1:lenz]
            
    #     return self.Mini
    
        
    # def flowMatching(self):
    #     intersection_a = [list(filter(lambda x: x in self.bundleData, sublist)) for sublist in self.flowTable]

    #     # Returns list ng intersections ng bundleData and flowTable
    #     # print "intersection", (intersection_a)

     
    #     try:

    #         # Gets the index of the matching flow
    #         matchedFlowIndex = intersection_a.index(self.bundleData)
    #         print "index ng intersection", matchedFlowIndex

    #         # Gets the matching flow (list/whole row)
    #         matchedFlow = self.flowTable[matchedFlowIndex]
    #         print "matched flow index", matchedFlow

    #         # Gets the matching flow ruleNo
    #         matchedFlowRuleNo = self.flowTable[matchedFlowIndex][0]
    #         print "matched flow rule", matchedFlowRuleNo

    #         # Gets corresponding action of matched flow 
    #         matchedFlowAction = self.flowTable[matchedFlowIndex][6]
    #         print "matched flow action", matchedFlowAction

    #         return matchedFlowAction

    #     except ValueError:
    #         print "No Matching Flow"           

    def flowMatching_v2(self):
        # Mano manong iteration to be able to check each field
        # For RegExp purposes
        # wildcards*
        rule_length = len(flowTable[0])

        # Iterates per row
        for index_i, i in enumerate(flowTable):
            # print bundle_date[index_i], index_i, i

            # Iterates per elem in row rule
            for index_j, j in enumerate(i):
                # If same dun sa element, or wildcard
                if((bundle_date[index_i][index_j] == j) || (j=='*')):
                    # print index_j, j
                    ctr = ctr+1
                    # per match, +1 sa counter
                else:
                    break

            if(ctr == rule_length):
                matchedFlowIndex = index_i
                matchedFlowAction = flowTable_master[matchedFlowIndex][-1]
            #     # if ctr == sa number of columns ng flow table, ibig sabihin match.
            #     # save index number to a var
            #     # exit then return yung index number nun.
                break

        # return action_integer dapat to eh
        # returns string
        return matchedFlowAction



        
        # v1 demo================================
        # intersection_a = [list(filter(lambda x: x in self.bundleData, sublist)) for sublist in self.flowTable]

        # # Returns list ng intersections ng bundleData and flowTable
        # # print "intersection", (intersection_a)

     
        # try:

        #     # Gets the index of the matching flow
        #     matchedFlowIndex = intersection_a.index(self.bundleData)
        #     print "index ng intersection", matchedFlowIndex

        #     # Gets the matching flow (list/whole row)
        #     matchedFlow = self.flowTable[matchedFlowIndex]
        #     print "matched flow index", matchedFlow

        #     # Gets the matching flow ruleNo
        #     matchedFlowRuleNo = self.flowTable[matchedFlowIndex][0]
        #     print "matched flow rule", matchedFlowRuleNo

        #     # Gets corresponding action of matched flow 
        #     matchedFlowAction = self.flowTable[matchedFlowIndex][6]
        #     print "matched flow action", matchedFlowAction

        #     return matchedFlowAction

        # except ValueError:
        #     print "No Matching Flow"   

    def __getIntersection(self):
        intersection_a = [list(filter(lambda x: x in self.bundleData, sublist)) for sublist in self.flowTable]
        # Returns list ng intersections ng bundleData and flowTable
        print "intersection", (intersection_a)
        return intersection_a

    def __getMatchedFlowIndex(self):
        matchedFlowIndex = __getIntersection().index(self.bundleData)
        print "index ng intersection", matchedFlowIndex
        return matchedFlowIndex        

    def __getMatchedFlowRuleNo(self):
        matchedFlowRuleNo = self.flowTable[matchedFlowIndex][0]
        # print "matched flow rule", matchedFlowRuleNo
        return matchedFlowRuleNo

    def __getMatchedFlow(self):            # Gets the matching flow (list/whole row)
        matchedFlow = self.flowTable[matchedFlowIndex]
        # print "matched flow index", matchedFlow
        return matchedFlow

    def createNewFlow(self, add_flow):
        self.flowTable.append(add_flow)
        # aList = [123, 'xyz', 'zara', 'abc']
        # aList.insert( 3, 2009)

        newRuleNo = self.getFlowTableLength()+1
        print "newRuleNo", newRuleNo
        newRule = [newRuleNo]
        # param ng add flow
        # rule_na_pinass = ['3', '5', '2', '172.24.1.5', '']
        newRule.extend(add_flow)
        # log me

    def editFlow(self, edit_flow, ruleNo):
        self.flowTable[ruleNo] = edit_flow
        # log me
        # b = [1, 1, 1]
        # b = [1,1,1,1,1]
        # print "editing flow[2] with: ", b  
        # flowTable[2][0:3] = b

    def deleteFlow(self, ruleNo):
        # pass rule number/numbers, then rekta index
        self.flowTable.remove(self.flowTable[ruleNo-1])
        # log me
    
def main():

    bundleData=['1', '4', '1', '172.24.1.1', '']
    match_flowTable=[['1', '1', '4', '1', '172.24.1.2', '', '1'], ['2', '1', '4', '1', '172.24.1.1', '', '0'], ['3', '1', '4', '1', '172.24.1.3', '', '5']]
    noMatch_flowTable=[['1', '1', '4', '1', '172.24.1.2', '', '1'], ['3', '1', '4', '1', '172.24.1.3', '', '5']]


    flow = FlowManager(bundleData, match_flowTable)
    flow.getFlowTable()


    x = flow.flowMatching()
    print "return value", x

    flow.createNewFlow(['3', '5', '2', '172.24.1.5', ''])

    print""

    print "flowTable"
    print(flow.getFlowTable())

    # flow__getIntersection()
    # flow.__getMatchedFlowIndex()


    # ==================================== v2 demo
    bundleData=['1', '4', '1', '172.24.1.1', '']
    flowTable_master=[['1', '1', '4', '1', '172.24.1.2', ''], ['2', '1', '4', '1', '172.24.1.1', ''], ['3', '1', '4', '1', '172.24.1.3', '']]
    flowTable_mini=[['1', '1', '4', '1', '172.24.1.2', '', '1'], ['2', '1', '4', '1', '172.24.1.1', '', '0'], ['3', '1', '4', '1', '172.24.1.3', '', '5']]
    
    
if __name__ == "__main__":
    main()