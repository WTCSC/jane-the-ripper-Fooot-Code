import hashlib
from jane_the_ripper import crackPasswords

def test_crackPasswords_md5(tmp_path):
    """
    Tests if crackPasswords will return the correct dictionary including the 
    md5 hash and ensures that its value {key, value} is the password (676767)
    """
    password = "676767"
    md5_hash = hashlib.md5(password.encode()).hexdigest()

    # Creates temp files because the function requires file input
    hashes_file = tmp_path / "hashes.txt"
    wordlist_file = tmp_path / "words.txt"

    hashes_file.write_text(md5_hash + "\n")
    wordlist_file.write_text(password + "\n")

    result = crackPasswords(str(hashes_file), str(wordlist_file), ("md5", hashlib.md5))

    assert md5_hash in result
    assert result[md5_hash].strip() == password

def test_crackPasswords_sha256(tmp_path):
    """
    Tests if crackPasswords will return the correct dictionary including the 
    sha256 hash and ensures that its value {key, value} is the password 
    (iAmaReallySecurePassword4354435!!!)
    """

    password = "iAmaReallySecurePassword4354435!!!"
    sha256_hash = hashlib.sha256(password.encode()).hexdigest()

    hashes_file = tmp_path / "hashes.txt"
    wordlist_file = tmp_path / "words.txt"

    hashes_file.write_text(sha256_hash + "\n")
    wordlist_file.write_text(password + "\n")

    result = crackPasswords(str(hashes_file), str(wordlist_file), ("sha256", hashlib.sha256))

    assert sha256_hash in result
    assert result[sha256_hash].strip() == password

def test_crackPasswords_sha1(tmp_path):
    """
    Tests if crackPasswords will return the correct dictionary including the 
    sha1 hash and ensures that its value {key, value} is the password 
    (reallyGoodPassword#67)
    """
    
    password = "reallyGoodPassword#67"
    sha1_hash = hashlib.sha1(password.encode()).hexdigest()

    hashes_file = tmp_path / "hashes.txt"
    wordlist_file = tmp_path / "words.txt"

    hashes_file.write_text(sha1_hash + "\n")
    wordlist_file.write_text(password + "\n")

    result = crackPasswords(str(hashes_file), str(wordlist_file), ("sha1", hashlib.sha1))

    assert sha1_hash in result
    assert result[sha1_hash].strip() == password


def test_crackPasswords_sha1_not_cracked(tmp_path):
    """
    Tests that the function handles hashes that are not found in words.txt.
    Does so by encoding a different hash (iAMNOTTHEPASSWORD) than the password
    (reallyGoodPassword#67)
    """
    password = "reallyGoodPassword#67"
    sha1_hash = hashlib.sha1("iAMNOTTHEPASSWORD".encode()).hexdigest() # creates a different hash to include a case where the hash is not found

    hashes_file = tmp_path / "hashes.txt"
    wordlist_file = tmp_path / "words.txt"

    hashes_file.write_text(sha1_hash + "\n")
    wordlist_file.write_text(password + "\n")

    result = crackPasswords(str(hashes_file), str(wordlist_file), ("sha1", hashlib.sha1))

    assert sha1_hash in result
    assert result[sha1_hash].strip() == "" # if the hash is not found, it will be an empty string

def test_crackPasswords_sha256_not_cracked(tmp_path):
    """
    Tests that the function handles hashes that are not found in words.txt.
    Does so by encoding a different hash (nopeNotThdpassword) than the password
    (iAmUnCrACkable21243)
    """
    password = "iAmUnCrACkable21243"
    sha256_hash = hashlib.sha256("nopeNotThdpassword".encode()).hexdigest()

    hashes_file = tmp_path / "hashes.txt"
    wordlist_file = tmp_path / "words.txt"

    hashes_file.write_text(sha256_hash + "\n")
    wordlist_file.write_text(password + "\n")

    result = crackPasswords(str(hashes_file), str(wordlist_file), ("sha256", hashlib.sha256))

    assert sha256_hash in result
    assert result[sha256_hash].strip() == ""

def test_crackPasswords_md5_not_cracked(tmp_path):
    """
    Tests that the function handles hashes that are not found in words.txt.
    Does so by encoding a different hash (notCracked) than the password
    (wowThis!Pass$wordIsSoSecuRe!!)
    """
        
    password = "wowThis!Pass$wordIsSoSecuRe!!"
    md5_hash = hashlib.md5("notCracked".encode()).hexdigest()

    # Creates temp files because the function requires file input
    hashes_file = tmp_path / "hashes.txt"
    wordlist_file = tmp_path / "words.txt"

    hashes_file.write_text(md5_hash + "\n")
    wordlist_file.write_text(password + "\n")

    result = crackPasswords(str(hashes_file), str(wordlist_file), ("md5", hashlib.md5))

    assert md5_hash in result
    assert result[md5_hash].strip() == ""