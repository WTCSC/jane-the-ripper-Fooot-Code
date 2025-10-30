import hashlib


def crackPasswords(hashFilePath, wordlistPath, algorithmToUse):
    
    targetHashes = set()
    uncrackableHashes = set()

    # shake_* algorithms require an explicit digest length
    explicitDigestLength = ""
    if algorithmToUse[0].startswith("shake_"):
        explicitDigestLength = input("Since any shake algorithm requires an explicit digest length, what would you like that to be?\n> ")

    with open(hashFilePath, "r") as hashesFile:
        for hash in hashesFile:
            targetHashes.add(hash.strip())

    with open(wordlistPath, "r") as wordListFile:
        for word in wordListFile:
            wordEncodedStripped = word.strip().encode()
            hashObject = algorithmToUse[1](wordEncodedStripped) # [1] is the function, [0] is the string

            
            if explicitDigestLength:
                hashedWord = hashObject.hexdigest(int(explicitDigestLength))
            else:
                hashedWord = hashObject.hexdigest()

            if hashedWord in targetHashes:
                print(f"[+] Cracked {hashedWord} --> {word}")
            else:
                uncrackableHashes.add(hashedWord)
    print("Cracking is finished, here are hashes that weren't found:")
    for uncrackedHash in uncrackableHashes:
        print(f"[-] {uncrackedHash}")

    

def main():
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
        # hashFilePath = input("Please input your hash file path\n> ")
        # wordlistFilePath = input("Please input your word list file path\n> ")
        hashAlgorithmType = input("Please enter the type of hash algorithm you would like to use?\n> ")
        while hashAlgorithmType not in availableHashingAlgorithms.keys():
            print("Please select from this available list:")
            print(list(availableHashingAlgorithms.keys())) # prints this, as it is a cleaner set than the one I made
            hashAlgorithmType = input("> ")

        algorithmToUse = (hashAlgorithmType, availableHashingAlgorithms[hashAlgorithmType]) # string of algorithm and function of algorithm

        crackPasswords("hashes.txt", "wordlist.txt", algorithmToUse)

        print("Would you like to try again?")
        tryAgain = False if input("(y or n)> ").lower() == "n" else True
    
if __name__ == "__main__":
    main()