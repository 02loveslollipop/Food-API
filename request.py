import requests
import hashlib

class ModelRequest:
    def __init__(self, host: str, argsList: list, port: str = 80,resource: str = None, protocol: str = 'http') -> None:
        self.host = host
        self.port = port
        self.port = port
        self.resource = resource
        self.protocol = protocol
        self.argsList = argsList
        if self.resource == None:
            self.url = f"{self.protocol}://{self.host}:{self.port}/"
        else:    
            self.url = f"{self.protocol}://{self.host}:{self.port}/{resource}"
        
    def setUrl(self,resource:str,protocol:str,host:str,port:str) -> None:
        self.url = f"{protocol}://{host}:{port}/{resource}"
    
    def request(self,args: list) -> requests.Response:
        
        if len(args) != len(self.argsList):
            raise ValueError("The length of the args and the argsList is different")

        header = {}
        for i in range(len(args)):
            header.update({self.argsList[i]: args[i]})
            
        print(header) #TODO: quitar esto
        try:
            return requests.get(self.url, headers=header)
        except requests.exceptions.ConnectionError as e:
            raise ConnectionRefusedError("The host isn't available, please check the host is up and running")