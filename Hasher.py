#!/usr/bin/python3
from hashlib import sha256
from os import listdir, remove
from os.path import isfile, isdir, join, split
from sys import exc_info
import threading

#
BLOCK_SIZE = 256
YELLOW_COLOR = '\033[93m'
WHITE_COLOR = '\033[0m'
UPDATE_TIMER = 3
ROOT_FOLDER = 'user_files'

hex_2_binary = lambda hex_str: \
        bin(int('1' + hex_str, 16))[3:]

xor = lambda x, y: \
        "".join([str(int(i) ^ int(j)) for i, j in zip(bin(int('1' + x, 16))[3:], bin(int('1' + y, 16))[3:])])

binary_2_hex = lambda bit_list: \
        hex(int('1' + bit_list, 2))[3:]

def exception_handling(error_str):
    print(YELLOW_COLOR)
    print("Error using '{0}' function: {1}".format(error_str.split(':')[0], error_str.split(':')[1]))
    exc_type, exc_obj, exc_tb = exc_info()
    fname = split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    print(WHITE_COLOR)


class Hasher:
    def __init__(self):
        self.hasher = sha256()
        self.__sha_size = 256
        self.__hasher_filename = "Hash/ServerHash.txt"
        self.__server_hash = '0' * (self.__sha_size >> 2)
        self.export_hash_server_to_file()
        self.check_if_server_updated()

        self.automatic_update_hash_server()

    def export_hash_server_to_file(self):
        try:
            with open(self.__hasher_filename, "w") as file:
                file.write(self.__server_hash)
        except Exception as e:
            exception_handling(str(e))

    def open_file(self, filename, folder_path, mode):
        try:
            self.hasher = sha256()
            filename_path = join(folder_path, filename)
            with open(filename_path, mode) as file:
                self.hasher.update(bytes(str(filename), 'utf-8'))
                buf = file.read(BLOCK_SIZE)
                while len(buf) > 0:
                    self.hasher.update(buf)
                    buf = file.read(BLOCK_SIZE)
        except Exception as e:
            exception_handling(str(e))
            return None

        return self.hasher.hexdigest()

    def check_if_server_updated(self):
        server_hash = '0' * (self.__sha_size >> 2)

        try:
            for folder_or_file_name in listdir(ROOT_FOLDER):
                if isfile(join(ROOT_FOLDER, folder_or_file_name)):
                    filename = folder_or_file_name
                    sha256_hash = self.open_file(filename, ROOT_FOLDER, "rb")
                    if sha256_hash is None:
                        return False
                    server_hash = binary_2_hex(xor(server_hash, sha256_hash))
                elif isdir((join(ROOT_FOLDER, folder_or_file_name))):
                    name_folder = join(ROOT_FOLDER, folder_or_file_name)
                    for filename in listdir(name_folder):
                        sha256_hash = self.open_file(filename, name_folder, "rb")
                        if sha256_hash is None:
                            return False
                        server_hash = binary_2_hex(xor(server_hash, sha256_hash))
        except Exception as e:
            exception_handling(str(e))
            return False

        if server_hash == self.__server_hash:
            return True

        self.__server_hash = server_hash
        self.export_hash_server_to_file()
        return False



    def get_server_hash(self):
        return self.__server_hash

    def automatic_update_hash_server(self):
        self.check_if_server_updated()
        threading.Timer(UPDATE_TIMER, self.automatic_update_hash_server).start()
sh = Hasher()
