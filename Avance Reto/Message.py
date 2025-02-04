class Message():
    environment_buffer = []
    def __init__(self,sender=None,receiver=None,performative=None,content=None):
        self.sender = sender
        self.receiver = receiver
        self.performative = performative
        self.content = content
    def __str__(self):
        return f"\n\
        Sender: {self.sender}, \n\
        Receiver: {self.receiver}, \n\
        Performative: {self.performative}, \n\
        Content: {self.content}"
    def send(self):
        """
        The send function is used to send a message to the environment buffer.
        """
        Message.environment_buffer.append(self)