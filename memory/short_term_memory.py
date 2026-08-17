from utils.summerize import summerize

class shortTermMemory:

    def __init__(self, max_message=10, summerize_batch=4):
        self.max_message = max_message
        self.summerize_batch = summerize_batch
        self.messages = []

    def add(self, message):
        self.messages.append(message)

        if (len(self.messages) > self.max_message + self.summerize_batch):
            messages = self.messages[0:self.summerize_batch]
            response = summerize(messages)

            self.messages = self.messages[self.summerize_batch:]
            self.messages.insert(0,{
                "role": "system",
                "content": response
            })

    def get_messages(self):
        return self.messages

    def clear_messages(self):
        self.messages = []