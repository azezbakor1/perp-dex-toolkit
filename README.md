# Perp DEX Tools — Multi-Exchange Trading Bot

![Python](https://img.shields.io/badge/Python-3.8%2B%20|%203.10–3.12-blue)
![License](https://img.shields.io/badge/License-Non--Commercial-lightgrey)
![Exchanges](https://img.shields.io/badge/Exchanges-EdgeX%20|%20Backpack%20|%20Paradex%20|%20Aster%20|%20Lighter%20|%20GRVT%20|%20Extended-success)

## Multi-Exchange Trading Bot

A modular trading bot supporting multiple exchanges (currently EdgeX, Backpack, Paradex, Aster, Lighter, GRVT, and Extended). The bot implements a strategy that places limit orders near market price and closes at a configured take-profit level—useful for building sustained trading volume with controlled wear.

## Referral Links (Rebates & Benefits)

#### EdgeX: [https://pro.edgex.exchange/referral/QUANT](https://pro.edgex.exchange/referral/QUANT)

Instant VIP 1 fees, +10% fee rebate, +10% bonus points.

#### Backpack: [https://backpack.exchange/join/quant](https://backpack.exchange/join/quant)

35% fee rebate via referral.

#### Paradex: [https://app.paradex.trade/r/quant](https://app.paradex.trade/r/quant)

10% taker fee rebate plus potential future benefits.

#### Aster: [https://www.asterdex.com/zh-CN/referral/5191B1](https://www.asterdex.com/zh-CN/referral/5191B1)

30% fee rebate and points boost.

#### GRVT: [https://grvt.io/exchange/sign-up?ref=QUANT](https://grvt.io/exchange/sign-up?ref=QUANT)

Up to 1.3× points boost (network-wide cap), automated rebates (per official timeline), and access to private trading competitions.

#### Extended: [https://app.extended.exchange/join/QUANT](https://app.extended.exchange/join/QUANT)

10% immediate fee discount; points boost (typically higher via ambassador referral than self-referral per docs); access to private volume competitions (prize pools up to $70,000; subject to official announcements).

## Installation

Recommended Python versions: 3.10–3.12

- GRVT requires Python ≥ 3.10
- Paradex requires Python 3.9–3.12
- Other exchanges require Python ≥ 3.8

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd perp-dex-tools
   ```

2. **Create and activate a virtual environment**

   Ensure you are not currently in any virtual environment:

   ```bash
   deactivate
   ```

   Create the environment:

   ```bash
   python3 -m venv env
   ```

   Activate the environment (activate before each use):

   ```bash
   source env/bin/activate  # Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   If switching environments, first ensure no venv is active:

   ```bash
   deactivate
   ```

   Activate the environment (activate before each use):

   ```bash
   source env/bin/activate  # Windows: env\Scripts\activate
   ```

   ```bash
   pip install -r requirements.txt
   ```

   **GRVT users**: additionally install the GRVT SDK:
   Activate the environment:

   ```bash
   source env/bin/activate  # Windows: env\Scripts\activate
   ```

   ```bash
   pip install grvt-pysdk
   ```

   **Paradex users**: use a dedicated virtual environment and install Paradex-specific dependencies:

   Ensure no venv is active:

   ```bash
   deactivate
   ```

   Create a dedicated environment (e.g., `para_env`):

   ```bash
   python3 -m venv para_env
   ```

   Activate the environment:

   ```bash
   source para_env/bin/activate  # Windows: para_env\Scripts\activate
   ```

   Install Paradex dependencies:

   ```bash
   pip install -r para_requirements.txt
   ```

4. **Environment variables**
   Create a `.env` file in the project root. Use `env_example.txt` as a template and fill in API keys/config for the exchanges you plan to use.

5. **Telegram bot (optional)**
   To receive notifications, follow the guide: [Telegram Bot Setup](docs/telegram-bot-setup-en.md).

## Strategy Overview

Before using this project, make sure you understand the strategy and its risks so you can configure parameters appropriately. The core idea is to place limit orders near market price, then close promptly at a configured take-profit level, aiming to accumulate volume with low wear over longer horizons.

In general, very small `--quantity` and very short `--wait-time` suit short-term, high-intensity volume pushes but may increase long-term wear. Tune parameters based on market conditions and your goals. For example (not prescriptive), a `wait-time` in the 450–650 second range can help maintain rhythm in choppy markets; scale `quantity` in line with your account size and risk tolerance.

### Core Workflow

1. Place limit orders near market
2. Monitor orders until filled
3. Place take-profit close orders
4. Manage positions and active orders
5. Cap concurrent orders for risk control
6. Use `--grid-step` to space close levels
7. Use `--stop-price` to halt trading

#### ⚙️ Key Parameters

- **quantity**: Order size per trade
- **direction**: Trading direction; `buy` for long, `sell` for short
- **take-profit**: Take-profit percentage (e.g., 0.02 means 0.02%)
- **max-orders**: Maximum concurrent active orders
- **wait-time**: Delay between orders (rate limiting)
- **grid-step**: Minimum spacing between this trade’s take-profit and the nearest existing close order
- **stop-price**: Price threshold to stop trading and exit
- **pause-price**: Price threshold to pause trading (resumes when price re-enters)

#### Grid Step

`--grid-step` constrains the minimum distance between the new trade’s intended close price and the nearest existing close order:

- Default -100: Disabled; no spacing constraint
- Positive (e.g., 0.5): Close must be at least 0.5% away from the nearest close
- Purpose: Reduce close-level clustering and improve execution/risk profile

Example (long with `--grid-step 0.5`):

- Existing close at 2000 USDT
- New close must be below 1990 USDT (2000 × (1 − 0.5%))
- Helps reduce density and improve overall strategy effectiveness

#### 📊 Example Flow

Assume ETH is $2000 and take-profit is 0.02%:

1. Open: Place buy at $2000.40 (slightly above market)
2. Fill: Order fills; long position acquired
3. Close: Immediately place sell at $2000.80 (TP)
4. Complete: Close order fills; ~0.02% profit
5. Repeat: Continue to next cycle

#### 🛡️ Risks & Controls

- Cap concurrency via `max-orders`
- Maintain spacing via `grid-step`
- Control cadence with `wait-time` to avoid chase traps
- Continuously monitor positions and orders
- Important: No built-in stop-loss; strong trends can cause large unrealized or realized losses

## Usage Examples

### EdgeX

ETH:

```bash
python runbot.py --exchange edgex --ticker ETH --quantity 0.1 --take-profit 0.02 --max-orders 40 --wait-time 450
```

ETH (with grid step):

```bash
python runbot.py --exchange edgex --ticker ETH --quantity 0.1 --take-profit 0.02 --max-orders 40 --wait-time 450 --grid-step 0.5
```

ETH (with stop price):

```bash
python runbot.py --exchange edgex --ticker ETH --quantity 0.1 --take-profit 0.02 --max-orders 40 --wait-time 450 --stop-price 5500
```

BTC:

```bash
python runbot.py --exchange edgex --ticker BTC --quantity 0.05 --take-profit 0.02 --max-orders 40 --wait-time 450
```

### Backpack

ETH Perpetual:

```bash
python runbot.py --exchange backpack --ticker ETH --quantity 0.1 --take-profit 0.02 --max-orders 40 --wait-time 450
```

ETH Perpetual (with grid step):

```bash
python runbot.py --exchange backpack --ticker ETH --quantity 0.1 --take-profit 0.02 --max-orders 40 --wait-time 450 --grid-step 0.3
```

ETH Perpetual (Boost mode):

```bash
python runbot.py --exchange backpack --ticker ETH --direction buy --quantity 0.1 --boost
```

### Aster

ETH:

```bash
python runbot.py --exchange aster --ticker ETH --quantity 0.1 --take-profit 0.02 --max-orders 40 --wait-time 450
```

ETH (Boost mode):

```bash
python runbot.py --exchange aster --ticker ETH --direction buy --quantity 0.1 --boost
```

### GRVT

BTC:

```bash
python runbot.py --exchange grvt --ticker BTC --quantity 0.05 --take-profit 0.02 --max-orders 40 --wait-time 450
```

### Extended

ETH:

```bash
python runbot.py --exchange extended --ticker ETH --quantity 0.1 --take-profit 0 --max-orders 40 --wait-time 450 --grid-step 0.1
```

## 🆕 Hedge Mode

The new Hedge Mode (`hedge_mode.py`) establishes offsetting positions on two exchanges to reduce directional risk.

### How it works

1. Open: Place a maker order on the selected exchange (e.g., Backpack)
2. Hedge: Once filled, immediately place a market order on Lighter to hedge
3. Close: Place another maker order on the selected exchange to exit
4. Close hedge: Place a market order on Lighter to exit the hedge

### Examples

```bash
# Run BTC hedge mode
python hedge_mode.py --exchange backpack --ticker BTC --size 0.05 --iter 20

# Run ETH hedge mode
python hedge_mode.py --exchange backpack --ticker ETH --size 0.1 --iter 20
```

### Parameters

- `--exchange`: Primary exchange (currently supports `backpack`)
- `--ticker`: Trading pair (e.g., BTC, ETH)
- `--size`: Quantity per order
- `--iter`: Number of trading cycles
- `--fill-timeout`: Maker order fill timeout (seconds; default 5)

## Configuration

### Environment Variables

#### General

- `ACCOUNT_NAME`: Optional label for the current account (useful for multi-account logging)

#### Telegram (optional)

- `TELEGRAM_BOT_TOKEN`: Bot token
- `TELEGRAM_CHAT_ID`: Chat ID

#### EdgeX

- `EDGEX_ACCOUNT_ID`: Account ID
- `EDGEX_STARK_PRIVATE_KEY`: API private key
- `EDGEX_BASE_URL`: API base URL (default: `https://pro.edgex.exchange`)
- `EDGEX_WS_URL`: WebSocket URL (default: `wss://quote.edgex.exchange`)

#### Backpack

- `BACKPACK_PUBLIC_KEY`: API key
- `BACKPACK_SECRET_KEY`: API secret

#### Paradex

- `PARADEX_L1_ADDRESS`: L1 wallet address
- `PARADEX_L2_PRIVATE_KEY`: L2 wallet private key (Profile → Wallet → “Copy Paradex Private Key”)

#### Aster

- `ASTER_API_KEY`: API key
- `ASTER_SECRET_KEY`: API secret

#### Lighter

- `API_KEY_PRIVATE_KEY`: API private key
- `LIGHTER_ACCOUNT_INDEX`: Account index
- `LIGHTER_API_KEY_INDEX`: API key index

#### GRVT

- `GRVT_TRADING_ACCOUNT_ID`: Trading account ID
- `GRVT_PRIVATE_KEY`: Private key
- `GRVT_API_KEY`: API key

#### Extended

- `EXTENDED_API_KEY`: API key
- `EXTENDED_STARK_KEY_PUBLIC`: Stark public key (visible after creating API)
- `EXTENDED_STARK_KEY_PRIVATE`: Stark private key (visible after creating API)
- `EXTENDED_VAULT`: Vault ID (visible after creating API)

**How to get `LIGHTER_ACCOUNT_INDEX`**

1. Append your wallet address to the following URL:

   ```
   https://mainnet.zklighter.elliot.ai/api/v1/account?by=l1_address&value=
   ```

2. Open the URL in your browser.
3. Search for `account_index` in the result. If you have subaccounts, you’ll see multiple indices: shorter is the main account; longer values are subaccounts.

### Command-line Arguments

- `--exchange`: Exchange: `edgex`, `backpack`, `paradex`, `aster`, `lighter`, `grvt`, `extended` (default: `edgex`)
- `--ticker`: Base asset (e.g., ETH, BTC, SOL). Contract ID is auto-resolved
- `--quantity`: Order quantity (default: 0.1)
- `--take-profit`: Take-profit percent (e.g., 0.02 means 0.02%)
- `--direction`: `buy` or `sell` (default: `buy`)
- `--env-file`: Account config file (default: `.env`)
- `--max-orders`: Max active orders (default: 40)
- `--wait-time`: Wait time between orders in seconds (default: 450)
- `--grid-step`: Minimum distance to the nearest close order in percent (default: -100 means no limit)
- `--stop-price`: If `direction` is `buy` and `price >= stop-price`, stop trading and exit (`sell` is symmetric; default: -1 means disabled). Avoids continually placing at perceived tops/bottoms.
- `--pause-price`: If `direction` is `buy` and `price >= pause-price`, pause; resume when price falls back (`sell` symmetric; default: -1 means disabled). Helps avoid phase-specific overplacement.
- `--boost`: Enable Boost mode (Aster and Backpack only).
  Boost logic: open with a maker order, close immediately with a taker order, repeat. Wear primarily comes from one maker fee, one taker fee, and slippage.

## Logging

Comprehensive logging is provided:

- **Transaction logs**: CSV files with order details
- **Debug logs**: Detailed, timestamped activity logs
- **Console output**: Real-time status updates
- **Error handling**: Thorough error logs and handling

## Q&A

### How do I configure multiple accounts for the same exchange on one device?

1. Create one `.env` per account (e.g., `account_1.env`, `account_2.env`).
2. Set `ACCOUNT_NAME=` in each (e.g., `ACCOUNT_NAME=MAIN`).
3. Provide each account’s API key/secret in its file.
4. Start with the corresponding `--env-file`, e.g., `python runbot.py --env-file account_1.env [other args...]`.

### How do I configure multiple exchanges on one device?

Put credentials for different exchanges in the same `.env` and switch via `--exchange`, e.g., `python runbot.py --exchange backpack [other args...]`.

### How do I trade multiple contracts for the same account and exchange?

After configuring the account in `.env`, select a contract with `--ticker`, e.g., `python runbot.py --ticker ETH [other args...]`.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests when applicable
5. Submit a pull request

## Contact

- X (Twitter): [@yourQuantGuy](https://x.com/yourQuantGuy)
- Issues & feature requests: open a ticket in this repository’s `Issues` tab

## License

This project is distributed under a Non-Commercial License—see `[LICENSE](LICENSE)` for details.

Important: This software is for personal learning and research only. Commercial use is prohibited without written permission. For commercial licensing, contact the author.

## Disclaimer

This software is for educational and research purposes only. Digital asset trading is risky and can result in significant losses. Use caution and only risk capital you can afford to lose. Use at your own risk.
