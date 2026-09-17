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

        order = self.orders.get(order_id)
        if order is None:
            raise ValueError("ORDER_NOT_FOUND")
        if order["status"] == "CANCELLED":
            raise ValueError("ORDER_ALREADY_CANCELLED")

        # Baseline gap 1: an empty idempotency key is currently accepted.
        # 基线缺陷1：当前仍然接受空的幂等键。
        # Baseline gap 2: repeated keys are not replayed from replay_cache.
        # 基线缺陷2：重复幂等键尚未从replay_cache返回原结果。
        order["status"] = "CANCELLED"
        result = {"order_id": order_id, "status": "CANCELLED"}
        self.audit_events.append({"event": "ORDER_CANCELLED", "order_id": order_id})
        return result

