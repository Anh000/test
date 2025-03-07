def so_sanh_va_dem_loi(file1, file2):

    loai_loi = {
        "Sai": 0
    }
    try:
        with open(file1, 'r') as f1, open(file2, 'r') as f2:
            line_number = 1
            line1 = f1.readline()
            line2 = f2.readline()

            while line1 or line2:
                if line1 != line2:
                    loai_loi["Sai"] += 1
                    print(f"Dòng {line_number} khác nhau:")
                    if line1:
                        print(f"  File 1: {line1.strip()}")
                    else:
                        print(f"  File 1 không còn nội dung.")
                    if line2:
                        print(f"  File 2: {line2.strip()}")
                    else:
                        print(f"  File 2 không còn nội dung.")

                line1 = f1.readline()
                line2 = f2.readline()
                line_number += 1
        for loai, so_luong in loai_loi.items():
            print(f"{loai}: {so_luong}")
        return loai_loi
    except FileNotFoundError:
        print("Một trong hai file không tồn tại.")
    except IOError:
        print("Lỗi khi đọc file.")
file1 = 'example_output.txt'
file2 = 'test_rar.txt'
ket_qua = so_sanh_va_dem_loi(file1, file2)