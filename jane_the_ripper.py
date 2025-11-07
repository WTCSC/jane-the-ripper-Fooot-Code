import hashlib
import os

def crackPasswords(hashFilePath: str, wordlistPath: str, algorithmToUse: tuple):
    """
    Cracks passwords using the given hash file, wordlist file, and algorithm
    
    Args:
        hashFilePath: Path to the file containing the hashes 
        wordlistFilePath: Path to the file containing the word list
        algorithmToUse: Algorithm that the user chose to use for cracking
    """

    targetHashes = set() # hashes from hashFilePath
    hashDict = {}

    # shake_* algorithms require an explicit digest length
    explicitDigestLength = ""
    if algorithmToUse[0].startswith("shake_"):
        explicitDigestLength = input("Since any shake algorithm requires an explicit digest length, what would you like that to be?\n> ")

    # Adds hashes to the set of target hashes
    with open(hashFilePath, "r") as hashesFile:
        for hash in hashesFile:
            targetHashes.add(hash.strip())
            hashDict[hash.strip()] = ""

    # Cracks passwords by comparing word hashes with target hashes
    with open(wordlistPath, "r") as wordListFile:
        for word in wordListFile:
            wordEncodedStripped = word.strip().encode()
            hashObject = algorithmToUse[1](wordEncodedStripped) # [1] is the function, [0] is the string
            
            # Calls a different function with a different argument for shake algorithms
            if explicitDigestLength:
                hashedWord = hashObject.hexdigest(int(explicitDigestLength))
            else:
                hashedWord = hashObject.hexdigest()

            # If hash is cracked, then print the cracked hash
            if hashedWord in targetHashes:
                hashDict[hashedWord] = word

    return hashDict

    

def main():
    # Hashing algorithms and their functions. Does this for ease of use. 
    # Functions can be accessed by the keys of the algorithm
    availableHashingAlgorithms = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha224': hashlib.sha224,
        'sha256': hashlib.sha256,
        'sha384': hashlib.sha384,
        'sha512': hashlib.sha512,
        'sha3_224': hashlib.sha3_224,
        'sha3_256': hashlib.sha3_256,
        'sha3_384': hashlib.sha3_384,
        'sha3_512': hashlib.sha3_512,
        'shake_128': hashlib.shake_128,
        'shake_256': hashlib.shake_256
    }
    tryAgain = True

    while tryAgain:
        # Path for hash file
        hashFilePath = input("Please input your hash file path\n> ")
        while not os.path.exists(hashFilePath):
            print("Please enter a valid path")
            hashFilePath = input("> ")

        # Path for word list
        wordlistFilePath = input("Please input your word list file path\n> ")
        while not os.path.exists(wordlistFilePath):
            print("Please enter a valid path")
            wordlistFilePath = input("> ")

        # Type of hash algorithm, given in the dictionary above
        hashAlgorithmType = input("Please enter the type of hash algorithm you would like to use?\n> ")
        while hashAlgorithmType not in availableHashingAlgorithms.keys():
            print("Please select from this available list:")
            print(list(availableHashingAlgorithms.keys())) # prints this, as it is a cleaner set than the one I made
            hashAlgorithmType = input("> ")

        algorithmToUse = (hashAlgorithmType, availableHashingAlgorithms[hashAlgorithmType]) # string of algorithm type and function of algorithm

        hashesDictionary = crackPasswords(hashFilePath, wordlistFilePath, algorithmToUse)
        for hashKey, wordValue in hashesDictionary.items():
            if wordValue:
                print(f"[+] Cracked {hashKey} --> {wordValue}")

            else:
                print(f"[-] Couldn't crack hash {hashKey}")

        print("Would you like to try again?")
        tryAgain = True if input("(y or n)> ").lower() == "y" else False
    
if __name__ == "__main__":
    main()