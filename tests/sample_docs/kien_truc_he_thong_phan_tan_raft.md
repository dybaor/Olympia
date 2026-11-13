# KIẾN TRÚC HỆ THỐNG PHÂN TÁN VÀ ĐỒNG THUẬN RAFT

## 1. TỔNG QUAN VÀ KHÁI NIỆM CỐT LÕI

Thuật toán Raft được định nghĩa là một giao thức đồng thuận phân tán (distributed consensus algorithm) được thiết kế nhằm mục đích quản lý bản sao nhật ký (replicated log) trên một cụm máy chủ, đảm bảo tính dễ hiểu hơn so với giao thức Paxos truyền thống.

Khái niệm **State Machine Replication** chính là kiến trúc nền tảng cho phép một tập hợp các máy chủ hoạt động độc lập nhưng đồng thuận trên cùng một chuỗi trạng thái xử lý dữ liệu.

Khái niệm **Nhiệm kỳ (Term)** đề cập đến các khoảng thời gian logic có số thứ tự tăng dần liên tục, đóng vai trò như một đồng hồ logic giúp các nút trong cụm nhận biết thông tin bị lỗi thời.

Khái niệm **Quorum (Đa số quá bán)** được định nghĩa là số lượng nút tối thiểu cần thiết để thông qua một quyết định trong cụm, tính bằng công thức quá bán `(N/2) + 1` trên tổng số `N` nút.

Khái niệm **Heartbeat (Nhịp tim)** chính là các thông điệp AppendEntries rỗng được gửi định kỳ từ nút Leader tới toàn bộ Follower để duy trì quyền lực và ngăn chặn các cuộc bầu cử mới không cần thiết.

## 2. NGUYÊN LÝ VÀ ĐỊNH LÝ HỆ THỐNG

Nguyên lý **Bầu cử Lãnh đạo (Leader Election)** khẳng định rằng tại một thời điểm trong một nhiệm kỳ nhất định, chỉ có tối đa một ứng viên có thể được bầu làm Leader nếu và chỉ nếu nó nhận được số phiếu bầu từ đa số quá bán các nút trong cụm.

Định lý **Log Matching Property** khẳng định rằng nếu hai nhật ký trên hai máy chủ khác nhau chứa một mục (entry) có cùng chỉ số index và cùng nhiệm kỳ term, thì hai nhật ký đó đồng nhất tại tất cả các mục từ đầu cho đến chỉ số đó.

Định luật **Leader Completeness** khẳng định rằng nếu một mục nhật ký đã được commit (chấp thuận) tại một nhiệm kỳ nhất định, thì mục đó nhất định sẽ hiện diện trong nhật ký của các Leader ở tất cả các nhiệm kỳ cao hơn tiếp theo.

## 3. MỐI QUAN HỆ NHÂN - QUẢ VÀ CƠ CHẾ VẬN HÀNH

Khi **nút Follower không nhận được Heartbeat từ Leader trong khoảng thời gian Election Timeout**, thì dẫn đến hiện tượng **nút Follower tự động chuyển trạng thái thành Candidate** theo cơ chế tăng nhiệm kỳ và phát động vòng bầu cử mới.

Khi **Leader nhận được xác nhận sao chép từ đa số quá bán (Quorum)**, thì dẫn tới kết quả **mục nhật ký được đánh dấu là committed** và được áp dụng vào máy trạng thái cục bộ của mọi nút.

Do **độ trễ mạng truyền thông vượt quá ngưỡng timeout quy định**, kéo theo **tình trạng chia cắt mạng cục bộ** làm cho các nút hiểu lầm rằng Leader hiện tại đã ngừng hoạt động.

## 4. CÁC TRƯỜNG HỢP NGOẠI LỆ VÀ ĐIỀU KIỆN BIÊN (EDGE CASES)

Tuy nhiên, trong trường hợp **Phân mảnh mạng (Network Partition / Split-brain)**, cụm máy chủ bị chia thành hai phân vùng tách biệt: phân vùng thiểu số sẽ không thể commit bất kỳ ghi chú nào vì không thể đạt được Quorum `(N/2) + 1`.

Tuy nhiên, thuật toán Raft **không còn đúng trong trường hợp Byzantine Fault** khi các nút trong hệ thống gửi thông điệp sai lệch có chủ đích hoặc có hành vi phá hoại; Raft chỉ chống chịu được lỗi sập nguồn (Crash-Recovery) mà không xử lý lỗi độc hại.

Ngoại trừ trường hợp **đồng hồ vật lý bị trôi dạt (Clock Drift)**, các nút trong Raft hoạt động dựa trên các bộ đếm thời gian ngẫu nhiên (Randomized Election Timers) từ 150ms đến 300ms nhằm giảm thiểu nguy cơ xung đột phiếu bầu giữa các ứng viên.

