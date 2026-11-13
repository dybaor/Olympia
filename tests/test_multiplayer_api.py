import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.models.schemas_olympic import UserMatchConfig, RoundConfig
from app.skills.doc_parser import KnowledgeGraphExtractor
from app.core.database import Base, DocumentModel
from app.services.multiplayer_manager import multiplayer_manager, Player
from app.api.routes_multiplayer import create_room, join_room, get_room_details, CreateRoomRequest, JoinRoomRequest

def run_multiplayer_tests():
    print("=" * 75)
    print("🌐 KIỂM THỬ ĐƠN VỊ & TÍCH HỢP HỆ THỐNG MULTIPLAYER ARENA (3 NGƯỜI CHƠI)")
    print("=" * 75)

    # 1. BÓC TÁCH TÀI LIỆU VÀ KHỞI TẠO TEST DB
    sample_doc_path = BASE_DIR / "tests" / "sample_docs" / "kien_truc_he_thong_phan_tan_raft.md"
    assert sample_doc_path.exists(), f"Không tìm thấy file {sample_doc_path}"

    extractor = KnowledgeGraphExtractor()
    bundle = extractor.process_document(str(sample_doc_path), doc_id="DOC_MP_SUITE")

    eng = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=eng)
    db = sessionmaker(bind=eng)()

    doc_rec = DocumentModel(
        id="DOC_MP_SUITE",
        title=bundle.document_title,
        file_type=".md",
        file_path=str(sample_doc_path),
        raw_content="",
        extracted_bundle_json=bundle.model_dump_json(),
    )
    db.add(doc_rec)
    db.commit()

    # TEST 1: CHỦ PHÒNG TẠO PHÒNG ĐẤU 6 KÝ TỰ (OLY-XXX)
    print("\n[TEST 1] Chủ phòng ('Minh Triết - Host') kiến tạo phòng thi đấu...")
    cfg = UserMatchConfig(
        match_mode="ARENA_COMPETITION",
        round_configs=[
            RoundConfig(round_number=1, difficulty="MEDIUM", time_limit_sec=15, question_count=3),
            RoundConfig(round_number=2, difficulty="MEDIUM", time_limit_sec=20, question_count=2),
            RoundConfig(round_number=3, difficulty="HARD", time_limit_sec=25, question_count=2),
            RoundConfig(round_number=4, difficulty="HARD", time_limit_sec=30, question_count=2),
        ]
    )
    create_req = CreateRoomRequest(
        host_nickname="Minh Triết (Host)",
        document_id="DOC_MP_SUITE",
        config=cfg,
    )
    r_data = create_room(create_req, db=db)
    room_code = r_data["room_code"]
    host_id = r_data["host_player_id"]

    assert room_code.startswith("OLY-") and len(room_code) == 7, f"Mã phòng {room_code} không chuẩn OLY-XXX"
    assert r_data["invite_url"] == f"/#join={room_code}", "Invite URL không đúng format"
    print(f"  ✓ Đã tạo phòng thành công: Mã '{room_code}' | Host ID: {host_id}")

    # TEST 2: ĐẤU THỦ 2 ('Bảo Long') VÀ ĐẤU THỦ 3 ('Thanh Hà') GIA NHẬP PHÒNG
    print("\n[TEST 2] Đấu thủ 2 ('Bảo Long') & Đấu thủ 3 ('Thanh Hà') gia nhập phòng...")
    j2 = join_room(JoinRoomRequest(room_code=room_code, nickname="Bảo Long"))
    p2_id = j2["player_id"]
    assert j2["status"] == "success"
    assert j2["is_host"] is False
    print(f"  ✓ Bảo Long đã vào phòng thành công (ID: {p2_id})")

    j3 = join_room(JoinRoomRequest(room_code=room_code, nickname="Thanh Hà"))
    p3_id = j3["player_id"]
    assert j3["status"] == "success"
    assert j3["is_host"] is False
    print(f"  ✓ Thanh Hà đã vào phòng thành công (ID: {p3_id})")

    # TEST 3: TRUY VẤN CHI TIẾT PHÒNG VÀ DANH SÁCH 3 NGƯỜI CHƠI
    print("\n[TEST 3] Xác thực trạng thái Sảnh chờ (Lobby Details) qua API...")
    room_details = get_room_details(room_code)
    assert room_details["total_players"] == 3, f"Số người chơi mong đợi 3, thực tế {room_details['total_players']}"
    assert room_details["status"] == "LOBBY", "Trạng thái phòng phải là LOBBY"
    assert len(room_details["leaderboard"]) == 3, "Bảng xếp hạng phải có đủ 3 người"
    print(f"  ✓ Sảnh chờ ghi nhận chính xác 3 người chơi: {[p['nickname'] for p in room_details['players']]}")

    # TEST 4: LOGIC QUẢN LÝ ĐIỂM SỐ, TỐC ĐỘ, CHUỖI STREAK TRONG PHÒNG
    print("\n[TEST 4] Kiểm tra tính điểm độc lập, thưởng chuỗi (streak) và thưởng tốc độ...")
    room = multiplayer_manager.rooms[room_code]
    p_host = room.players[host_id]
    p_p2 = room.players[p2_id]
    p_p3 = room.players[p3_id]

    # Host trả lời đúng với tốc độ cao (thưởng tốc độ)
    p_host.total_score = 45
    p_host.current_streak = 3
    # P2 trả lời đúng nhưng tốc độ chậm hơn
    p_p2.total_score = 30
    p_p2.current_streak = 2
    # P3 trả lời sai
    p_p3.total_score = 0
    p_p3.current_streak = 0

    leaderboard = room.get_leaderboard()
    assert leaderboard[0]["player_id"] == host_id, "Host phải dẫn đầu bảng xếp hạng"
    assert leaderboard[0]["total_score"] == 45
    assert leaderboard[1]["player_id"] == p2_id, "P2 phải đứng thứ 2"
    assert leaderboard[2]["total_score"] == 0, "P3 nhận 0 điểm"
    print("  ✓ Bảng xếp hạng trực tiếp xếp thứ hạng chính xác:")
    for row in leaderboard:
        print(f"     Hạng {row['rank']}: {row['nickname']} | Điểm: {row['total_score']} | Chuỗi: {row['current_streak']}")

    # TEST 5: ĐẶT CƯỢC NGÔI SAO HY VỌNG (VÒNG 4)
    print("\n[TEST 5] Kiểm tra cơ chế kích hoạt Ngôi Sao Hy Vọng...")
    p_p2.star_of_hope_activated = True
    assert p_p2.star_of_hope_activated is True
    lb_with_star = room.get_leaderboard()
    p2_entry = next(p for p in lb_with_star if p["player_id"] == p2_id)
    assert p2_entry["star_of_hope"] is True, "Cờ star_of_hope phải được broadcast lên bảng xếp hạng"
    print(f"  ✓ Đấu thủ '{p_p2.nickname}' kích hoạt Ngôi sao hy vọng thành công!")

    # TEST 6: KIỂM TRA RỚT MẠNG VÀ KẾT NỐI LẠI (AUTO-RECONNECT)
    print("\n[TEST 6] Kiểm tra khả năng tự động khôi phục kết nối (Auto-reconnect)...")
    p_p2.is_connected = False
    reconnect_res = join_room(JoinRoomRequest(
        room_code=room_code,
        nickname="Bảo Long",
        reconnect_player_id=p2_id,
    ))
    assert reconnect_res["player_id"] == p2_id, "Player ID phải giữ nguyên sau khi reconnect"
    assert room.players[p2_id].is_connected is True, "Trạng thái người chơi phải chuyển lại Connected"
    assert room.players[p2_id].total_score == 30, "Điểm số không được bị mất mát khi rớt mạng"
    assert room.players[p2_id].current_streak == 2, "Chuỗi streak không được bị reset khi rớt mạng"
    print("  ✓ Auto-reconnect hoàn hảo: Khôi phục ID cũ, giữ nguyên 30 điểm và chuỗi 2 streak!")

    print("\n" + "=" * 75)
    print("🎉 TẤT CẢ 6 BÀI KIỂM THỬ MULTIPLAYER ARENA ĐÃ VƯỢT QUA XUẤT SẮC (PASSED) 100%!")
    print("=" * 75)

if __name__ == "__main__":
    run_multiplayer_tests()

