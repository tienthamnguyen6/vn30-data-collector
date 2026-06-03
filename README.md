# 📈 VN30 Financial Data Collector

Công cụ tự động thu thập dữ liệu tài chính và lịch sử giao dịch của các mã cổ phiếu thuộc rổ VN30 từ Vietstock, phục vụ kiểm định mô hình CAPM.

---

## 🎯 Mục tiêu

- Thay thế việc tải thủ công từng file CSV mất nhiều giờ
- Làm sạch và chuẩn hóa dữ liệu thô để sẵn sàng cho phân tích định lượng
- Lưu trữ dữ liệu có cấu trúc phục vụ kiểm định mô hình CAPM

---

## ⚙️ Tech Stack

| Công cụ | Mục đích |
|---|---|
| Python 3.x | Ngôn ngữ chính |
| Pandas | Xử lý và làm sạch dữ liệu |
| NumPy | Tính toán định lượng |
| Requests / aiohttp | Gọi API bất đồng bộ |
| GitHub | Quản lý phiên bản |

---

## 🚀 Cài đặt & Chạy

```bash
# 1. Clone repo
git clone https://github.com/tienthamnguyen6/vn30-data-collector.git
cd vn30-data-collector

# 2. Cài thư viện
pip install -r requirements.txt

# 3. Chạy script thu thập dữ liệu
python main.py
```

---

## 📁 Cấu trúc thư mục

```
vn30-data-collector/
├── main.py              # Script chính
├── scraper.py           # Logic thu thập dữ liệu
├── cleaner.py           # Làm sạch dữ liệu thô
├── requirements.txt     # Danh sách thư viện
├── data/
│   └── output/          # Dữ liệu sau xử lý (.csv)
└── README.md
```

---

## 📊 Kết quả

- Thu thập dữ liệu **30 mã cổ phiếu VN30** tự động
- Giảm thời gian thu thập từ **nhiều giờ xuống dưới 1 phút**
- Output sạch, sẵn sàng đưa vào mô hình CAPM

---

## 👤 Tác giả

**Nguyễn Tiến Thẩm**
- LinkedIn: [linkedin.com/in/nguyentientham](https://linkedin.com/in/nguyentientham)
- GitHub: [github.com/tienthamnguyen6](https://github.com/tienthamnguyen6)
