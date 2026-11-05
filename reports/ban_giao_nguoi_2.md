# Bàn giao dữ liệu cho người 2

## Các tệp cần nhận

- `data/raw/kidney_disease.csv`, `data/README.md`, `reports/data_dictionary.md`.
- `src/config.py`, `src/preprocess.py`.
- `notebooks/01_eda.ipynb`, `reports/figures/`, `reports/tables/`, `reports/bao_cao_nguoi_1.md`.
- `tests/test_preprocess.py`, `requirements.txt` và README.

## Hợp đồng dữ liệu

`X` là DataFrame có đủ 24 cột trong `FEATURE_COLUMNS`; cột `id` được phép có hoặc không. Hàm trả về đúng thứ tự 24 cột, không sửa đầu vào. Ô thiếu được giữ; không chấp nhận thiếu hẳn cột, cột lạ, cột trùng hoặc đưa classification vào X. Giao diện nhận CSV không có nhãn vẫn dùng được.

Cột số được ép float; mã sg/al/su lưu dạng số; các biến văn bản dùng object và np.nan để tương thích SimpleImputer/OneHotEncoder. Token số không hợp lệ hoặc giá trị phân loại văn bản ngoài miền sẽ báo ValueError. Đây chưa phải bộ kiểm tra phạm vi lâm sàng; người 3 cần bổ sung kiểm tra khoảng số và thông báo lỗi giao diện theo nguồn thống nhất.

`encode_target` chuẩn hóa ckd/notckd thành 1/0, chấp nhận nhãn số đã mã hóa và từ chối nhãn thiếu hoặc lạ. Không điền nhãn, không xóa hàng. Hàm `clean_raw` chỉ là tiện ích cho EDA, chạy được cả trên X lẫn bảng có nhãn.

## Cách gọi

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import FunctionTransformer
from src.config import RAW_DATA_PATH, TARGET, RANDOM_STATE
from src.preprocess import clean_features, encode_target

raw = pd.read_csv(RAW_DATA_PATH)
X = raw.drop(columns=[TARGET])  # có thể còn id; cleaner sẽ loại
Y = encode_target(raw[TARGET])
X_train, X_test, y_train, y_test = train_test_split(
    X, Y, test_size=0.2, stratify=Y, random_state=RANDOM_STATE
)
cleaner = FunctionTransformer(clean_features, validate=False)
# Đặt cleaner làm bước đầu Pipeline, tiếp theo ColumnTransformer và mô hình.
# Fit toàn bộ Pipeline bằng CV trên X_train/y_train; không fit trên X_test.
```

Cách chọn imputer, mã hóa sg/al/su, scale, class_weight và siêu tham số thuộc người 2, thực hiện bằng CV trên train. Không chọn từ biểu đồ toàn tập hoặc kết quả test. Cleaner không học tham số, còn median/mode/scaler có học tham số và phải fit riêng trong mỗi fold.

## Đã kiểm tra và chưa kiểm tra

8 nhóm kiểm thử bao gồm dữ liệu thực, token thiếu, schema, nhãn lỗi, không sửa đầu vào, chạy lặp, thứ tự cột, FunctionTransformer + ColumnTransformer + imputer/encoder/scaler và lưu–nạp bằng joblib. Có kiểm tra 80 dòng đầu vào không nhãn, trong đó một dòng toàn ô thiếu, đầu ra hữu hạn và nạp lại giống nhau.

Bộ kiểm tra tích hợp chỉ kiểm tra đường đi dữ liệu, không huấn luyện bộ phân loại, không tính CV/test score và không phải cách chia train/test chính thức của thực nghiệm. Chưa thay thế việc người 2 kiểm tra Pipeline mô hình cuối cùng hoặc người 3 kiểm thử giao diện.

EDA đã mô tả toàn dataset, do đó nhóm phải ghi nhận giới hạn này. Không dùng quan sát về test để quyết định lựa chọn mô hình/thuộc tính. Giữ test khỏi các quyết định tiếp theo.

## Xác nhận khi nhận bàn giao

Người 2 chạy lại kiểm thử và notebook, xác nhận hiểu hợp đồng X/y, bổ sung pipeline mô hình rồi đánh giá theo kế hoạch. Người tải CSV bổ sung URL tải trực tiếp và ngày tải thực tế nếu còn biết. Không ghi ngày xác nhận hoặc tên người nhận khi việc đó chưa diễn ra.

## Kết quả kiểm tra phần người 1

Ngày kiểm tra: 05/11/2026. Phạm vi: bước 1, 3, 4, 5 theo phân công; kiểm tra thêm giao diện bàn giao dữ liệu cho người 2.

### Kết luận

Sản phẩm dữ liệu và EDA gần hoàn tất, ước lượng 90–95% theo checklist nội bộ. Không phải điểm môn học hoặc mức hoàn thành toàn dự án. Còn cần người tải xác nhận URL/ngày tải thực tế của CSV và người 2 xác nhận tích hợp vào pipeline mô hình cuối cùng.

Mức hiểu của người thực hiện chưa được chấm vì chưa có câu trả lời hoặc buổi trình bày. Tài liệu tự học được giữ riêng trên máy người 1; việc mã chạy được chưa đủ để đánh giá mức hiểu.

### Những gì đã kiểm tra thực tế

| Kiểm tra | Kết quả |
|---|---|
| Notebook chạy từ kernel mới | Đạt, toàn bộ 23 ô mã chạy theo thứ tự, đã lưu output |
| Hình và nhận xét | Có đủ mã tạo 12 hình và 12 nhận xét biểu đồ; đã xem bản tổng hợp hình |
| Bảng xuất | Có chất lượng dữ liệu, thống kê số/phân loại, dữ liệu thiếu, tương quan và rbc/appet theo lớp |
| Dữ liệu sau làm sạch | 400×25; CKD=250, Not CKD=150; nhãn thiếu=0; trùng=0 |
| Bộ kiểm thử bàn giao | 8/8 nhóm kiểm thử đạt |
| Tích hợp tiền xử lý sklearn | FunctionTransformer → ColumnTransformer → imputer/encoder/scaler chạy được |
| Dự đoán đầu vào không nhãn | Biến đổi được 80 dòng X không có id/nhãn, trong đó một dòng toàn ô thiếu |
| Tính nhất quán khi lưu–nạp | joblib nạp lại cho kết quả biến đổi khớp |
| Thư viện hiện tại | pip check không phát hiện phụ thuộc lỗi |
| CSV gốc | Giữ nguyên; SHA-256 khớp bản ghi trong data/README.md |

### Quy trình đã được điều chỉnh

1. Ghi mục tiêu, đối tượng sử dụng, X/y, lớp dương và chỉ số trước khi phân tích.
2. Xem dữ liệu thô để nhận diện lỗi; ghi nguồn và từ điển.
3. Làm sạch bằng quy tắc cố định, không điền thiếu hoặc học thống kê.
4. EDA trên bảng đã sửa định dạng, xuất bảng/hình và viết nhận xét có số liệu.
5. Tách clean_features và encode_target, kiểm tra đường đi đầu vào không nhãn và bàn giao.
6. Người 2 thực hiện chia train/test trước các bước học tham số, rồi Pipeline và CV trên train.

Đã bỏ ô htn lặp và ô nhận xét trống, thay số lượng lớp ghi cứng bằng tính từ dữ liệu, thêm mã tái tạo rbc/appet, bổ sung mô tả dữ liệu và nhận xét còn thiếu.

### Giới hạn xác minh

- Đã kiểm tra trong `.venv` hiện có với các phiên bản ghi tại requirements.txt; chưa dựng một môi trường mới hoàn toàn hoặc chạy trên máy khác.
- Bộ kiểm tra sklearn chỉ xác nhận hợp đồng dữ liệu và khả năng lưu–nạp tiền xử lý; không có bộ phân loại, CV score hoặc kết quả test của mô hình.
- Chưa xác minh lịch sử tải trực tiếp của CSV; nguồn tham chiếu gốc không thay thế lịch sử này.
- EDA đã xem toàn dataset; không dùng quan sát ấy để điều chỉnh theo test, và phải nêu giới hạn này trong báo cáo thực nghiệm.
- Kiểm tra miền giá trị số mang ý nghĩa lâm sàng, upload CSV và thông báo lỗi giao diện còn thuộc phần người 3; cleaner đã kiểm tra schema, token số, vô hạn và miền phân loại văn bản.

### Chạy kiểm tra lại

Tại thư mục gốc trong PowerShell:

```powershell
.\.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m pip check
```

Mở notebook bằng môi trường dự án, Restart Kernel and Run All. Khi thay dataset, cập nhật cả nhận xét và báo cáo theo số liệu mới.

