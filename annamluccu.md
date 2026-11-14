# BỘ 300 CÂU HỎI TRẮC NGHIỆM ÔN TẬP MẠNG MÁY TÍNH TOÀN DIỆN

*(Chương 1: Tổng quan & Hiệu năng | Chương 2: Tầng Ứng dụng | Chuyên đề: Địa chỉ IP IPv4, Subnetting, CIDR & IPv6)*

---

## PHẦN 1: CHƯƠNG 1 – TỔNG QUAN, MÔ HÌNH PHÂN TẦNG & HIỆU NĂNG MẠNG (100 CÂU)

#### **Câu 1:** Đơn vị dữ liệu (PDU) tại Tầng Ứng dụng (Application Layer) được gọi là:  
**A. Message**  
B. Segment  
C. Datagram  
D. Frame  
* **Giải thích:** Tầng Ứng dụng trao đổi các thông điệp (Message) giữa các tiến trình phân tán.

#### **Câu 2:** Đơn vị dữ liệu (PDU) tại Tầng Giao vận (Transport Layer) trong mô hình Internet được gọi là:  
A. Message  
**B. Segment**  
C. Datagram  
D. Frame  
* **Giải thích:** Tầng Giao vận đóng gói dữ liệu ứng dụng kèm header giao vận tạo thành Segment.

#### **Câu 3:** Đơn vị dữ liệu (PDU) tại Tầng Mạng (Network Layer) được gọi là:  
A. Message  
B. Segment  
**C. Datagram**  
D. Frame  
* **Giải thích:** Tầng Mạng đóng gói Segment kèm tiêu đề mạng IP tạo thành Datagram (hoặc packet).

#### **Câu 4:** Đơn vị dữ liệu (PDU) tại Tầng Liên kết dữ liệu (Link Layer) được gọi là:  
A. Message  
B. Segment  
C. Datagram  
**D. Frame**  
* **Giải thích:** Tầng Liên kết dữ liệu bọc tiêu đề và đuôi kiểm tra lỗi tạo thành Frame trước khi phát tín hiệu vật lý.

#### **Câu 5:** Đơn vị dữ liệu truyền qua môi trường ở Tầng Vật lý (Physical Layer) là:  
A. Frame  
**B. Bit**  
C. Byte  
D. Packet  
* **Giải thích:** Tầng Vật lý chịu trách nhiệm truyền tải các chuỗi bit nhị phân thô qua đường truyền.

#### **Câu 6:** Thứ tự 5 tầng trong kiến trúc phân tầng Internet từ đỉnh xuống đáy là:  
A. Application, Network, Transport, Link, Physical  
**B. Application, Transport, Network, Link, Physical**  
C. Physical, Link, Network, Transport, Application  
D. Application, Presentation, Session, Transport, Network  
* **Giải thích:** Kiến trúc Internet gồm 5 tầng: Ứng dụng, Giao vận, Mạng, Liên kết dữ liệu và Vật lý.

#### **Câu 7:** Hai tầng nào có trong mô hình 7 tầng OSI nhưng được tích hợp vào Tầng Ứng dụng trong Internet?  
**A. Presentation và Session**  
B. Network và Transport  
C. Link và Physical  
D. Transport và Session  
* **Giải thích:** Hai tầng Trình diễn (Presentation) và Phiên (Session) không tách rời mà do chính ứng dụng đảm nhiệm nếu cần.

#### **Câu 8:** Quá trình gắn thêm tiêu đề (Header) khi dữ liệu đi từ tầng trên xuống tầng dưới gọi là:  
A. Giải gói (Decapsulation)  
**B. Đóng gói (Encapsulation)**  
C. Phân mảnh (Fragmentation)  
D. Dồn kênh (Multiplexing)  
* **Giải thích:** Encapsulation là quá trình tầng dưới nhận PDU của tầng trên làm payload và gắn thêm header điều khiển của mình.

#### **Câu 9:** Quá trình bóc tách tiêu đề khi gói tin đi từ tầng dưới lên tầng trên tại máy nhận gọi là:  
A. Encapsulation  
**B. Decapsulation**  
C. Segmentation  
D. Aggregation  
* **Giải thích:** Decapsulation là quá trình máy nhận bóc tiêu đề của tầng hiện tại và chuyển phần dữ liệu tải lên tầng kế trên.

#### **Câu 10:** Thiết bị mạng nào sau đây triển khai đủ cả 5 tầng giao thức Internet?  
A. Router vùng lõi  
B. Switch mạng LAN  
**C. Hệ thống đầu cuối (Hosts/End systems)**  
D. Repeater  
* **Giải thích:** Chỉ các thiết bị đầu cuối (Hosts) mới chạy các ứng dụng mạng và triển khai đầy đủ cả 5 tầng giao thức.

#### **Câu 11:** Thiết bị Router vùng lõi Internet thông thường xử lý gói tin đến tầng nào?  
A. Tầng 1 (Vật lý)  
B. Tầng 2 (Liên kết)  
**C. Tầng 3 (Mạng)**  
D. Tầng 4 (Giao vận)  
* **Giải thích:** Router là thiết bị chuyển mạch gói tầng mạng, kiểm tra địa chỉ IP đích để định tuyến nên xử lý tới Tầng 3.

#### **Câu 12:** Thiết bị Switch mạng LAN thông thường đọc và xử lý thông tin ở tầng nào?  
A. Tầng 1 (Vật lý)  
**B. Tầng 2 (Liên kết dữ liệu)**  
C. Tầng 3 (Mạng)  
D. Tầng 4 (Giao vận)  
* **Giải thích:** Switch mạng LAN đọc địa chỉ MAC trong tiêu đề Frame để chuyển mạch nên hoạt động ở Tầng 2.

#### **Câu 13:** Thiết bị Repeater và Hub hoạt động thuần túy ở tầng nào trong mô hình mạng?  
**A. Tầng 1 (Vật lý)**  
B. Tầng 2 (Liên kết dữ liệu)  
C. Tầng 3 (Mạng)  
D. Tầng 4 (Giao vận)  
* **Giải thích:** Repeater và Hub chỉ khuếch đại tín hiệu điện/quang và phát lại mà không đọc thông tin địa chỉ MAC hay IP.

#### **Câu 14:** Đặc trưng cốt lõi của Chuyển mạch kênh (Circuit Switching) là:  
A. Tài nguyên được cấp phát động theo gói  
**B. Tài nguyên được dành riêng cố định cho phiên kết nối**  
C. Dữ liệu được chia nhỏ thành các frame  
D. Router sử dụng cơ chế lưu-và-chuyển-tiếp  
* **Giải thích:** Chuyển mạch kênh dành riêng một đường truyền hoặc khe thời gian/dải tần cố định suốt thời gian phiên liên lạc.

#### **Câu 15:** Đặc trưng cốt lõi của Chuyển mạch gói (Packet Switching) là:  
A. Dành riêng tài nguyên băng thông  
B. Không xuất hiện hàng đợi  
**C. Chia nhỏ dữ liệu thành các gói và dùng cơ chế store-and-forward**  
D. Chỉ hỗ trợ truyền tín hiệu tương tự  
* **Giải thích:** Dữ liệu được băm nhỏ thành gói tin, router nhận đủ gói rồi mới chuyển tiếp (store-and-forward) và chia sẻ thống kê tài nguyên.

#### **Câu 16:** Kỹ thuật dồn kênh nào chia đường truyền vật lý thành các dải tần số cố định riêng biệt?  
A. TDM (Time-Division Multiplexing)  
**B. FDM (Frequency-Division Multiplexing)**  
C. WDM quang học  
D. Statistical Multiplexing  
* **Giải thích:** FDM chia sẻ phổ tần số của liên kết thành các kênh tần số hẹp dành riêng cho từng kết nối.

#### **Câu 17:** Kỹ thuật dồn kênh nào chia thời gian truyền trên kênh thành các khe thời gian (time slots) luân phiên?  
A. FDM  
**B. TDM**  
C. CDM  
D. CSMA/CD  
* **Giải thích:** TDM phân chia trục thời gian thành các khung tuần hoàn, mỗi kết nối được gán các khe thời gian cố định.

#### **Câu 18:** Hiện tượng mất gói tin (Packet Loss) tại router trong mạng chuyển mạch gói chủ yếu do:  
A. Hỏng cáp quang ngầm  
**B. Tràn bộ nhớ đệm hàng đợi (Buffer Overflow)**  
C. Tốc độ ánh sáng thay đổi  
D. Tiêu đề gói tin bị xóa  
* **Giải thích:** Khi tốc độ gói tin đến vượt quá tốc độ xử lý/đẩy đi của cổng ra, hàng đợi đầy dẫn đến tràn bộ đệm và mất gói.

#### **Câu 19:** Nguyên lý Store-and-forward tại router chuyển mạch gói có nghĩa là:  
A. Router chuyển tiếp ngay khi nhận được bit đầu tiên  
**B. Router phải nhận trọn vẹn toàn bộ gói tin trước khi bắt đầu phát lên liên kết ra**  
C. Router lưu gói tin vĩnh viễn trên ổ cứng  
D. Router chỉ gửi gói tin khi mạng không có ai dùng  
* **Giải thích:** Store-and-forward đòi hỏi router phải lưu đủ L bit của gói tin vào bộ nhớ đệm rồi mới bắt đầu truyền bit đầu tiên ra đường truyền.

#### **Câu 20:** Ưu điểm lớn nhất của Chuyển mạch gói so với Chuyển mạch kênh là:  
A. Đảm bảo băng thông cố định 100%  
**B. Hiệu quả sử dụng tài nguyên cao hơn nhờ dồn kênh thống kê cho lưu lượng đột biến**  
C. Độ trễ luôn bằng 0  
D. Không bao giờ bị mất gói tin  
* **Giải thích:** Chuyển mạch gói chia sẻ tài nguyên linh hoạt theo nhu cầu thực tế của người dùng, không lãng phí băng thông khi người dùng nghỉ.

#### **Câu 21:** Tổng thời gian trễ tại một nút mạng (Total Nodal Delay) gồm 4 thành phần là:  
**A. Trễ xử lý, trễ hàng đợi, trễ truyền gói, trễ lan truyền**  
B. Trễ DNS, trễ TCP, trễ HTTP, trễ hàng đợi  
C. Trễ cáp, trễ switch, trễ router, trễ host  
D. Trễ mã hóa, trễ giải mã, trễ nén, trễ truyền  
* **Giải thích:** Tổng trễ d_nodal = d_proc + d_queue + d_trans + d_prop.

#### **Câu 22:** Công thức tính độ trễ truyền gói (Transmission Delay - d_trans) cho gói L bits qua liên kết băng thông R bps là:  
A. d_trans = R / L  
**B. d_trans = L / R**  
C. d_trans = d / s  
D. d_trans = s / d  
* **Giải thích:** Độ trễ truyền gói là thời gian để đẩy toàn bộ L bit của gói tin vào liên kết: d_trans = L / R.

#### **Câu 23:** Công thức tính độ trễ lan truyền (Propagation Delay - d_prop) trên quãng đường d với vận tốc truyền sóng s là:  
**A. d_prop = d / s**  
B. d_prop = s / d  
C. d_prop = L / R  
D. d_prop = d * s  
* **Giải thích:** Độ trễ lan truyền là thời gian 1 bit di chuyển từ đầu phát đến đầu thu trên môi trường vật lý: d_prop = d / s.

#### **Câu 24:** Vận tốc truyền sóng (s) trong cáp đồng xoắn đôi hoặc cáp sợi quang xấp xỉ khoảng:  
A. 3 * 10^8 m/s  
**B. 2 * 10^8 m/s**  
C. 1 * 10^6 m/s  
D. 340 m/s  
* **Giải thích:** Tốc độ truyền sóng điện từ trong môi trường vật lý hữu tuyến khoảng 2 * 10^8 m/s (chậm hơn vận tốc ánh sáng trong chân không một chút).

#### **Câu 25:** Thành phần độ trễ nào có giá trị biến động mạnh nhất tùy thuộc vào lưu lượng mạng tức thời?  
A. Trễ xử lý (d_proc)  
B. Trễ lan truyền (d_prop)  
**C. Trễ hàng đợi (d_queue)**  
D. Trễ truyền gói (d_trans)  
* **Giải thích:** Trễ hàng đợi phụ thuộc trực tiếp vào số lượng gói tin đang xếp hàng chờ trước nó, biến động từ 0 đến rất lớn khi nghẽn.

#### **Câu 26:** Cường độ lưu lượng (Traffic Intensity) được tính bằng công thức:  
**A. I = (L * a) / R**  
B. I = (R * a) / L  
C. I = (L * R) / a  
D. I = a / (L * R)  
* **Giải thích:** Với L là độ dài gói (bit), a là tốc độ gói đến (gói/s) và R là băng thông (bps). L*a là tốc độ bit đến hàng đợi.

#### **Câu 27:** Khi cường độ lưu lượng I xấp xỉ 0 (I << 1), độ trễ hàng đợi trung bình sẽ:  
A. Tiến tới vô cùng  
**B. Rất nhỏ và tiến gần về 0**  
C. Bằng độ trễ lan truyền  
D. Gây tràn bộ đệm  
* **Giải thích:** Khi lưu lượng đến rất thưa thớt so với năng lực phục vụ của đường truyền, gói tin đến hầu như được phát ngay mà không phải chờ.

#### **Câu 28:** Khi cường độ lưu lượng I tiến gần đến 1 (I -> 1), độ trễ hàng đợi trung bình sẽ:  
A. Giảm dần về 0  
**B. Tăng vọt phi tuyến lên rất lớn**  
C. Không đổi  
D. Tự động chia đôi  
* **Giải thích:** Khi I -> 1, hàng đợi phình to rất nhanh, thời gian chờ đợi trung bình của các gói tin tăng vọt theo hàm phi tuyến.

#### **Câu 29:** Khi cường độ lưu lượng I > 1 trong một khoảng thời gian dài, hiện tượng gì chắc chắn xảy ra?  
A. Tốc độ mạng tăng gấp đôi  
B. Gói tin truyền nhanh hơn  
**C. Hàng đợi tăng vô hạn và bắt đầu xảy ra tràn bộ đệm gây mất gói**  
D. Băng thông R tự động nâng cấp  
* **Giải thích:** Lượng dữ liệu đổ về lớn hơn tốc độ giải tỏa của liên kết ra, bộ đệm sớm muộn sẽ đầy 100% và buộc router phải drop gói tin.

#### **Câu 30:** Thông lượng (Throughput) của một kết nối đầu cuối qua nhiều liên kết nối tiếp bị quyết định bởi:  
A. Liên kết có băng thông lớn nhất  
**B. Liên kết có băng thông thấp nhất (Bottleneck link)**  
C. Tổng băng thông của tất cả các liên kết  
D. Độ trễ của router trung gian  
* **Giải thích:** Bottleneck link là liên kết thắt cổ chai, giới hạn tốc độ truyền dữ liệu tối đa của toàn tuyến.

#### **Câu 31:** Gói tin kích thước L = 1.000 bytes truyền qua liên kết có băng thông R = 10 Mbps. Trễ truyền gói d_trans là:  
A. 0,1 ms  
**B. 0,8 ms**  
C. 8 ms  
D. 1 ms  
* **Giải thích:** L = 1.000 * 8 = 8.000 bits. R = 10 * 10^6 bps. d_trans = 8.000 / 10.000.000 = 0,0008 s = 0,8 ms.

#### **Câu 32:** Gói tin kích thước L = 1.500 bytes truyền qua đường truyền R = 100 Mbps. Trễ truyền gói d_trans là:  
**A. 0,12 ms**  
B. 1,2 ms  
C. 0,015 ms  
D. 15 ms  
* **Giải thích:** L = 1.500 * 8 = 12.000 bits. R = 100 * 10^6 bps. d_trans = 12.000 / 100.000.000 = 0,00012 s = 0,12 ms.

#### **Câu 33:** Khoảng cách giữa hai trạm d = 1.000 km, vận tốc truyền sóng s = 2 * 10^8 m/s. Trễ lan truyền d_prop là:  
A. 2 ms  
**B. 5 ms**  
C. 10 ms  
D. 0,5 ms  
* **Giải thích:** d = 1.000.000 m. d_prop = 1.000.000 / (2 * 10^8) = 0,005 s = 5 ms.

#### **Câu 34:** Khoảng cách giữa hai router d = 2.500 km, vận tốc truyền sóng s = 2,5 * 10^8 m/s. Trễ lan truyền d_prop là:  
A. 1 ms  
**B. 10 ms**  
C. 25 ms  
D. 5 ms  
* **Giải thích:** d = 2.500.000 m. d_prop = 2.500.000 / (2,5 * 10^8) = 0,01 s = 10 ms.

#### **Câu 35:** Một tệp tin truyền từ Server đến Client qua 2 liên kết: R1 = 50 Mbps, R2 = 10 Mbps. Thông lượng cực đại là:  
A. 50 Mbps  
B. 60 Mbps  
**C. 10 Mbps**  
D. 25 Mbps  
* **Giải thích:** Throughput = min(R1, R2) = min(50, 10) = 10 Mbps do liên kết R2 là nút thắt cổ chai.

#### **Câu 36:** Server truyền tệp qua 3 liên kết nối tiếp có băng thông lần lượt là 100 Mbps, 20 Mbps, 50 Mbps. Thông lượng là:  
A. 100 Mbps  
**B. 20 Mbps**  
C. 50 Mbps  
D. 170 Mbps  
* **Giải thích:** Throughput = min(100, 20, 50) = 20 Mbps.

#### **Câu 37:** Một đường truyền chuyển mạch kênh có băng thông 4 Gbps, mỗi kết nối cần 200 Mbps. Số người dùng tối đa đồng thời là:  
**A. 20 người dùng**  
B. 40 người dùng  
C. 10 người dùng  
D. 50 người dùng  
* **Giải thích:** Số kết nối tối đa = 4.000 Mbps / 200 Mbps = 20 người dùng.

#### **Câu 38:** Một gói tin L = 2.000 bytes được gửi qua liên kết R = 1 Gbps. Thời gian đẩy gói tin vào đường truyền là:  
**A. 0,016 ms**  
B. 0,16 ms  
C. 1,6 ms  
D. 0,002 ms  
* **Giải thích:** L = 16.000 bits. R = 10^9 bps. d_trans = 16.000 / 10^9 = 0,000016 s = 0,016 ms.

#### **Câu 39:** Nếu độ dài gói tin tăng gấp đôi trong khi băng thông không đổi thì:  
**A. Độ trễ truyền gói tăng gấp đôi**  
B. Độ trễ lan truyền tăng gấp đôi  
C. Độ trễ xử lý giảm một nửa  
D. Băng thông đường truyền giảm một nửa  
* **Giải thích:** Do d_trans = L / R, khi L tăng gấp 2 lần thì d_trans tăng tỷ lệ thuận gấp 2 lần.

#### **Câu 40:** Nếu khoảng cách vật lý giữa hai máy tính tăng gấp 3 lần thì thành phần độ trễ nào tăng gấp 3?  
A. Trễ truyền gói (d_trans)  
**B. Trễ lan truyền (d_prop)**  
C. Trễ xử lý nút (d_proc)  
D. Trễ hàng đợi (d_queue)  
* **Giải thích:** Do d_prop = d / s, khi khoảng cách d tăng 3 lần thì trễ lan truyền tăng tỷ lệ thuận 3 lần.

#### **Câu 41:** Cấu trúc topo mạng nào kết nối tất cả các máy trạm vào một thiết bị trung tâm duy nhất như Switch?  
**A. Star Topology (Hình sao)**  
B. Ring Topology (Hình vòng)  
C. Bus Topology (Đường trục)  
D. Mesh Topology (Dạng lưới)  
* **Giải thích:** Mạng hình sao kết nối các host qua các liên kết điểm-điểm độc lập tới thiết bị chuyển mạch trung tâm.

#### **Câu 42:** Trong mạng hình sao (Star), nếu một sợi cáp nối tới một máy trạm bị đứt thì:  
A. Toàn bộ mạng ngừng hoạt động  
**B. Chỉ máy trạm đó mất kết nối, các máy khác vẫn hoạt động bình thường**  
C. Switch trung tâm bị hỏng  
D. Mạng tự chuyển sang dạng vòng  
* **Giải thích:** Mỗi trạm có đường truyền độc lập tới switch nên sự cố trên một nhánh không làm ảnh hưởng các nhánh khác.

#### **Câu 43:** Cấu trúc topo mạng nào có các máy trạm cùng chia sẻ một đường cáp trục chung duy nhất?  
A. Star Topology  
**B. Bus Topology**  
C. Ring Topology  
D. Tree Topology  
* **Giải thích:** Bus Topology nối tất cả các nút vào một đường trục chung, tín hiệu phát từ một nút lan truyền trên toàn trục cáp.

#### **Câu 44:** Phương tiện truyền dẫn có dây nào chống nhiễu điện từ tốt nhất và cho tốc độ truyền cao nhất trên khoảng cách xa?  
A. Cáp đôi xoắn không bọc kim (UTP)  
B. Cáp đồng trục (Coaxial Cable)  
**C. Cáp sợi quang (Fiber Optic)**  
D. Cáp đôi xoắn bọc kim (STP)  
* **Giải thích:** Cáp quang sử dụng xung ánh sáng để truyền dẫn bit, hoàn toàn không bị ảnh hưởng bởi nhiễu điện từ.

#### **Câu 45:** Cáp xoắn đôi (Twisted Pair) thực hiện xoắn các cặp dây lại với nhau nhằm mục đích chính là:  
A. Làm cho sợi cáp dẻo dai hơn  
**B. Giảm thiểu hiện tượng nhiễu xuyên âm (Crosstalk) và nhiễu điện từ từ bên ngoài**  
C. Tăng trọng lượng của dây cáp  
D. Tiết kiệm kim loại đồng  
* **Giải thích:** Việc xoắn các cặp dây đối xứng giúp triệt tiêu từ trường gây nhiễu cảm ứng lẫn nhau giữa các cặp dây và từ môi trường.

#### **Câu 46:** Mạng truy cập gia đình DSL (Digital Subscriber Line) sử dụng hạ tầng truyền dẫn vật lý có sẵn nào?  
**A. Hạ tầng dây điện thoại cố định bằng đồng**  
B. Hạ tầng truyền hình cáp đồng trục  
C. Hạ tầng cáp quang chôn ngầm  
D. Hạ tầng sóng vô tuyến vi ba  
* **Giải thích:** DSL tận dụng đường dây điện thoại bằng đồng sẵn có để truyền dữ liệu số ở dải tần số cao hơn tần số thoại.

#### **Câu 47:** Mạng truy cập cáp (Cable Internet) sử dụng kiến trúc ghép nối nào kết hợp cáp quang và cáp đồng trục?  
A. FTTH  
**B. HFC (Hybrid Fiber Coax)**  
C. DSL  
D. Dial-up  
* **Giải thích:** HFC kết hợp cáp quang từ nhà mạng đến các nút phân phối quang khu vực, sau đó dùng cáp đồng trục nối vào từng hộ gia đình.

#### **Câu 48:** Công nghệ mạng truy cập FTTH (Fiber to the Home) có đặc điểm nổi bật là:  
**A. Kéo sợi cáp quang trực tiếp từ tổng đài nhà mạng đến tận nhà thuê bao**  
B. Chỉ sử dụng sóng vô tuyến vệ tinh  
C. Tốc độ chậm hơn mạng DSL truyền thống  
D. Sử dụng dây đôi xoắn UTP dài 100 km  
* **Giải thích:** FTTH cung cấp đường truyền sợi quang trực tiếp đến tận nhà người dùng, mang lại băng thông rất cao và ổn định.

#### **Câu 49:** Phương tiện truyền dẫn không dây nào sử dụng sóng điện từ lan truyền đa hướng trong không gian?  
A. Cáp sợi quang  
**B. Sóng vô tuyến (Radio Waves)**  
C. Cáp đồng trục  
D. Tia laser hữu tuyến  
* **Giải thích:** Sóng vô tuyến truyền tín hiệu số qua không gian, truyền xuyên tường và hỗ trợ tính di động cho người dùng.

#### **Câu 50:** Môi trường truyền dẫn vật lý được phân thành 2 nhóm lớn là:  
**A. Môi trường định hướng (Guided) và môi trường không định hướng (Unguided)**  
B. Môi trường cáp đồng và môi trường cáp quang  
C. Môi trường trong nhà và ngoài trời  
D. Môi trường số và môi trường tương tự  
* **Giải thích:** Guided media định hướng sóng truyền trong vật thể rắn (đồng, quang); Unguided media truyền sóng tự do trong không khí/chân không.

#### **Câu 51:** Hình thức tấn công làm ngập lụt một máy chủ bằng lượng truy vấn khổng lồ từ nhiều máy tính ma (botnet) gọi là:  
A. Packet Sniffing  
B. IP Spoofing  
**C. DDoS (Distributed Denial of Service)**  
D. Man-in-the-middle  
* **Giải thích:** DDoS sử dụng mạng lưới botnet phân tán để đánh sập tài nguyên tính toán hoặc làm nghẽn băng thông của máy chủ nạn nhân.

#### **Câu 52:** Kỹ thuật đặt card mạng ở chế độ promiscuous mode để thu thập và đọc trộm các gói tin trên mạng chia sẻ gọi là:  
**A. Packet Sniffing**  
B. IP Spoofing  
C. DDoS  
D. Port Scanning  
* **Giải thích:** Packet Sniffing nghe lén các khung tin đi qua môi trường truyền chung để trích xuất mật khẩu, dữ liệu không mã hóa.

#### **Câu 53:** Hành vi kẻ tấn công chèn một địa chỉ IP nguồn giả mạo vào gói tin để đánh lừa máy nhận được gọi là:  
A. Packet Sniffing  
**B. IP Spoofing**  
C. Buffer Overflow  
D. Trojan Horse  
* **Giải thích:** IP Spoofing là việc giả mạo địa chỉ IP nguồn để mạo danh máy tin cậy hoặc chuyển hướng phản hồi tới nạn nhân khác.

#### **Câu 54:** Hình thức tấn công nào kẻ tấn công bí mật đứng giữa cuộc đàm thoại của 2 bên để nghe lén và sửa đổi dữ liệu?  
**A. Man-in-the-middle (MitM)**  
B. DDoS  
C. Port Scanning  
D. Ping of Death  
* **Giải thích:** Kẻ tấn công đóng giả làm thực thể đích đối với máy gửi và đóng giả làm máy gửi đối với thực thể đích để chặn bắt luồng tin.

#### **Câu 55:** Để phòng chống hiệu quả hình thức nghe lén Packet Sniffing, giải pháp cốt lõi là:  
A. Tăng băng thông đường truyền  
**B. Sử dụng các giao thức mã hóa dữ liệu (như SSL/TLS, SSH, HTTPS)**  
C. Rút dây cáp mạng  
D. Dùng cáp đôi xoắn rẻ tiền hơn  
* **Giải thích:** Mã hóa đảm bảo kẻ nghe lén dù bắt được gói tin cũng chỉ thấy chuỗi bit vô nghĩa mà không đọc được nội dung gốc.

#### **Câu 56:** Một phần mềm độc hại có khả năng tự sao chép và tự động lây lan qua mạng mà không cần người dùng kích hoạt gọi là:  
A. Virus  
**B. Worm (Sâu máy tính)**  
C. Spyware  
D. Adware  
* **Giải thích:** Worm là mã độc tự động quét mạng tìm lỗ hổng và tự nhân bản lây nhiễm sang các host khác mà không cần tương tác của con người.

#### **Câu 57:** Một phần mềm độc hại đòi hỏi người dùng phải thực thi một tệp tin (mở file đính kèm, chạy file exe) để lây nhiễm gọi là:  
**A. Virus**  
B. Worm  
C. Botnet  
D. Packet Switch  
* **Giải thích:** Virus máy tính cần gắn mình vào một chương trình chủ và phụ thuộc vào hành vi kích hoạt của người dùng để lây lan.

#### **Câu 58:** Tập hợp hàng ngàn thiết bị bị nhiễm mã độc và chịu sự điều khiển từ xa của hacker được gọi là:  
A. Router cluster  
**B. Botnet**  
C. Intranet  
D. VLAN  
* **Giải thích:** Botnet gồm các máy tính/thiết bị IoT bị chiếm quyền điều khiển (zombie) sẵn sàng nhận lệnh mở đợt tấn công đồng loạt.

#### **Câu 59:** Công cụ kiểm tra tính thông suốt mạng `ping` hoạt động bằng cách gửi thông điệp ICMP nào?  
**A. ICMP Echo Request và nhận lại ICMP Echo Reply**  
B. ICMP Time Exceeded  
C. ICMP Destination Unreachable  
D. ICMP Redirect  
* **Giải thích:** Ping phát gói Echo Request (Type 8) đến máy đích và lắng nghe gói Echo Reply (Type 0) phản hồi để đo RTT.

#### **Câu 60:** Chương trình `traceroute` thăm dò danh sách các router trên đường đi dựa trên việc tăng dần giá trị trường nào?  
A. Checksum trong TCP  
**B. TTL (Time-To-Live) trong tiêu đề IP**  
C. Sequence Number  
D. Port Number  
* **Giải thích:** Traceroute gửi gói tin với TTL = 1, 2, 3... để kích hoạt các thông điệp lỗi ICMP Time Exceeded từ từng router dọc đường.

#### **Câu 61:** Khái niệm 'End-to-End Argument' trong thiết kế kiến trúc Internet có ý nghĩa là:  
**A. Mọi chức năng phức tạp nên được cài đặt tại các thiết bị đầu cuối thay vì đặt trong mạng lõi**  
B. Mạng lõi phải chịu trách nhiệm sửa lỗi và kiểm soát luồng cho ứng dụng  
C. Tất cả các máy tính phải có cùng cấu hình phần cứng  
D. Mạng Internet chỉ hoạt động khi có kết nối cáp quang  
* **Giải thích:** Mạng lõi Internet được thiết kế tối giản, nhanh và thông minh ở vùng biên (end systems) để dễ dàng triển khai ứng dụng mới.

#### **Câu 62:** Địa chỉ MAC được sử dụng để định danh thiết bị ở tầng nào trong mô hình Internet?  
A. Tầng Mạng  
B. Tầng Giao vận  
**C. Tầng Liên kết dữ liệu**  
D. Tầng Ứng dụng  
* **Giải thích:** Địa chỉ MAC (48 bit) là địa chỉ vật lý gắn liền với card mạng, hoạt động tại Tầng Liên kết dữ liệu để giao tiếp cục bộ.

#### **Câu 63:** Địa chỉ IP được sử dụng để định danh giao diện mạng ở tầng nào?  
**A. Tầng Mạng**  
B. Tầng Liên kết dữ liệu  
C. Tầng Giao vận  
D. Tầng Vật lý  
* **Giải thích:** Địa chỉ IP là địa chỉ logic toàn cầu thuộc Tầng Mạng, phục vụ cho việc định tuyến và chuyển tiếp liên mạng.

#### **Câu 64:** Số hiệu cổng (Port Number) được sử dụng để định danh thực thể nào tại Tầng Giao vận?  
A. Một card mạng vật lý  
**B. Một tiến trình (process) cụ thể chạy trên máy tính**  
C. Một dây cáp mạng  
D. Một router trung gian  
* **Giải thích:** Port kết hợp với địa chỉ IP tạo thành socket để phân phát dữ liệu chính xác cho tiến trình ứng dụng đang chạy.

#### **Câu 65:** Hiện tượng nghẽn mạng (Network Congestion) xảy ra khi:  
**A. Có quá nhiều nguồn phát gửi quá nhiều dữ liệu quá nhanh khiến các hàng đợi trong mạng bị quá tải**  
B. Mất kết nối vật lý  
C. Người dùng không trả tiền cước Internet  
D. Tất cả các router bị virus tấn công  
* **Giải thích:** Nghẽn mạng là tình trạng quá tải hàng đợi tại các router khi lưu lượng tổng thể vượt quá dung lượng xử lý của hạ tầng.

#### **Câu 66:** Cơ chế kiểm soát luồng (Flow Control) khác với kiểm soát tắc nghẽn (Congestion Control) ở điểm nào?  
**A. Kiểm soát luồng chống làm tràn bộ đệm bên nhận; kiểm soát tắc nghẽn chống làm tràn bộ đệm các router trong mạng lõi**  
B. Kiểm soát luồng chạy ở tầng mạng; kiểm soát tắc nghẽn chạy ở tầng ứng dụng  
C. Kiểm soát luồng dùng UDP; kiểm soát tắc nghẽn dùng TCP  
D. Cả hai cơ chế là hoàn toàn giống hệt nhau  
* **Giải thích:** Flow control là bảo vệ máy nhận (end-to-end), còn Congestion control là bảo vệ hạ tầng mạng lõi khỏi bị sụp đổ.

#### **Câu 67:** Trong mô hình chuyển mạch gói, việc phân mảnh gói tin lớn thành nhiều gói nhỏ giúp:  
**A. Giảm độ trễ truyền gói tổng thể qua các chặng trung gian nhờ xử lý đường ống (pipelining)**  
B. Tăng kích thước tiêu đề gói tin  
C. Làm cho gói tin không bao giờ bị mất  
D. Bỏ qua bước định tuyến  
* **Giải thích:** Gói nhỏ cho phép router thứ nhất vừa truyền gói 2 thì router thứ hai đã có thể chuyển tiếp gói 1 song song.

#### **Câu 68:** Một nhà cung cấp dịch vụ Internet cấp 1 (Tier-1 ISP) có đặc trưng là:  
A. Phải mua băng thông từ các ISP khác  
**B. Có mạng lưới phủ sóng toàn cầu và kết nối trực tiếp ngang hàng (peering) với nhau không mất phí**  
C. Chỉ phục vụ khách hàng cá nhân  
D. Không có router vùng lõi  
* **Giải thích:** Tier-1 ISP là các nhà mạng xương sống Internet toàn cầu, kết nối trực tiếp với nhau thông qua thỏa thuận peering tự do.

#### **Câu 69:** Điểm kết nối Internet IXP (Internet Exchange Point) được thành lập nhằm mục đích:  
**A. Cho phép các ISP trao đổi lưu lượng trực tiếp với nhau mà không phải trả phí qua mạng trung gian**  
B. Bán dây cáp mạng  
C. Lưu trữ trang web của chính phủ  
D. Cấp phát địa chỉ MAC  
* **Giải thích:** IXP là điểm đấu nối trung lập nơi nhiều ISP và mạng nội dung (CDN) kết nối trực tiếp để tiết kiệm chi phí trung chuyển.

#### **Câu 70:** Tiêu chuẩn hóa các giao thức Internet chủ yếu do tổ chức kỹ thuật nào ban hành?  
**A. IETF (thông qua các tài liệu RFC)**  
B. IEEE  
C. ISO  
D. W3C  
* **Giải thích:** IETF (Internet Engineering Task Force) phát triển và chuẩn hóa các giao thức Internet thông qua các tài liệu Request for Comments (RFC).

#### **Câu 71:** Cho liên kết có R = 100 Mbps, độ dài d = 2.000 km, s = 2 * 10^8 m/s, gói tin L = 1.000 bytes. Đại lượng nào lớn hơn?  
A. Trễ truyền gói d_trans lớn hơn nhiều trễ lan truyền d_prop  
**B. Trễ lan truyền d_prop lớn hơn nhiều trễ truyền gói d_trans**  
C. Hai độ trễ bằng nhau  
D. Cả hai độ trễ đều bằng 0  
* **Giải thích:** d_trans = 8.000 / 10^8 = 0,08 ms. d_prop = 2.000.000 / (2*10^8) = 10 ms. Như vậy d_prop (10 ms) lớn hơn rất nhiều d_trans (0,08 ms).

#### **Câu 72:** Tích số giữa băng thông và độ trễ (Bandwidth-Delay Product - R * d_prop) biểu thị:  
**A. Số lượng bit tối đa có thể lấp đầy trên đường truyền tại một thời điểm**  
B. Tổng thời gian truyền tệp tin  
C. Số lượng router trên đường đi  
D. Kích thước bộ nhớ đệm của máy nhận  
* **Giải thích:** BDP đo dung lượng của 'ống dẫn' truyền thông, tính bằng số bit có thể nằm trên đường truyền khi tín hiệu đang bay.

#### **Câu 73:** Trong mạng cáp quang liên lục địa qua đại dương, thành phần độ trễ nào chiếm tỷ trọng áp đảo?  
**A. Trễ lan truyền (d_prop)**  
B. Trễ truyền gói (d_trans)  
C. Trễ xử lý nút (d_proc)  
D. Trễ mã hóa  
* **Giải thích:** Do khoảng cách địa lý hàng nghìn km qua đại dương, trễ lan truyền (hàng chục đến hàng trăm ms) chiếm phần lớn tổng trễ.

#### **Câu 74:** Khi một gói tin bị hủy tại router do tràn bộ đệm, toàn bộ băng thông và tài nguyên mà các liên kết trước đó đã tiêu tốn cho gói tin đó sẽ:  
A. Được router hoàn trả lại  
**B. Bị lãng phí hoàn toàn**  
C. Tự động bù đắp bằng gói tin mới  
D. Chuyển thành tiền cước  
* **Giải thích:** Đây là tổn thất lớn của nghẽn mạng: năng lực truyền dẫn ở các chặng trước trở thành vô ích khi gói bị drop ở chặng sau.

#### **Câu 75:** Trường hợp nào sau đây khiến thông lượng thực tế của kết nối thấp hơn nhiều so với băng thông lý thuyết?  
A. Đường truyền có nhiều luồng dữ liệu khác cùng chia sẻ liên kết thắt cổ chai  
B. Máy nhận có kích thước cửa sổ nhận quá nhỏ  
C. Tỷ lệ mất gói cao khiến TCP phải liên tục giảm tốc độ phát  
**D. Tất cả các nguyên nhân trên**  
* **Giải thích:** Thông lượng thực tế chịu tác động đồng thời của chia sẻ băng thông, kiểm soát luồng máy nhận và thuật toán kiểm soát tắc nghẽn.

#### **Câu 76:** Giao thức nào sau đây KHÔNG thuộc tầng ứng dụng trong mô hình 5 tầng Internet?  
A. HTTP  
B. FTP  
**C. IP**  
D. DNS  
* **Giải thích:** IP là giao thức cốt lõi hoạt động tại Tầng Mạng (Network Layer).

#### **Câu 77:** Giao thức nào sau đây hoạt động ở Tầng Giao vận cung cấp dịch vụ truyền dữ liệu phi kết nối, không tin cậy?  
A. TCP  
**B. UDP**  
C. IP  
D. HTTP  
* **Giải thích:** UDP (User Datagram Protocol) là giao thức giao vận phi kết nối, truyền dữ liệu nhanh nhưng không đảm bảo độ tin cậy.

#### **Câu 78:** Giao thức nào sau đây hoạt động ở Tầng Giao vận cung cấp dịch vụ truyền dữ liệu hướng kết nối, tin cậy?  
**A. TCP**  
B. UDP  
C. ICMP  
D. ARP  
* **Giải thích:** TCP (Transmission Control Protocol) đảm bảo truyền dữ liệu tin cậy, đúng thứ tự, có kiểm soát luồng và kiểm soát tắc nghẽn.

#### **Câu 79:** Một hệ thống mạng gồm 10 máy tính kết nối dạng lưới toàn phần (Mesh Topology). Số lượng đường cáp nối cần thiết là:  
A. 10  
**B. 45**  
C. 90  
D. 20  
* **Giải thích:** Công thức số liên kết trong mạng Full-Mesh là N*(N-1)/2 = 10 * 9 / 2 = 45 đường cáp.

#### **Câu 80:** Trong mạng hình vòng (Ring Topology), thẻ bài (Token) đóng vai trò gì?  
**A. Quyền phát dữ liệu trên đường truyền chung**  
B. Địa chỉ IP của router  
C. Khóa bảo mật wifi  
D. Công cụ đo độ trễ  
* **Giải thích:** Chỉ trạm nào đang nắm giữ Token mới được phép phát dữ liệu vào vòng, giúp chống xung đột đường truyền.

#### **Câu 81:** Sự khác biệt căn bản giữa Switch và Hub là:  
**A. Switch tạo ra các miền xung đột (collision domain) riêng biệt cho từng cổng, trong khi Hub là một miền xung đột chung**  
B. Hub thông minh hơn Switch  
C. Switch chỉ dùng cho mạng không dây  
D. Hub hỗ trợ chuyển mạch gói còn Switch dùng chuyển mạch kênh  
* **Giải thích:** Switch cách ly lưu lượng từng cổng, còn Hub phát lặp lại bit nhận được ra tất cả các cổng còn lại (broadcast bừa bãi).

#### **Câu 82:** Độ trễ xử lý nút (Nodal Processing Delay) thường bao gồm các tác vụ nào?  
**A. Kiểm tra tính toàn vẹn bit ở header gói tin và tra cứu bảng định tuyến tìm cổng ra**  
B. Chờ đợi các gói tin phía trước đi hết  
C. Đẩy các bit vào sợi cáp quang  
D. Mã hóa dữ liệu ứng dụng  
* **Giải thích:** Trễ xử lý là thời gian CPU của router kiểm tra checksum, xác định địa chỉ IP đích và chọn giao diện mạng thích hợp.

#### **Câu 83:** Khi truyền một tệp tin lớn qua kết nối TCP, tốc độ truyền dữ liệu tức thời thường có dạng răng cưa (sawtooth) vì:  
**A. Thuật toán kiểm soát tắc nghẽn AIMD của TCP liên tục tăng cửa sổ cho đến khi mất gói thì giảm đi một nửa**  
B. Dây cáp mạng bị nóng lên theo chu kỳ  
C. Người dùng liên tục bật tắt máy tính  
D. Bộ nhớ đệm của router tự động xóa định kỳ  
* **Giải thích:** TCP tăng dần kích thước cửa sổ cộng gộp (Additive Increase) và giảm một nửa khi phát hiện nghẽn (Multiplicative Decrease).

#### **Câu 84:** Kỹ thuật Packet Sniffing KHÔNG THỂ giải mã được nội dung thông tin nếu phiên làm việc sử dụng giao thức nào?  
A. HTTP thuần  
B. Telnet  
C. FTP  
**D. HTTPS (SSL/TLS)**  
* **Giải thích:** HTTPS mã hóa toàn bộ dữ liệu ứng dụng trước khi gửi, kẻ nghe lén chỉ thu được chuỗi mật mã không thể đọc được nội dung.

#### **Câu 85:** Một máy chủ Web nhận được 1.000 yêu cầu/giây từ một địa chỉ IP duy nhất. Đây có thể là dấu hiệu của cuộc tấn công:  
**A. DoS đơn nguồn**  
B. DDoS phân tán  
C. Nghe lén cáp quang  
D. Nhiễm virus cục bộ  
* **Giải thích:** Tấn công từ chối dịch vụ xuất phát từ một máy duy nhất là tấn công DoS (Denial of Service).

#### **Câu 86:** Tại sao mạng Internet công cộng không áp dụng Chuyển mạch kênh cho lưu lượng duyệt Web?  
**A. Vì duyệt web có tính chất đột biến cao (truyền một lúc rồi người dùng đọc trang rất lâu), dùng chuyển mạch kênh sẽ lãng phí tài nguyên**  
B. Vì chuyển mạch kênh đắt tiền hơn cáp quang  
C. Vì chuyển mạch kênh không hỗ trợ truyền văn bản  
D. Vì chuyển mạch kênh chỉ dành cho truyền hình  
* **Giải thích:** Lưu lượng web nghỉ ngơi phần lớn thời gian đọc, chuyển mạch gói cho phép hàng ngàn người khác dùng chung băng thông lúc đó.

#### **Câu 87:** Khi một gói tin đi qua 5 router chuyển mạch gói từ nguồn đến đích, gói tin phải chịu trễ lưu-và-chuyển-tiếp (store-and-forward) bao nhiêu lần?  
A. 1 lần  
B. 5 lần  
**C. 6 lần (tại máy nguồn và 5 router)**  
D. Không lần nào  
* **Giải thích:** Mỗi chặng truyền (từ máy nguồn và tại mỗi router trung gian) đều phải nạp đủ gói rồi mới đẩy sang liên kết tiếp theo.

#### **Câu 88:** Giả sử không có mất mát và trễ hàng đợi bằng 0, thời gian truyền một gói tin L bits qua N liên kết nối tiếp có cùng tốc độ R là:  
**A. N * (L / R) + tổng trễ lan truyền**  
B. L / (N * R)  
C. N * (R / L)  
D. (N - 1) * (L / R)  
* **Giải thích:** Gói tin phải được truyền qua N chặng liên tiếp, mỗi chặng tốn L/R thời gian truyền cộng với thời gian bay trên đường truyền.

#### **Câu 89:** Băng thông (Bandwidth / Transmission Rate) của một liên kết được đo bằng đơn vị chuẩn nào?  
A. Bytes trên giây (Bps)  
**B. Bits trên giây (bps)**  
C. Hertz (Hz)  
D. Gói tin trên giây  
* **Giải thích:** Tốc độ truyền dữ liệu trong mạng máy tính luôn được đo bằng đơn vị chuẩn là số bit truyền được trong một giây (bps).

#### **Câu 90:** Dung lượng một gói tin được biểu diễn bằng Byte, khi tính độ trễ truyền gói (L / R) bắt buộc phải:  
A. Giữ nguyên đơn vị Byte  
**B. Nhân số Byte với 8 để đổi sang đơn vị bit**  
C. Chia số Byte cho 8  
D. Đổi sang đơn vị Hertz  
* **Giải thích:** Vì tốc độ đường truyền R tính bằng bps (bit/giây), nên kích thước L phải đổi sang bit: L(bits) = Kích thước(Bytes) * 8.

#### **Câu 91:** Cáp quang biển xuyên đại dương kết nối các châu lục là thành phần thuộc phân vùng nào của Internet?  
A. Mạng truy cập (Access Network)  
B. Mạng biên (Network Edge)  
**C. Mạng lõi (Network Core)**  
D. Mạng LAN nội bộ  
* **Giải thích:** Hệ thống cáp quang biển liên kết các ISP cấp cao tạo thành trục xương sống của mạng lõi Internet.

#### **Câu 92:** Thiết bị Modem (Modulator-Demodulator) có chức năng cơ bản là:  
**A. Chuyển đổi tín hiệu số (digital) của máy tính thành tín hiệu tương tự (analog) truyền trên đường truyền và ngược lại**  
B. Quét virus máy tính  
C. Định tuyến gói tin IP  
D. Phân chia tên miền  
* **Giải thích:** Modem điều chế tín hiệu số thành sóng tương tự để truyền đi xa và giải điều chế tín hiệu thu được thành bit số cho máy tính.

#### **Câu 93:** Mô hình mạng mà trong đó một máy trạm vừa có thể đóng vai trò máy khách (Client) vừa có thể đóng vai trò máy chủ (Server) là:  
A. Mô hình Client-Server thuần túy  
**B. Mô hình P2P (Peer-to-Peer)**  
C. Mô hình Master-Slave  
D. Mô hình Mainframe  
* **Giải thích:** Trong mạng P2P, mỗi peer vừa yêu cầu tải dữ liệu từ người khác (client) vừa chia sẻ dữ liệu của mình cho người khác (server).

#### **Câu 94:** Một liên kết truyền thông có thông lượng R = 10 Mbps. Thời gian để truyền hết một tệp tin dung lượng 25 MBytes qua liên kết này là:  
A. 2,5 giây  
**B. 20 giây**  
C. 200 giây  
D. 2 giây  
* **Giải thích:** Kích thước tệp = 25 * 8 = 200 Mbits. Thời gian truyền = 200 Mbits / 10 Mbps = 20 giây.

#### **Câu 95:** Một hình ảnh dung lượng 2 MBytes được tải qua đường truyền có tốc độ tải thực tế 4 Mbps. Thời gian tải tệp là:  
A. 0,5 giây  
**B. 4 giây**  
C. 8 giây  
D. 16 giây  
* **Giải thích:** Dung lượng = 2 * 8 = 16 Mbits. Thời gian = 16 Mbits / 4 Mbps = 4 giây.

#### **Câu 96:** Tấn công giả mạo (Spoofing) thường được kẻ xấu kết hợp với mục đích gì?  
**A. Giấu tung tích thực sự của kẻ tấn công hoặc đánh lừa hệ thống xác thực dựa trên IP**  
B. Tăng tốc độ kết nối Internet  
C. Khôi phục mật khẩu bị mất  
D. Bảo vệ dữ liệu cá nhân  
* **Giải thích:** Giả mạo IP giúp kẻ tấn công qua mặt các tường lửa lọc theo IP hoặc hướng luồng phản hồi tấn công về phía nạn nhân khác.

#### **Câu 97:** Đặc tính quan trọng nhất của các giao thức chuẩn Internet (RFC) là gì?  
**A. Là các tiêu chuẩn mở (Open standards), cho phép thiết bị của các nhà sản xuất khác nhau tương tác hoàn toàn với nhau**  
B. Bảo mật tuyệt đối không thể bị tấn công  
C. Chỉ chạy được trên hệ điều hành Windows  
D. Được bảo hộ bản quyền thương mại khép kín  
* **Giải thích:** Tính chất mở của chuẩn Internet cho phép mọi phần cứng và phần mềm tương thích và giao tiếp thông suốt trên toàn cầu.

#### **Câu 98:** Trong mô hình Internet, tầng nào chịu trách nhiệm truyền dữ liệu hop-by-hop giữa 2 router lân cận nối trực tiếp?  
A. Tầng Mạng  
B. Tầng Giao vận  
**C. Tầng Liên kết dữ liệu**  
D. Tầng Ứng dụng  
* **Giải thích:** Tầng Liên kết dữ liệu chịu trách nhiệm chuyển giao frame qua từng chặng (hop-by-hop) giữa hai nút kề nhau trên cùng một link.

#### **Câu 99:** Trong mô hình Internet, tầng nào chịu trách nhiệm truyền gói tin end-to-end từ máy nguồn tới máy đích qua nhiều router?  
A. Tầng Liên kết dữ liệu  
**B. Tầng Mạng**  
C. Tầng Giao vận  
D. Tầng Vật lý  
* **Giải thích:** Tầng Mạng chịu trách nhiệm vận chuyển gói tin trên toàn tuyến đường (end-to-end routing) từ trạm nguồn đến trạm đích.

#### **Câu 100:** Trong mô hình Internet, tầng nào chịu trách nhiệm giao tiếp process-to-process giữa hai tiến trình ứng dụng?  
**A. Tầng Giao vận**  
B. Tầng Mạng  
C. Tầng Liên kết dữ liệu  
D. Tầng Vật lý  
* **Giải thích:** Tầng Giao vận cung cấp kênh truyền thông logic trực tiếp giữa các tiến trình ứng dụng chạy trên hai máy chủ khác nhau.

## PHẦN 2: CHƯƠNG 2 – TẦNG ỨNG DỤNG (CÂU 101 – 200)

#### **Câu 101:** Trong kiến trúc Client-Server, máy chủ (Server) có đặc điểm nào sau đây?  
**A. Luôn hoạt động 24/7 và sở hữu địa chỉ IP tĩnh cố định**  
B. Chỉ bật khi có yêu cầu từ client  
C. Có IP thay đổi liên tục  
D. Chủ động gửi dữ liệu tới client trước  
* **Giải thích:** Server là thực thể phục vụ trung tâm, luôn lắng nghe yêu cầu và phải có địa chỉ IP cố định.

#### **Câu 102:** Trong kiến trúc Client-Server, máy khách (Client) có đặc điểm nào sau đây?  
A. Luôn bật liên tục  
B. Có IP tĩnh  
**C. Chủ động khởi tạo phiên liên lạc với máy chủ**  
D. Trực tiếp phục vụ các client khác  
* **Giải thích:** Client khởi tạo kết nối khi có nhu cầu; các client không giao tiếp trực tiếp với nhau.

#### **Câu 103:** Ưu điểm vượt trội của mạng ngang hàng (P2P) so với Client-Server là:  
A. Dễ quản lý tập trung  
**B. Tính tự mở rộng dung lượng phục vụ (Self-scalability)**  
C. Bảo mật tuyệt đối  
D. Không cần Internet  
* **Giải thích:** Mỗi peer khi tải về đồng thời đóng góp băng thông tải lên giúp năng lực toàn mạng tự tăng theo số người dùng.

#### **Câu 104:** Giao thức nào sau đây hoạt động ở Tầng Ứng dụng?  
A. IP  
B. TCP  
**C. HTTP**  
D. Ethernet  
* **Giải thích:** HTTP là giao thức truyền tải siêu văn bản ở Tầng Ứng dụng.

#### **Câu 105:** Số hiệu cổng mặc định của dịch vụ Web HTTP là:  
A. 21  
B. 25  
**C. 80**  
D. 443  
* **Giải thích:** HTTP sử dụng cổng mặc định TCP 80.

#### **Câu 106:** Số hiệu cổng mặc định của dịch vụ Web bảo mật HTTPS là:  
A. 80  
**B. 443**  
C. 8080  
D. 22  
* **Giải thích:** HTTPS sử dụng cổng mặc định TCP 443.

#### **Câu 107:** Số hiệu cổng mặc định của giao thức truyền thư SMTP là:  
**A. 25**  
B. 110  
C. 143  
D. 53  
* **Giải thích:** SMTP sử dụng cổng mặc định TCP 25.

#### **Câu 108:** Số hiệu cổng mặc định của giao thức phân giải tên miền DNS là:  
A. 80  
**B. 53**  
C. 67  
D. 161  
* **Giải thích:** DNS sử dụng cổng mặc định UDP 53.

#### **Câu 109:** Giao thức truyền tệp FTP sử dụng cổng nào cho kênh điều khiển (Control Connection)?  
A. Cổng 20  
**B. Cổng 21**  
C. Cổng 80  
D. Cổng 25  
* **Giải thích:** FTP dùng cổng 21 cho kênh điều khiển và cổng 20 cho kênh dữ liệu.

#### **Câu 110:** Giao thức HTTP được định nghĩa là 'phi trạng thái' (Stateless) vì:  
**A. Máy chủ không lưu giữ thông tin về các yêu cầu trước đó của máy khách**  
B. HTTP chạy trên UDP  
C. HTTP chỉ dùng cho văn bản  
D. Các trang web không cập nhật  
* **Giải thích:** Server xử lý từng request độc lập và không nhớ trạng thái quá khứ của client.

#### **Câu 111:** Phương thức HTTP nào yêu cầu máy chủ chỉ gửi về phần Header mà không gửi phần Body?  
A. GET  
**B. HEAD**  
C. POST  
D. PUT  
* **Giải thích:** HEAD có định dạng phản hồi giống GET nhưng bỏ trống phần Entity Body để kiểm tra thông tin tài nguyên.

#### **Câu 112:** Phương thức HTTP nào dùng để gửi dữ liệu từ form của client lên server trong Entity Body?  
A. GET  
**B. POST**  
C. HEAD  
D. TRACE  
* **Giải thích:** POST đưa dữ liệu biểu mẫu vào phần thân của thông điệp để gửi lên server xử lý.

#### **Câu 113:** Mã trạng thái phản hồi HTTP 200 có ý nghĩa là:  
**A. Yêu cầu thành công (OK)**  
B. Di chuyển vĩnh viễn  
C. Không tìm thấy trang  
D. Lỗi nội bộ server  
* **Giải thích:** Mã 200 OK biểu thị yêu cầu đã được máy chủ tiếp nhận và xử lý thành công.

#### **Câu 114:** Mã trạng thái HTTP 301 biểu thị điều gì?  
**A. Moved Permanently**  
B. Not Modified  
C. Bad Request  
D. Unauthorized  
* **Giải thích:** Mã 301 thông báo tài nguyên đã đổi địa chỉ cố định sang URL mới.

#### **Câu 115:** Mã trạng thái HTTP 404 biểu thị điều gì?  
A. Server Error  
**B. Not Found**  
C. Forbidden  
D. OK  
* **Giải thích:** Mã 404 là lỗi client khi URL yêu cầu không tồn tại trên server.

#### **Câu 116:** Mã trạng thái HTTP 500 biểu thị điều gì?  
A. Client Error  
**B. Internal Server Error**  
C. Success  
D. Redirect  
* **Giải thích:** Mã 500 là lỗi phát sinh từ nội bộ chương trình hoặc cấu hình của server.

#### **Câu 117:** Trong Non-persistent HTTP, mỗi kết nối TCP phục vụ truyền tải bao nhiêu đối tượng?  
**A. Duy nhất 1 đối tượng**  
B. Tối đa 5 đối tượng  
C. Tất cả các đối tượng  
D. Tùy thuộc vào băng thông  
* **Giải thích:** Non-persistent HTTP đóng kết nối TCP ngay sau khi truyền xong 1 đối tượng.

#### **Câu 118:** Tải 1 đối tượng bằng Non-persistent HTTP tiêu tốn thời gian trễ tối thiểu là:  
A. 1 RTT  
**B. 2 RTT + thời gian truyền file**  
C. 3 RTT  
D. 0 RTT  
* **Giải thích:** Gồm 1 RTT để bắt tay TCP và 1 RTT để gửi HTTP GET và nhận dữ liệu.

#### **Câu 119:** Persistent HTTP được đặt làm mặc định từ phiên bản nào?  
A. HTTP/0.9  
B. HTTP/1.0  
**C. HTTP/1.1**  
D. HTTP/2  
* **Giải thích:** HTTP/1.1 quy định mặc định giữ kết nối TCP mở để phục vụ nhiều yêu cầu liên tiếp.

#### **Câu 120:** Cơ chế Cookies được thiết kế nhằm mục đích:  
**A. Duy trì trạng thái phiên làm việc của người dùng trên nền giao thức HTTP phi trạng thái**  
B. Tăng tốc độ cáp quang  
C. Mã hóa đường truyền  
D. Xóa tệp rác  
* **Giải thích:** Cookie giúp website nhận diện người dùng, duy trì giỏ hàng và trạng thái đăng nhập.

#### **Câu 121:** Trong HTTP Conditional GET, client gửi trường header nào để kiểm tra tính cập nhật của bộ nhớ đệm?  
**A. If-modified-since:**  
B. Set-cookie:  
C. User-Agent:  
D. Host:  
* **Giải thích:** Header If-modified-since mang mốc thời gian của bản sao để hỏi server tệp đã đổi chưa.

#### **Câu 122:** Nếu đối tượng trên server chưa bị sửa đổi, server phản hồi yêu cầu Conditional GET bằng mã:  
A. 200 OK  
**B. 304 Not Modified**  
C. 404 Not Found  
D. 500 Server Error  
* **Giải thích:** Mã 304 thông báo bản sao trong cache vẫn hợp lệ, phần thân thông điệp rỗng.

#### **Câu 123:** Vấn đề nghẽn đầu hàng (Head-of-Line Blocking) trong HTTP/1.1 xảy ra khi:  
**A. Đối tượng lớn ở đầu hàng truyền chậm làm tắc tất cả các đối tượng nhỏ phía sau trên cùng kết nối TCP**  
B. Cáp quang bị đứt  
C. DNS bị lỗi  
D. Server hết bộ nhớ  
* **Giải thích:** HTTP/1.1 truyền dữ liệu tuần tự nên tệp lớn phía trước sẽ chặn các tệp phía sau.

#### **Câu 124:** HTTP/2 giải quyết vấn đề nghẽn đầu hàng bằng kỹ thuật nào?  
A. Chuyển sang dùng UDP  
**B. Chia nhỏ thông điệp thành các frames nhị phân và truyền xen kẽ (interleaving) trên cùng 1 kết nối TCP**  
C. Cấm dùng hình ảnh  
D. Tăng số port  
* **Giải thích:** HTTP/2 ghép kênh nhị phân cho phép nhiều request/response truyền song song xen kẽ.

#### **Câu 125:** Giao thức nào chịu trách nhiệm chuyển thư giữa các Mail Server trên mạng Internet?  
A. POP3  
B. IMAP  
**C. SMTP**  
D. HTTP  
* **Giải thích:** SMTP là giao thức đẩy thư tiêu chuẩn giữa các máy chủ thư điện tử.

#### **Câu 126:** SMTP sử dụng giao thức giao vận nào ở cổng mặc định bao nhiêu?  
A. UDP cổng 25  
**B. TCP cổng 25**  
C. TCP cổng 110  
D. UDP cổng 53  
* **Giải thích:** SMTP chạy trên nền TCP tin cậy ở cổng chuẩn 25.

#### **Câu 127:** Các thông điệp truyền qua SMTP nguyên bản bị giới hạn ở chuẩn mã hóa nào?  
**A. 7-bit ASCII**  
B. 16-bit Unicode  
C. Nhị phân 32-bit  
D. Base64  
* **Giải thích:** SMTP ban đầu chỉ thiết kế cho văn bản ký tự 7-bit ASCII.

#### **Câu 128:** Chuẩn nào cho phép đính kèm tệp âm thanh, hình ảnh, nhị phân trong thư điện tử?  
**A. MIME**  
B. HTML  
C. DNS  
D. FTP  
* **Giải thích:** MIME mã hóa dữ liệu nhị phân thành chuỗi ký tự an toàn để truyền qua SMTP.

#### **Câu 129:** Chuỗi ký tự quy ước kết thúc khối dữ liệu DATA trong phiên SMTP là:  
A. QUIT  
**B. Một dòng chỉ chứa dấu chấm (CRLF.CRLF)**  
C. EXIT  
D. END  
* **Giải thích:** Quy chuẩn RFC quy định một dấu chấm nằm riêng biệt trên một dòng để báo hết thư.

#### **Câu 130:** Lệnh nào dùng để kết thúc phiên làm việc SMTP và ngắt kết nối TCP?  
A. BYE  
**B. QUIT**  
C. CLOSE  
D. EXIT  
* **Giải thích:** Client gửi lệnh QUIT để server xác nhận mã 221 và đóng kết nối.

#### **Câu 131:** Cổng dịch vụ mặc định của giao thức kéo thư POP3 là:  
A. TCP cổng 25  
**B. TCP cổng 110**  
C. TCP cổng 143  
D. UDP cổng 110  
* **Giải thích:** POP3 sử dụng cổng mặc định TCP 110.

#### **Câu 132:** Cổng dịch vụ mặc định của giao thức kéo thư IMAP là:  
A. TCP cổng 25  
B. TCP cổng 110  
**C. TCP cổng 143**  
D. UDP cổng 143  
* **Giải thích:** IMAP sử dụng cổng mặc định TCP 143.

#### **Câu 133:** Ưu điểm vượt trội của IMAP so với POP3 là:  
**A. Đồng bộ hóa thư mục và trạng thái đọc/chưa đọc tập trung trực tiếp trên server**  
B. Tốc độ tải nhanh hơn cáp quang  
C. Không cần mật khẩu  
D. Không tốn băng thông  
* **Giải thích:** IMAP lưu trữ cây thư mục và trạng thái trên server giúp người dùng truy cập nhất quán trên nhiều thiết bị.

#### **Câu 134:** Cấp cao nhất trong hệ thống máy chủ DNS toàn cầu là:  
A. TLD DNS Server  
B. Authoritative DNS Server  
**C. Root DNS Server**  
D. Local DNS Server  
* **Giải thích:** Root DNS Server đứng ở đỉnh của cây phân cấp tên miền toàn cầu.

#### **Câu 135:** Máy chủ quản lý các đuôi tên miền .com, .net, .vn thuộc cấp nào?  
A. Root DNS  
**B. TLD (Top-Level Domain) DNS**  
C. Authoritative DNS  
D. Local DNS  
* **Giải thích:** TLD server phụ trách các tên miền cấp cao nhất theo lĩnh vực và quốc gia.

#### **Câu 136:** Máy chủ lưu trữ chính thức các bản ghi của một tổ chức cụ thể gọi là:  
A. Root DNS  
B. TLD DNS  
**C. Authoritative DNS (Máy chủ thẩm quyền)**  
D. Proxy DNS  
* **Giải thích:** Authoritative server chứa bản ghi gốc của tổ chức đó.

#### **Câu 137:** Bản ghi tài nguyên DNS Type A thực hiện ánh xạ nào?  
**A. Hostname sang địa chỉ IPv4**  
B. Hostname sang địa chỉ IPv6  
C. Tên bí danh sang tên chính thức  
D. Tên miền sang mail server  
* **Giải thích:** Type A lưu trữ địa chỉ IPv4 tương ứng với hostname.

#### **Câu 138:** Bản ghi DNS Type AAAA thực hiện ánh xạ nào?  
A. Hostname sang IPv4  
**B. Hostname sang IPv6**  
C. Domain sang DNS server  
D. Domain sang Mail server  
* **Giải thích:** Type AAAA lưu trữ địa chỉ IPv6 128-bit.

#### **Câu 139:** Bản ghi DNS Type CNAME chứa thông tin gì trong trường Value?  
A. Địa chỉ IPv4  
**B. Tên miền chính thức (Canonical Hostname)**  
C. Tên mail server  
D. Địa chỉ MAC  
* **Giải thích:** CNAME ánh xạ một tên biệt danh (alias) sang tên miền chính thức.

#### **Câu 140:** Bản ghi DNS Type MX chứa thông tin gì trong trường Value?  
A. Địa chỉ IP máy chủ web  
**B. Tên của máy chủ thư điện tử (Mail Server)**  
C. Tên máy chủ DNS  
D. Mã chứng chỉ  
* **Giải thích:** Type MX định danh máy chủ mail phụ trách nhận thư cho domain.

#### **Câu 141:** Bản ghi DNS Type NS chứa thông tin gì trong trường Value?  
**A. Tên của máy chủ DNS thẩm quyền (Authoritative Name Server)**  
B. Địa chỉ IPv4 của client  
C. Tên router  
D. Mã bưu chính  
* **Giải thích:** Type NS xác định hostname của máy chủ DNS quản lý vùng tên miền đó.

#### **Câu 142:** DNS sử dụng giao thức giao vận nào ở cổng mặc định bao nhiêu?  
A. TCP cổng 80  
**B. UDP cổng 53**  
C. TCP cổng 25  
D. UDP cổng 67  
* **Giải thích:** DNS chạy trên UDP cổng 53 để phản hồi truy vấn phân giải nhanh chóng.

#### **Câu 143:** Trường TTL trong bản ghi DNS có ý nghĩa là:  
**A. Thời gian cho phép lưu bản ghi trong bộ nhớ đệm Cache (tính bằng giây)**  
B. Số chặng router  
C. Kích thước gói tin  
D. Số người truy cập  
* **Giải thích:** TTL đếm ngược thời gian bản ghi hợp lệ trong cache trước khi phải truy vấn lại.

#### **Câu 144:** Trong công nghệ DASH, tệp MPD (Media Presentation Description) chứa thông tin gì?  
A. Mã độc  
**B. Danh sách các phân đoạn video, URL và các mức bitrate tương ứng**  
C. Video gốc  
D. Mật khẩu người dùng  
* **Giải thích:** Tệp MPD là bản mô tả giúp client biết các mức chất lượng video có sẵn để chọn tải.

#### **Câu 145:** Trong BitTorrent, tập hợp tất cả các peer cùng chia sẻ một tệp gọi là:  
A. Cluster  
**B. Swarm**  
C. Tracker  
D. Subnet  
* **Giải thích:** Swarm là cộng đồng các nút mạng đang cùng tải và upload tệp torrent.

#### **Câu 146:** Một peer đã tải đủ 100% tệp và tiếp tục mở máy tải lên cho người khác gọi là:  
A. Leecher  
**B. Seeder**  
C. Tracker  
D. Client  
* **Giải thích:** Seeder là máy trạm đã có trọn vẹn tệp và chỉ chia sẻ cho mạng.

#### **Câu 147:** Chiến lược 'Rarest First' trong BitTorrent có nghĩa là:  
**A. Ưu tiên tải các mảnh hiếm nhất trong nhóm lân cận trước**  
B. Tải mảnh nhẹ nhất  
C. Tải ngẫu nhiên  
D. Tải từ seeder giàu nhất  
* **Giải thích:** Tải mảnh hiếm giúp nhanh chóng nhân bản các phần dữ liệu ít bản sao trong swarm.

#### **Câu 148:** Thuật toán Tit-for-Tat trong BitTorrent định kỳ 10 giây thực hiện việc gì?  
A. Xóa dữ liệu  
**B. Chọn 4 peer gửi nhanh nhất để mở luồng tải lên (unchoke) cho họ**  
C. Đổi IP  
D. Đóng kết nối  
* **Giải thích:** Tit-for-Tat ưu tiên cấp phát upload cho các peer có đóng góp tốc độ tải cao nhất.

#### **Câu 149:** CDN (Content Distribution Network) tối ưu hóa truyền video trực tuyến bằng cách:  
**A. Đặt các máy chủ biên phân tán gần người dùng và điều hướng truy cập qua DNS**  
B. Bắt người dùng xem quảng cáo  
C. Giảm kích thước video  
D. Ép dùng cáp quang  
* **Giải thích:** CDN đưa nội dung đến các cụm máy chủ gần người dùng nhất để giảm trễ và giảm tải mạng lõi.

#### **Câu 150:** Mã phản hồi HTTP 401 Unauthorized có ý nghĩa là:  
A. Yêu cầu thành công  
**B. Đòi hỏi người dùng phải đăng nhập/xác thực**  
C. Không tìm thấy trang  
D. Lỗi server  
* **Giải thích:** Mã 401 yêu cầu client cung cấp thông tin xác thực để truy cập tài nguyên.

#### **Câu 151:** Giao thức nào sau đây chạy ở Tầng Ứng dụng để quản lý cấu hình mạng tự động?  
**A. DHCP**  
B. ARP  
C. ICMP  
D. TCP  
* **Giải thích:** DHCP là giao thức tầng ứng dụng chạy trên UDP để cấp phát IP động cho client.

#### **Câu 152:** DHCP sử dụng cổng UDP nào cho Server và Client?  
**A. Server cổng 67 và Client cổng 68**  
B. Server cổng 80 và Client cổng 8080  
C. Server cổng 53 và Client cổng 53  
D. Server cổng 25 và Client cổng 110  
* **Giải thích:** DHCP Server lắng nghe cổng 67, Client nhận phản hồi ở cổng 68.

#### **Câu 153:** Quá trình cấp phát IP của DHCP gồm 4 bước theo thứ tự (DORA) là:  
**A. Discover -> Offer -> Request -> Acknowledge**  
B. Request -> Offer -> Discover -> Ack  
C. Detect -> Open -> Reset -> Ack  
D. Discover -> Open -> Receive -> Apply  
* **Giải thích:** Client phát broadcast Discover, server trả Offer, client gửi Request, server chốt Acknowledge.

#### **Câu 154:** Khi client gửi thông điệp DHCP Discover, địa chỉ IP đích là:  
A. 127.0.0.1  
**B. 255.255.255.255 (Broadcast)**  
C. 0.0.0.0  
D. 192.168.1.1  
* **Giải thích:** Client chưa có IP nên gửi broadcast 255.255.255.255 với IP nguồn là 0.0.0.0.

#### **Câu 155:** Giao thức SNMP (Simple Network Management Protocol) hoạt động ở tầng nào?  
A. Tầng Mạng  
B. Tầng Giao vận  
**C. Tầng Ứng dụng**  
D. Tầng Liên kết  
* **Giải thích:** SNMP là giao thức tầng ứng dụng dùng để giám sát và quản trị các thiết bị mạng.

#### **Câu 156:** SNMP sử dụng giao thức giao vận nào ở cổng mặc định bao nhiêu?  
A. TCP cổng 161  
**B. UDP cổng 161**  
C. TCP cổng 80  
D. UDP cổng 53  
* **Giải thích:** SNMP gửi truy vấn qua UDP cổng 161 và nhận bẫy sự kiện (Traps) ở cổng 162.

#### **Câu 157:** Giao thức Telnet truyền dữ liệu đăng nhập từ xa dưới dạng nào?  
**A. Văn bản thô (Plain text) không mã hóa**  
B. Mã hóa SSL/TLS  
C. Chuỗi hàm băm MD5  
D. Mã hóa khóa công khai RSA  
* **Giải thích:** Telnet truyền mật khẩu và lệnh dưới dạng plain text, rất dễ bị bắt trộm bằng packet sniffing.

#### **Câu 158:** Giao thức nào thay thế hoàn toàn Telnet để cung cấp phiên đăng nhập dòng lệnh từ xa an toàn?  
A. FTP  
**B. SSH (Secure Shell)**  
C. HTTP  
D. SMTP  
* **Giải thích:** SSH chạy trên TCP cổng 22, mã hóa toàn bộ phiên làm việc và xác thực bằng khóa công khai.

#### **Câu 159:** Cổng dịch vụ mặc định của giao thức SSH là:  
A. Cổng 21  
**B. Cổng 22**  
C. Cổng 23  
D. Cổng 25  
* **Giải thích:** SSH mặc định lắng nghe kết nối tại cổng TCP 22.

#### **Câu 160:** Cổng dịch vụ mặc định của giao thức Telnet là:  
A. Cổng 21  
B. Cổng 22  
**C. Cổng 23**  
D. Cổng 25  
* **Giải thích:** Telnet truyền thống sử dụng cổng TCP 23.

#### **Câu 161:** Trong HTTP, mã phản hồi 206 Partial Content thường xuất hiện khi nào?  
A. Tải toàn bộ tệp tin  
**B. Client yêu cầu tải một dải byte cụ thể (Range request) để tiếp tục tải tệp bị gián đoạn**  
C. Trang web bị xóa  
D. Server hết băng thông  
* **Giải thích:** Mã 206 dùng cho tính năng resume download hoặc streaming phân đoạn.

#### **Câu 162:** Mã phản hồi HTTP 403 Forbidden có nghĩa là:  
A. Không tìm thấy trang  
**B. Server hiểu yêu cầu nhưng từ chối thực hiện (không có quyền truy cập)**  
C. Yêu cầu thành công  
D. Chuyển hướng vĩnh viễn  
* **Giải thích:** Mã 403 biểu thị client không có thẩm quyền truy cập tài nguyên bị khóa.

#### **Câu 163:** Mã phản hồi HTTP 503 Service Unavailable có nghĩa là:  
A. Tài nguyên đã bị xóa  
**B. Server hiện tạm thời không thể xử lý yêu cầu do quá tải hoặc đang bảo trì**  
C. Client nhập sai URL  
D. Chuyển hướng  
* **Giải thích:** Mã 503 thông báo server tạm ngưng phục vụ trong thời gian ngắn.

#### **Câu 164:** Trường header Content-Length trong HTTP Response cho biết thông tin gì?  
**A. Kích thước của phần Entity Body tính bằng byte**  
B. Số lượng hình ảnh  
C. Độ dài URL  
D. Thời gian xử lý  
* **Giải thích:** Content-Length khai báo dung lượng byte của dữ liệu tải về để trình duyệt biết khi nào kết thúc nhận.

#### **Câu 165:** Trường header Content-Type trong HTTP Response dùng để làm gì?  
**A. Khai báo kiểu phương tiện (MIME type) của dữ liệu trả về (như text/html, image/jpeg)**  
B. Khai báo địa chỉ IP của server  
C. Khai báo mật khẩu  
D. Khai báo ngôn ngữ lập trình  
* **Giải thích:** Content-Type giúp trình duyệt biết cách hiển thị hoặc mở đúng ứng dụng tương ứng với tệp.

#### **Câu 166:** Giao thức WebSocket cung cấp kênh truyền thông có đặc điểm gì?  
**A. Kênh truyền hai chiều toàn phần (Full-duplex) trên 1 kết nối TCP duy nhất sau khi bắt tay qua HTTP**  
B. Kênh truyền một chiều  
C. Chạy trên nền UDP  
D. Phi trạng thái hoàn toàn  
* **Giải thích:** WebSocket duy trì kết nối persistent 2 chiều liên tục cho các ứng dụng realtime như chat, sàn chứng khoán.

#### **Câu 167:** Giao thức NTP (Network Time Protocol) chạy ở tầng nào và có nhiệm vụ gì?  
**A. Tầng Ứng dụng, đồng bộ đồng hồ thời gian giữa các máy tính trên mạng qua UDP cổng 123**  
B. Tầng Mạng, định tuyến gói tin  
C. Tầng Giao vận, đo RTT  
D. Tầng Liên kết, bấm giờ cáp quang  
* **Giải thích:** NTP dùng UDP cổng 123 để đồng bộ giờ hệ thống chính xác tới mili-giây.

#### **Câu 168:** Trong DNS, tên miền gốc (Root Domain) được biểu diễn bằng ký hiệu nào?  
**A. Dấu chấm '.' ở cuối tên miền**  
B. Dấu gạch chéo '/'  
C. Chữ 'root'  
D. Ký tự '@'  
* **Giải thích:** Ví dụ `www.google.com.` với dấu chấm cuối cùng đại diện cho gốc của cây DNS toàn cầu.

#### **Câu 169:** Một FQDN (Fully Qualified Domain Name) là gì?  
**A. Tên miền đầy đủ xác định chính xác vị trí của host trong cây phân cấp DNS từ lá đến gốc**  
B. Địa chỉ IP tĩnh  
C. Địa chỉ MAC phần cứng  
D. Tên người dùng máy tính  
* **Giải thích:** FQDN chứa đầy đủ các nhãn phân cấp từ tên host đến domain và TLD.

#### **Câu 170:** Bản ghi tài nguyên DNS Type SOA (Start of Authority) lưu trữ thông tin gì?  
**A. Thông tin quản trị cốt lõi của một DNS zone (server chính, email quản trị, serial number, refresh rate)**  
B. Địa chỉ IPv4 của client  
C. Mật khẩu máy chủ  
D. Tên card mạng  
* **Giải thích:** Bản ghi SOA đứng đầu mỗi file cấu hình zone để quản lý đồng bộ giữa Primary và Secondary DNS.

#### **Câu 171:** Bản ghi tài nguyên DNS Type TXT thường được sử dụng trong thực tế để làm gì?  
**A. Lưu trữ văn bản tùy ý phục vụ xác thực quyền sở hữu tên miền, cấu hình SPF và DKIM chống giả mạo email**  
B. Tăng tốc độ mạng  
C. Lưu trữ hình ảnh  
D. Định tuyến gói tin  
* **Giải thích:** Bản ghi TXT là công cụ quan trọng để nhúng các chính sách bảo mật email như SPF, DMARC.

#### **Câu 172:** Trong kiến trúc email, phần mềm MUA (Mail User Agent) là gì?  
**A. Chương trình giao diện email của người dùng (như Thunderbird, Outlook, ứng dụng di động)**  
B. Máy chủ mail  
C. Router biên  
D. Cáp quang  
* **Giải thích:** MUA là ứng dụng cho phép người dùng soạn, gửi, nhận và đọc thư.

#### **Câu 173:** Trong kiến trúc email, phần mềm MTA (Mail Transfer Agent) là gì?  
**A. Chương trình máy chủ chuyển tiếp thư chạy ngầm (như Postfix, Sendmail) sử dụng SMTP**  
B. Trình duyệt web  
C. Hộp thư rác  
D. Card mạng  
* **Giải thích:** MTA là thực thể server thực hiện định tuyến và chuyển giao email giữa các trạm trung gian.

#### **Câu 174:** Giao thức LDAP (Lightweight Directory Access Protocol) thường được ứng dụng để làm gì?  
**A. Truy vấn và xác thực tài khoản người dùng tập trung trong các tổ chức doanh nghiệp**  
B. Truyền video trực tiếp  
C. Định tuyến IP  
D. Quét virus  
* **Giải thích:** LDAP chạy ở tầng ứng dụng (cổng 389) để tra cứu danh bạ người dùng và phân quyền tập trung.

#### **Câu 175:** Khi người dùng gõ URL vào trình duyệt, tiến trình nào bắt buộc phải hoàn thành trước khi gửi HTTP Request?  
**A. Phân giải tên miền qua DNS để lấy địa chỉ IP của Web Server**  
B. Gửi email thông báo  
C. Đổi mật khẩu máy tính  
D. Quét đĩa cứng  
* **Giải thích:** Trình duyệt bắt buộc phải có địa chỉ IP từ DNS mới có thể khởi tạo kết nối TCP tới server.

#### **Câu 176:** Giao thức nào sau đây chạy ở tầng ứng dụng để truyền tải file siêu văn bản có hỗ trợ liên kết?  
**A. HTTP**  
B. FTP  
C. SNMP  
D. DNS  
* **Giải thích:** HTTP là nền tảng của World Wide Web hỗ trợ truyền văn bản và các tài nguyên đa phương tiện liên kết.

#### **Câu 177:** Kỹ thuật 'Pipelining' trong HTTP/1.1 cho phép client:  
**A. Gửi liên tiếp nhiều HTTP Request mà không cần chờ phản hồi của từng request trước đó**  
B. Mở 100 kết nối TCP cùng lúc  
C. Tải video bằng UDP  
D. Xóa cookie tự động  
* **Giải thích:** Pipelining cho phép gửi gối đầu các yêu cầu để tối ưu hóa thời gian chờ phản hồi.

#### **Câu 178:** Vì sao kỹ thuật Pipelining trong HTTP/1.1 ít được các trình duyệt bật mặc định?  
**A. Do vấn đề nghẽn đầu hàng (HOL blocking) ở tầng ứng dụng và khả năng tương thích kém của một số proxy**  
B. Do tốn quá nhiều điện  
C. Do cáp quang không hỗ trợ  
D. Do vi phạm bản quyền  
* **Giải thích:** Nếu request đầu bị chậm, toàn bộ chuỗi response phía sau đều bị nghẽn lại.

#### **Câu 179:** Trong HTTP/2, cơ chế 'Server Push' cho phép máy chủ làm gì?  
**A. Chủ động gửi các tài nguyên phụ (như CSS, JavaScript) cho client trước khi client gửi yêu cầu**  
B. Tự động cài phần mềm vào máy client  
C. Xóa lịch sử duyệt web  
D. Gửi tin nhắn rác  
* **Giải thích:** Server đoán trước client cần gì sau khi tải HTML để đẩy sớm, giúp trang web load nhanh hơn.

#### **Câu 180:** Trong mô hình P2P BitTorrent, tệp tin .torrent chứa nội dung gì?  
**A. Địa chỉ URL của Tracker và mã băm SHA-1 của tất cả các mảnh (chunks) trong tệp**  
B. Toàn bộ nội dung tệp video  
C. Mật khẩu máy tính  
D. Địa chỉ MAC của người tạo  
* **Giải thích:** Tệp .torrent chỉ là metadata hướng dẫn client tìm tracker và kiểm tra tính toàn vẹn của từng mảnh tải về.

#### **Câu 181:** Độ tin cậy của các mảnh tải về trong BitTorrent được kiểm tra bằng cách nào?  
**A. So sánh mã băm SHA-1 của mảnh tải về với mã băm chuẩn lưu trong tệp .torrent**  
B. Nhờ router kiểm tra  
C. Hỏi lại seeder  
D. Đếm số byte  
* **Giải thích:** Nếu mã băm khớp, mảnh đó đảm bảo vẹn toàn không bị lỗi hoặc bị chỉnh sửa ác ý.

#### **Câu 182:** Trong BitTorrent, 'DHT (Distributed Hash Table)' được sử dụng để làm gì?  
**A. Cho phép mạng P2P hoạt động hoàn toàn không cần máy chủ Tracker tập trung (Trackerless torrent)**  
B. Tăng tốc độ tải lên  
C. Khóa tệp bản quyền  
D. Xóa các máy dùng wifi  
* **Giải thích:** DHT biến chính các peer thành một mạng phân tán tìm kiếm lẫn nhau thông qua giao thức Kademlia.

#### **Câu 183:** Khi người dùng xem video trên YouTube bằng DASH, nếu mạng đột ngột bị chậm, hiện tượng gì sẽ xảy ra?  
**A. Video tự động hạ độ phân giải xuống mức bitrate thấp hơn để xem mượt mà không bị dừng hình**  
B. Trình duyệt tự động đóng lại  
C. Video tự xóa  
D. Máy tính phát tiếng kêu  
* **Giải thích:** DASH thích ứng linh hoạt: chọn đoạn tiếp theo ở độ phân giải thấp hơn để duy trì phát liên tục.

#### **Câu 184:** CDN sử dụng kỹ thuật 'Anycast DNS' nhằm mục đích gì?  
**A. Nhiều máy chủ DNS ở các châu lục cùng dùng 1 IP để router tự dẫn người dùng tới máy gần nhất theo bảng định tuyến BGP**  
B. Làm cho website nhanh hơn cáp quang  
C. Bảo mật chống hack  
D. Tiết kiệm tên miền  
* **Giải thích:** Anycast định tuyến gói tin tới cụm server DNS gần nhất theo khoảng cách mạng.

#### **Câu 185:** Trong kiến trúc Web Cache, mã 'ETag (Entity Tag)' là gì?  
**A. Một chuỗi định danh duy nhất (thường là mã băm nội dung) đại diện cho một phiên bản cụ thể của tệp tin**  
B. Địa chỉ IP của proxy  
C. Tên của tác giả  
D. Ngày hết hạn cookie  
* **Giải thích:** Client dùng header `If-None-Match: <ETag>` để kiểm tra xem nội dung tệp có thực sự đổi hay chưa.

#### **Câu 186:** Một trang web gồm 1 HTML và 3 ảnh. Nếu dùng Persistent HTTP có Pipelining, thời gian tải trọn vẹn là:  
**A. 3 RTT**  
B. 10 RTT  
C. 1 RTT  
D. 12 RTT  
* **Giải thích:** 1 RTT bắt tay TCP + 1 RTT tải HTML + 1 RTT gửi đồng loạt request và nhận cả 3 ảnh = 3 RTT.

#### **Câu 187:** Phương thức HTTP nào được dùng để kiểm tra các tùy chọn giao tiếp mà máy chủ hỗ trợ?  
**A. OPTIONS**  
B. TRACE  
C. CONNECT  
D. HEAD  
* **Giải thích:** OPTIONS trả về danh sách các HTTP methods mà server cho phép thực thi trên URL đó.

#### **Câu 188:** Phương thức HTTP TRACE được thiết kế cho mục đích gì?  
**A. Thực hiện vòng lặp phản hồi (echo) để kiểm tra những gì trung gian (proxy) đã sửa đổi trên request**  
B. Tải dữ liệu lớn  
C. Xóa tài nguyên  
D. Mã hóa mật khẩu  
* **Giải thích:** TRACE phản hồi lại nguyên trạng request nhận được để phục vụ gỡ lỗi mạng.

#### **Câu 189:** Trong HTTP Request, dòng đầu tiên bao gồm 3 trường thông tin theo thứ tự là:  
**A. Phương thức (Method), Đường dẫn (URL/URI), Phiên bản giao thức (Version)**  
B. Phiên bản, Mã trạng thái, Cụm từ  
C. Host, URL, Port  
D. Header, Body, Trailer  
* **Giải thích:** Ví dụ: `GET /index.html HTTP/1.1`.

#### **Câu 190:** Trong HTTP Response, dòng đầu tiên (Status Line) bao gồm các trường thông tin là:  
**A. Phiên bản giao thức, Mã trạng thái (Status Code), Cụm từ mô tả (Reason Phrase)**  
B. Phương thức, URL, Ngày tháng  
C. Host, IP, Port  
D. Tên Server, Mã lỗi, Kích thước  
* **Giải thích:** Ví dụ: `HTTP/1.1 200 OK`.

#### **Câu 191:** Trường header `Referer` trong HTTP Request cho máy chủ biết điều gì?  
**A. Địa chỉ URL của trang web chứa liên kết dẫn người dùng đến trang hiện tại**  
B. Địa chỉ MAC của router  
C. Tên nhà mạng ISP  
D. Số lần nhấp chuột  
* **Giải thích:** Referer dùng để phân tích lưu lượng nguồn truy cập và thống kê người dùng.

#### **Câu 192:** Cơ chế 'Same-Origin Policy' trên trình duyệt web ngăn chặn điều gì?  
**A. Ngăn chặn mã JavaScript của một trang web độc hại truy cập vào cookie và dữ liệu của trang web khác**  
B. Ngăn tải video  
C. Ngăn chặn kết nối wifi  
D. Ngăn người dùng mở nhiều tab  
* **Giải thích:** Chính sách cùng nguồn gốc là tường thành bảo mật cốt lõi bảo vệ phiên làm việc của người dùng trên Web.

#### **Câu 193:** CORS (Cross-Origin Resource Sharing) trong kiến trúc Web dùng để:  
**A. Cho phép máy chủ khai báo những nguồn (origin) bên ngoài nào được phép truy cập tài nguyên của nó qua JavaScript**  
B. Tăng tốc mạng cáp quang  
C. Đổi địa chỉ IP  
D. Mã hóa ổ cứng  
* **Giải thích:** CORS sử dụng các HTTP header đặc thù để nới lỏng chính sách Same-Origin một cách có kiểm soát.

#### **Câu 194:** Trong phiên SMTP, mã phản hồi 250 từ máy chủ có nghĩa là:  
**A. Hành động yêu cầu đã hoàn tất thành công (Requested mail action okay/completed)**  
B. Lỗi xác thực  
C. Hộp thư không tồn tại  
D. Đang bận  
* **Giải thích:** Mã 250 là phản hồi thành công chuẩn cho các lệnh HELO, MAIL FROM, RCPT TO trong SMTP.

#### **Câu 195:** Trong phiên SMTP, mã phản hồi 354 sau lệnh DATA có nghĩa là:  
**A. Bắt đầu nhập nội dung thư, kết thúc bằng CRLF.CRLF**  
B. Lỗi cú pháp  
C. Đóng kết nối  
D. Thư bị từ chối  
* **Giải thích:** Mã 354 cho phép client bắt đầu truyền các dòng tiêu đề và nội dung của thông điệp.

#### **Câu 196:** Tấn công 'Open Mail Relay' xảy ra khi:  
**A. Mail Server được cấu hình lỏng lẻo cho phép bất kỳ ai từ bên ngoài gửi thư chuyển tiếp tới bất kỳ đâu mà không xác thực**  
B. Server bị mất kết nối  
C. Email bị quá tải  
D. Người dùng quên mật khẩu  
* **Giải thích:** Hacker thường lợi dụng các Open Relay để phát tán hàng triệu thư rác (spam) ẩn danh.

#### **Câu 197:** Giao thức DNS sử dụng cổng TCP 53 trong trường hợp nào?  
**A. Zone Transfer giữa các DNS Server và khi phản hồi dữ liệu truy vấn vượt quá 512 bytes**  
B. Tất cả các truy vấn thông thường  
C. Khi xem video  
D. Không bao giờ dùng TCP  
* **Giải thích:** DNS tự động chuyển sang TCP khi gói UDP bị cắt cụt (cờ Truncation TC=1) hoặc đồng bộ dữ liệu lớn.

#### **Câu 198:** Trong DNS, cờ 'AA (Authoritative Answer)' trong thông điệp phản hồi cho biết:  
**A. Câu trả lời được gửi từ chính máy chủ thẩm quyền quản lý tên miền đó chứ không phải từ bộ nhớ đệm**  
B. Câu trả lời bị sai  
C. Tên miền đã hết hạn  
D. Bị tấn công  
* **Giải thích:** Cờ AA xác nhận tính chính thống và tin cậy cao nhất của thông tin phân giải.

#### **Câu 199:** Tấn công 'Kaminsky Attack' trong lịch sử mạng nhắm vào lỗ hổng của dịch vụ nào?  
**A. DNS Cache Poisoning đánh lừa Local DNS server bằng Transaction ID giả mạo**  
B. HTTP Web Server  
C. SMTP Mail Server  
D. DHCP Server  
* **Giải thích:** Lỗ hổng Dan Kaminsky cho phép kẻ tấn công đầu độc toàn bộ bộ nhớ đệm DNS chỉ trong vài giây.

#### **Câu 200:** Để phòng chống giả mạo bản ghi DNS toàn cầu, chuẩn bảo mật mở rộng nào được triển khai?  
**A. DNSSEC (DNS Security Extensions) sử dụng chữ ký số mật mã**  
B. SSL  
C. WPA2  
D. NAT  
* **Giải thích:** DNSSEC sử dụng hệ thống chứng thực chữ ký số công khai để đảm bảo tính toàn vẹn và xác thực nguồn gốc bản ghi DNS.

## PHẦN 3: CHUYÊN ĐỀ ĐỊA CHỈ IP – IPV4, SUBNETTING, CIDR & IPV6 (CÂU 201 – 300)

#### **Câu 201:** Địa chỉ IPv4 có độ dài bao nhiêu bit?  
A. 16 bit  
**B. 32 bit**  
C. 48 bit  
D. 128 bit  
* **Giải thích:** IPv4 gồm 32 bit nhị phân, chia thành 4 octet số thập phân cách nhau dấu chấm.

#### **Câu 202:** Tiêu đề chuẩn của một gói tin IPv4 khi không có tùy chọn (Options) có kích thước là:  
**A. 20 bytes**  
B. 40 bytes  
C. 64 bytes  
D. 32 bytes  
* **Giải thích:** Header IPv4 mặc định có kích thước tối thiểu là 20 bytes.

#### **Câu 203:** Trường Header Checksum trong tiêu đề gói tin IPv4 có nhiệm vụ kiểm tra lỗi cho:  
A. Toàn bộ gói tin (cả Header và Payload)  
**B. Chỉ riêng phần tiêu đề Header của gói tin**  
C. Chỉ phần Payload  
D. Cả tầng giao vận  
* **Giải thích:** Checksum của IPv4 chỉ kiểm tra phần Header; phần payload do tầng giao vận (TCP/UDP) kiểm tra.

#### **Câu 204:** Tại sao trường Header Checksum trong IPv4 bắt buộc phải được tính lại tại mỗi router chuyển tiếp?  
**A. Do trường Time-To-Live (TTL) bị giảm đi 1 tại mỗi router**  
B. Do địa chỉ IP đích thay đổi  
C. Do kích thước dữ liệu bị co lại  
D. Do số port bị đổi  
* **Giải thích:** Mỗi khi TTL giảm, nội dung của 20 byte header thay đổi, buộc router phải tính lại checksum.

#### **Câu 205:** Trường Time-To-Live (TTL) trong tiêu đề IPv4 có mục đích chính là:  
A. Đo thời gian truyền gói  
**B. Ngăn ngừa gói tin bị lặp vòng vô tận trên mạng bằng cách giới hạn số chặng router đi qua**  
C. Định danh gói tin  
D. Kiểm tra mật khẩu  
* **Giải thích:** TTL giảm 1 qua mỗi router; khi TTL = 0, gói tin bị hủy và router gửi thông điệp ICMP Time Exceeded về nguồn.

#### **Câu 206:** Trong tiêu đề IPv4, trường 'Protocol' mang giá trị bằng 6 chỉ thị dữ liệu bên trong thuộc giao thức nào?  
A. UDP  
**B. TCP**  
C. ICMP  
D. OSPF  
* **Giải thích:** Protocol = 6 chỉ thị TCP; Protocol = 17 chỉ thị UDP; Protocol = 1 chỉ thị ICMP.

#### **Câu 207:** Trong tiêu đề IPv4, trường 'Protocol' mang giá trị bằng 17 chỉ thị dữ liệu bên trong thuộc giao thức nào?  
A. TCP  
**B. UDP**  
C. IGMP  
D. BGP  
* **Giải thích:** Giá trị 17 là mã định danh chuẩn của giao thức giao vận phi kết nối UDP.

#### **Câu 208:** Phân mảnh gói tin (Fragmentation) trong IPv4 xảy ra khi:  
**A. Datagram có kích thước lớn hơn đơn vị truyền cực đại (MTU) của liên kết đường truyền đi ra**  
B. Router bị mất điện  
C. Mạng bị nghẽn  
D. Gói tin truyền bằng wifi  
* **Giải thích:** Nếu kích thước gói vượt quá MTU (như MTU của Ethernet là 1500 bytes), router bắt buộc phải chia nhỏ gói tin.

#### **Câu 209:** Quá trình tái hợp (Reassembly) các mảnh của gói tin IPv4 bị phân mảnh được thực hiện ở đâu?  
A. Tại router kế tiếp  
B. Tại router biên  
**C. Chỉ tại hệ thống đầu cuối nhận (Destination Host)**  
D. Tại switch mạng LAN  
* **Giải thích:** Router chỉ phân mảnh; việc ghép lại toàn bộ các mảnh thành datagram gốc chỉ diễn ra tại máy đích cuối cùng.

#### **Câu 210:** Trường 'Identification' (16 bit) trong tiêu đề IPv4 có vai trò gì trong phân mảnh?  
**A. Gán mã số nhận dạng giống hệt nhau cho tất cả các mảnh xuất phát từ cùng một datagram ban đầu**  
B. Đo thời gian truyền  
C. Đánh số cổng  
D. Chứa mật khẩu  
* **Giải thích:** Máy đích dựa vào trường Identification và địa chỉ nguồn để gom đúng các mảnh thuộc cùng một gói tin.

#### **Câu 211:** Cờ 'More Fragments (MF)' trong tiêu đề IPv4 mang giá trị bằng 0 có nghĩa là:  
A. Phía sau vẫn còn các mảnh tiếp theo  
**B. Đây là mảnh cuối cùng của datagram (hoặc gói tin không bị phân mảnh)**  
C. Gói tin bị lỗi  
D. Gói tin truyền bằng TCP  
* **Giải thích:** MF = 1 báo hiệu còn mảnh phía sau; MF = 0 báo hiệu đây là mảnh kết thúc.

#### **Câu 212:** Trường 'Fragment Offset' (13 bit) trong tiêu đề IPv4 được tính theo đơn vị khối bao nhiêu byte?  
A. 1 byte  
B. 4 bytes  
**C. 8 bytes**  
D. 16 bytes  
* **Giải thích:** Offset đo vị trí bắt đầu của dữ liệu mảnh trong gói gốc theo đơn vị khối 8-byte (Offset = Byte_start / 8).

#### **Câu 213:** Một gói tin IPv4 dài 4000 bytes (header 20 bytes) qua liên kết MTU = 1500 bytes. Mảnh thứ nhất mang lượng dữ liệu là:  
A. 1500 bytes  
**B. 1480 bytes**  
C. 1400 bytes  
D. 1000 bytes  
* **Giải thích:** Payload tối đa mỗi mảnh = MTU - Header = 1500 - 20 = 1480 bytes (chia hết cho 8).

#### **Câu 214:** Giá trị Fragment Offset của mảnh thứ nhất luôn luôn bằng:  
**A. 0**  
B. 1  
C. 185  
D. 1480  
* **Giải thích:** Mảnh đầu tiên chứa các byte dữ liệu bắt đầu từ vị trí 0 nên Offset = 0 / 8 = 0.

#### **Câu 215:** Mảnh thứ hai mang dữ liệu từ byte 1480 đến 2959. Giá trị trường Fragment Offset của mảnh thứ hai là:  
**A. 185**  
B. 1480  
C. 370  
D. 0  
* **Giải thích:** Offset = 1480 / 8 = 185.

#### **Câu 216:** Mảnh thứ ba mang dữ liệu từ byte 2960 đến 3979. Giá trị trường Fragment Offset của mảnh thứ ba là:  
A. 185  
**B. 370**  
C. 2960  
D. 495  
* **Giải thích:** Offset = 2960 / 8 = 370.

#### **Câu 217:** Trong kiến trúc CIDR, ký hiệu `/prefix` biểu thị điều gì?  
A. Số lượng máy chủ trong mạng  
**B. Số bit thuộc phần mạng (Network portion) tính từ trái sang phải**  
C. Số lượng router  
D. Chỉ số phiên bản  
* **Giải thích:** Prefix chỉ định độ dài chuỗi bit 1 liên tục trong Subnet Mask đại diện cho phần mạng.

#### **Câu 218:** Subnet Mask chuẩn của một mạng có tiền tố `/24` là:  
A. 255.0.0.0  
B. 255.255.0.0  
**C. 255.255.255.0**  
D. 255.255.255.255  
* **Giải thích:** 24 bit 1 liên tiếp = 8 bit + 8 bit + 8 bit + 0 bit = 255.255.255.0.

#### **Câu 219:** Subnet Mask chuẩn tương ứng với tiền tố `/26` là:  
A. 255.255.255.128  
**B. 255.255.255.192**  
C. 255.255.255.224  
D. 255.255.255.240  
* **Giải thích:** Octet cuối có 2 bit 1: 128 + 64 = 192 -> 255.255.255.192.

#### **Câu 220:** Subnet Mask chuẩn tương ứng với tiền tố `/27` là:  
A. 255.255.255.192  
**B. 255.255.255.224**  
C. 255.255.255.240  
D. 255.255.255.248  
* **Giải thích:** Octet cuối có 3 bit 1: 128 + 64 + 32 = 224 -> 255.255.255.224.

#### **Câu 221:** Subnet Mask chuẩn tương ứng với tiền tố `/28` là:  
A. 255.255.255.224  
**B. 255.255.255.240**  
C. 255.255.255.248  
D. 255.255.255.252  
* **Giải thích:** Octet cuối có 4 bit 1: 128 + 64 + 32 + 16 = 240 -> 255.255.255.240.

#### **Câu 222:** Subnet Mask chuẩn tương ứng với tiền tố `/30` là:  
A. 255.255.255.248  
**B. 255.255.255.252**  
C. 255.255.255.254  
D. 255.255.255.255  
* **Giải thích:** Octet cuối có 6 bit 1: 256 - 4 = 252 -> 255.255.255.252.

#### **Câu 223:** Công thức tính số lượng địa chỉ gán được cho host trong khối mạng có h bit host là:  
A. 2^h  
**B. 2^h - 2**  
C. 2^(32-h)  
D. 2^h - 1  
* **Giải thích:** Luôn trừ 2 địa chỉ dành riêng: Địa chỉ Mạng (toàn bit 0) và Địa chỉ Broadcast (toàn bit 1).

#### **Câu 224:** Một mạng con có tiền tố `/25` có thể cấp phát tối đa cho bao nhiêu host?  
A. 128 host  
**B. 126 host**  
C. 62 host  
D. 254 host  
* **Giải thích:** Số bit host h = 32 - 25 = 7. Số host = 2^7 - 2 = 128 - 2 = 126 host.

#### **Câu 225:** Một mạng con có tiền tố `/26` có thể cấp phát tối đa cho bao nhiêu host?  
A. 64 host  
**B. 62 host**  
C. 30 host  
D. 14 host  
* **Giải thích:** h = 32 - 26 = 6. Số host = 2^6 - 2 = 64 - 2 = 62 host.

#### **Câu 226:** Một mạng con có tiền tố `/27` có thể cấp phát tối đa cho bao nhiêu host?  
A. 32 host  
**B. 30 host**  
C. 16 host  
D. 14 host  
* **Giải thích:** h = 32 - 27 = 5. Số host = 2^5 - 2 = 32 - 2 = 30 host.

#### **Câu 227:** Một mạng con có tiền tố `/28` có thể cấp phát tối đa cho bao nhiêu host?  
A. 16 host  
**B. 14 host**  
C. 8 host  
D. 6 host  
* **Giải thích:** h = 32 - 28 = 4. Số host = 2^4 - 2 = 16 - 2 = 14 host.

#### **Câu 228:** Một mạng con có tiền tố `/29` có thể cấp phát tối đa cho bao nhiêu host?  
A. 8 host  
**B. 6 host**  
C. 4 host  
D. 2 host  
* **Giải thích:** h = 32 - 29 = 3. Số host = 2^3 - 2 = 8 - 2 = 6 host.

#### **Câu 229:** Tiền tố `/30` thường được dùng chuyên biệt cho kết nối nào?  
A. Mạng LAN văn phòng  
**B. Liên kết điểm-điểm (Point-to-Point) giữa 2 router trên đường WAN**  
C. Mạng Wifi công cộng  
D. Mạng máy chủ dữ liệu lớn  
* **Giải thích:** Khối /30 có đúng 2 host dùng được (2^2 - 2 = 2), vừa đủ cho 2 đầu router mà không lãng phí địa chỉ.

#### **Câu 230:** Cần cấp phát IP cho mạng có 50 máy tính, tiền tố CIDR tiết kiệm và phù hợp nhất là:  
A. /25  
**B. /26**  
C. /27  
D. /24  
* **Giải thích:** 2^h - 2 >= 50 -> h = 6 (2^6 - 2 = 62 host). Prefix = 32 - 6 = /26.

#### **Câu 231:** Cần cấp phát IP cho mạng có 100 máy tính, tiền tố CIDR phù hợp nhất là:  
A. /24  
**B. /25**  
C. /26  
D. /27  
* **Giải thích:** 2^h - 2 >= 100 -> h = 7 (2^7 - 2 = 126 host). Prefix = 32 - 7 = /25.

#### **Câu 232:** Cần cấp phát IP cho mạng có 12 máy tính, tiền tố CIDR phù hợp nhất là:  
A. /27  
**B. /28**  
C. /29  
D. /30  
* **Giải thích:** 2^h - 2 >= 12 -> h = 4 (2^4 - 2 = 14 host). Prefix = 32 - 4 = /28.

#### **Câu 233:** Dải địa chỉ nào sau đây thuộc không gian mạng riêng (Private IP) Lớp A theo RFC 1918?  
**A. 10.0.0.0/8**  
B. 172.16.0.0/12  
C. 192.168.0.0/16  
D. 169.254.0.0/16  
* **Giải thích:** RFC 1918 quy định Lớp A Private là 10.0.0.0 đến 10.255.255.255 (tiền tố /8).

#### **Câu 234:** Dải địa chỉ nào sau đây thuộc không gian mạng riêng (Private IP) Lớp B theo RFC 1918?  
**A. 172.16.0.0 đến 172.31.255.255 (/12)**  
B. 172.0.0.0/8  
C. 172.32.0.0/16  
D. 172.16.0.0/16  
* **Giải thích:** Lớp B Private trải dài từ 172.16.0.0 đến 172.31.255.255 (gồm 16 mạng /16, tiền tố /12).

#### **Câu 235:** Dải địa chỉ nào sau đây thuộc không gian mạng riêng (Private IP) Lớp C theo RFC 1918?  
**A. 192.168.0.0 đến 192.168.255.255 (/16)**  
B. 192.169.0.0/16  
C. 192.0.0.0/8  
D. 192.168.1.0/24  
* **Giải thích:** Lớp C Private bao gồm toàn bộ không gian 192.168.0.0/16.

#### **Câu 236:** Địa chỉ IP nào sau đây là địa chỉ Public có thể định tuyến trên Internet toàn cầu?  
A. 10.1.2.3  
B. 172.20.10.5  
C. 192.168.100.1  
**D. 8.8.8.8**  
* **Giải thích:** 8.8.8.8 là IP Public của Google DNS; các địa chỉ còn lại đều thuộc RFC 1918 Private IP.

#### **Câu 237:** Địa chỉ IPv4 `127.0.0.1` thuộc dải nào và dùng cho mục đích gì?  
A. Dải Private IP  
**B. Dải Loopback (127.0.0.0/8) dùng để kiểm thử phần mềm trên chính máy cục bộ**  
C. Dải Multicast  
D. Dải Broadcast  
* **Giải thích:** Mọi gói gửi đến 127.0.0.0/8 đều được phần mềm mạng cuộn ngược lại localhost mà không phát ra ngoài.

#### **Câu 238:** Dải địa chỉ `169.254.0.0/16` trong IPv4 được gọi là:  
**A. APIPA (Automatic Private IP Addressing) / Link-Local**  
B. Loopback  
C. Public IP  
D. Class D Multicast  
* **Giải thích:** Hệ điều hành tự gán địa chỉ thuộc dải này khi card mạng bật DHCP nhưng không tìm thấy DHCP Server.

#### **Câu 239:** Dải địa chỉ IPv4 Lớp D (224.0.0.0 đến 239.255.255.255) được dành riêng cho:  
A. Thử nghiệm  
**B. Định tuyến Multicast**  
C. Gán cho máy trạm thông thường  
D. Kết nối WAN  
* **Giải thích:** Lớp D dùng riêng cho truyền thông một-nhiều (Multicasting).

#### **Câu 240:** Địa chỉ `255.255.255.255` là địa chỉ:  
**A. Limited Broadcast (Quảng bá giới hạn trong mạng LAN cục bộ)**  
B. Loopback  
C. Mạng toàn cầu  
D. Default Gateway  
* **Giải thích:** Gói gửi đến 255.255.255.255 được chuyển đến tất cả host trong cùng mạng LAN và bị router chặn lại.

#### **Câu 241:** Địa chỉ `0.0.0.0` trong IPv4 biểu thị điều gì khi host gửi DHCP Discover?  
A. Địa chỉ Loopback  
**B. Chưa có địa chỉ IP xác định (This host on this network)**  
C. Địa chỉ của router  
D. Địa chỉ broadcast  
* **Giải thích:** Khi chưa được cấp IP, máy dùng 0.0.0.0 làm Source IP tạm thời để xin cấp phát.

#### **Câu 242:** Cho host `192.168.1.70/26`. Địa chỉ mạng chứa host này là:  
A. 192.168.1.0  
**B. 192.168.1.64**  
C. 192.168.1.128  
D. 192.168.1.32  
* **Giải thích:** Bước nhảy /26 là 64. Các mạng: .0, .64, .128. Số 70 nằm trong dải .64 đến .127 nên mạng là 192.168.1.64.

#### **Câu 243:** Địa chỉ Broadcast của mạng con chứa host `192.168.1.70/26` là:  
A. 192.168.1.63  
**B. 192.168.1.127**  
C. 192.168.1.255  
D. 192.168.1.191  
* **Giải thích:** Mạng bắt đầu tại .64 và bước nhảy 64 -> Broadcast là 64 + 64 - 1 = 127.

#### **Câu 244:** Dải địa chỉ IP hợp lệ có thể gán cho host trong mạng `192.168.1.64/26` là:  
A. 192.168.1.64 đến 192.168.1.127  
**B. 192.168.1.65 đến 192.168.1.126**  
C. 192.168.1.65 đến 192.168.1.127  
D. 192.168.1.1 đến 192.168.1.62  
* **Giải thích:** Bỏ qua địa chỉ mạng (.64) và địa chỉ broadcast (.127), dải host là .65 đến .126.

#### **Câu 245:** Cho host `10.0.5.140/27`. Địa chỉ mạng của host này là:  
**A. 10.0.5.128**  
B. 10.0.5.96  
C. 10.0.5.140  
D. 10.0.5.0  
* **Giải thích:** Bước nhảy /27 là 32. Các mạng: .0, .32, .64, .96, .128, .160. Host .140 nằm giữa 128 và 159 nên mạng là 10.0.5.128.

#### **Câu 246:** Địa chỉ Broadcast của mạng `10.0.5.128/27` là:  
**A. 10.0.5.159**  
B. 10.0.5.160  
C. 10.0.5.255  
D. 10.0.5.143  
* **Giải thích:** Broadcast = 128 + 32 - 1 = 159.

#### **Câu 247:** Cho host `172.16.10.25/28`. Địa chỉ mạng là:  
A. 172.16.10.0  
**B. 172.16.10.16**  
C. 172.16.10.32  
D. 172.16.10.24  
* **Giải thích:** Bước nhảy /28 là 16. Các mạng: .0, .16, .32. Host .25 nằm trong dải .16 đến .31 nên mạng là 172.16.10.16.

#### **Câu 248:** Địa chỉ Broadcast của mạng `172.16.10.16/28` là:  
**A. 172.16.10.31**  
B. 172.16.10.32  
C. 172.16.10.15  
D. 172.16.10.63  
* **Giải thích:** Broadcast = 16 + 16 - 1 = 31.

#### **Câu 249:** Trong kỹ thuật VLSM, nguyên tắc bắt buộc khi phân bổ là:  
**A. Sắp xếp danh sách mạng theo nhu cầu số host giảm dần và cấp phát cho mạng lớn nhất trước**  
B. Cấp cho mạng nhỏ nhất trước  
C. Cấp ngẫu nhiên  
D. Chia tất cả các mạng theo cùng 1 mask  
* **Giải thích:** Cấp mạng lớn trước đảm bảo các ranh giới nhị phân khớp chuẩn, chống phân mảnh và tránh trùng lấn địa chỉ.

#### **Câu 250:** Kỹ thuật Route Aggregation (Supernetting) thực hiện việc gì?  
**A. Gom nhiều tuyến mạng con liền kề có chung tiền tố thành một mục định tuyến duy nhất**  
B. Chia nhỏ mạng  
C. Đổi IPv4 sang IPv6  
D. Tăng số lượng host  
* **Giải thích:** Giúp thu gọn bảng định tuyến của các router vùng lõi, giảm tải bộ nhớ và tăng tốc xử lý gói tin.

#### **Câu 251:** Địa chỉ IPv6 có độ dài bao nhiêu bit?  
A. 32 bit  
B. 64 bit  
**C. 128 bit**  
D. 256 bit  
* **Giải thích:** IPv6 dài đúng 128 bit, cung cấp không gian địa chỉ khổng lồ 2^128.

#### **Câu 252:** Một địa chỉ IPv6 được biểu diễn bằng bao nhiêu nhóm số Hexadecimal?  
A. 4 nhóm  
B. 6 nhóm  
**C. 8 nhóm (mỗi nhóm 16 bit cách nhau dấu hai chấm ':')**  
D. 16 nhóm  
* **Giải thích:** Định dạng chuẩn: xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx:xxxx.

#### **Câu 253:** Kích thước tiêu đề (Header) cố định của gói tin IPv6 là bao nhiêu byte?  
A. 20 bytes  
B. 32 bytes  
**C. 40 bytes**  
D. 64 bytes  
* **Giải thích:** Tiêu đề IPv6 được thiết kế cố định 40 bytes để router xử lý cực nhanh và loại bỏ trường Options lộn xộn.

#### **Câu 254:** Trường nào sau đây có trong tiêu đề IPv4 nhưng BỊ BÃI BỎ HOÀN TOÀN trong tiêu đề IPv6?  
**A. Header Checksum**  
B. Source Address  
C. Destination Address  
D. Payload Length  
* **Giải thích:** IPv6 bỏ Header Checksum để giảm tải tính toán cho router; việc kiểm tra lỗi giao cho Tầng 2 và Tầng 4.

#### **Câu 255:** Cơ chế phân mảnh gói tin tại router trung gian trong IPv6 được xử lý như thế nào?  
A. Router tiếp tục phân mảnh như IPv4  
**B. Router không được phép phân mảnh; router hủy gói và gửi ICMPv6 Packet Too Big để máy gửi tự giảm kích thước**  
C. IPv6 cấm gửi gói tin lớn hơn 100 bytes  
D. Gói tin tự động nén lại  
* **Giải thích:** Chỉ có máy gửi (Source Host) mới được phân mảnh gói tin trong IPv6 thông qua Path MTU Discovery.

#### **Câu 256:** Hình thức truyền thông nào sau đây đã bị BÃI BỎ HOÀN TOÀN trong kiến trúc IPv6?  
A. Unicast  
B. Multicast  
**C. Broadcast**  
D. Anycast  
* **Giải thích:** IPv6 không còn khái niệm Broadcast; mọi tác vụ gửi tin đại trà được thay thế bằng Multicast hiệu quả hơn.

#### **Câu 257:** Loại địa chỉ nào trong IPv6 gửi gói tin tới giao diện mạng gần nhất (theo bảng định tuyến) trong một nhóm?  
A. Unicast  
B. Multicast  
**C. Anycast**  
D. Broadcast  
* **Giải thích:** Anycast gửi tới nút gần nhất trong nhóm cùng chia sẻ địa chỉ (thường dùng cho cụm DNS root/CDN).

#### **Câu 258:** Địa chỉ Loopback chuẩn trong mạng IPv6 được viết rút gọn là:  
**A. ::1**  
B. ::  
C. fe80::1  
D. ff02::1  
* **Giải thích:** Loopback IPv6 gồm 127 bit 0 và 1 bit 1 cuối cùng, viết nén là `::1` (tương đương 127.0.0.1 của IPv4).

#### **Câu 259:** Địa chỉ 'Unspecified Address' (toàn bộ 128 bit bằng 0) trong IPv6 được viết rút gọn là:  
A. ::1  
**B. ::**  
C. 0::0  
D. fe80::  
* **Giải thích:** Địa chỉ `::` đại diện cho việc host chưa có địa chỉ (tương đương 0.0.0.0 của IPv4).

#### **Câu 260:** Quy tắc rút gọn số 0 ở đầu mỗi nhóm Hexadecimal trong IPv6 cho phép viết `:00ab:` thành:  
**A. :ab:**  
B. :a0b0:  
C. :b:  
D. :0000:  
* **Giải thích:** Các số 0 dẫn đầu (leading zeros) trong mỗi nhóm 4 ký tự Hex có thể bỏ đi, ví dụ 00ab thành ab.

#### **Câu 261:** Quy tắc nén chuỗi nhóm số 0 liên tiếp bằng dấu `::` trong một địa chỉ IPv6 được áp dụng tối đa bao nhiêu lần?  
**A. Duy nhất 1 lần**  
B. Tối đa 2 lần  
C. Tùy ý không giới hạn  
D. 3 lần  
* **Giải thích:** Dấu `::` chỉ được xuất hiện DUY NHẤT 1 LẦN để đảm bảo tính xác định khi phục hồi lại đủ 8 nhóm.

#### **Câu 262:** Nếu một địa chỉ IPv6 có 2 cụm số 0 liên tiếp dài bằng nhau, quy tắc chuẩn (RFC 5952) ưu tiên đặt `::` ở đâu?  
**A. Ở cụm số 0 đầu tiên xuất hiện từ trái sang phải**  
B. Ở cụm cuối cùng  
C. Không được đặt  
D. Tùy ý  
* **Giải thích:** RFC 5952 quy định nén cụm đầu tiên nếu độ dài chuỗi số 0 bằng nhau.

#### **Câu 263:** Rút gọn chính xác địa chỉ `2001:0db8:0000:0000:0000:0000:1428:57ab` là:  
**A. 2001:db8::1428:57ab**  
B. 2001:db8:0:0:0:0:1428:57ab  
C. 2001:db8::0::1428:57ab  
D. 2001:0db8::1428:57ab  
* **Giải thích:** Bỏ số 0 đầu ở 0db8 thành db8, nén 4 nhóm 0000 thành `::`.

#### **Câu 264:** Rút gọn chính xác địa chỉ `fe80:0000:0000:0000:0000:0000:0000:0001` là:  
**A. fe80::1**  
B. fe80:0:0:0:0:0:0:1  
C. fe80::0001  
D. fe80:0::1  
* **Giải thích:** Bỏ các số 0 đầu nhóm cuối thành 1, nén 7 nhóm số 0 ở giữa thành `::`.

#### **Câu 265:** Rút gọn chính xác địa chỉ `2001:0000:0000:00ab:0000:0000:0000:0001` theo tiêu chuẩn nén cụm dài nhất là:  
**A. 2001:0:0:ab::1**  
B. 2001::ab::1  
C. 2001::ab:0:0:0:1  
D. 2001:0000:0000:ab::1  
* **Giải thích:** Cụm 3 nhóm số 0 ở sau dài hơn cụm 2 nhóm ở trước nên được nén thành `::`; cụm trước thành 0:0.

#### **Câu 266:** Dải địa chỉ Link-Local trong IPv6 có tiền tố nhị phân bắt đầu bằng:  
**A. fe80::/10**  
B. fc00::/7  
C. 2000::/3  
D. ff00::/8  
* **Giải thích:** Link-Local luôn bắt đầu bằng 10 bit nhị phân `1111 1110 10`, viết tắt là `fe80::/10`.

#### **Câu 267:** Đặc điểm cơ bản của địa chỉ IPv6 Link-Local (`fe80::/10`) là:  
**A. Chỉ có giá trị hoạt động trong phân đoạn liên kết mạng nội bộ, router tuyệt đối không định tuyến ra ngoài**  
B. Định tuyến toàn cầu trên Internet  
C. Là địa chỉ máy chủ mail  
D. Bị xóa sau 1 phút  
* **Giải thích:** Link-Local được tạo tự động để giao tiếp trong mạng LAN cục bộ và làm next-hop cho giao thức định tuyến.

#### **Câu 268:** Dải địa chỉ Unique Local Address (ULA) trong IPv6 có tiền tố chuẩn là:  
**A. fc00::/7 (thực tế sử dụng nhánh fd00::/8)**  
B. fe80::/10  
C. 2001::/16  
D. ff02::/16  
* **Giải thích:** ULA tương đương với Private IP của IPv4, dùng trong mạng nội bộ tổ chức và bắt đầu bằng `fd`.

#### **Câu 269:** Dải địa chỉ Global Unicast trong IPv6 (định tuyến công cộng toàn cầu) có tiền tố là:  
**A. 2000::/3**  
B. fe80::/10  
C. fc00::/7  
D. ff00::/8  
* **Giải thích:** Global Unicast chiếm 1/8 không gian địa chỉ IPv6, bắt đầu bằng 3 bit `001` (dải từ 2000:: đến 3fff::).

#### **Câu 270:** Dải địa chỉ Multicast trong IPv6 bắt đầu bằng tiền tố nào?  
**A. ff00::/8**  
B. fe80::/10  
C. fc00::/7  
D. ::/128  
* **Giải thích:** Mọi địa chỉ Multicast trong IPv6 đều bắt đầu bằng byte `FF` (8 bit 1 liên tiếp).

#### **Câu 271:** Địa chỉ Multicast `ff02::1` trong IPv6 được gửi tới đối tượng nào?  
**A. Tất cả các nút mạng (All Nodes/Hosts) trong liên kết cục bộ**  
B. Tất cả các router trong liên kết  
C. Chỉ máy chủ DNS  
D. Mạng Internet toàn cầu  
* **Giải thích:** `ff02::1` thay thế cho địa chỉ Broadcast toàn mạng trong mạng LAN cục bộ.

#### **Câu 272:** Địa chỉ Multicast `ff02::2` trong IPv6 được gửi tới đối tượng nào?  
**A. Tất cả các Router (All Routers) trong liên kết cục bộ**  
B. Tất cả các máy tính  
C. Chỉ máy in mạng  
D. Tất cả máy chủ Web  
* **Giải thích:** `ff02::2` dùng khi host muốn tìm kiếm hoặc gửi thông điệp yêu cầu tới các router lân cận.

#### **Câu 273:** Giao thức nào trong IPv6 thay thế hoàn toàn cho giao thức phân giải địa chỉ ARP của IPv4?  
**A. NDP (Neighbor Discovery Protocol) chạy trên ICMPv6**  
B. DHCPv6  
C. DNSv6  
D. NAT64  
* **Giải thích:** NDP sử dụng các gói tin ICMPv6 Multicast để tìm địa chỉ MAC và phát hiện hàng xóm lân cận.

#### **Câu 274:** Thông điệp NDP nào tương đương với gói tin ARP Request trong IPv4?  
**A. Neighbor Solicitation (NS)**  
B. Neighbor Advertisement (NA)  
C. Router Solicitation (RS)  
D. Router Advertisement (RA)  
* **Giải thích:** Host gửi NS (gói Multicast) để hỏi địa chỉ MAC của nút đích mang IP tương ứng.

#### **Câu 275:** Thông điệp NDP nào tương đương với gói tin ARP Reply trong IPv4?  
**A. Neighbor Advertisement (NA)**  
B. Neighbor Solicitation (NS)  
C. Echo Reply  
D. Router Advertisement  
* **Giải thích:** Nút đích phản hồi NA chứa địa chỉ MAC của mình cho nút gửi.

#### **Câu 276:** Tính năng DAD (Duplicate Address Detection) trong IPv6 dùng để làm gì?  
**A. Kiểm tra xem địa chỉ IPv6 vừa cấu hình có bị trùng lặp với máy nào khác trong mạng LAN hay không**  
B. Tăng tốc độ truyền  
C. Đo độ trễ mạng  
D. Xóa bản ghi cũ  
* **Giải thích:** Trước khi gán địa chỉ, host gửi gói NS thăm dò chính IP đó; nếu có ai phản hồi NA tức là IP đã bị trùng.

#### **Câu 277:** Cơ chế tự cấu hình địa chỉ không trạng thái SLAAC (Stateless Address Autoconfiguration) hoạt động như thế nào?  
**A. Host nhận tiền tố mạng /64 từ Router Advertisement (RA) và tự tạo phần Interface ID 64-bit còn lại**  
B. Host phải xin IP từ DHCP Server  
C. Host tự chọn ngẫu nhiên toàn bộ 128 bit  
D. Host nhận IP từ DNS  
* **Giải thích:** SLAAC cho phép thiết bị cắm vào mạng là tự có IP toàn cầu mà không cần máy chủ quản lý trạng thái DHCP.

#### **Câu 278:** Thông điệp Router Advertisement (RA) được router gửi định kỳ hoặc phản hồi theo yêu cầu qua địa chỉ Multicast nào?  
**A. ff02::1 (All Nodes)**  
B. ff02::2 (All Routers)  
C. fe80::1  
D. ::1  
* **Giải thích:** Router gửi RA tới `ff02::1` để cung cấp tiền tố mạng (Prefix), MTU và cờ cấu hình cho tất cả các host.

#### **Câu 279:** Quy chuẩn EUI-64 tạo ra phần Interface ID 64-bit từ địa chỉ MAC 48-bit bằng cách nào?  
**A. Chèn `FF:FE` vào giữa MAC và đảo ngược bit thứ 7 (Universal/Local) của byte đầu tiên**  
B. Chèn `EE:EE` vào cuối MAC  
C. Xóa bỏ 16 bit đầu của MAC  
D. Nhân đôi địa chỉ MAC  
* **Giải thích:** Chèn chuỗi `FF:FE` vào giữa byte 3 và byte 4, sau đó lật bit thứ 7 (U/L bit) của byte thứ nhất.

#### **Câu 280:** Địa chỉ MAC là `00:11:22:33:44:55`. Khi áp dụng chuẩn EUI-64, byte đầu tiên `00` chuyển thành:  
**A. 02**  
B. 01  
C. 00  
D. 03  
* **Giải thích:** `00` là `0000 0000`. Lật bit thứ 7 từ trái sang thành `0000 0010` tương đương số Hex là `02`.

#### **Câu 281:** Địa chỉ MAC là `02:AA:BB:CC:DD:EE`. Khi áp dụng chuẩn EUI-64, byte đầu tiên `02` chuyển thành:  
**A. 00**  
B. 02  
C. 01  
D. 03  
* **Giải thích:** `02` là `0000 0010`. Lật bit thứ 7 thành `0000 0000` tương đương số Hex là `00`.

#### **Câu 282:** Địa chỉ MAC là `00:50:56:C0:00:08`. Interface ID 64-bit theo chuẩn EUI-64 là:  
**A. 0250:56ff:fec0:0008**  
B. 0050:56ff:fec0:0008  
C. 0250:56ee:eec0:0008  
D. 0350:56ff:fec0:0008  
* **Giải thích:** Byte đầu `00` thành `02`, chèn `ff:fe` vào giữa tạo thành `0250:56ff:fec0:0008`.

#### **Câu 283:** Địa chỉ MAC là `10:20:30:40:50:60`. Byte đầu `10` chuyển thành giá trị nào trong EUI-64?  
**A. 12**  
B. 10  
C. 11  
D. 00  
* **Giải thích:** `10` là `0001 0000`. Lật bit thứ 7 thành `0001 0010` tương đương số Hex là `12`.

#### **Câu 284:** Độ dài tiền tố chuẩn (Standard Subnet Prefix) của hầu hết các mạng con IPv6 cho người dùng cuối là:  
**A. /64**  
B. /48  
C. /32  
D. /128  
* **Giải thích:** Chuẩn quốc tế ấn định 64 bit cho phần mạng (Network ID) và 64 bit cho phần giao diện (Interface ID) để SLAAC hoạt động.

#### **Câu 285:** Một ISP cấp cho doanh nghiệp một khối mạng `/48`. Doanh nghiệp có thể chia được tối đa bao nhiêu mạng con `/64`?  
**A. 65.536 mạng con (/64)**  
B. 256 mạng  
C. 16 mạng  
D. 4.096 mạng  
* **Giải thích:** Số bit subnet mượn được = 64 - 48 = 16 bit. Số mạng con = 2^16 = 65.536 mạng /64.

#### **Câu 286:** Kỹ thuật chuyển tiếp 'Dual-Stack' (Song song hai ngăn xếp) có đặc điểm là:  
**A. Các thiết bị mạng cài đặt và chạy đồng thời cả 2 ngăn xếp giao thức IPv4 và IPv6 trên cùng một giao diện card mạng**  
B. Gói tin IPv6 bị xóa  
C. Chỉ hỗ trợ mạng không dây  
D. Đổi toàn bộ thiết bị phần cứng  
* **Giải thích:** Dual-Stack cho phép thiết bị tương thích cả 2 giao thức, giao tiếp tự nhiên với cả thế giới v4 và v6.

#### **Câu 287:** Kỹ thuật chuyển tiếp 'Tunneling' (Đường hầm) có đặc điểm là:  
**A. Đóng gói toàn bộ gói tin IPv6 vào bên trong trường Payload của gói tin IPv4 để đi xuyên qua mạng IPv4 trung gian**  
B. Chạy cáp ngầm dưới lòng đất  
C. Xóa bỏ địa chỉ IPv4  
D. Dịch cổng NAT  
* **Giải thích:** Router biên đóng gói IPv6 vào IPv4 như một tải dữ liệu, khi đến đầu kia đường hầm thì mở gói lấy lại gói IPv6 nguyên bản.

#### **Câu 288:** Kỹ thuật chuyển tiếp 'NAT64' kết hợp 'DNS64' cho phép:  
**A. Một máy tính thuần IPv6 giao tiếp thông suốt với một máy chủ thuần IPv4 trên Internet**  
B. Tăng tốc độ tải file  
C. Mã hóa wifi  
D. Chuyển đổi cáp đồng sang cáp quang  
* **Giải thích:** NAT64 chuyển đổi tiêu đề giữa v6 và v4, DNS64 tạo địa chỉ IPv6 tổng hợp để máy thuần v6 trỏ tới máy thuần v4.

#### **Câu 289:** Tại sao cơ chế phân mảnh của IPv6 lại giúp tăng tốc độ định tuyến của các router vùng lõi?  
**A. Vì router không phải tốn tài nguyên CPU để cắt nhỏ và kiểm tra phân mảnh gói tin dọc đường**  
B. Vì gói tin IPv6 nhỏ hơn  
C. Vì IPv6 chỉ chạy trên cáp quang  
D. Vì không cần địa chỉ IP  
* **Giải thích:** Giao toàn bộ việc kiểm soát kích thước gói tin cho máy nguồn giúp router lõi chỉ tập trung chuyển mạch cực nhanh.

#### **Câu 290:** Trường 'Next Header' (8 bit) trong tiêu đề gói tin IPv6 có chức năng tương đương trường nào của IPv4?  
**A. Protocol**  
B. Type of Service  
C. Identification  
D. TTL  
* **Giải thích:** Next Header xác định giao thức kế tiếp (như TCP=6, UDP=17) hoặc trỏ tới tiêu đề mở rộng (Extension Header).

#### **Câu 291:** Trường 'Hop Limit' (8 bit) trong tiêu đề gói tin IPv6 có chức năng tương đương trường nào của IPv4?  
**A. Time-To-Live (TTL)**  
B. Header Checksum  
C. Version  
D. Offset  
* **Giải thích:** Hop Limit giảm đi 1 qua mỗi chặng router, hủy gói tin khi về 0 để ngăn chặn lặp vòng vô hạn.

#### **Câu 292:** Trong IPv6, các tùy chọn bổ sung (như thông tin định tuyến, bảo mật IPsec) được triển khai dưới dạng:  
**A. Các tiêu đề mở rộng (Extension Headers) nằm xen giữa tiêu đề cố định 40-byte và phần tải giao vận**  
B. Trường Options ở cuối gói tin  
C. Chèn vào dữ liệu người dùng  
D. Chèn vào địa chỉ MAC  
* **Giải thích:** Extension Headers tạo thành một chuỗi liên kết linh hoạt qua trường Next Header mà không làm phình to tiêu đề cơ sở.

#### **Câu 293:** Bản ghi tài nguyên DNS nào được sử dụng để phân giải tên miền sang địa chỉ IPv6?  
**A. Type AAAA**  
B. Type A  
C. Type CNAME  
D. Type PTR  
* **Giải thích:** Type AAAA (thường gọi là Quad-A) lưu trữ địa chỉ IPv6 128-bit.

#### **Câu 294:** Một khối mạng IPv6 được viết là `2001:db8:acad::/48`. Địa chỉ mạng con thứ nhất có tiền tố `/64` là:  
**A. 2001:db8:acad:0000::/64**  
B. 2001:db8:acad:ffff::/64  
C. 2001:db8:acad::1/64  
D. 2001:db8:acad:1000::/64  
* **Giải thích:** 16 bit subnet đầu tiên bắt đầu từ giá trị `0000`, tạo thành mạng con `2001:db8:acad:0000::/64` (hoặc `2001:db8:acad::/64`).

#### **Câu 295:** Địa chỉ mạng con thứ hai có tiền tố `/64` trong khối mạng trên là:  
**A. 2001:db8:acad:1::/64**  
B. 2001:db8:acad:2::/64  
C. 2001:db8:acad:10::/64  
D. 2001:db8:acad:0100::/64  
* **Giải thích:** 16 bit subnet tiếp theo tăng lên 1 đơn vị Hex: `0001`, viết rút gọn là `2001:db8:acad:1::/64`.

#### **Câu 296:** Một host có địa chỉ IPv6 Link-Local là `fe80::1`. Host này có thể giao tiếp được với những thiết bị nào?  
**A. Chỉ các thiết bị nằm trong cùng một phân đoạn mạng LAN / Broadcast domain với nó**  
B. Tất cả các máy chủ trên toàn cầu  
C. Các máy chủ đặt tại Mỹ  
D. Chỉ router nhà mạng  
* **Giải thích:** Địa chỉ Link-Local không thể định tuyến qua router nên phạm vi giao tiếp bị giới hạn trong liên kết cục bộ.

#### **Câu 297:** Giao thức DHCPv6 hoạt động ở chế độ 'Stateless DHCPv6' nhằm mục đích gì?  
**A. Cung cấp các thông số phụ như địa chỉ DNS Server, Domain Name cho host sau khi host đã tự có IP qua SLAAC**  
B. Cấp phát IP  
C. Đo tốc độ mạng  
D. Cấp địa chỉ MAC  
* **Giải thích:** Stateless DHCPv6 không cần lưu trạng thái cấp phát IP mà chỉ bổ sung thêm thông tin cấu hình mạng bổ trợ.

#### **Câu 298:** Giao thức DHCPv6 hoạt động ở chế độ 'Stateful DHCPv6' khi nào?  
**A. Khi mạng yêu cầu máy chủ DHCP phải quản lý chặt chẽ và cấp phát trực tiếp từng địa chỉ IPv6 cho client**  
B. Khi không có cáp quang  
C. Khi mạng dùng IPv4  
D. Khi router bị hỏng  
* **Giải thích:** Stateful DHCPv6 hoạt động tương tự DHCPv4 truyền thống, theo dõi danh sách cho thuê (lease) của từng host.

#### **Câu 299:** Trong phân lớp IPv4 truyền thống (Classful), khối địa chỉ bắt đầu bằng các bit nhị phân `110` thuộc lớp nào?  
**A. Lớp C (Dải từ 192.0.0.0 đến 223.255.255.255)**  
B. Lớp A  
C. Lớp B  
D. Lớp D  
* **Giải thích:** Lớp A bắt đầu bằng `0`, Lớp B bắt đầu bằng `10`, Lớp C bắt đầu bằng `110`, Lớp D bắt đầu bằng `1110`.

#### **Câu 300:** Động lực lớn nhất thúc đẩy toàn cầu chuyển đổi từ IPv4 sang IPv6 là gì?  
**A. Không gian địa chỉ IPv4 32-bit (khoảng 4,3 tỷ địa chỉ) đã hoàn toàn cạn kiệt trước sự bùng nổ của thiết bị di động và IoT**  
B. IPv4 chạy quá chậm  
C. Cáp quang không hỗ trợ IPv4  
D. Do lệnh cấm của các nhà mạng  
* **Giải thích:** IPv6 với 128 bit cung cấp không gian địa chỉ gần như vô tận (khoảng 3,4 * 10^38 địa chỉ), đáp ứng cho mọi thiết bị trên trái đất.

