import socket, sys, threading
import select
import GnuPG
key_home = 'WhereYouWantYourKeyDirectory'
gpg = gnupg.GPG(gnupghome=key_home)

PORT = 9876

class ChatClient(threading.Thread):

    def __init__(self, port, host='localhost'):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, port))
        # Create public/private key if doesn't exist
        key_name = 'Pujitha'
        key_email = 'poojithampalli@gmail.com'
        rsa_default = 'RSA'
        key_type = '2048'
        key_information = gpg.gen_key_input(name_real=key_name,name_email=key_email, key_type=rsa_default, key_length=key_type)
        self.key = gpg.gen_key(key_information)
        print(gpg.list_keys())

    def send_message(self, msg):
        # Encrypt chat messages in this method
        msg = gpg.encrypt(msg, recipients=[], symmetric="AES256",passphrase="happy")
        data = bytes(msg, 'utf-8')
        self.socket.send(data)

    def ReceiveMessage(self):
        # Decrypt chat messages in this method
        while(True):
            data = self.socket.recv(1024)
            if data:
                msgD = gpg.decrypt(data, passphrase="happy")
                msg = msgD.decode('utf-8')
                print(msg)

    def run(self):
        print("Starting Client")

        # Currently only sends the username
        self.username = input("Username: ")
        self.email = input("Email: ")
        result = gpg.recv_keys('pgp.mit.edu',self.key)
        keyid = gpg.list_keys()[0]['keyid'] # First Public key on ring
        ascii_armored_public_keys = gpg.export_keys(keyids)
        print(ascii_armored_public_keys)
        gpg.recv_keys('pgp.mit.edu',keyid)
        data = bytes(self.username,keyid, 'utf-8')
        self.socket.send(data)

        # Need to get session passphrase
        
        # Starts thread to listen for data
        threading.Thread(target=self.ReceiveMessage).start()
        decrypted_data = gpg.decrypt(encrypted_passphrase, passphrase='my passphrase')
        while(True):
            msg = input(username+":")
            self.send_message(msg)
        
if __name__ == '__main__':
    client = ChatClient(PORT)
    client.start() # This start run()
