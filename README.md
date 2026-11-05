# Features
Send Email: MY_EMAIL, TO_EMAIL, MY_PASSWORD
Stock Alerts: STOCK_API_KEY
Flight Alerts: SERPAPI_API_KEY

Backlog Stories
1. Flag to switch between local and github code
2. Get data from google sheets instead of local excel (H) / Use DB
3. Get data for ReIT & InvIT
4. Put in available flight permutations (H)

Nifty REITs & InvITs
| S. No. | Name                                      | Symbol     | Allocation | Share Price | Best Price | Return | 
|--------|-------------------------------------------|------------|------------|-------------|------------|--------|-
| 1.     | Embassy Office Parks ReIT                 | EMBASSY.BO | 25.84 %    | Rs. 423     | 400 - 420  | 6.08 % | 
| 2.     | Brookfield India Real Estate Trust        | BIRET.BO   | 15.42 %    | Rs. 314     | 285 - 300  | 6.92 % | 
| 3.     | Nexus Select Trust                        | Symbol     | 13.26%     | Rs. 159     | Best Price | 5.84 % | 
| 4.     | IndiGrid Infrastructure Trust ***         | Symbol     | 11.37%     | Rs. 146     | Best Price | 9.56 % | 
| 5.     | Knowledge Realty Trust                    | Symbol     | 7.60%      | Rs. 112     | Best Price | 5.72 % | 
| 6.     | Mindspace Business Parks ReIT             | Symbol     | 7.20%      | Rs. 492     | Best Price | 5.07 % | 
| 7.     | Powergrid Infrastructure Investment Trust | Symbol     | 5.19%      | Rs. 103     | Best Price | 2.4  % | 
| 8.     | IRB InvIT Fund                ***         | Symbol     | 4.46%      | Rs. 63      | Best Price | 9.94 % | 
| 9.     | Raajmarg Infra Investment Trust           | Symbol     | 3.22%      | Rs. 121     | Best Price | 1.98 % | 
| 10.    | Indus Infra Trust             **          | Symbol     | 2.25%      | Rs. 126     | Best Price | 10.9 % | 
| 11.    | Capital Infra Trust           **          | Symbol     | 0%         | Rs. 77      | Best Price | 13.3 % | 

**ITC** — 5.61% FMCG + hotels + paper, strong brands and pricing power, defensive during downturns, long uninterrupted dividend history.
Lower yield than the PSUs but a genuinely inflation-resistant business, which matters over a retirement horizon. 
Risk is regulatory/taxation action on the cigarette business, which still drives most profit.

## API Usage Limits
- Stock - Limit 25 Requests Per Day - Using 6 / 21 - www.alphavantage.co
- Flight - Limit 250 Calls Per Month & 50 Calls Per Hour (27th) - Using 2 weekly / daily (~8 / 60 monthly) - serpapi.com

Stocks Excel - CONDITION_OPERATORS = {">": gt,"<": lt,"=": eq,"!=": ne,"<=": le,">=": ge}
