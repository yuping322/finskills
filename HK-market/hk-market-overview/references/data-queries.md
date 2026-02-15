# Data Queries: HK Market Overview (港股市场概览)

港股市场概览数据查询说明，包括数据源、查询方法和数据格式。

## Data Sources

### Primary Sources

#### 1. Hong Kong Exchange (HKEX)
- **Real-time Market Data**: Live prices, volumes, order book
- **Index Data**: HSI, HSCEI, HSCCI, HSTECH
- **Sector Indices**: 11 major sector indices
- **Market Statistics**: Daily market statistics and summaries

**API Endpoints**:
```
GET /market-data/real-time/indices
GET /market-data/real-time/stocks
GET /market-data/historical/indices
GET /market-data/market-statistics
```

#### 2. Hang Seng Indexes Company
- **Index Constituents**: Current and historical constituents
- **Index Calculations**: Index methodology and calculations
- **Sector Classifications**: GICS sector classifications
- **Index Performance**: Historical performance data

**API Endpoints**:
```
GET /indices/constituents/{index_code}
GET /indices/performance/{index_code}
GET /indices/sector-weights/{index_code}
GET /indices/historical/{index_code}
```

#### 3. Major Data Vendors
- **Bloomberg**: Real-time market data and analytics
- **Reuters**: Comprehensive market data and news
- **Wind**: Chinese market data provider
- **Choice**: Financial data and analytics

## Query Types

### 1. Market Overview Queries

#### Real-time Market Data
```sql
-- Get current market overview
SELECT 
    index_code,
    index_name,
    current_price,
    change_amount,
    change_percentage,
    volume,
    turnover,
    timestamp
FROM market_overview_realtime
WHERE timestamp = (SELECT MAX(timestamp) FROM market_overview_realtime);
```

#### Historical Market Data
```sql
-- Get historical index performance
SELECT 
    date,
    index_code,
    open_price,
    high_price,
    low_price,
    close_price,
    volume,
    turnover
FROM market_index_history
WHERE index_code IN ('HSI', 'HSCEI', 'HSCCI', 'HSTECH')
    AND date BETWEEN '2026-01-01' AND '2026-02-15'
ORDER BY date, index_code;
```

### 2. Sector Performance Queries

#### Sector Returns
```sql
-- Get sector performance for current day
SELECT 
    sector_code,
    sector_name,
    current_price,
    change_percentage,
    volume,
    market_cap,
    flow_amount
FROM sector_performance
WHERE date = CURRENT_DATE
ORDER BY change_percentage DESC;
```

#### Sector Historical Performance
```sql
-- Get sector performance over time
SELECT 
    date,
    sector_code,
    sector_name,
    close_price,
    change_percentage,
    relative_strength
FROM sector_performance_history
WHERE sector_code = 'TECH'
    AND date >= '2026-01-01'
ORDER BY date;
```

### 3. Market Sentiment Queries

#### Market Breadth
```sql
-- Get market breadth indicators
SELECT 
    date,
    total_stocks,
    advancing_stocks,
    declining_stocks,
    unchanged_stocks,
    breadth_percentage,
    new_highs,
    new_lows
FROM market_breadth
WHERE date >= '2026-02-01'
ORDER BY date DESC;
```

#### Volatility and Fear Index
```sql
-- Get volatility and fear indicators
SELECT 
    date,
    vix_index,
    fear_greed_index,
    put_call_ratio,
    volatility_index,
    market_sentiment
FROM market_sentiment
WHERE date >= '2026-02-01'
ORDER BY date DESC;
```

### 4. Liquidity Queries

#### Market Liquidity
```sql
-- Get market liquidity metrics
SELECT 
    date,
    total_turnover,
    average_spread,
    market_depth,
    liquidity_score,
    trading_activity
FROM market_liquidity
WHERE date >= '2026-02-01'
ORDER BY date DESC;
```

#### Individual Stock Liquidity
```sql
-- Get liquidity for top stocks
SELECT 
    stock_code,
    stock_name,
    turnover,
    average_spread,
    bid_ask_spread,
    liquidity_score
FROM stock_liquidity
WHERE date = CURRENT_DATE
    AND turnover > 100000000
ORDER BY turnover DESC
LIMIT 20;
```

## Data Formats

### Real-time Data Format
```json
{
  "timestamp": "2026-02-15T16:00:00Z",
  "market_overview": {
    "indices": [
      {
        "code": "HSI",
        "name": "恒生指数",
        "price": 18500.00,
        "change": 222.00,
        "change_pct": 1.21,
        "volume": 120000000000,
        "turnover": 450000000000
      }
    ],
    "sectors": [
      {
        "code": "TECH",
        "name": "科技",
        "change_pct": 2.1,
        "flow": 1500000000,
        "relative_strength": 1.75
      }
    ]
  }
}
```

### Historical Data Format
```json
{
  "date": "2026-02-15",
  "indices": {
    "HSI": {
      "open": 18278.00,
      "high": 18550.00,
      "low": 18250.00,
      "close": 18500.00,
      "volume": 120000000000,
      "turnover": 450000000000
    }
  },
  "sectors": {
    "TECH": {
      "close": 4200.00,
      "change_pct": 2.1,
      "volume": 32000000000
    }
  }
}
```

## API Integration

### Authentication
```python
import requests

# HKEX API authentication
headers = {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
}
```

### Real-time Data Request
```python
def get_market_overview():
    url = "https://api.hkex.com.hk/market-data/real-time/overview"
    response = requests.get(url, headers=headers)
    return response.json()

def get_sector_performance():
    url = "https://api.hkex.com.hk/market-data/real-time/sectors"
    response = requests.get(url, headers=headers)
    return response.json()
```

### Historical Data Request
```python
def get_historical_data(index_code, start_date, end_date):
    url = f"https://api.hkex.com.hk/market-data/historical/{index_code}"
    params = {
        'start_date': start_date,
        'end_date': end_date
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()
```

## Data Processing

### Data Cleaning
```python
def clean_market_data(data):
    """Clean and validate market data"""
    # Remove outliers
    data = remove_outliers(data, threshold=3)
    
    # Handle missing values
    data = fill_missing_values(data, method='forward_fill')
    
    # Validate data ranges
    data = validate_ranges(data)
    
    return data
```

### Data Aggregation
```python
def calculate_sector_returns(sector_stocks):
    """Calculate sector returns from constituent stocks"""
    sector_returns = {}
    for sector, stocks in sector_stocks.items():
        weights = calculate_market_cap_weights(stocks)
        returns = calculate_weighted_returns(stocks, weights)
        sector_returns[sector] = returns
    
    return sector_returns
```

### Data Transformation
```python
def calculate_technical_indicators(price_data):
    """Calculate technical indicators"""
    data = price_data.copy()
    
    # Moving averages
    data['MA5'] = data['close'].rolling(window=5).mean()
    data['MA20'] = data['close'].rolling(window=20).mean()
    
    # RSI
    data['RSI'] = calculate_rsi(data['close'])
    
    # MACD
    data['MACD'] = calculate_macd(data['close'])
    
    return data
```

## Quality Control

### Data Validation Rules
```python
def validate_market_data(data):
    """Validate market data quality"""
    errors = []
    
    # Check for missing values
    if data.isnull().any().any():
        errors.append("Missing values detected")
    
    # Check for outliers
    outliers = detect_outliers(data)
    if outliers:
        errors.append(f"Outliers detected: {outliers}")
    
    # Check data consistency
    if not check_data_consistency(data):
        errors.append("Data inconsistency detected")
    
    return errors
```

### Data Completeness Check
```python
def check_data_completeness(date):
    """Check if all required data is available for a date"""
    required_data = [
        'market_overview',
        'sector_performance',
        'market_sentiment',
        'liquidity_metrics'
    ]
    
    missing_data = []
    for data_type in required_data:
        if not data_exists(date, data_type):
            missing_data.append(data_type)
    
    return missing_data
```

## Performance Optimization

### Query Optimization
```sql
-- Optimized query for market overview
CREATE INDEX idx_market_overview_timestamp ON market_overview_realtime(timestamp);
CREATE INDEX idx_sector_performance_date ON sector_performance(date);
CREATE INDEX idx_market_sentiment_date ON market_sentiment(date);
```

### Caching Strategy
```python
# Cache frequently accessed data
cache_config = {
    'market_overview': {'ttl': 60},  # 1 minute
    'sector_performance': {'ttl': 300},  # 5 minutes
    'historical_data': {'ttl': 86400},  # 1 day
}
```

## Error Handling

### Common Error Scenarios
```python
def handle_api_errors(response):
    """Handle common API errors"""
    if response.status_code == 429:
        return "Rate limit exceeded, please retry later"
    elif response.status_code == 500:
        return "Server error, please try again"
    elif response.status_code == 401:
        return "Authentication failed, check API key"
    else:
        return f"Unknown error: {response.status_code}"
```

### Data Recovery
```python
def recover_missing_data(date, data_type):
    """Recover missing data from alternative sources"""
    # Try backup data sources
    backup_sources = ['bloomberg', 'reuters', 'wind']
    
    for source in backup_sources:
        try:
            data = fetch_from_source(source, date, data_type)
            if validate_data(data):
                return data
        except Exception:
            continue
    
    # Use interpolation if no backup available
    return interpolate_data(date, data_type)
```

---

*港股市场概览数据查询 - 完整的数据获取和处理指南*
