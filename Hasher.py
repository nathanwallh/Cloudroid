#!/usr/bin/python3
from hashlib import sha256
from os import listdir, remove
from os.path import isfile, isdir, join, split
from sys import exc_info
#
BLOCK_SIZE = 256
YELLOW_COLOR = '\033[93m'
WHITE_COLOR = '\033[0m'

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


def save_file(filename, folder_path):
    print("Please write the data fie")
    file_input = input()
    data = ""
    while file_input:
        data += file_input + "\r\n"
        file_input = input()
    try:
        file = open(join(folder_path, filename), 'w')
        [file.write(line) for line in data]
    except Exception as e:
        exception_handling(str(e))
        return None


class Hasher:
    def __init__(self):
        self.hasher = sha256()
        self.__sha_size = 256
        self.__hasher_filename = "Hash/ServerHash.txt"
        self.__server_hash = "0"
        self.check_if_server_updated()

    def read_hash_server_file(self):
        self.__server_hash = '0' * (self.__sha_size >> 2)
        if isfile(self.__hasher_filename):
            self.__server_hash = [str(data) for data in open(self.__hasher_filename, 'r', encoding="utf-8")][0]
            if self.__server_hash.__len__() != (self.__sha_size >> 2):
                self.__server_hash = '0' * (self.__sha_size >> 2)

        return self.__server_hash

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
        folder_list = listdir()
        try:
            for name_folder in folder_list:
                if str(name_folder).split(".").__len__() > 2:
                    for filename in name_folder:
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

    def check_if_server_equal_to_hash(self, server_hash):
        return self.__server_hash == server_hash

    def make_sha256_for_folder(self, folder_path):
        self.hasher = sha256()
        folder_hash = '0' * (self.__sha_size >> 2)

        try:
            dir_path = listdir(folder_path)
            if not dir_path:
                raise NotADirectoryError

            for filename in dir_path:
                sha256_hash = self.open_file(filename, folder_path, "rb")
                if sha256_hash is None:
                    return None
                folder_hash = binary_2_hex(xor(folder_hash, sha256_hash))

        except Exception as e:
            exception_handling(str(e))
            return None

        return self.hasher.hexdigest()

    def update_file(self, folder_path, filename):
        try:
            if not isfile(join(folder_path, filename)):
                raise FileNotFoundError

            sha256_hash = self.open_file(filename, folder_path, "rb")
            if sha256_hash is None:
                return None

            self.__server_hash = binary_2_hex(xor(self.__server_hash, sha256_hash))
            save_file(filename, folder_path)
            if sha256_hash is None:
                return None
            # Why?!
            sha256_hash = self.open_file(filename, folder_path, "rb")
            if sha256_hash is None:
                return None
            self.__server_hash = binary_2_hex(xor(self.__server_hash, sha256_hash))

        except Exception as e:
            exception_handling(str(e))
            return None

        return True

    def delete_file(self, folder_path, filename):
        try:
            filename_path = join(folder_path, filename)
            if not isfile(filename_path):
                raise FileNotFoundError
        except FileNotFoundError as e:
            print(YELLOW_COLOR, "The file isn't exist!!", WHITE_COLOR)
            return None

        try:
            sha256_hash = self.open_file(filename, folder_path, "rb")
            if sha256_hash is None:
                return None

            self.__server_hash = binary_2_hex(xor(self.__server_hash, sha256_hash))
            remove(filename_path)

        except Exception as e:
            exception_handling(str(e))
            return None

        return True

    def create_file(self, folder_path, filename):
        try:
            if isfile(join(folder_path, filename)):
                raise FileExistsError

            save_file(filename, folder_path)
            sha256_hash = self.open_file(filename, folder_path, "rb")
            if sha256_hash is None:
                return None

            self.__server_hash = binary_2_hex(xor(self.__server_hash, sha256_hash))

        except Exception as e:
            print(YELLOW_COLOR, "The file is exist!!", WHITE_COLOR)
            return None
        return True

    def get_server_hash(self):
        return self.__server_hash


def main():
    server_hash = '0' * (256 >> 2)
    # 8b8ee48308eeff9f9f293463b5d32d465d47c7299ee79120f3c9bec5bc5ec34f


    hasher = Hasher()
    hasher.create_file("Oren", "1.txt")
    hasher.create_file("Oren", "2.txt")
    hasher.create_file("Oren1", "1.txt")
    hasher.create_file("Oren1", "2.txt")
    s = hasher.get_server_hash()
    print(s)
    hasher.update_file("Oren1", "2.txt")
    s = hasher.get_server_hash()
    print(s)
    hasher.delete_file("Oren", "1.txt")
    hasher.delete_file("Oren", "2.txt")
    hasher.delete_file("Oren1", "1.txt")
    hasher.delete_file("Oren1", "2.txt")

    s = hasher.get_server_hash()
    hasher.export_hash_server_to_file()
    print(s)


if __name__ == "__main__":
    main()
