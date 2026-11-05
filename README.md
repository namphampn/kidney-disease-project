# Dự án phân loại bệnh thận mạn tính

Hiện thư mục hoàn thiện phần dữ liệu và EDA của người 1: bước 1, 3, 4, 5. Chưa có thực nghiệm mô hình, ứng dụng Streamlit hoặc kết quả đánh giá cuối cùng.

Bài toán: nhận 24 thuộc tính để phân loại CKD=1 / Not CKD=0. Ưu tiên Recall CKD, theo dõi thêm Precision, F1, ROC-AUC và baseline. Dự án phục vụ học tập và demo.

## Bắt đầu đọc

1. [Báo cáo dữ liệu và EDA](reports/bao_cao_nguoi_1.md).
2. [Bàn giao, kết quả kiểm tra và mức hoàn thành](reports/ban_giao_nguoi_2.md).

Nguồn CSV và dấu kiểm nằm trong [data/README.md](data/README.md); ý nghĩa cột trong [từ điển dữ liệu](reports/data_dictionary.md). Nguồn mô tả gốc UCI đã đối chiếu; URL/ngày tải thực tế của CSV cục bộ cần người tải bổ sung.

## Chạy trên Windows PowerShell

Chạy tại thư mục gốc dự án. Dùng Python 3.13 như môi trường đã kiểm tra.

```powershell
# Chỉ tạo khi chưa có môi trường .venv
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m jupyter notebook
```

Trong Jupyter chọn kernel Python của `.venv`, mở `notebooks/01_eda.ipynb`, chọn Restart Kernel and Run All. Notebook tạo lại 12 ảnh trong `reports/figures/` và các bảng trong `reports/tables/`. Chạy từ thư mục gốc hoặc thư mục notebooks; không chạy từ một thư mục tùy ý khác.

Notebook đã lưu kết quả lần chạy kiểm tra. Hình và bảng sẽ ghi đè khi chạy lại; CSV gốc không bị ghi đè. Báo cáo Markdown chứa nhận xét theo dataset hiện tại; nếu thay dữ liệu, phải cập nhật số liệu và lời nhận xét trong notebook/báo cáo, không chỉ chạy lại biểu đồ.

## Phạm vi các phần

- Người 1: mục tiêu, nguồn, kiểm tra dữ liệu, làm sạch định dạng, EDA và bàn giao.
- Người 2: tách X/y, chia train/test phân tầng, Pipeline/CV, chọn và đánh giá mô hình.
- Người 3: ứng dụng, kiểm thử cuối, tài liệu chung và demo.

Không fit imputer/scaler trên toàn dataset. `clean_features` chỉ nhận X; `encode_target` xử lý y riêng. Xem tài liệu bàn giao trước khi ghép pipeline.

Các phiên bản trong requirements là môi trường đã kiểm tra phần dữ liệu, chưa bao gồm Streamlit hay thư viện phát sinh ở các phần sau. Chưa kiểm chứng cài lại từ đầu trên một máy khác.
