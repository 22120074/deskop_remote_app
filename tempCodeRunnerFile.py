    # def putkeyboard(self, client_socket):
    #     on_release = True
    #     while on_release:
    #         with keyboard.Listener(
    #             on_press = lambda key: self.keyPressed(key, client_socket),
    #             on_release = lambda key: self.keyReleased(key, client_socket)
    #         ) as listener:
    #             listener.join()
    
        
    # def getKeyName(self, key):
    #     if isinstance(key, keyboard.KeyCode):
    #         return key.char
    #     else:
    #         return str(key)


    # def keyPressed(self, key,client_socket):
    #     keyName = self.getKeyName(key)
    #     # print(keyName)
    #     message = f"{'keyboard'},{keyName},{'on_press'} "
    #     client_socket.send(message.encode('utf-8'))
    #     time.sleep(0.1)

        
    # def keyReleased(self, key,client_socket):
    #     keyName = self.getKeyName(key)
    #     # AAA print(keyName)
    #     message = f"{'keyboard'},{keyName},{'on_release'} "
    #     client_socket.send(message.encode('utf-8'))
    #     if key == keyboard.Key.esc:
    #         return False
    #     time.sleep(0.1)

