# Từ điển dữ liệu

Định nghĩa và đơn vị tham chiếu: [UCI CKD](https://archive.ics.uci.edu/dataset/336/chronic+kidney+disease).
Giữ cách ghi đơn vị của nguồn; không tự sửa đơn vị hoặc quy đổi giá trị.
CSV cục bộ dùng `wc`, `rc`, `classification`; tài liệu nguồn có thể dùng tên tương đương `wbcc`, `rbcc`, `class`.

| Cột | Ý nghĩa | Đơn vị nguồn | Biểu diễn |
|---|---|---|---|
| age | Tuổi | năm | số |
| bp | Huyết áp | mm/Hg | số |
| sg | Tỷ trọng nước tiểu | — | mã phân loại |
| al | Albumin | — | mã mức 0–5 |
| su | Đường | — | mã mức 0–5 |
| rbc | Tình trạng hồng cầu | — | normal/abnormal |
| pc | Tế bào mủ | — | normal/abnormal |
| pcc | Cụm tế bào mủ | — | present/notpresent |
| ba | Vi khuẩn | — | present/notpresent |
| bgr | Đường huyết ngẫu nhiên | mgs/dl | số |
| bu | Urê máu | mgs/dl | số |
| sc | Creatinine huyết thanh | mgs/dl | số |
| sod | Natri | mEq/L | số |
| pot | Kali | mEq/L | số |
| hemo | Hemoglobin | gms theo UCI | số |
| pcv | Thể tích hồng cầu | UCI không ghi rõ | số |
| wc | Số lượng bạch cầu | cells/cumm | số |
| rc | Số lượng hồng cầu | millions/cmm | số |
| htn | Tăng huyết áp | — | yes/no |
| dm | Tiểu đường | — | yes/no |
| cad | Bệnh động mạch vành | — | yes/no |
| appet | Khẩu vị | — | good/poor |
| pe | Phù chân | — | yes/no |
| ane | Thiếu máu | — | yes/no |

`id` là định danh trong CSV cục bộ, bị loại khỏi X. `classification` là nhãn: CKD=1, Not CKD=0; phải tách riêng khỏi X.
`sg`, `al`, `su` có dtype số sau khi đọc nhưng không mặc định là đại lượng liên tục. Cách mã hóa cuối cùng do người 2 đánh giá trên train.
`rbc` khác `rc`; `bp` khác `htn`. Thiếu là chưa biết giá trị, không có nghĩa là không mắc bệnh.
Các miền mã là quy ước dữ liệu, không phải ngưỡng chẩn đoán. Kiểm tra khoảng số hợp lý cho giao diện do người 3 bổ sung sau khi thống nhất với nguồn.
