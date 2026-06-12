import os
import pandas as pd
from vnstock import stock_historical_data
from supabase import create_client, Client
from datetime import datetime, timedelta

# Lấy thông tin bảo mật từ GitHub Environment
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Thiếu cấu hình cặp khóa SUPABASE_URL hoặc SUPABASE_KEY trong Secrets!")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Danh sách cổ phiếu theo dõi
tickers = ['FPT', 'MBB', 'VNM']

# Thiết lập khoảng thời gian: Lấy khoảng 5 ngày gần nhất để chắc chắn có giá phiên trước (t-1) nhằm tính Return
today = datetime.now()
start_date = (today - timedelta(days=5)).strftime('%Y-%m-%d')
end_date = today.strftime('%Y-%m-%d')

for ticker in tickers:
    # 1. EXTRACT: Lấy chuỗi dữ liệu lịch sử ngắn hạn
    df = stock_historical_data(symbol=ticker, start_date=start_date, end_date=end_date, resolution='1D')
    
    if not df.empty:
        # 2. TRANSFORM: Sắp xếp theo ngày tăng dần và tính toán Return bằng Pandas
        df['time'] = pd.to_datetime(df['time'])
        df = df.sort_values(by='time').reset_index(drop=True)
        
        # Tính tỷ suất sinh lời: (P_t - P_{t-1}) / P_{t-1}
        df['daily_return'] = df['close'].pct_change()
        
        # Chỉ lọc lấy bản ghi của ngày hôm nay (hoặc ngày gần nhất có dữ liệu mới) để nạp vào DB
        # Ở đây lấy dòng cuối cùng trong chuỗi dữ liệu vừa cào
        latest_row = df.iloc[-1]
        trade_date_str = latest_row['time'].strftime('%Y-%m-%d')
        close_price = float(latest_row['close'])
        daily_return_val = latest_row['daily_return']
        
        # Nếu dòng cuối là ngày đầu tiên trong chuỗi (không tính được return) thì gán None (NULL) hoặc 0
        if pd.isna(daily_return_val):
            daily_return_val = 0.0
        else:
            daily_return_val = float(daily_return_val)

        # Chuẩn bị gói dữ liệu (Payload)
        data_payload = {
            "ticker": ticker,
            "trade_date": trade_date_str,
            "close_price": close_price,
            "daily_return": daily_return_val
        }
        
        # 3. LOAD: Đẩy dữ liệu vào Supabase
        try:
            # Nhờ có ràng buộc UNIQUE(ticker, trade_date) trong DB của bạn, 
            # sử dụng upsert sẽ giúp cập nhật nếu trùng hoặc thêm mới nếu chưa có.
            supabase.table('vn30_daily_prices').upsert(data_payload).execute()
            print(f"✅ Đã cập nhật thành công {ticker} ngày {trade_date_str} với Return: {daily_return_val:.5f}")
        except Exception as e:
            print(f"⚠️ Lỗi khi cập nhật {ticker}: {e}")
