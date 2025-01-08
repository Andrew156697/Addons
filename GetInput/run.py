import os
import json

def load_configuration():
    """
    Đọc cấu hình từ tệp options.json của Home Assistant.
    """
    try:
        # Đường dẫn mặc định của tệp cấu hình trong addon
        config_path = "/data/options.json"
        
        # Đọc tệp JSON
        with open(config_path, "r") as file:
            config = json.load(file)
        
        # Lấy giá trị của 'head' từ cấu hình
        head = config.get("head", 50)  # Mặc định 50 nếu không được thiết lập
        if not (0 <= head <= 100):
            raise ValueError(f"Invalid head value: {head}. Must be between 0 and 100.")
        
        print(f"Configured head value: {head}")
        return head
    except FileNotFoundError:
        print("Configuration file not found.")
        return 50  # Giá trị mặc định nếu không tìm thấy tệp
    except ValueError as e:
        print(f"Configuration error: {e}")
        return 50  # Giá trị mặc định nếu có lỗi
# Load configuration
head = load_configuration()

# Hiển thị giá trị của `head`
print(f"Head angle is set to: {head}°")
