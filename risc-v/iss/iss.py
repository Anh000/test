# Hàm nhập file, đọc và xuất dữ liệu trong file
def inp(file_path):
    # Reset file output
    reset_file('datamem_output.txt')
    memory = Memory()
    decoder = Instruction()
    executor = Executor(memory)
    try:
        # Mở file văn bản với chế độ đọc
        with open(file_path, 'r') as file:
           # Lặp qua từng dòng trong file
            for line in file:
                    # Xử lý và nạp nội dung vào file 
                    binary = line.strip()
                    if len(binary) == 32:
                        decoded_instr = decoder.instruction(binary)
                        if decoded_instr:
                            executor.inst(decoded_instr)
        # Reset file output
        reset_file('datamem_output.txt')
        memory.save_to_file('datamem_output.txt')
    except FileNotFoundError:
        print(f"Không tìm thấy file: {file_path}")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
# Reset file 
def reset_file(ten_file):
    with open(ten_file, 'w') as f:
        pass
# Xử lý memory
class Memory:
    def __init__(self):
        self.data = [0] * 32
        self.registers = [0] * 32
        
    def write_word(self, address, value):
        index = address // 4
        if 0 <= index < 32:
            self.data[index] = value & 0xFFFFFFFF
            
    def read_word(self, address):
        index = address // 4
        if 0 <= index < 32:
            return self.data[index]
        return 0
    
    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            for value in self.data:
                binary = format(value & 0xFFFFFFFF, '032b')
                f.write(binary + '\n')
# Xử lý lệnh
class Instruction:
    def instruction(self, binary):
        opcode = binary[-7:]

        if opcode == "1100011":  # B-type (BNE)
            rs1 = int(binary[12:17], 2)
            rs2 = int(binary[7:12], 2)
            imm = (int(binary[0], 2) << 12) + \
                  (int(binary[24], 2) << 11) + \
                  (int(binary[1:7], 2) << 5) + \
                  (int(binary[20:24], 2) << 1)
            funct3 = binary[17:20]
            return {"type": "B", "opcode": opcode, "rs1": rs1, "rs2": rs2, 
                    "funct3": funct3, "imm": imm}
        
        elif opcode == "1101111":  # JAL
            rd = int(binary[20:25], 2)
            imm = (int(binary[0], 2) << 20) + \
                  (int(binary[12:20], 2) << 12) + \
                  (int(binary[11], 2) << 11) + \
                  (int(binary[1:11], 2) << 1)
            if imm & 0x100000:  # Sign extend
                imm = imm - 0x200000
            return {"type": "J", "opcode": opcode, "rd": rd, "imm": imm}
        
        elif opcode == "0110111":  # LUI
            rd = int(binary[20:25], 2)
            imm = int(binary[0:20], 2)
            return {"type": "U", "opcode": opcode, "rd": rd, "imm": imm}
        
        elif opcode == "0010111":  # AUIPC
            rd = int(binary[20:25], 2)
            imm = int(binary[0:20], 2)
            return {"type": "U", "opcode": opcode, "rd": rd, "imm": imm}
            
        elif opcode == "0010011":  # I-type
            rd = int(binary[20:25], 2)
            funct3 = binary[17:20]
            rs1 = int(binary[12:17], 2)
            imm = int(binary[0:12], 2)
            return {"type": "I", "opcode": opcode, "rd": rd, "rs1": rs1, "funct3": funct3, "imm": imm}
            
        elif opcode == "0100011":  # S-type
            imm = binary[0:7] + binary[20:25]
            rs2 = int(binary[7:12], 2)
            rs1 = int(binary[12:17], 2)
            funct3 = binary[17:20]
            return {"type": "S", "opcode": opcode, "rs1": rs1, "rs2": rs2, "funct3": funct3, "imm": int(imm, 2)}
            
        elif opcode == "0110011":  # R-type
            rd = int(binary[20:25], 2)
            funct3 = binary[17:20]
            rs1 = int(binary[12:17], 2)
            rs2 = int(binary[7:12], 2)
            funct7 = binary[0:7]
            return {"type": "R", "opcode": opcode, "rd": rd, "rs1": rs1, "rs2": rs2, "funct3": funct3, "funct7": funct7}
# Thực thi
class Executor:
    def __init__(self, memory):
        self.memory = memory
        self.pc = 0
    
    def inst(self, decoded_instr):
        if not decoded_instr:
            return
            
        instr_type = decoded_instr["type"]
        should_increment_pc = True  # Mặc định tăng PC
        
        if instr_type == "R":
            self.r_type(decoded_instr)
        elif instr_type == "I":
            self.i_type(decoded_instr)
        elif instr_type == "S":
            self.s_type(decoded_instr)
        elif instr_type == "U":
            self.u_type(decoded_instr)
        elif instr_type == "B":
            should_increment_pc = not self.b_type(decoded_instr)
        elif instr_type == "J":
            should_increment_pc = False
            self.pc = self.j_type(decoded_instr)
            
        self.memory.registers[0] = 0  # x0 luôn bằng 0
        
        if should_increment_pc:
            self.pc += 4
    
    def r_type(self, instr):
        rd = instr["rd"]
        rs1 = instr["rs1"]
        rs2 = instr["rs2"]
        funct3 = instr["funct3"]
        funct7 = instr["funct7"]
        
        val1 = self.memory.registers[rs1]
        val2 = self.memory.registers[rs2]
        
        result = 0
        if funct3 == "000":  # ADD/SUB
            if funct7 == "0000000":
                result = val1 + val2
            elif funct7 == "0100000":
                result = val1 - val2
        elif funct3 == "001":  # SLL
            result = val1 << (val2 & 0x1F)
        elif funct3 == "010":  # SLT
            result = 1 if (val1 < val2) else 0
        elif funct3 == "101":  # SRL
            result = (val1 & 0xFFFFFFFF) >> (val2 & 0x1F)
        elif funct3 == "110":  # OR
            result = val1 | val2
        elif funct3 == "111":  # AND
            result = val1 & val2
        elif funct3 == "100":  # XOR
            result = val1 ^ val2
            
        self.memory.registers[rd] = result & 0xFFFFFFFF
    
    def i_type(self, instr):
        rd = instr["rd"]
        rs1 = instr["rs1"]
        imm = instr["imm"]
        if imm & 0x800:
            imm = imm - 0x1000
            
        val1 = self.memory.registers[rs1]
        
        if instr["funct3"] == "000":  # ADDI
            result = val1 + imm
            self.memory.registers[rd] = result & 0xFFFFFFFF
        elif instr["funct3"] == "010":  # LW
            address = (val1 + imm) & 0xFFFFFFFF
            self.memory.registers[rd] = self.memory.read_word(address)
    
    def s_type(self, instr):
        rs1 = instr["rs1"]
        rs2 = instr["rs2"]
        imm = instr["imm"]
        if imm & 0x800:
            imm = imm - 0x1000
        
        base = self.memory.registers[rs1]
        address = imm
        value = self.memory.registers[rs2]
        
        if instr["funct3"] == "010":  # SW
            self.memory.write_word(address, value)

    def b_type(self, instr):
        rs1 = instr["rs1"]
        rs2 = instr["rs2"]
        imm = instr["imm"]
        
        val1 = self.memory.registers[rs1]
        val2 = self.memory.registers[rs2]
        
        if instr["funct3"] == "001":  # BNE
            if val1 != val2:
                self.pc = self.pc + imm
                return True
        return False
    
    def u_type(self, instr):
        rd = instr["rd"]
        imm = instr["imm"]
        
        if instr["opcode"] == "0110111":  # LUI
            self.memory.registers[rd] = imm << 12
        elif instr["opcode"] == "0010111":  # AUIPC
            self.memory.registers[rd] = (self.pc + (imm << 12)) & 0xFFFFFFFF

    def j_type(self, instr):
        rd = instr["rd"]
        imm = instr["imm"]
        
        # Lưu địa chỉ return vào rd
        self.memory.registers[rd] = self.pc + 4
        
        # Tính địa chỉ nhảy tới
        return self.pc + imm

inp(input('Nhap ten file: '))