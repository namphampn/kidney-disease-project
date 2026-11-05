# Nguồn và hiện trạng dữ liệu

File dùng trong dự án: `data/raw/kidney_disease.csv`. Giữ nguyên file này; làm sạch trên bản sao trong bộ nhớ.

Nguồn mô tả gốc: [UCI Chronic Kidney Disease](https://archive.ics.uci.edu/dataset/336/chronic+kidney+disease).
Trích dẫn: Rubini, L., Soundarapandian, P., & Eswaran, P. (2015). Chronic Kidney Disease [Dataset]. DOI: https://doi.org/10.24432/C5G020. Giấy phép gốc CC BY 4.0.
Đối chiếu tài liệu nguồn ngày 05/11/2026.

CSV cục bộ có 400 dòng, 26 cột: 24 thuộc tính, `classification` và `id`.
URL tải trực tiếp, ngày tải và các bước chuyển đổi trước khi đưa vào thư mục hiện chưa được ghi nhận.
Chưa xác minh bản CSV này trùng toàn bộ giá trị với bản gốc UCI. Người đã tải dữ liệu cần bổ sung lịch sử đó; không suy đoán URL Kaggle.

Dấu kiểm SHA-256 của CSV đang dùng:

`835c57ec100db2d3751165fae615fec425caf444cca23bab6a853d4c08bf5556`

Nhãn thô có `ckd`, `notckd` và `ckd\t`. Các cột `pcv`, `wc`, `rc` có token `\t?`.
Quy tắc xử lý và bảng trước/sau nằm trong notebook; không ghi đè CSV gốc.
Không tự điền nhãn thiếu hay xóa giá trị cực trị chưa kiểm chứng.
