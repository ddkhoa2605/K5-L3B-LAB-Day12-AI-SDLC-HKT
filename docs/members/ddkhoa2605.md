# ddkhoa2605 — phản tư cá nhân (≤ 200 từ)

- **Tôi đã làm:**
  - Integrator + Release, phụ trách `sim/quan`, `day`, `shop`: Quán lõi 1 bếp 1 bàn v1.0, mở rộng 2 bếp 4 bàn 6 món v1.1 ([#4](https://github.com/ddkhoa2605/K5-L3B-LAB-Day12-AI-SDLC-HKT/pull/4), [#5](https://github.com/ddkhoa2605/K5-L3B-LAB-Day12-AI-SDLC-HKT/pull/5)).
  - Vòng ngày `day.py`, tạm dừng `pause.py`, Shop nâng cấp và ADR-0001, ADR-0002.
  - Chuyển đổi kho cá thể v1.2, hao tươi 0.25/s, nhả giữ chỗ khi ươn, chốt giá theo độ tươi ([#20](https://github.com/ddkhoa2605/K5-L3B-LAB-Day12-AI-SDLC-HKT/pull/20)).
  - Mở rộng Khách đặt trước (reservations) 20 test đạt ([#21](https://github.com/ddkhoa2605/K5-L3B-LAB-Day12-AI-SDLC-HKT/pull/21)).
  - Viết `tools/soak.py` cho Phase 4, tổng hợp CHANGELOG và gắn tag release.
- **Tôi đã review:**
  - Review toàn bộ các PR của Người 1, 3, 4; điều phối standup và thứ tự merge.
- **AI sai ở đâu và tôi phát hiện thế nào:**
  - AI nhầm frame tick k sinh event tick k+1 nên đặt kỳ vọng tick lệch 1 đơn vị; shell script heredoc không nháy làm mất chữ trong `clarify.md`.
  - Phát hiện qua `git diff` và kiểm tra terminal sau khi chạy.
- **Điều tôi học được:**
  - Khi đổi hợp đồng schema, cắt thẳng một lần dứt khoát kèm adapter tạm thời giúp nhóm không bị tắc nghẽn tích hợp.
