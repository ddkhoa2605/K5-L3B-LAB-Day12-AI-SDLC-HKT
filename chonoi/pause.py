"""Tạm dừng (TICKET-02 mục 4.2). Xét cạnh `pause` TRƯỚC mọi cạnh khác.

Vào pause: chỉ tăng tick ngoài và phát `paused`; mọi cạnh hành động (và `buy`) bị bỏ qua, `sim_tick`, `phase_tick`,
lịch, timer đứng yên. Cạnh lên `pause` kế tiếp phát `resumed` và chạy gameplay NGAY trong bước đó.
Dùng chung cho gather, quan (runner.Session) và day (day.DaySession).
"""


class PauseGate:
    def __init__(self):
        self.paused = False

    def handle(self, inp):
        """Trả (tên event hoặc None, có chạy gameplay bước này không)."""
        edge = inp.pressed("pause")
        if not self.paused:
            if edge:
                self.paused = True
                return "paused", False
            return None, True
        if edge:
            self.paused = False
            return "resumed", True
        return None, False
