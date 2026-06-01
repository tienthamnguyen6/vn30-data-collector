import os
import pandas as pd
from vnstock import stock_historical_data
from supabase import create_client, Client
from datetime import datetime, timedelta

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Tạm thời chạy 3 mã để test biểu đồ trước
tickers = ['FPT', 'MBB', 'VNM']

# --- ĐÃ SỬA LẠI LOGIC THỜI GIAN ---
# Lấy chính xác giờ Việt Nam (UTC+7) để máy chủ GitHub không bị lệch ngày
today_vn = datetime.utcnow() + timedelta(hours=7)
target_date = today_vn.strftime('%Y-%m-%d') 

for ticker in tickers:
    # Lấy dữ liệu của đúng ngày hôm nay (target_date)
    df = stock_historical_data(symbol=ticker, start_date=target_date, end_date=target_date, resolution='1D')
    
    if not df.empty:
        close_price = float(df['close'].iloc[0])
        
        data_payload = {
            "ticker": ticker,
            "trade_date": target_date,
            "close_price": close_price,
            "daily_return": 0.0 
        }
        
        try:
            data, count = supabase.table('vn30_daily_prices').insert(data_payload).execute()
            print(f"✅ Đã cập nhật thành công {ticker} ngày {target_date}")
        except Exception as e:
            print(f"⚠️ Lỗi khi cập nhật {ticker}: {e}")
