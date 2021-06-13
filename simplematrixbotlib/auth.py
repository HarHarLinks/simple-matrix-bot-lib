from fernet_wrapper import Wrapper as fw

class Creds:
    """
    A class to store and handle login credentials.

    ...

    Attributes
    ----------
    homeserver : str
        The homeserver for the bot to connect to. Begins with "https://".
    
    username : str
        The username for the bot to connect as.
    
    password : str
        The password for the bot to connect with.

    """
    def __init__(self, homeserver, username, password, session_stored_file='session.txt'):
        """
        Initializes the simplematrixbotlib.Creds class.

        Parameters
        ----------
        homeserver : str
            The homeserver for the bot to connect to. Begins with "https://".
    
        username : str
            The username for the bot to connect as.
    
        password : str
            The password for the bot to connect with.
        
        session_stored_file : str, optional
            Location for the bot to read and write device_name and access_token. The data within this file is encrypted and decrypted with the password parameter using the cryptography package. If set to None, session data will not be saved to file.
        
        """

        self.homeserver = homeserver
        self.username = username
        self.password = password
        self._session_stored_file = session_stored_file
    
    def session_read_file(self):
        """
        Reads and decrypts the device_name and access_token from file

        """
        if self._session_stored_file:
            try:
                with open(self._session_stored_file, 'r') as f:
                    encrypted_session_data = f.readlines()
                    file_exists = True
                    
            except FileNotFoundError:
                file_exists = False
                print(f'device_name and access_token are not found at {self._session_stored_file}. New device_name and access_token will be created.')
            
            if file_exists:
                key = fw.key_from_pass(self.password)
                decrypted_session_data = fw.decrypt(encrypted_session_data, key)
                
                self.device_name = decrypted_session_data[0]
                self.access_token = decrypted_session_data[1]
        
        else:
            file_exists = False
        
        if not file_exists:
            self.device_name = None
            self.access_token = None
    
    def session_write_file(self):
        """
        Encrypts and writes to file the device_name and access_token.

        """
        if self._session_stored_file:
            session_data = [self.device_name, self.access_token]
            key = fw.key_from_pass(self.password)
            encrypted_session_data = fw.encrypt(session_data, key)

            with open(self._session_stored_file, 'w') as f:
                f.write('{encrypted_session_data}')

            print('device_name and access_token are encrypted and saved to file')
        
        else:
            print('device_name and access_token will not be saved')
            
