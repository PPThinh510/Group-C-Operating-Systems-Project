# LẬP LỊCH CPU - THUẬT TOÁN SJF KHÔNG ƯU TIÊN
# (Shortest Job First - Non-Preemptive)
# Công thức:
# Completion Time (CT)  = thời điểm tiến trình kết thúc
# Turnaround Time (TAT) = CT - Arrival Time
# Waiting Time    (WT)  = TAT - Burst Time
# Response Time   (RT)  = Start Time - Arrival Time


def nhap_tien_trinh():
    """Nhập danh sách tiến trình từ bàn phím."""
    print("      LẬP LỊCH CPU - THUẬT TOÁN SJF KHÔNG ƯU TIÊN")

    while True:
        try:
            n = int(input("\nNhập số lượng tiến trình: "))
            if n <= 0:
                print("  [!] Số tiến trình phải >= 1. Vui lòng nhập lại.")
                continue
            break
        except ValueError:
            print("  [!] Vui lòng nhập số nguyên.")

    tien_trinh = []
    print()
    for i in range(n):
        print(f"Tiến trình P{i + 1}")
        while True:
            try:
                at = int(input("Arrival Time(AT): "))
                if at < 0:
                    print("[!]AT phải >= 0.")
                    continue
                break
            except ValueError:
                print("[!] Vui lòng nhập số nguyên.")

        while True:
            try:
                bt = int(input("Burst Time(BT): "))
                if bt <= 0:
                    print("[!]BT phải >= 1.")
                    continue
                break
            except ValueError:
                print("[!]Vui lòng nhập số nguyên.")

        tien_trinh.append({
            "id": f"P{i + 1}",
            "at": at,
            "bt": bt,
            "index": i,
        })

    return tien_trinh


def tinh_sjf_khong_uu_tien(tien_trinh):
    """
    Áp dụng thuật toán SJF không ưu tiên:
      - Tại mỗi thời điểm, chọn tiến trình đã đến có Burst Time nhỏ nhất.
      - Khi một tiến trình đã chạy thì chạy đến khi hoàn thành, không bị ngắt.
      - Nếu BT bằng nhau thì ưu tiên AT nhỏ hơn, sau đó đến thứ tự nhập.
      - Tính CT, TAT, WT, RT cho từng tiến trình.
      - Trả về danh sách kết quả và chuỗi Gantt.
    """
    ds = sorted(tien_trinh, key=lambda p: (p["at"], p["index"]))
    chua_xong = ds.copy()
    ket_qua = []
    gantt = []
    thoi_gian = 0

    while chua_xong:
        san_sang = [p for p in chua_xong if p["at"] <= thoi_gian]

        # Nếu chưa có tiến trình nào đến, CPU rảnh
        if not san_sang:
            p_ke_tiep = min(chua_xong, key=lambda p: (p["at"], p["index"]))
            gantt.append(("Idle", thoi_gian, p_ke_tiep["at"]))
            thoi_gian = p_ke_tiep["at"]
            continue

        # Chọn tiến trình có Burst Time nhỏ nhất
        p = min(san_sang, key=lambda x: (x["bt"], x["at"], x["index"]))
        chua_xong.remove(p)

        start = thoi_gian
        ct = thoi_gian + p["bt"]
        tat = ct - p["at"]
        wt = tat - p["bt"]
        rt = start - p["at"]

        gantt.append((p["id"], start, ct))
        ket_qua.append({
            "id": p["id"],
            "at": p["at"],
            "bt": p["bt"],
            "start": start,
            "ct": ct,
            "tat": tat,
            "wt": wt,
            "rt": rt,
        })
        thoi_gian = ct

    ket_qua.sort(key=lambda r: int(r["id"][1:]))
    return ket_qua, gantt


def ve_gantt(gantt):
    """In biểu đồ Gantt dạng text ra màn hình."""
    print("=" * 20)
    print("  BIỂU ĐỒ GANTT")
    print("=" * 20)

    top = "  |"
    for label, start, end in gantt:
        width = max(len(label) + 2, (end - start) * 3)
        top += label.center(width) + "|"
    print(top)

    timeline = "  "
    prev = None
    for label, start, end in gantt:
        width = max(len(label) + 2, (end - start) * 3)
        if prev is None:
            timeline += str(start).ljust(width + 1)
        else:
            timeline += str(start).center(1).ljust(width + 1)
        prev = end
    timeline += str(gantt[-1][2])
    print(timeline)


def in_bang_ket_qua(ket_qua):
    """In bảng kết quả chi tiết."""
    print("\n" + "=" * 20)
    print("  BẢNG KẾT QUẢ")
    print("=" * 20)
    tieu_de = (f"  {'TT':<6} {'AT':>5} {'BT':>5} {'Start':>7} "
               f"{'CT':>6} {'TAT':>6} {'WT':>6} {'RT':>6}")
    print(tieu_de)
    print("  " + "-" * 71)

    tong_tat = tong_wt = tong_rt = 0
    for r in ket_qua:
        print(f"  {r['id']:<6} {r['at']:>5} {r['bt']:>5} {r['start']:>7} "
              f"{r['ct']:>6} {r['tat']:>6} {r['wt']:>6} {r['rt']:>6}")
        tong_tat += r["tat"]
        tong_wt += r["wt"]
        tong_rt += r["rt"]

    n = len(ket_qua)
    print("  " + "-" * 71)
    print(f"  {'Trung bình':<35}"
          f"{'':>6} {tong_tat/n:>6.2f} {tong_wt/n:>6.2f} {tong_rt/n:>6.2f}")

    return tong_tat / n, tong_wt / n, tong_rt / n


def in_tong_ket(ket_qua, avg_tat, avg_wt, avg_rt):
    """In phần tổng kết và đánh giá hiệu năng."""
    max_ct = max(r["ct"] for r in ket_qua)
    min_at = min(r["at"] for r in ket_qua)
    tong_bt = sum(r["bt"] for r in ket_qua)
    tong_thoi_gian = max_ct - min_at
    cpu_util = (tong_bt / tong_thoi_gian) * 100 if tong_thoi_gian > 0 else 0

    print("\n" + "=" * 55)
    print("  TỔNG KẾT HIỆU NĂNG")
    print("=" * 55)
    print(f"  Số tiến trình          : {len(ket_qua)}")
    print(f"  Tổng thời gian chạy    : {tong_thoi_gian} đơn vị")
    print(f"  CPU Utilization        : {cpu_util:.1f}%")
    print(f"  Avg Turnaround Time    : {avg_tat:.2f}")
    print(f"  Avg Waiting Time       : {avg_wt:.2f}")
    print(f"  Avg Response Time      : {avg_rt:.2f}")
    print("=" * 55)


def giai_thich_buoc(ket_qua, gantt):
    """In giải thích từng bước thực thi."""
    print("\n" + "=" * 30)
    print("  GIẢI THÍCH TỪNG BƯỚC")
    print("=" * 30)
    ket_qua_dict = {r["id"]: r for r in ket_qua}
    for label, start, end in gantt:
        if label == "Idle":
            print(f"  t={start:>3} → {end:>3} : CPU rảnh (chưa có tiến trình)")
        else:
            r = ket_qua_dict[label]
            print(f"  t={start:>3} → {end:>3} : Chọn {label} vì có BT nhỏ nhất "
                  f"trong hàng đợi sẵn sàng → CT={r['ct']}, TAT={r['tat']}, WT={r['wt']}")


def chay_lai():
    while True:
        lua_chon = input("\n  Chạy lại? (c = có / k = không): ").strip().lower()
        if lua_chon in ("c", "co", "y", "yes"):
            return True
        if lua_chon in ("k", "khong", "n", "no"):
            return False
        print("  [!] Vui lòng nhập 'c' hoặc 'k'.")


# CHƯƠNG TRÌNH CHÍNH
if __name__ == "__main__":
    while True:
        tien_trinh = nhap_tien_trinh()
        ket_qua, gantt = tinh_sjf_khong_uu_tien(tien_trinh)

        ve_gantt(gantt)
        avg_tat, avg_wt, avg_rt = in_bang_ket_qua(ket_qua)
        in_tong_ket(ket_qua, avg_tat, avg_wt, avg_rt)
        giai_thich_buoc(ket_qua, gantt)

        if not chay_lai():
            print("\n  Kết thúc chương trình. Tạm biệt!\n")
            break
