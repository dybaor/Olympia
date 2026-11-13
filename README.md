# ĐẤU TRƯỜNG TRI THỨC (OLYMPIC ARENA & PRACTICE DOJO)
> Hệ thống web tự động phân tích sâu tài liệu học thuật/kỹ thuật và kiến tạo đấu trường thi đấu Olympic 4 vòng kết hợp Phòng Luyện tập (Practice Dojo) thông qua 5 Agent AI chuyên biệt.

---

## 🌟 HỆ THỐNG 5 AGENT ĐIỀU PHỐI (MULTI-AGENT SWARM)

1. **Agent 1: `Knowledge_Graph_Extractor`**
   - Hỗ trợ định dạng: **PDF, DOCX, Markdown (.md), Plain Text (.txt)**.
   - Phân đoạn ngữ cảnh (**Semantic Sliding Window Chunking**).
   - Gắn nhãn phân tầng nhận thức theo thang đo **Bloom Taxonomy**:
     - `REMEMBER` (Nhận biết định nghĩa cốt lõi)
     - `UNDERSTAND` (Thông hiểu nguyên lý)
     - `APPLY` (Vận dụng định lý & quan hệ nhân-quả)
     - `ANALYZE_EVALUATE` (Phân tích, phản biện & điều kiện biên Edge Cases)

2. **Agent 2: `Dynamic_Olympic_Architect`**
   - Nhận cấu hình từ **Phòng cấu hình trước trận đấu (Pre-Match Setup / Match Lobby)**.
   - Tham số hóa độ khó linh hoạt: `EASY | MEDIUM | HARD | EXTREME` và thời gian từng vòng.
   - Sinh kèm **2 tầng gợi ý tiến tiến** (`progressive_hints`) và lời giải bóc tách từng bước (`step_by_step_explanation`).
   - Hỗ trợ tạo biến thể câu hỏi tương tự (`generate_question_variant`) phục vụ rèn luyện.

3. **Agent 3: `Adversarial_Fact_Checker`**
   - Hội đồng thẩm định chất lượng đối kháng: Kiểm tra chéo 100% câu hỏi và trích dẫn gốc.
   - Loại bỏ câu hỏi ảo giác (hallucination), kiểm tra chất lượng 2 tầng gợi ý và các phương án gây nhiễu.

4. **Agent 4: `Practice_&_Arena_Engine`**
   - **Chế độ Thi đấu (Olympic Arena):** Khóa hoàn toàn gợi ý, đếm ngược nghiêm ngặt (xác thực thời gian ở Backend chống gian lận), thưởng tốc độ, thưởng chuỗi combo và cược Ngôi sao hy vọng (Star of Hope).
   - **Chế độ Luyện tập (Practice Dojo):** Mở khóa 2 tầng gợi ý (`Gợi ý 1: Tư duy` & `Gợi ý 2: Manh mối mấu chốt`), trả về lời giải từng bước ngay khi trả lời, hỗ trợ làm lại và luyện câu hỏi biến thể.

5. **Agent 5: `Fullstack_App_Builder`**
   - Màn hình Phòng chờ (Match Lobby): Thanh trượt thời gian (5s - 90s), dropdown độ khó từng vòng 1 -> 4, bộ lọc phạm vi luyện tập.
   - Giao diện thi đấu kịch tính với Web Audio API synthesizer tái tạo âm thanh không cần tải file ngoài.
   - Biểu đồ Radar 5 chiều nhận thức tổng kết năng lực sau trận đấu.

---

## 🚀 KHỞI ĐỘNG NHANH VỚI 1 CLICK

Chạy trực tiếp bằng 1 nhấp đúp chuột mà **không cần cài đặt Python**:
👉 **`Chay_Khong_Can_Python.bat`** (hoặc `start_arena.bat`)

Trình duyệt sẽ tự động mở trang web tại: **`http://localhost:8000`**.
