ORACLE 2 - UNSAFE STATE (BANKER'S ALGORITHM)
Mục tiêu
Kiểm tra tính đúng đắn của thuật toán Banker trong trường hợp hệ thống ở trạng thái không an toàn (UNSAFE).

Dữ liệu đầu vào
File: oracle_2_unsafe.csv

Available:

(0, 0, 0)

Allocation Matrix:

P0 = (0,1,0) P1 = (2,0,0) P2 = (3,0,2) P3 = (2,1,1) P4 = (0,0,2)

Max Matrix:

P0 = (7,5,3) P1 = (8,2,2) P2 = (9,0,2) P3 = (4,2,2) P4 = (4,3,3)

Tính Need Matrix
Need = Max − Allocation

P0 = (7,4,3)

P1 = (6,2,2)

P2 = (6,0,0)

P3 = (2,1,1)

P4 = (4,3,1)

Tính tay thuật toán Banker
Trạng thái ban đầu:

Available = (0,0,0)

Kiểm tra các tiến trình:

P0 = (7,4,3) > (0,0,0) → Không chạy được

P1 = (6,2,2) > (0,0,0) → Không chạy được

P2 = (6,0,0) > (0,0,0) → Không chạy được

P3 = (2,1,1) > (0,0,0) → Không chạy được

P4 = (4,3,1) > (0,0,0) → Không chạy được

Không tồn tại tiến trình nào thỏa mãn:

Need ≤ Available

Do đó không có tiến trình nào được thực thi.

Không có tiến trình hoàn thành nên không có tài nguyên nào được giải phóng.

Giá trị Available không thay đổi:

Available = (0,0,0)

Thuật toán Banker dừng lại.

Safe Sequence
Không tồn tại Safe Sequence.

Kết quả chương trình
Status: UNSAFE

Safe Sequence:

Không tồn tại

Kết luận
Hệ thống ở trạng thái UNSAFE.

Không tồn tại chuỗi an toàn vì không có tiến trình nào có thể được cấp phát tài nguyên tại thời điểm ban đầu.

Kết quả tính tay phải trùng khớp hoàn toàn với kết quả chương trình, chứng minh việc cài đặt thuật toán Banker là chính xác đối với bộ dữ liệu Oracle 2.