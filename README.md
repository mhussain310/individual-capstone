# Weather Conditions and IBM's Stock Market Movements - Project Plan

## Getting Started (Locally)

1. Obtain API keys from [WeatherAPI](https://www.weatherapi.com/) (for weather data) and [AlphaVantage](https://www.alphavantage.co/) (for stock data).
2. Ensure you are at the root of the project directory and create a `.env` file.
3. Copy the snippet below into your `.env` file and add in your API keys where necessary. (Do **NOT** change the names of the variables).

```env
# API Keys
WEATHER_API_KEY=<INSERT YOUR WeatherAPI API KEY HERE>
STOCK_API_KEY=<INSERT YOUR AlphaVantage API KEY HERE>

# Database Configuration for development (sqlite db)
DB_NAME=data/database.db
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

4. Open a terminal, and ensure you are the root of the project directory.
5. Create a virtual environment and activate it.

```bash
python -m venv venv
source venv/bin/activate      # On macOS/Linux
source venv\Scripts\activate       # On Windows
```

6. Run `pip install -r requirements-setup.txt`.
7. Finally, run `pip install -e .` to install the project as a package.
8. To run the ETL pipeline, run `python scripts/run_etl.py`.
9. To run the Streamlit App, run `streamlit run scripts/app.py`.

## Problem Statement

**Is there a relationship between weather conditions and IBM's stock market movements?**

### Why Investigate This?

Stock market movements are influenced by various factors. However, recent studies suggest that weather conditions may also play a role in market fluctuations. I often find myself being less productive on days when there is little to no sunshine, compared to days when there are. So, I want to know if that is also the case with the stock market, particularly focusing on IBM after a recent trip to their headquarters. With this project, I aim to explore the relationship between weather conditions and IBM's stock market trends using real-time and historical data.

## User Stories & Acceptance Criteria

### **User Story 1: Extract and Process Weather Data**

```txt
As a data engineer, I want to fetch historical and real-time weather data so that I can analyse its potential impact on IBM's stock market trends.
```

**Acceptance Criteria:**

- The system should retrieve current weather data (such as temperature, humidity, wind speed) from a Weather API.
- The system should store current weather data into a source database.
- The system should periodically run to retrieve the current weather data.

### **User Story 2: Extract and Process IBM Stock Market Data**

```txt
As a data engineer, I want to collect IBM's stock market data so that I can compare it with weather data.
```

**Acceptance Criteria:**

- The system should fetch historical and real-time IBM stock market data from a Stock Market API.
- The system should store IBM stock data in a structured format for analysis.

### **User Story 3: Data Cleaning and Preparation**

```txt
As a data engineer, I want to clean the collected data so that it is ready for analysis.
```

**Acceptance Criteria:**

- The system should handle missing or incomplete weather and IBM stock data.
- The system should standardise date and time formats.

### **User Story 4: Analyse Correlations Between Weather and IBM's Stock Movements**

```txt
As a data engineer, I want to perform analysis to determine whether weather conditions correlate with IBM's stock market movements.
```

**Acceptance Criteria:**

- The system should calculate aggregations between weather variables and IBM stock price changes.
- The system should generate visualizations to illustrate trends.
- The system should provide a summary of the findings.

### **User Story 5: Build a Streamlit App for Visualization**

```txt
As a user, I want to view interactive charts and insights on a web-based dashboard so that I can explore trends in an intuitive way.
```

**Acceptance Criteria:**

- The system should display historical IBM stock market and weather data.
- The system should allow users to filter data based on time periods and locations.
- The system should include interactive visualizations to explore correlations.

## Definition of Done

- [ ] Weather data is successfully extracted and stored in a source database.
- [ ] IBM stock market data is successfully extracted and stored in a structured format.
- [ ] Data is cleaned and formatted for analysis.
- [ ] Analysis is performed, and correlations are assessed.
- [ ] Visualizations and insights are generated in a Streamlit dashboard.

## Tools & Technologies

- **Weather API**: WeatherAPI
- **Stock Market API**: Alpha Vantage
- **Python Libraries**: Pandas, Matplotlib, Seaborn, Streamlit

## High-Level Flowchart

```mermaid
graph TD;
A[Start] --> B[Extract Historical Weather Data from API];
A --> C[Extract IBM Stock Market Data from API. Includes current and historical data];
A --> X[Extract Current Weather Data from API];
X --> Y[Clean Current Weather Data];
B --> D[Clean Historical Weather Data];
C --> E[Clean Stock Market Data];
Y --> F[Merge Current Weather & Stock Data];
E --> F;
E --> G;
D --> G[Merge Historical Weather & Stock Data];
F --> H[Perform Analysis];
G --> H;
H --> I[Generate Visualisations];
I --> J[Develop Streamlit App];
J --> K[End];
```
