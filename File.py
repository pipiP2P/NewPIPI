class File_Info:
    PARTS_PATH = shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, None, 0) + "Completed"
    def __init__(self, name, description, size, num_of_parts, _hash):
        self.name = name
        self.description = description
        self.size = size
        self.num_of_parts = num_of_parts
        self._hash = _hash

    def to_string(self):
        return (self.name + ";" + self.description + ";" + str(self.size) + ";" +
                str(self.num_of_parts) + ";" + self._hash).encode("base64")

    def print_file_info(self):
        print self.name
        print "\tFile Description: " + self.description
        print "\tFile Size: " + str(self.size) + " Bytes"
        print "\tNumber of Parts: " + str(self.num_of_parts)
        print "\tFile Hash " + self._hash

    def get_hash(self):
        return self._hash

    def get_name(self):
        return self.name

    def get_size(self):
        return self.size

    def get_file_content(self, part_number):
        if part_number <= self.num_of_parts:
            requested_part_path = PARTS_PATH + "COMPLETED" + "\\" + self.name + str(part_number)


    def get_num_of_parts(self):
        return self.num_of_parts
