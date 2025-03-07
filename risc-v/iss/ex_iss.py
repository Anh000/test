# Hàm nhập file, đọc và xuất dữ liệu trong file
def inp(file_path):
    # Reset file output
    reset_file('iss_output.txt')
    try:
        # Mở file văn bản với chế độ đọc
        with open(file_path, 'r') as file:
           # Lặp qua từng dòng trong file
            for line in file:
                    # Xử lý và nạp nội dung vào file 
                    print(line)
                    print(instruction('line'))
    except FileNotFoundError:
        print(f"Không tìm thấy file: {file_path}")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
# Hàm thêm nội dung vào file 
def write_to_file(content):
    # Nhập tên file output
    file_path = 'iss_output.txt'
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
# Lấy bit đầu-bit sau cho trước 
def get_bits(bin_str, end, start):
    binary_str = bin_str.zfill(32) 
    # Kiểm tra tính hợp lệ của chỉ số
    if start < 0 or end >= len(binary_str) or start > end:
        raise ValueError("Chỉ số không hợp lệ")
    # Tính toán lại chỉ số để lấy từ phải sang trái
    new_start = len(binary_str) - end - 1
    new_end = len(binary_str) - start - 1
    return binary_str[new_start:new_end+1]
# Đọc thanh ghi
def register_name(bin_str):
    return ('x'+str(int(bin_str, 2)))
# Tách lệnh 
def instruction(bin_str):
    opcode = get_bits(bin_str, 6, 0)
    if opcode == '0110011':
        return R_format(bin_str)
    elif opcode in ('0010011', '0000011', '1100111'):
        return I_format(bin_str)
    elif opcode == '0100011':
        return S_format(bin_str)
    elif opcode == '1100011':
        return B_format(bin_str)
    elif opcode == '1101111':
        return J_format(bin_str)
    elif opcode in ('0110111', '0010111'):
        return U_format(bin_str)
    else:
        return None
# R-format
def R_format(bin_str):
    rd = get_bits(bin_str, 11, 7)
    funct3 = get_bits(bin_str, 14, 12)
    rs1 = get_bits(bin_str, 19, 15)
    rs2 = get_bits(bin_str, 24, 20)
    funct7 = get_bits(bin_str, 31, 25)
    # Tìm lệnh 
    if (int(funct3, 2) == int('0x0', 16)) and (int(funct7, 2) == int('0x00', 16)):
        inst = 'add'
    elif (int(funct3, 2) == int('0x0', 16)) and (int(funct7, 2) == int('0x20', 16)):
        inst = 'sub'
    elif (int(funct3, 2) == int('0x4', 16)) and (int(funct7, 2) == int('0x00', 16)):
        inst = 'xor'
    elif (int(funct3, 2) == int('0x6', 16)) and (int(funct7, 2) == int('0x00', 16)):
        inst = 'or'
    elif (int(funct3, 2) == int('0x7', 16)) and (int(funct7, 2) == int('0x00', 16)):
        inst = 'and'
    elif (int(funct3, 2) == int('0x1', 16)) and (int(funct7, 2) == int('0x00', 16)):
        inst = 'sll'
    elif (int(funct3, 2) == int('0x5', 16)) and (int(funct7, 2) == int('0x00', 16)):
        inst = 'srl'
    elif (int(funct3, 2) == int('0x5', 16)) and (int(funct7, 2) == int('0x20', 16)):
        inst = 'sra'
    elif (int(funct3, 2) == int('0x2', 16)) and (int(funct7, 2) == int('0x00', 16)):
        inst = 'slt'
    elif (int(funct3, 2) == int('0x3', 16)) and (int(funct7, 2) == int('0x00', 16)):
        inst = 'sltu'
    else:
        inst = None
    return (inst, register_name(rd) + ', ' + register_name(rs1) + ', ' + register_name(rs2))
# S-format
def S_format(bin_str):
    imm = get_bits(bin_str, 11, 5)+get_bits(bin_str, 4, 0)
    funct3 = get_bits(bin_str, 14, 12)
    rs1 = get_bits(bin_str, 19, 15)
    rs2 = get_bits(bin_str, 24, 20)
    if (int(funct3, 2) == int('0x0', 16)):
        inst = 'sb'
    elif (int(funct3, 2) == int('0x1', 16)):
        inst = 'sh'
    elif (int(funct3, 2) == int('0x2', 16)):
        inst = 'sw'
    else:
        inst = None
    return (inst, register_name(rs1) + ', ' + register_name(rs2) + ', ' + str(int(imm, 2)))
# I-format
def I_format(bin_str):
    opcode = get_bits(bin_str, 6, 0)
    rd = get_bits(bin_str, 11, 7)
    funct3 = get_bits(bin_str, 14, 12)
    rs1 = get_bits(bin_str, 19, 15)
    if opcode == '0010011' and (int(funct3, 2) == int('0x1', 16) or int(funct3, 2) == int('0x5', 16)):
        imm = get_bits(bin_str, 24, 20)
        funct7 = get_bits(bin_str, 31, 25)
    else: imm = get_bits(bin_str, 31, 20)
    
    if (opcode == '0010011') and (int(funct3, 2) == int('0x0', 16)):
        inst = 'addi'
    elif (opcode == '0010011') and (int(funct3, 2) == int('0x4', 16)):
        inst = 'xori'
    elif (opcode == '0010011') and (int(funct3, 2) == int('0x6', 16)):
        inst = 'ori'
    elif (opcode == '0010011') and (int(funct3, 2) == int('0x7', 16)):
        inst = 'andi'
    elif (opcode == '0010011') and (int(funct3, 2) == int('0x1', 16)) and (int(funct7, 2) == int('0x00', 16)):
        inst = 'slli'
    elif (opcode == '0010011') and (int(funct3, 2) == int('0x5', 16)) and (int(funct7, 2) == int('0x00', 16)):
        inst = 'srli'
    elif (opcode == '0010011') and (int(funct3, 2) == int('0x5', 16)) and (int(funct7, 2) == int('0x20', 16)):
        inst = 'srai'
    elif (opcode == '0010011') and (int(funct3, 2) == int('0x2', 16)):
        inst = 'slti'
    elif (opcode == '0010011') and (int(funct3, 2) == int('0x3', 16)):
        inst = 'sltiu'
    elif (opcode == '0000011') and (int(funct3, 2) == int('0x0', 16)):
        inst = 'lb'
    elif (opcode == '0000011') and (int(funct3, 2) == int('0x1', 16)):
        inst = 'lh'
    elif (opcode == '0000011') and (int(funct3, 2) == int('0x2', 16)):
        inst = 'lw'
    elif (opcode == '0000011') and (int(funct3, 2) == int('0x4', 16)):
        inst = 'lbu'
    elif (opcode == '0000011') and (int(funct3, 2) == int('0x5', 16)):
        inst = 'lhu'
    else:
        inst = None
    return (inst, register_name(rd) + ', ' + register_name(rs1) + ', ' + str(int(imm, 2)))
# B-format
def B_format(bin_str):
    imm = get_bits(bin_str, 31, 31)+get_bits(bin_str, 7, 7)+get_bits(bin_str, 30, 25)+get_bits(bin_str, 11, 8)
    funct3 = get_bits(bin_str, 14, 12)
    rs1 = get_bits(bin_str, 19, 15)
    rs2 = get_bits(bin_str, 24, 20)
    if (int(funct3, 2) == int('0x0', 16)):
        inst = 'beq'
    elif (int(funct3, 2) == int('0x1', 16)):
        inst = 'bne'
    elif (int(funct3, 2) == int('0x4', 16)):
        inst = 'blt'
    elif (int(funct3, 2) == int('0x5', 16)):
        inst = 'bge'
    elif (int(funct3, 2) == int('0x6', 16)):
        inst = 'bltu'
    elif (int(funct3, 2) == int('0x7', 16)):
        inst = 'bgeu'
    else:
        inst = None
    return (inst, register_name(rs1) + ', ' + register_name(rs2) + ', ' + str(int(imm, 2)))
# J-format
def J_format(bin_str):
    opcode = get_bits(bin_str, 6, 0)
    imm = get_bits(bin_str, 31, 31)+get_bits(bin_str, 19, 12)+get_bits(bin_str, 20, 20)+get_bits(bin_str, 30, 21)
    rd = get_bits(bin_str, 11, 7)
    if opcode == '1101111':
        inst = 'jal'
    else:
        inst = None
    return (inst, register_name(rd) + ', ' + str(int(imm, 2)))
# U-format
def U_format(bin_str):
    opcode = get_bits(bin_str, 6, 0)
    rd = get_bits(bin_str, 11, 7)
    imm = get_bits(bin_str, 31, 12)
    if opcode == '0110111':
        inst = 'lui'
    elif opcode == '0010111':
        inst = 'auipc'
    else:
        inst = None
    return (inst, register_name(rd) + ', ' + str(int(imm, 2)))

print(instruction('00000000000100100001000010010111'))
print(instruction('00000010011000101000000001100011'))
print(instruction('01000000011100110000001010110011'))
