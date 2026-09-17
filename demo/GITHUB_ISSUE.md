# Make cancellation idempotent / 让取消订单支持幂等

## English request

As an order API owner, I need repeated cancellation requests with the same idempotency key to return the original result, so that client retries do not create inconsistent behavior or duplicate audit events.

Acceptance criteria:

1. Empty keys return `IDEMPOTENCY_KEY_REQUIRED`.
2. The first valid cancellation succeeds.
3. Repeating the same key returns the original response.
4. Only one audit event is created.
5. All four repository tests pass.

Constraints: change only `src/order_service.py`; do not add dependencies.

## 中文需求

作为订单API负责人，我希望使用相同幂等键的重复取消请求返回第一次结果，避免客户端重试导致行为不一致或产生重复审计事件。

验收条件：

1. 空幂等键返回`IDEMPOTENCY_KEY_REQUIRED`。
2. 第一次有效取消成功。
3. 使用相同键重试时返回第一次响应。
4. 只产生一条审计事件。
5. 仓库中的四个测试全部通过。

约束：只修改`src/order_service.py`，不得新增依赖。

