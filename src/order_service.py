"""Tiny order service used by the AIDLC demo. / AIDLC演示使用的极简订单服务。"""


class OrderService:
    """In-memory service with idempotent order cancellation.

    内存订单服务；支持幂等取消订单。
    """

    def __init__(self) -> None:
        self.orders = {"ORDER-1001": {"status": "PAID"}}
        self.audit_events: list[dict[str, str]] = []
        self.replay_cache: dict[str, dict[str, str]] = {}

    def cancel_order(self, order_id: str, idempotency_key: str) -> dict[str, str]:
        """Cancel a paid order. / 取消一个已支付订单。"""

        if not idempotency_key:
            raise ValueError("IDEMPOTENCY_KEY_REQUIRED")

        if idempotency_key in self.replay_cache:
            return self.replay_cache[idempotency_key]

        order = self.orders.get(order_id)
        if order is None:
            raise ValueError("ORDER_NOT_FOUND")
        if order["status"] == "CANCELLED":
            raise ValueError("ORDER_ALREADY_CANCELLED")

        order["status"] = "CANCELLED"
        result = {"order_id": order_id, "status": "CANCELLED"}
        self.audit_events.append({"event": "ORDER_CANCELLED", "order_id": order_id})
        self.replay_cache[idempotency_key] = result
        return result
