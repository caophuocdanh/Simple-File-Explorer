
import os
from flask import Flask, render_template, send_from_directory, abort, request
from datetime import datetime
import math
import sys

app = Flask(__name__)

# Đường dẫn tuyệt đối đến thư mục gốc cần chia sẻ
SHARED_FILES_DIR = os.path.join(os.getcwd(), 'files')

def get_icon_for_filename(filename):
    """Trả về Font Awesome icon class dựa trên phần mở rộng của file."""
    ext = os.path.splitext(filename)[1].lower()
    if ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg']:
        return 'fas fa-image'  # Icon ảnh
    elif ext in ['.mp4', '.mov', '.avi', '.mkv', '.webm']:
        return 'fas fa-video'  # Icon video
    elif ext in ['.mp3', '.wav', '.flac', '.aac', '.ogg']:
        return 'fas fa-music'  # Icon nhạc
    elif ext in ['.exe', '.msi']:
        return 'fas fa-cog'  # Icon ứng dụng/cài đặt
    elif ext in ['.zip', '.rar', '.7z', '.tar', '.gz']:
        return 'fas fa-file-archive'  # Icon file nén
    elif ext == '.iso':
        return 'fas fa-compact-disc' # Icon file ảnh đĩa
    elif ext == '.gho':
        return 'fas fa-ghost' # Icon file Norton Ghost
    elif ext in ['.txt', '.md']:
        return 'fas fa-file-alt'  # Icon văn bản
    elif ext in ['.json', '.xml', '.html', '.css', '.js', '.py']:
        return 'fas fa-file-code'  # Icon mã
    elif ext == '.pdf':
        return 'fas fa-file-pdf' # Icon PDF
    elif ext in ['.doc', '.docx']:
        return 'fas fa-file-word'  # Icon Word
    elif ext in ['.xls', '.xlsx']:
        return 'fas fa-file-excel'  # Icon Excel
    elif ext in ['.ppt', '.pptx']:
        return 'fas fa-file-powerpoint'  # Icon PowerPoint
    else:
        return 'fas fa-file'  # Icon file chung

def get_human_readable_size(size_bytes):
    """Chuyển đổi kích thước file (bytes) sang định dạng dễ đọc."""
    if size_bytes <= 0:
        return "0 B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def get_directory_size(directory):
    """Tính tổng dung lượng của một thư mục (đệ quy)."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # Bỏ qua các liên kết tượng trưng để tránh tính lặp
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

@app.route('/')
@app.route('/<path:subpath>')
def list_directory(subpath=''):
    """
    Hiển thị danh sách các file và thư mục con với thông tin chi tiết.
    """
    try:
        # --- Logic sắp xếp ---
        sort_by = request.args.get('sort', 'name')
        sort_order = request.args.get('order', 'asc')
        
        requested_path = os.path.join(SHARED_FILES_DIR, subpath)
        
        if not os.path.abspath(requested_path).startswith(os.path.abspath(SHARED_FILES_DIR)):
            abort(404)

        if not os.path.exists(requested_path) or not os.path.isdir(requested_path):
            abort(404)

        items_details = []
        
        dir_items = sorted([item for item in os.listdir(requested_path) if os.path.isdir(os.path.join(requested_path, item))])
        file_items = sorted([item for item in os.listdir(requested_path) if os.path.isfile(os.path.join(requested_path, item))])

        for item_name in dir_items:
            item_path = os.path.join(requested_path, item_name)
            stat_info = os.stat(item_path)
            items_details.append({
                "is_dir": True,
                "icon": 'fas fa-folder',
                "name": item_name,
                "created": datetime.fromtimestamp(stat_info.st_mtime).strftime('%d/%m/%Y %I:%M %p'),
                "type": "File Folder",
                "size": "-",
                "raw_size": -1, # Thư mục luôn ở trên khi sort theo size
                "raw_date": stat_info.st_mtime
            })

        for item_name in file_items:
            item_path = os.path.join(requested_path, item_name)
            stat_info = os.stat(item_path)
            ext = os.path.splitext(item_name)[1].lower()
            file_type = f"{ext[1:].upper()} File" if ext else "File"
            
            viewable_exts = {
                # Hình ảnh
                '.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg',
                # Video
                '.mp4', '.webm', '.ogg',
                # Âm thanh
                '.mp3', '.wav', '.flac',
                # Văn bản
                '.txt', '.md', '.json', '.xml', '.html', '.css', '.js', '.py', '.pdf'
            }
            is_viewable = ext in viewable_exts

            items_details.append({
                "is_dir": False,
                "is_viewable": is_viewable,
                "icon": get_icon_for_filename(item_name),
                "name": item_name,
                "created": datetime.fromtimestamp(stat_info.st_mtime).strftime('%d/%m/%Y %I:%M %p'),
                "type": file_type,
                "size": get_human_readable_size(stat_info.st_size),
                "raw_size": stat_info.st_size,
                "raw_date": stat_info.st_mtime
            })

        # --- Áp dụng logic sắp xếp ---
        sort_key_map = {
            'name': lambda x: x['name'].lower(),
            'date': lambda x: x['raw_date'],
            'type': lambda x: x['type'].lower(),
            'size': lambda x: x['raw_size']
        }
        
        sort_key_func = sort_key_map.get(sort_by, sort_key_map['name'])
        is_reverse = (sort_order == 'desc')

        # Tách thư mục và file để sắp xếp riêng, đảm bảo thư mục luôn ở trên
        dirs = sorted([item for item in items_details if item['is_dir']], key=sort_key_func, reverse=is_reverse)
        files = sorted([item for item in items_details if not item['is_dir']], key=sort_key_func, reverse=is_reverse)
        sorted_items = dirs + files

        parent_path = os.path.dirname(subpath) if subpath else None

        breadcrumbs = []
        if subpath:
            parts = subpath.split('/')
            path_so_far = ''
            for part in parts:
                if path_so_far:
                    path_so_far += '/' + part
                else:
                    path_so_far = part
                breadcrumbs.append({'name': part, 'path': path_so_far})
        
        total_size_str = None
        # Luôn tính tổng dung lượng của thư mục chia sẻ gốc
        total_size_bytes = get_directory_size(SHARED_FILES_DIR)
        total_size_str = get_human_readable_size(total_size_bytes)

        return render_template('index.html', 
                               items=sorted_items, 
                               current_path=subpath,
                               parent_path=parent_path,
                               breadcrumbs=breadcrumbs,
                               sort_by=sort_by,
                               sort_order=sort_order,
                               total_size=total_size_str)
    except Exception as e:
        # Log the error for debugging
        app.logger.error(f"Error in list_directory: {e}")
        # Return a user-friendly error page
        abort(500) # Internal Server Error

@app.route('/view/<path:filepath>')
def view_file(filepath):
    """Hiển thị file trong trình duyệt thay vì tải xuống."""
    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    view_dir = os.path.join(SHARED_FILES_DIR, directory)

    if not os.path.abspath(view_dir).startswith(os.path.abspath(SHARED_FILES_DIR)):
        abort(404)

    # `as_attachment=False` (hoặc bỏ qua) sẽ yêu cầu trình duyệt hiển thị file
    return send_from_directory(view_dir, filename)

@app.route('/download/<path:filepath>')
def download_file(filepath):
    """
    Xử lý việc tải file.
    """
    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    download_dir = os.path.join(SHARED_FILES_DIR, directory)

    if not os.path.abspath(download_dir).startswith(os.path.abspath(SHARED_FILES_DIR)):
        abort(404)

    return send_from_directory(download_dir, filename, as_attachment=True)

if __name__ == '__main__':
    # Kiểm tra và tạo thư mục chia sẻ nếu chưa có
    if not os.path.exists(SHARED_FILES_DIR):
        print(f"Thư mục '{SHARED_FILES_DIR}' không tồn tại. Đang tạo mới...")
        os.makedirs(SHARED_FILES_DIR)
        print(f"Đã tạo thành công thư mục '{SHARED_FILES_DIR}'.")
    elif not os.path.isdir(SHARED_FILES_DIR):
        print(f"Lỗi: Đường dẫn '{SHARED_FILES_DIR}' tồn tại nhưng không phải là thư mục. Vui lòng kiểm tra lại.")
        sys.exit(1)

    # Cổng mặc định là 5000, có thể bị ghi đè bởi tham số dòng lệnh
    port = 5000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Lỗi: '{sys.argv[1]}' không phải là một số cổng hợp lệ. Dùng cổng mặc định 5000.")
    
    print(f"--- Khởi động server tại http://0.0.0.0:{port} ---")
    print("--- Nhấn CTRL+C để dừng server ---")
    app.run(debug=True, host='0.0.0.0', port=port)
