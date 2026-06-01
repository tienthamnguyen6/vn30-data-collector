import os
import pandas as pd
from vnstock import stock_historical_data
from supabase import create_client, Client
from datetime import datetime, timedelta

# 1. Cấu hình kết nối
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. Danh sách 30 mã cổ phiếu VN30 (Cập nhật tĩnh)
vn30_tickers = [
    "ACB", "BCM", "BID", "BVH", "CTG", "FPT", "GAS", "GVR", "HDB", "HPG",
    "MBB", "MSN", "MWG", "PLX", "POW", "SAB", "SHB", "SSB", "SSI", "STB",
    "TCB", "TPB", "VCB", "VHM", "VIB", "VIC", "VJC", "VNM", "VPB", "VRE"
]

today = datetime.now()
yesterday = (today - timedelta(days=1)).strftime('%Y-%m-%d')

# Khởi tạo một "chiếc giỏ" rỗng (List) để gom dữ liệu
data_payloads = []

# 3. EXTRACT: Vòng lặp lấy dữ liệu và bỏ vào giỏ
print(f"Đang lấy dữ liệu ngày {yesterday}...")
for ticker in vn30_tickers:
    try:
        df = stock_historical_data(symbol=ticker, start_date=yesterday, end_date=yesterday, resolution='1D')
        
        if not df.empty:
            close_price = float(df['close'].iloc[0])
            # Bỏ dữ liệu vào giỏ thay vì đẩy lên ngay
            data_payloads.append({
                "ticker": ticker,
                "trade_date": yesterday,
                "close_price": close_price,
                "daily_return": 0.0
            })
    except Exception as e:
        # Lỗi 1 mã thì bỏ qua, chạy tiếp mã khác (chống sập hệ thống)
        print(f"⚠️ Không lấy được dữ liệu {ticker}: {e}")

# 4. LOAD (Batch Insert): Đẩy toàn bộ giỏ lên Supabase trong 1 câu lệnh
if data_payloads: # Nếu giỏ có đồ
    try:
        # Hàm insert() của Supabase hỗ trợ nhận 1 list chứa nhiều dòng dữ liệu
        data, count = supabase.table('vn30_daily_prices').insert(data_payloads).execute()
        print(f"✅ Đã lưu thành công {len(data_payloads)} mã VN30 vào Database!")
    except Exception as e:
        print(f"⚠️ Lỗi khi đẩy lên Database: {e}")
else:
    print(f"⚠️ Ngày {yesterday} trống rỗng (có thể là cuối tuần hoặc ngày nghỉ lễ).")
