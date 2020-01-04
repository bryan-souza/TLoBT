__all__ = ["Message","MessageLog"]

import textwrap
import mechanics.colors as colors

class Message:
    def __init__(self, text, color=colors.white):
        self.text = text
        self.color = color

class MessageLog:
    def __init__(self, x, width, height):
        self.messages = []
        self.x = x
        self.width = width
        self.height = height


    def add_message(self, message):
        #Dividir a mensagem em multiplas linhas caso necessario
        new_msg_lines = textwrap.wrap(message.text, self.width)

        for line in new_msg_lines:
            #caso o log esteja cheio, apagar a primeira linha pra dar espaco
            if len(self.messages) == self.height:
                del self.messages[0]

            #Adicionar uma nova linha ao log como mensagem
            self.messages.append(Message(line, message.color))
