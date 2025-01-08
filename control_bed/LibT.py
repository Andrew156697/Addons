def parse_frame(send_frame):
    # Loại bỏ ký tự '#' ở đầu chuỗi
    if send_frame.startswith("#"):
        send_frame = send_frame[1:]

    # Tách các phần tử bằng ký tự '|'
    parts = send_frame.split("|")

    # Chuyển đổi các phần tử thành số nguyên
    try:
        bed_parameters = [int(part) for part in parts]
    except ValueError:
        raise ValueError("send_frame chứa giá trị không phải số.")

    # Gắn các giá trị vào các biến
    if len(bed_parameters) != 8:
        raise ValueError("send_frame không chứa đủ 8 giá trị.")

    return bed_parameters
