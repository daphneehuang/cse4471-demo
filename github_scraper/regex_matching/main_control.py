from regex_matching_strings import match_api_key as MatchAPI
from regex_matching_strings import match_password as MatchPW
from regex_matching_strings import match_crypto as MatchCrypto
from regex_matching_strings import match_bitcoin as MatchBitcion 
from regex_matching_strings import match_email as MatchEmail

gfilestr = ""
#takes in a map, runs regex matching on text, and returns type/line number of match
def main(fileMap):
    outputMap = {}
    for key in fileMap:
        outputMap[key] = []
        findMatches(key,fileMap[key],outputMap)
        
    return outputMap


def getLine(filestr=gfilestr):
    prevnl = -1
    while True:
      nextnl = filestr.find('\n', prevnl + 1)
      if nextnl < 0: break
      yield filestr[prevnl + 1:nextnl]
      prevnl = nextnl

def findMatches(key,fileString,outputMap):
    print("finding matches")
    idx = 1
    for line in getLine(fileString):
      if(MatchAPI(line)):
        outputMap[key] = ["API:" + str(idx)]
      if(MatchPW(line)):
        outputMap[key] = ["Password:" + str(idx)]
      if(MatchCrypto(line)):
        outputMap[key] = ["Crypto:" + str(idx)]
      if(MatchBitcion(line)):
        outputMap[key] = ["Bitcoin:" + str(idx)]
      if(MatchEmail(line)):
        outputMap[key] = ["Email:" + str(idx)]

        idx +=1
            

if __name__ == '__main__':
    pass