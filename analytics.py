import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import json

DATABASE_URL = "postgresql://user:password@localhost:5432/autoflow"

def get_kpis():
    """Extracts data from PostgreSQL and computes KPIs using pandas."""
    print("Connecting to database for analytics...")
    engine = create_engine(DATABASE_URL)
    
    # Load tables into pandas DataFrames
    users_df = pd.read_sql_table('users', con=engine)
    sales_df = pd.read_sql_table('sales', con=engine)
    
    # Ensure date columns are datetime objects
    users_df['signup_date'] = pd.to_datetime(users_df['signup_date'])
    sales_df['date'] = pd.to_datetime(sales_df['date'])
    
    today = pd.to_datetime(datetime.now().date())
    seven_days_ago = today - timedelta(days=7)
    fourteen_days_ago = today - timedelta(days=14)
    
    # KPIs for this week (last 7 days)
    this_week_sales = sales_df[(sales_df['date'] > seven_days_ago) & (sales_df['date'] <= today)]
    this_week_revenue = this_week_sales['amount'].sum()
    this_week_aov = this_week_sales['amount'].mean() if not this_week_sales.empty else 0.0
    
    this_week_signups = users_df[(users_df['signup_date'] > seven_days_ago) & (users_df['signup_date'] <= today)]
    new_signups = len(this_week_signups)
    
    # KPIs for last week (7 to 14 days ago)
    last_week_sales = sales_df[(sales_df['date'] > fourteen_days_ago) & (sales_df['date'] <= seven_days_ago)]
    last_week_revenue = last_week_sales['amount'].sum()
    
    # Revenue Growth
    if last_week_revenue > 0:
        revenue_growth = ((this_week_revenue - last_week_revenue) / last_week_revenue) * 100
    else:
        revenue_growth = 100.0 if this_week_revenue > 0 else 0.0

    kpis = {
        "report_date": today.strftime('%Y-%m-%d'),
        "this_week_revenue": round(this_week_revenue, 2),
        "last_week_revenue": round(last_week_revenue, 2),
        "revenue_growth_percentage": round(revenue_growth, 2),
        "new_signups_this_week": new_signups,
        "average_order_value_this_week": round(this_week_aov, 2)
    }
    
    return json.dumps(kpis, indent=4)

if __name__ == "__main__":
    print(get_kpis())
