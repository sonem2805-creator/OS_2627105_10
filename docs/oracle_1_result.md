ORACLE 1 - SAFE STATE (BANKER'S ALGORITHM)
Mục tiêu
Kiểm tra tính đúng đắn của thuật toán Banker trong trường hợp hệ thống ở trạng thái an toàn (SAFE).

Dữ liệu đầu vào
File: oracle_1_safe.csv

Available:

(3, 3, 2)

Allocation Matrix:

P0 = (0,1,0) P1 = (2,0,0) P2 = (3,0,2) P3 = (2,1,1) P4 = (0,0,2)

Max Matrix:

P0 = (7,5,3) P1 = (3,2,2) P2 = (9,0,2) P3 = (2,2,2) P4 = (4,3,3)

Tính Need Matrix
Need = Max − Allocation

P0 = (7,4,3) P1 = (1,2,2) P2 = (6,0,0) P3 = (0,1,1) P4 = (4,3,1)

Tính tay thuật toán Banker
Trạng thái ban đầu:

Available = (3,3,2)

Kiểm tra các tiến trình:

P0 = (7,4,3) > (3,3,2) → Không chạy được

P1 = (1,2,2) ≤ (3,3,2) → Chạy được

P2 = (6,0,0) > (3,3,2) → Không chạy được

P3 = (0,1,1) ≤ (3,3,2) → Chạy được

P4 = (4,3,1) > (3,3,2) → Không chạy được

Chọn P1 thực thi.

Sau khi P1 hoàn thành:

Available = (3,3,2) + (2,0,0) = (5,3,2)

Tiếp tục kiểm tra:

P3 = (0,1,1) ≤ (5,3,2)

Chọn P3 thực thi.

Sau khi P3 hoàn thành:

Available = (5,3,2) + (2,1,1) = (7,4,3)

Tiếp tục kiểm tra:

P4 = (4,3,1) ≤ (7,4,3)

Chọn P4 thực thi.

Sau khi P4 hoàn thành:

Available = (7,4,3) + (0,0,2) = (7,4,5)

Tiếp tục kiểm tra:

P0 = (7,4,3) ≤ (7,4,5)

Chọn P0 thực thi.

Sau khi P0 hoàn thành:

Available = (7,4,5) + (0,1,0) = (7,5,5)

Tiếp tục kiểm tra:

P2 = (6,0,0) ≤ (7,5,5)

Chọn P2 thực thi.

Sau khi P2 hoàn thành:

Available = (7,5,5) + (3,0,2) = (10,5,7)

Safe Sequence
P1 → P3 → P4 → P0 → P2

Kết quả chương trình
Status: SAFE

Safe Sequence:

P1 → P3 → P4 → P0 → P2

Kết luận
Hệ thống ở trạng thái SAFE.

Tồn tại chuỗi an toàn:

P1 → P3 → P4 → P0 → P2

Kết quả tính tay trùng khớp hoàn toàn với kết quả chương trình, chứng minh việc cài đặt thuật toán Banker là chính xác đối với bộ dữ liệu Oracle 1.