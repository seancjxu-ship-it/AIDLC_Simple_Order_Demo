"""Tiny order service used by the AIDLC demo. / AIDLC演示使用的极简订单服务。"""


class OrderService:
    """In-memory service with an intentionally incomplete baseline.

    内存订单服务；初始基线故意保留未完成的幂等能力。
    """

    def __init__(self) -> None:
        self.orders = {"ORDER-1001": {"status": "PAID"}}
        self.audit_events: list[dict[str, str]] = []
        self.replay_cache: dict[str, dict[str, str]] = {}

    def cancel_order(self, order_id: str, idempotency_key: str) -> dict[str, str]:
        """Cancel a paid order. / 取消一个已支付订单。"""

        # REQ-KEY: Reject an empty idempotency key before changing state.
        # REQ-KEY：在修改状态之前拒绝空的幂等键。
        if not idempotency_key:
            raise ValueError("IDEMPOTENCY_KEY_REQUIRED")

        # REQ-REPLAY: If the key exists in replay_cache, return the stored
        # response immediately. This check must happen before the CANCELLED
        # state check so a duplicate request is replayed, not rejected.
        # REQ-REPLAY：如果键已存在于replay_cache，立即返回已保存的响应。
        # 此检查必须位于CANCELLED状态检查之前，否则重复请求会被拒绝而非重放。
        if idempotency_key in self.replay_cache:
            return self.replay_cache[idempotency_key]

        # REQ-NOT-FOUND: An unknown order returns ORDER_NOT_FOUND.
        # REQ-NOT-FOUND：未知订单返回ORDER_NOT_FOUND。
        order = self.orders.get(order_id)
        if order is None:
            raise ValueError("ORDER_NOT_FOUND")
        if order["status"] == "CANCELLED":
            raise ValueError("ORDER_ALREADY_CANCELLED")

        # REQ-CANCEL: Cancel the order, create one audit event, and save the
        # response in replay_cache so repeated keys replay without a duplicate
        # audit event (REQ-AUDIT).
        # REQ-CANCEL：取消订单、生成一条审计事件，并把响应保存到replay_cache，
        # 使重复幂等键重放且不产生重复审计事件（REQ-AUDIT）。
        order["status"] = "CANCELLED"
        result = {"order_id": order_id, "status": "CANCELLED"}
        self.audit_events.append({"event": "ORDER_CANCELLED", "order_id": order_id})
        self.replay_cache[idempotency_key] = result
        return result
