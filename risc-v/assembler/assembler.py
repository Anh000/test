# Hàm nhập file, đọc và xuất dữ liệu trong file
def inp(file_path):
    # Reset file output
    reset_file('example_output.txt')
    try:
        # Mở file văn bản với chế độ đọc
        with open(file_path, 'r') as file:
           # Lặp qua từng dòng trong file
            for line in file:
                if line.startswith('#'):
                    continue
                elif line.startswith('exit'):
                    continue
                else: 
                    # Tách kí tự trong câu
                    line = line.replace(",", " ").replace("(", " ").replace(")", " ")
                    lst = line.split()
                    # Xử lý và nạp nội dung vào file 
                    write_to_file(binary_result(lst))
    except FileNotFoundError:
        print(f"Không tìm thấy file: {file_path}")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
# Hàm thêm nội dung vào file 
def write_to_file(content):
    # Nhập tên file output
    file_path = 'example_output.txt'
    try:
        # Mở file văn bản với chế độ ghi
        with open(file_path, 'a') as file:
            # Ghi nội dung vào file
            file.write(content+'\n')
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
# Reset file 
def reset_file(ten_file):
    with open(ten_file, 'w') as f:
        pass
# Chuyển số thập phân hoặc số thập lục phân sang số nhị phân với số bit cho trước
def binary_with_fixed_bits(number, bits, base=10):
    if base == 10:
        binary_str = bin(int(number))[2:]
        return binary_str.zfill(bits)
    elif base == 16:
        binary_str = bin(int(number, 16))[2:]
        return binary_str.zfill(bits)
# Lấy bit đầu-bit sau cho trước (đầu vào số nguyên)
def get_bits(imm, end, start):
    # Tạo mặt nạ
    mask = ((1 << (end - start + 1)) - 1) << start
    # Thực hiện phép AND và dịch phải
    result = (int(imm) & mask) >> start
    result = bin(result)[2:]
    return result.zfill(end-start+1)
# Chuyển opcode
def opcode(inst):
    if inst in ('add', 'sub', 'xor', 'or', 'and', 'sll', 'srl', 'sra', 'slt', 'sltu'):
        return '0110011'
    elif inst in ('addi', 'xori', 'ori', 'andi', 'slli', 'srli', 'srai', 'slti', 'sltiu'):
        return '0010011'
    elif inst in ('lb', 'lh', 'lw', 'lbu', 'lhu'):
        return '0000011'
    elif inst in ('sb', 'sh', 'sw'):
        return '0100011'
    elif inst in ('beq', 'bne', 'blt', 'bge', 'bltu', 'bgeu'):
        return '1100011'
    elif inst == 'jal':
        return '1101111'
    elif inst == 'jalr':
        return '1100111'
    elif inst == 'lui':
        return '0110111'
    elif inst == 'auipc':
        return '0010111'
    else:
        return 'Error'
# Chuyển funct3
def funct3(inst):
    if inst in ('add', 'sub', 'addi', 'lb', 'sb', 'beq', 'jalr'):
        return '000'
    elif inst in('sll', 'slli', 'lh', 'sh', 'bne'):
        return '001'
    elif inst in ('slt', 'slti', 'lw', 'sw'):
        return '010'
    elif inst in ('sltu', 'sltiu'):
        return '011'
    elif inst in ('xor', 'xori', 'lbu', 'blt'):
        return '100'
    elif inst in ('srl', 'sra', 'srli', 'srai', 'lhu', 'bge'):
        return '101'
    elif inst in ('or', 'ori', 'bltu'):
        return '110'
    elif inst in ('and', 'andi', 'bgeu'):
        return '111'
    else:
        return 'Error'
# Chuyển funct7
def funct7(inst):
    if inst in ('add', 'xor', 'or', 'and', 'sll', 'srl', 'slt', 'sltu'):
        return '0000000'
    elif inst in ('sub', 'sra'):
        return '0100000'
    elif inst in ('slli', 'srli'):
        return '0000000'
    elif inst == 'srai':
        return '0100000'
    else:
        return 'Error'
# Chuyển toán hạng thanh ghi
def register_number(name):
    # Kiểm tra xem tên biến có đúng định dạng x[số] không
  if name.startswith('x') and name[1:].isdigit():
    # Lấy phần số sau chữ x
    so = int(name[1:])
    # Kiểm tra xem số có nằm trong khoảng từ 0 đến 31
    if 0 <= so <= 31:
      return binary_with_fixed_bits(so, 5)
  return 'Error'
# Xử lý file
def offset(list):
    count = 1
    count_next = 1
    try:
        # Mở file văn bản với chế độ đọc
        with open(file_path, 'r') as file:
           # Lặp qua từng dòng trong file
            for line in file:
                if line.startswith(list[0]):
                    break
                elif line.startswith('#'):
                    continue
                count += 1
        with open(file_path, 'r') as file:
           # Lặp qua từng dòng trong file
            for line in file:
                if list[0] in ('beq', 'bne', 'blt', 'bge', 'bltu', 'bgeu'):
                    if line.startswith(list[3]):
                        break
                    elif line.startswith('#'):
                        continue
                    count_next += 1
                elif list[0] == 'jal':
                    if line.startswith(list[2]):
                        break
                    elif line.startswith('#'):
                        continue
                    count_next += 1
    except FileNotFoundError:
        print(f"Không tìm thấy file: {file_path}")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
    return ((count_next-count)*4)

def binary_result(list):
    # R-format
    if list[0] in ('add', 'sub', 'xor', 'or', 'and', 'sll', 'srl', 'sra', 'slt', 'sltu'):
        return (funct7(list[0])+register_number(list[3])+register_number(list[2])+funct3(list[0])+register_number(list[1])+opcode(list[0]))
    # I-format
    elif list[0] in ('addi', 'xori', 'ori', 'andi', 'slli', 'srli', 'srai', 'slti', 'sltiu', 'lb', 'lh', 'lw', 'lbu', 'lhu', 'jalr'):
        if list[0] in ('slli', 'srli', 'srai'):
            return (funct7(list[0])+binary_with_fixed_bits(list[3], 5)+register_number(list[2])+funct3(list[0])+register_number(list[1])+opcode(list[0]))
        elif list[0] in ('lb', 'lh', 'lw', 'lbu', 'lhu', 'jalr'):
            list[2], list[3] = list[3], list[2]
        return (binary_with_fixed_bits(list[3], 12)+register_number(list[2])+funct3(list[0])+register_number(list[1])+opcode(list[0]))
    # S-format
    elif list[0] in ('sb', 'sh', 'sw'):
        return (get_bits(list[2], 11, 5)+register_number(list[1])+register_number(list[3])+funct3(list[0])+get_bits(list[2], 4, 0)+opcode(list[0]))
    # U-format
    elif list[0] in ('lui', 'auipc'):
        return (binary_with_fixed_bits(list[2], 20, 16)+register_number(list[1]) + opcode(list[0]))
    # B-format
    elif list[0] in ('beq', 'bne', 'blt', 'bge', 'bltu', 'bgeu'):
        return (get_bits(offset(list), 12, 12)+get_bits(offset(list), 10, 5)+register_number(list[2])+register_number(list[1])+funct3(list[0])+get_bits(offset(list), 4, 1)+get_bits(offset(list), 11, 11)+opcode(list[0]))
    # J-format
    elif list[0] == 'jal':
        return (get_bits(offset(list), 20, 20)+get_bits(offset(list), 10, 1)+get_bits(offset(list), 11, 11)+get_bits(offset(list), 19, 12)+register_number(list[1])+opcode(list[0]))
    else:
        return 'Error'

# Nhập tên file
file_path = input("Enter file name: ")
inp(file_path)