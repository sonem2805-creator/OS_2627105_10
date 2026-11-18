ORACLE 3 - RESOURCE REQUEST DENIED
Mục tiêu
Kiểm tra tính đúng đắn của thuật toán Banker khi một tiến trình yêu cầu lượng tài nguyên vượt quá khả năng cấp phát của hệ thống.

Dữ liệu đầu vào
Available:

(3,3,2)

Request của tiến trình P1:

(5,5,5)

Kiểm tra điều kiện
Thuật toán Banker chỉ cho phép cấp phát khi:

Request ≤ Available

So sánh:

Request = (5,5,5)

Available = (3,3,2)

Ta có:

5 > 3

5 > 3

5 > 2

Do đó:

Request > Available

Điều kiện không thỏa mãn.

Tính tay
Hệ thống không đủ tài nguyên để đáp ứng yêu cầu của P1.

Không thực hiện cấp phát thử.

Không chạy bước kiểm tra Safe State.

Yêu cầu bị từ chối ngay tại bước kiểm tra Available.

Kết quả chương trình
Status: REQUEST DENIED

Hoặc:

Request exceeds available resources

Kết luận
Yêu cầu tài nguyên của P1 vượt quá lượng tài nguyên hiện có trong hệ thống.

Thuật toán Banker phải từ chối yêu cầu.

Kết quả tính tay phải trùng khớp với kết quả chương trình.