ORACLE TEST REPORT
Thành viên thực hiện
Lê Công Vinh

ORACLE 1 - SAFE STATE
Kết quả mong đợi
SAFE

Safe Sequence:

P1 → P3 → P4 → P0 → P2

Kết quả chương trình
SAFE

Safe Sequence:

P1 → P3 → P4 → P0 → P2

Kết luận
Kết quả tính tay trùng khớp với kết quả chương trình.

Oracle 1 đạt yêu cầu.

ORACLE 2 - UNSAFE STATE
Kết quả mong đợi
UNSAFE

Không tồn tại Safe Sequence.

Kết quả chương trình
UNSAFE

Không tồn tại Safe Sequence.

Kết luận
Không có tiến trình nào thỏa mãn điều kiện:

Need ≤ Available

Thuật toán kết luận hệ thống ở trạng thái UNSAFE.

Oracle 2 đạt yêu cầu.

ORACLE 3 - RESOURCE REQUEST DENIED
Request
Process:

P1

Request:

(5,5,5)

Available:

(3,3,2)

Kết quả mong đợi
REQUEST DENIED

Kết quả chương trình
REQUEST DENIED

Kết luận
Request lớn hơn Available nên hệ thống từ chối cấp phát tài nguyên.

Oracle 3 đạt yêu cầu.

ORACLE 4 - DEADLOCK DETECTION AND RECOVERY
Kết quả mong đợi
Deadlock Detected

Deadlocked Processes:

P1, P2, P3

Recovery Success

Kết quả chương trình
Deadlock Detected

Recovery Success

Kết luận
Thuật toán phát hiện chính xác trạng thái deadlock và thực hiện phục hồi thành công.

Oracle 4 đạt yêu cầu.

TỔNG KẾT
Oracle	Nội dung	Kết quả
Oracle 1	SAFE	PASS
Oracle 2	UNSAFE	PASS
Oracle 3	Resource Request Denied	PASS
Oracle 4	Deadlock Recovery	PASS
Kết luận chung
Các bộ Oracle đã được xây dựng để kiểm tra:

SAFE State
UNSAFE State
Resource Request Denied
Deadlock Detection and Recovery
Kết quả thực thi chương trình trùng khớp với kết quả tính tay và kết quả mong đợi.

Xác nhận chương trình hoạt động đúng trong các trường hợp kiểm thử chính.
