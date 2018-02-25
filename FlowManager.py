import requests, json

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

    def __init__(self, flowTable):
        self.flowTable = flowTable


    # def getFlowTableLength(self):
    #     self.flowTableLength = len(self.flowTable)
    #     return len(self.flowTableLength)

    def getFlowTable(self):
        # print self.flowTable
        return self.flowTable

    def getBundleData(self, bundleData):
        self.bundleData = bundleData
        return self.bundleData

    def matchFlow(self, bundleData):
        self.bundleData = bundleData
        rule_length = len(self.flowTable[0][1:-1])
        matchedFlowAction = 'No Flow Action Found'
        # Iterates per row
        for ruleIndex, rule in enumerate(self.flowTable):
            # print "==="
            # print "rule #:" + str(ruleIndex) + "rule: " + str(rule)
            # print "==="
            # print ""

            # Iterates per field(columb) in flow rule(row)


            #bundleData_updated = [type, bundleSeq, sid, ipAddr, d_ave_gt, d_ave_eq, d_ave_lt, d_min_gt, d_min_eq, d_min_lt, d_max_gt, d_max_eq, d_max_lt]
            #bundleData_final = [type, bundleSeq, sid, ipAddr, averageData, minData, maxData]

            ctr = 0
            for fieldIndex, ruleField in enumerate(rule[1:-1]):
                # print "ruleField: bundleData: ", ruleField, self.bundleData[fieldIndex]
                
                if((fieldIndex == 4) || (fieldIndex == 7) || (fieldIndex == 10) || (fieldIndex == 6) || (fieldIndex == 9) || (fieldIndex == 12) ):
                    #d_ave_gt
                    if(fieldIndex == 4):
                        if(self.bundleData[4] > ruleField or ruleField=='*'):
                            ctr = ctr+1
                    #d_min_gt
                    elif(fieldIndex == 7):
                        if(self.bundleData[5] > ruleField or ruleField=='*'):
                            ctr = ctr+1
                    #d_max_gt
                    elif(fieldIndex == 10):
                        if(self.bundleData[6] > ruleField or ruleField=='*'):
                            ctr = ctr+1

                    # d_ave_lt
                    elif(fieldIndex == 6):
                        if(self.bundleData[4] < ruleField or ruleField=='*'):
                            ctr = ctr+1
                    # d_min_lt
                    elif(fieldIndex == 9):
                        if(self.bundleData[5] < ruleField or ruleField=='*'):
                            ctr = ctr+1
                    #d_max_lt
                    elif(fieldIndex == 12):
                        if(self.bundleData[6] < ruleField or ruleField=='*'):
                            ctr = ctr+1
                    else:
                        pass

                else(self.bundleData[fieldIndex] == ruleField or ruleField=='*'):
                    # print "fieldIndex: " + str(fieldIndex) + " ruleField: " + str(ruleField) + " bundleData: " + self.bundleData[fieldIndex]                        
                    ctr = ctr+1
             
            # Checks if kumagat sa certain flow rule
            if(ctr == rule_length):

                # print ""
                # print "==="
                matchedFlowIndex = ruleIndex
                # print "matchedFlowRule (Index): ", matchedFlowIndex 
                
                matchedFlowRule = self.flowTable[ruleIndex]
                # print "Flow Rule", matchedFlowRule

                matchedFlowAction = self.flowTable[matchedFlowIndex][-1]
                break

        return matchedFlowAction

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
        # aList.insert( index_to_be_inserted/rule_no, flow_object)
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

    def packetIn(self, bundleJSON):
        server_url="http://sd-dtn-controller.herokuapp.com/packet_in"
        # Insert IP_address here
        # data = json.dumps({'name':'Test connection', 'description':'Here here'})
        r = requests.post(server_url, bundleJSON)
        print r

    def sync(self):
        server_url="http://sd-dtn-controller.herokuapp.com/sync"
        r = requests.get(url = server_url)
        # print "r\n\n", r
        # print "status_code:\n\n", r.status_code
        # print "headers\n\n", r.headers
        # print "Content-Type\n\n", r.headers['Content-Type']
        print "Content:\n", r.content
        # Send back ung flow list via url, tapos get request as params



    
def main():

    # ==================================== v2 demo
    # bundleData=[['1', '4', '1', '172.24.1.1', '']]
    bundleData=['1', '4', '1', '172.24.1.1', '']
    flowTable_mini=[['1', '4', '1', '172.24.1.2', ''], ['1', '4', '1', '172.24.1.1', ''], ['1', '4', '1', '172.24.1.3', '']]
    flowTable_master=[['1', '1', '4', '1', '172.24.1.226', '', '1'], ['2', '1', '4', '1', '172.24.1.1', '', '0'], ['3', '1', '4', '1', '172.24.1.3', '', '5']]
    
    flow = FlowManager(flowTable_master)
    
    print "Getting Master Flow Table"
    print(flow.getFlowTable())

    print""
    print "Get bundleData"
    print(flow.getBundleData(bundleData))


    print""
    print "Matching flows"
    x = flow.matchFlow(bundleData)
    print "Matched Flow Action", x

if __name__ == "__main__":
    main()