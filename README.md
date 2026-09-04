# bee-strategy —— 蜂王震荡套利策略

> 冲高失败=阻力（涨到阻力做空）、探底失败=支撑（跌到支撑做多）。

## 策略

- **strategy_id**: `xrp_swing_v1`
- **标的**: XRP-USDT-SWAP（永续）
- **方向**: 现价贴近阻力 → 做空；贴近支撑 → 做多；中间 → 观望
- **止盈**: +3% ｜ **止损**: -2%

## 信号

出信号时写 `signals/latest.json`（9 字段），并 `git push` 触发交易机器人。

## 结构

```
bee-strategy/
├── strategy.py          # 信号生成脚本
├── signals/latest.json  # 最新信号
├── history/             # 历史信号归档
└── README.md
```
