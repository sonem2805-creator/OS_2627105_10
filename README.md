MÔ PHỎNG THUẬT TOÁN BANKER VÀ PHÁT HIỆN / PHỤC HỒI DEADLOCK

Đề tài: Mô phỏng Thuật toán Banker và Phát hiện / Phục hồi Deadlock (Mã đề tài: OS_DLK_10)

Lớp học phần: 012012500105

Mã nhóm LMS: OS_2627105_10

Môn học: Hệ điều hành - Trường Đại học Giao thông vận tải TP.HCM (UTH)

Giảng viên hướng dẫn: ThS. Mai Ngọc Châu

Link GitHub: https://github.com/sonem2805-creator/OS_2627105_10

==================================================

GIỚI THIỆU VÀ MỤC TIÊU DỰ ÁN

Dự án xây dựng phần mềm mô phỏng các cơ chế quản lý tài nguyên trong Hệ điều hành:

Tránh Deadlock: Kiểm tra trạng thái an toàn (Safety Check) và xử lý yêu cầu cấp phát tài nguyên (Resource Request) theo Thuật toán Banker.

Phát hiện và Phục hồi Deadlock: Tìm danh sách các tiến trình bị tắc nghẽn và mô phỏng việc giải phóng tài nguyên để phục hồi hệ thống.

==================================================

PHÂN CÔNG VAI TRÒ VÀ NHIỆM VỤ THÀNH VIÊN

[ BẢNG PHÂN CÔNG VAI TRÒ CHÍNH ]

Nguyễn Thanh Hiển (Trưởng nhóm): Quản lý tiến độ, quản trị GitHub, viết Báo cáo Word/PDF và làm Slide thuyết trình.

Hà Vũ Khang (Core Lead 1): Lập trình Lõi Thuật toán Banker.

Đan Ngọc Sơn (Core Lead 2): Lập trình Lõi Thuật toán Phát hiện và Phục hồi Deadlock.

Lê Công Vinh (Data & Tester): Lập trình module đọc/ghi file CSV, bắt lỗi dữ liệu, tính bài toán mẫu và quay Video Demo.

Huỳnh Nguyễn Nhất Huy (GUI Developer): Thiết kế và lập trình Giao diện Desktop (PyQt6/WinForms).

[ LỘ TRÌNH THỰC HIỆN CHI TIẾT TỪ TUẦN 1 ĐẾN TUẦN 8 ]

Tuần 1 - Khởi tạo dự án và Phân công công việc (Đã hoàn thành):

Cả nhóm: Chốt đề tài OS_DLK_10, lập GitHub Repository chính thức.

Hiển: Phân chia vai trò 5 thành viên, tạo cấu trúc thư mục code chuẩn.

Khang, Sơn, Vinh, Huy: Nhận nhiệm vụ, cài đặt môi trường làm việc Python và Git.

Tuần 2 - Lập Mô hình toán học và Bản chạy thử Terminal (Đã hoàn thành):

Khang & Sơn: Viết thuật toán Banker và Phát hiện Deadlock dạng cơ bản chạy trên màn hình Terminal (Proof of Concept).

Vinh: Chuẩn hóa dữ liệu ma trận đầu vào (Allocation, Max, Available, Need).

Huy: Vẽ phác thảo giao diện phần mềm (Wireframe).

Hiển: Soạn thảo nội dung Báo cáo Tiến độ Checkpoint 01 (Chương 1 và Chương 2).

Tuần 3 và 4 - Đóng gói Lõi Thuật toán và Module Đọc/Ghi CSV (Đã hoàn thành):

Khang & Sơn: Đóng gói các hàm kiểm tra an toàn và phát hiện bế tắc vào thư mục source/banker.py theo mô hình Clean Architecture.

Vinh: Lập trình xong các hàm doc_file_csv và ghi_file_csv để nạp dữ liệu từ thư mục input/ và tự động xuất kết quả ra thư mục output/.

Hiển & Huy: Kiểm tra tính liên kết của mã nguồn main.py và đóng gói hồ sơ nộp Checkpoint 01 đúng hạn lên LMS.

Tuần 5 - Phát triển Giao diện GUI Desktop (Đang thực hiện):

Huy: Vẽ giao diện Desktop (nút chọn file CSV, các bảng ma trận, các nút bấm chạy thuật toán).

Khang & Sơn: Chỉnh code thuật toán trả về dữ liệu chuẩn để Huy đưa lên màn hình (Màu Xanh = An toàn, Màu Đỏ = Deadlock).

Vinh: Ghép phần đọc file CSV vào giao diện để khi bấm chọn file thì dữ liệu tự điền vào bảng.

Hiển: Soạn trước Chương 3 (Thiết kế và Cài đặt phần mềm) trong báo cáo Word.

Tuần 6 - Kiểm thử (Test) và Đo tốc độ (Stress Test):

Vinh: Tự giải 3 đến 5 bài toán ra giấy để làm kết quả mẫu, cho phần mềm chạy đối chiếu xem đúng hay sai.

Khang & Sơn: Tạo file CSV dữ liệu lớn (50, 100, 500 tiến trình) cho thuật toán chạy thử để đo thời gian xử lý.

Huy: Thêm thanh cuộn cho các bảng ma trận lớn trên giao diện.

Hiển: Thu thập số liệu đưa vào Chương 4 (Thực nghiệm và Đánh giá) trong báo cáo Word.

Tuần 7 - Sửa lỗi và Tối ưu phần mềm:

Vinh & Huy: Bắt các lỗi người dùng nhập sai (file rỗng, nhập chữ thay vì số, nhập số âm) và hiện thông báo nhắc nhở.

Khang & Sơn: Dọn dẹp mã nguồn, xóa code thừa và thêm ghi chú giải thích thuật toán.

Hiển: Duyệt mã nguồn lần cuối trên GitHub, chốt bản chính thức v1.0 và viết Chương 5 (Kết luận).

Tuần 8 - Hoàn thiện Báo cáo, Video Demo và Bảo vệ Đồ án:

Hiển: Căn chỉnh file Báo cáo Word (8 đến 12 trang), xuất PDF và làm Slide thuyết trình.

Vinh: Quay video màn hình thao tác ứng dụng từ A đến Z, đăng lên YouTube hoặc Google Drive lấy link.

Cả nhóm: Ôn tập lại thuật toán để cùng Trưởng nhóm trả lời câu hỏi bảo vệ đồ án.
