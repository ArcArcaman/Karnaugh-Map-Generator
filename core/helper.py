
def is_boolean(val):
    if val == 0 or val == 1 or val == '0' or val == '1':
        return True
    
    return False


class KMap:

    @classmethod
    def find_id(cls, idx, size):
        idx_int = int(idx)
        _offset = [0, 1, 3, 2]

        start_val = idx_int//4
        offset_val = _offset[idx_int%4]
        id = bin(4*start_val + offset_val)[2:]

        return id.zfill(size)

    @classmethod
    def find_idx(cls, row_id, col_id):
        row_int = int(row_id, 2)
        col_int = int(col_id, 2)

        _offset = [0, 1, 3, 2]

        row_start_val = row_int//4
        row_offset = _offset[row_int%4]
        row_idx = 4*row_start_val + row_offset

        col_start_val = col_int//4
        col_offset = _offset[col_int%4]
        col_idx = 4*col_start_val + col_offset

        return (row_idx, col_idx)


    def __init__(self, row_count, col_count, row_name, col_name):
        self.row_bit_count = row_count
        self.col_bit_count = col_count
        self.row_count = 2**row_count
        self.col_count = 2**col_count
        self.row_name = row_name
        self.col_name = col_name
        self._kmap = [['X' for _ in range(2**col_count)] for _ in range(2**row_count)]
    
    
    def set(self, row_id, col_id, val):
        row_idx, col_idx = self.find_idx(row_id, col_id)

        self._kmap[row_idx][col_idx] = val

    
    def __str__(self):
        result = self.row_name+" \\ "+self.col_name+"\n"
        result += "\t"+"\t".join([self.find_id(i, self.col_bit_count) for i in range(self.col_count)])+"\n"
        for i in range(self.row_count):
            result += self.find_id(i, self.row_bit_count)+"\t"+"\t".join(self._kmap[i])+"\n"
        
        return result