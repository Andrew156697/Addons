def Decode_frame(frame):
    """
    Tách 8 số sau dấu # đầu tiên từ chuỗi.

    Args:
        frame: Chuỗi chứa dữ liệu.

    Returns:
        list: Danh sách các số được tách từ chuỗi sau dấu #.
    """
    # Tìm vị trí dấu # đầu tiên
    first_hash_index = frame.find('#')
    
    if first_hash_index == -1:
        raise ValueError("Không tìm thấy dấu # trong chuỗi.")

    # Cắt chuỗi từ vị trí dấu # đầu tiên
    frame_part = frame[first_hash_index + 1:]

    # Tách chuỗi tại dấu '|'
    parts = frame_part.split('|')

    # Lấy 8 giá trị đầu tiên sau dấu #
    if len(parts) < 8:
        raise ValueError("Không có đủ 8 giá trị sau dấu #.")

    # Chuyển các phần tử thành số nguyên
    try:
        numbers = [int(part) for part in parts[:8]]
    except ValueError:
        raise ValueError("Chuỗi chứa giá trị không phải số.")

    return numbers

def combine_values(*values):
    return "#" + "|".join(map(str, values))

# Ví dụ sử dụng
# var1 = 1
# var2 = 0
# var3 = 50
# var4 = 50
# var5 = 50
# var6 = 6000
# var7 = 6000
# var8 = 6000

# combined_frame = combine_values(var1, var2, var3, var4, var5, var6, var7, var8)
# print(f"Gộp các giá trị lại: {combined_frame}")

