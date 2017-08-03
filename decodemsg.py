import base64

msg = "Sh5dOxUVS0JCFhkUblERXFRQRR4CblEVQV1dVFhJOxNRDgsRFlxdOhMTQ1RVFhUOaRMQSF5DRUoJbkxWCVhfUktLKh8UQlQWHRkJLxUeR1RHVFRLIAJRDgsRFkxAIhkVRVRVFhUOaQQXTFNYRUoJbkxW CUJQV1wJYlZRSF5eFhkUblEBR18QFkQ= "
key = "<emailID>"

msgnokey = base64.b64decode(msg)
print(msgnokey)
secret = ""
for i, c in enumerate(msgnokey):
    s= chr(c^ord(key[i % len(key)]))
    secret += s
    print(c, key[i%len(key)], s)
print (secret)

########### output ############
#
# {
#   'success'     : 'great',
#   'colleague'   : 'esteemed',
#   'efforts'     : 'incredible',
#   'achievement' : 'unlocked',
#   'rabbits'     : 'safe',
#   'foo'         : 'win!'
#}
#
##
