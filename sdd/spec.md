# FEAT-001 — Idempotent Order Cancellation / 幂等取消订单

## English

### Goal

Make repeated cancellation requests safe when the caller supplies the same idempotency key.

### Requirements

- **REQ-KEY:** Reject an empty idempotency key with `IDEMPOTENCY_KEY_REQUIRED`.
- **REQ-CANCEL:** The first valid request changes `PAID` to `CANCELLED`.
- **REQ-REPLAY:** A repeated key returns the original successful response.
- **REQ-AUDIT:** A repeated key must not create a second audit event.
- **REQ-NOT-FOUND:** An unknown order returns `ORDER_NOT_FOUND`.

### Non-goals

- No database, HTTP server, authentication, payment reversal, or distributed locking.
- Do not change public method names or test commands.

## 中文

### 目标

调用方使用相同幂等键时，重复的取消请求必须安全。

### 需求

- **REQ-KEY：** 空幂等键必须返回`IDEMPOTENCY_KEY_REQUIRED`。
- **REQ-CANCEL：** 第一次有效请求把状态从`PAID`改为`CANCELLED`。
- **REQ-REPLAY：** 重复幂等键返回第一次成功响应。
- **REQ-AUDIT：** 重复幂等键不得产生第二条审计事件。
- **REQ-NOT-FOUND：** 未知订单返回`ORDER_NOT_FOUND`。

### 非目标

- 不引入数据库、HTTP服务、认证、退款或分布式锁。
- 不修改公共方法名和测试命令。

