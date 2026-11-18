ORACLE 4 - DEADLOCK DETECTION AND RECOVERY
Mục tiêu
Kiểm tra tính đúng đắn của thuật toán phát hiện deadlock và cơ chế phục hồi deadlock của hệ thống.

Dữ liệu đầu vào
File: deadlock_detection.csv

Available:

(0,0,0)

Allocation Matrix:

P0 = (0,1,0)

P1 = (2,0,0)

P2 = (3,0,3)

P3 = (2,1,1)

Request Matrix:

P0 = (0,0,0)

P1 = (2,0,2)

P2 = (0,0,1)

P3 = (1,0,0)

Thực hiện thuật toán phát hiện Deadlock
Trạng thái ban đầu:

Available = (0,0,0)

Bước 1
Kiểm tra P0:

Request P0 = (0,0,0)

(0,0,0) ≤ (0,0,0)

P0 có thể hoàn thành.

Giải phóng Allocation của P0:

(0,1,0)

Available mới:

(0,1,0)

Bước 2
Kiểm tra P1:

Request P1 = (2,0,2)

(2,0,2) > (0,1,0)

Không thể hoàn thành.

Kiểm tra P2:

Request P2 = (0,0,1)

(0,0,1) > (0,1,0)

Không thể hoàn thành.

Kiểm tra P3:

Request P3 = (1,0,0)

(1,0,0) > (0,1,0)

Không thể hoàn thành.

Sau khi kiểm tra toàn bộ:

Các tiến trình:

P1, P2, P3

đều không thể hoàn thành.

Kết quả phát hiện Deadlock
Các tiến trình bị kẹt:

P1
P2
P3
Hệ thống xảy ra deadlock.

Phục hồi Deadlock
Chọn tiến trình nạn nhân:

P2
Thu hồi Allocation của P2:

(3,0,3)
Available mới:

(0,1,0)
+
(3,0,3)
=
(3,1,3)
Kiểm tra lại:

P1:

Request P1 = (2,0,2)
<=
Available (3,1,3)
P1 hoàn thành.

Available:

(3,1,3)
+
(2,0,0)
=
(5,1,3)
P3:

Request P3 = (1,0,0)
<=
Available (5,1,3)
P3 hoàn thành.

Available:

(5,1,3)
+
(2,1,1)
=
(7,2,4)
Tất cả các tiến trình còn lại đều có thể hoàn thành.

Hệ thống thoát khỏi trạng thái deadlock.

Kết quả chương trình
Deadlock Detected: YES

Deadlocked Processes:

P1

P2

P3

Victim Process:

P2

Recovery Status:

SUCCESS

Kết luận
Hệ thống ban đầu xảy ra deadlock.

Các tiến trình:

P1, P2, P3

bị kẹt tài nguyên.

Sau khi chọn P2 làm tiến trình nạn nhân và thu hồi tài nguyên của P2, hệ thống có đủ tài nguyên để tiếp tục thực thi các tiến trình còn lại.

Deadlock được phục hồi thành công.

Kết quả tính tay phải trùng khớp với kết quả chương trình.
