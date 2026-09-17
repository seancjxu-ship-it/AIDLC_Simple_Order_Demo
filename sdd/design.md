# Minimal Design / 最小设计

## English

Keep the solution inside `src/order_service.py`.

1. Validate `idempotency_key` before changing state.
2. If the key exists in `replay_cache`, return the stored response immediately.
3. Validate the order and its current state.
4. Cancel the order, create one audit event, and save the response in `replay_cache`.

The replay check must happen before the `CANCELLED` state check; otherwise a duplicate request is rejected instead of replayed.

## 中文

修改范围保持在`src/order_service.py`内。

1. 修改状态之前校验`idempotency_key`。
2. 如果键已存在于`replay_cache`，立即返回已保存的响应。
3. 校验订单和当前状态。
4. 取消订单、生成一条审计事件，并把响应保存到`replay_cache`。

重放检查必须位于`CANCELLED`状态检查之前，否则重复请求会被拒绝，而不是返回第一次结果。

