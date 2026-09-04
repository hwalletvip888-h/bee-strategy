#!/usr/bin/env python3
"""蜂王震荡套利策略 —— 信号生成。

规律（用户实战验证）：
  冲高失败 = 阻力（价格反复冲到某个高点、收盘却站不上 = 被挡回来）-> 涨到阻力做空
  探底失败 = 支撑（价格反复跌到某个低点、收盘却跌不破 = 被挡回来）-> 跌到支撑做多

信号（写入 signals/latest.json，9 字段）：
  strategy_id / symbol / direction / quantity / price / stop_loss / take_profit / confidence / timestamp

止盈止损：止盈 +3%、止损 -2%（价格反向百分比）。
"""
import json
import subprocess
from datetime import datetime, timezone


def emit_signal(strategy_id, symbol, direction, quantity, price, stop_loss, take_profit, confidence):
    signal = {
        "strategy_id": strategy_id,
        "symbol": symbol,
        "direction": direction,
        "quantity": str(quantity),
        "price": str(price),
        "stop_loss": str(stop_loss),
        "take_profit": str(take_profit),
        "confidence": confidence,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    with open("signals/latest.json", "w", encoding="utf-8") as f:
        json.dump(signal, f, ensure_ascii=False, indent=2)

    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    with open(f"history/{date_str}.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(signal) + "\n")

    subprocess.run(["git", "add", "signals/latest.json", f"history/{date_str}.json"])
    subprocess.run(["git", "commit", "-m", f"signal: {direction} {symbol} @ {price}"])
    subprocess.run(["git", "push"])
    print(f"[信号已推] {direction} {symbol} @ {price} 止损 {stop_loss} 止盈 {take_profit}")


if __name__ == "__main__":
    # 示例：XRP 现价 1.4626 贴近阻力 1.4842，做空；止盈跌 3%、止损涨 2%
    emit_signal(
        strategy_id="xrp_swing_v1",
        symbol="XRP-USDT-SWAP",
        direction="short",
        quantity=10,
        price=1.4626,
        stop_loss=1.4919,
        take_profit=1.4187,
        confidence=0.8,
    )
