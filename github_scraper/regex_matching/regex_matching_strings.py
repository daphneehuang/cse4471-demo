import re


# matches emails
def match_email(line):
    #https://emailregex.com/
    email = re.compile(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)')
    output = re.findall(email,line)  
    if(len(output) > 0):
        print("Email found")
        print(output)
        return True
    return False

# matches Bitcoin private key, URI, extended public key
def match_bitcoin(line): 
    bitcoinAddress = re.compile(r'[13][a-km-zA-HJ-NP-Z1-9]{25,34}')
    bitcoinURI = re.compile(r'bitcoin:([13][a-km-zA-HJ-NP-Z1-9]{25,34})')
    bitcoinExtendedPublicKey = re.compile(r'(xpub[a-km-zA-HJ-NP-Z1-9]{100,108})(\\?c=\\d*&h=bip\\d{2,3})?')
    bitcoinPrivateKey = re.compile(r'[5KL][1-9A-HJ-NP-Za-km-z]{50,51}')

    regexes = [bitcoinAddress,bitcoinPrivateKey, bitcoinURI, bitcoinExtendedPublicKey]
    
    for regex in regexes:
        output = re.findall(regex,line)  
    if(len(output) > 0):
        print("Bitcoin info found")
        return True
    return False

# matches cryptokeys
def match_crypto(line):
    # keys in hex
    # 56-64 bit keys (DES)
    hex64bit = re.compile(r'[a-fA-F0-9]{14,16}')
    # 128, 192, 256 bit keys with extra parity bits (AES)
    hex128Bit = re.compile(r'[a-fA-F0-9]{32,36}') 
    hex192Bit = re.compile(r'[a-fA-F0-9]{48,54}')
    hex256Bit = re.compile(r'[a-fA-F0-9]{64,72}')
    # 2048 bit key (RSA)
    hex2048Bit = re.compile(r'[a-fA-F0-9]{512}')

    #keys in base64
    base64 = re.compile(r'^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4})(?:=[A-Za-z0-9+/]{4})?$')

    regexes = [hex64bit, hex128Bit, hex192Bit, hex256Bit, hex2048Bit, base64]

    for regex in regexes:
        output = re.findall(regex,line)  
    if(len(output) > 0):
        print("Crypto key info found")
        return True
    return False

# matches passwords
def match_password(line):
    # password with at least 8 characters, one uppercase, one lowercase, one number and one special character
    pw1 = re.compile(r'(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#?!@$%^&*-])[A-Za-z\d#?!@$%^&*-]{8,}')
    # password with variable name 'password', 'pw', or 'p'
    pw2 = re.compile(r'(?:password|pw|p)(?: ?= ?)"?[A-Za-z\d#?!@$%^&*-]+"?')

    regexes = [pw1, pw2]

    for regex in regexes:
        output = re.findall(regex,line)  
    if(len(output) > 0):
        print("Password found")
        return True
    return False

#matches API keys
def match_api_key(line):
    #https://gist.github.com/hsuh/88360eeadb0e8f7136c37fd46a62ee10
    #AWSaccessKeyID = re.compile(r'(?<![A-Z0-9])[A-Z0-9]{20}(?![A-Z0-9])')
    AWSsecretAccessKey = re.compile(r'(?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])')
    AWSsecretAccessKeyAlternative = re.compile(r'[0-9a-zA-Z/+]{40}')
    #https://people.eecs.berkeley.edu/~rohanpadhye/files/key_leaks-msr15.pdf
    #Bitly
    BITsecretAccessKey = re.compile(r'R_[0-9a-f]{32}')
    #Facebook
    FBsecretAccessKey = re.compile(r'[0-9a-f]{32}')

    #FLICKR
    FLsecretAccessKey = re.compile(r'[0-9a-f]{16}')

    #Foursquare
    FSsecretAccessKey = re.compile(r'[0-9A-Z]{48}')

    #LinkedIn
    LIsecretAccessKey = re.compile(r'[0-9a-zA-Z]{16}')

    #Twitter
    TWsecretAccessKey = re.compile(r'[0-9a-zA-Z]{35,44}')

    #only letter
    onlyLetters = re.compile(r'^[a-zA-Z]+$')
    regexar = [AWSaccessKeyID,AWSsecretAccessKey,BITaccessKeyID,BITsecretAccessKey,FBaccessKeyID,FLsecretAccessKey,AWSsecretAccessKeyAlternative]
    
    for exp in regexar:
        output = re.findall(exp,line)  
    if(len(output) > 0 && onlyLetters.match(output[0]) == None):
        print("Api key found")
        return True
    return False

if __name__ == '__main__':
    pass
