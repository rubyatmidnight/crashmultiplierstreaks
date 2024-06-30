import pandas as pd
import hmac
import hashlib

# original code by Seal, adjusted by rubyatmidnight

def createCrashMulti(hash):
    part1 = int(hash[0], 16) * (16 ** 7)
    part2 = int(hash[1], 16) * (16 ** 6)
    part3 = int(hash[2], 16) * (16 ** 5)
    part4 = int(hash[3], 16) * (16 ** 4)
    part5 = int(hash[4], 16) * (16 ** 3)
    part6 = int(hash[5], 16) * (16 ** 2)
    part7 = int(hash[6], 16) * (16 ** 1)
    part8 = int(hash[7], 16) * (16 ** 0)
   
    result = (part1 + part2 + part3 + part4 + part5 + part6 + part7 + part8)
    finalResult = (4294967296 / ((int(result) + 1))) * (.99)
    return finalResult

def createCrashHistory(crashseed, histlength):
    crashList = []
    messageDec = int(input("Enter 1 for stake.com, or 2 for stake.us: "))
    
    if messageDec == 1:
        messageChoice = '0000000000000000001b34dc6a1e86083f95500b096231436e9b25cbdd0075c4'
    else:
        messageChoice = '000000000000000000066448f2f56069750fc40c718322766b6bdf63fdcf45b8'

    for i in range(0, histlength):
        currHash = hmac.new(bytes(crashseed, 'utf-8'), messageChoice.encode("utf-8"), hashlib.sha256).hexdigest()
       
        crashseed = hashlib.sha256(crashseed.encode("utf-8")).hexdigest()
        crashList.append(createCrashMulti(currHash))
    crashdf = pd.DataFrame(crashList)
    crashdf.rename(columns={0: "Multiplier"}, inplace=True)
   
    return crashdf

def findStreaks(df, max_multiplier):
    maskSetting = int(input("Type '1' for consecutive losses, or '2' for consecutive wins: "))
    if maskSetting == 1:
        mask = df['Multiplier'] < max_multiplier
    else:
        mask = df['Multiplier'] >= max_multiplier
    consecutiveCount = mask.astype(int).groupby((mask != mask.shift()).cumsum()).cumsum()
    return consecutiveCount.groupby(level=0).max().value_counts()

print("You can find the round hash by clicking a result on the game screen in the top right.")

roundHash = input("Please input the most recent round hash, found by clicking the round information: ")
roundCall = int(input("Please input the most recent round number (to check all rounds), or how many rounds back you would like to check: "))
print("Please wait while past results are being generated... this may take a few seconds for larger amounts.")

df = createCrashHistory(roundHash, roundCall)
multiTarget = float(input("Enter desired multiplier 1.01 to 99999999: "))

for max_multiplier in [multiTarget]:
    print(f"Consecutive streaks with multiplier = {max_multiplier}:")
    print(findStreaks(df, max_multiplier))
    print()

