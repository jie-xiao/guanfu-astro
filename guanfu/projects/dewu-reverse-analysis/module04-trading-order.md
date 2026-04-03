# 得物小程序逆向分析 - 交易模块（知微负责）

## 一、订单状态机

```javascript
订单状态枚举：
├── unpaid      // 待付款
├── unShipped   // 待发货
├── shipped     // 已发货
├── completed   // 已完成
├── cancelled   // 已取消
└── closed      // 已关闭

关联组件：
├── statusInfo        // 状态信息
├── OrderStatus       // 订单状态组件
├── StatusHeader      // 状态头部
└── logisticInfo      // 物流信息
```

## 二、核心API

| API | 方法 | 版本 | 用途 |
|-----|------|------|------|
| `/api/v1/h5/biz-aggregate/h5/buy/createOrder` | POST | v5.48.0 | 创建订单 |
| `/api/v1/h5/biz-aggregate/h5/buy/confirmOrder` | POST | v5.23.0/5.75.0 | 确认订单 |
| `/api/v1/h5/biz-aggregate/buyerH5OrderQueryUnitApi/queryDetailH5` | GET | v5.22.0 | 订单详情 |
| `/api/v1/h5/biz-aggregate/userInformation-biz/userInfoAddressApi/parseStreetForH5` | POST | - | 地址解析 |

## 三、支付体系

```javascript
支付方法（PayMethodEnum）：
├── wxPayment    // 微信支付
├── aliPayment   // 支付宝
└── QQPayment    // QQ钱包

回调机制：microSendOrder
├── 发送支付 → 等待回调
├── SUCCESS → 订单成功
└── RETRY → 重试机制（最大N次）
```

## 四、反爬保护

```javascript
RESIST_PACHONG_APIS 重点保护：
├── /trade-price-center/price/h5/buy-layer  ← 价格核心
├── /index/fire/flow/product/detail
├── /search/fire/search/list
└── /commodity/fire/last-sold-list
```

## 五、订单组件架构

```
order/
├── OrderConfirmPage.html      // 订单确认（webview）
├── BuyPaySuccessPageV2       // 支付成功页
├── CancelOrder               // 取消订单
├── ShippingDetailPage        // 物流详情
├── buyer/
│   ├── OrderDetail/         // 订单详情（webview）
│   │   ├── statusInfo       // 状态信息
│   │   ├── address         // 收货地址
│   │   ├── brandInfo       // 品牌信息
│   │   ├── logisticInfo    // 物流
│   │   └── buttonsArea     // 操作按钮
│   ├── orderList/          // 订单列表
│   └── CancelSuccessful/    // 取消成功
├── wxpay/cashier            // 微信收银台
└── alipay/cashier           // 支付宝收银台
```

## 六、完整交易流程

```
1. 创建订单: POST /biz-aggregate/h5/buy/createOrder
2. 获取地址: POST /userInformation-biz/userInfoAddressApi/parseStreetForH5
3. 选择优惠: order/components/couponListModal
4. 确认订单: POST /biz-aggregate/h5/buy/confirmOrder
5. 发起支付: sendPayment → wxPayment/aliPayment/QQPayment
```

## 七、分析结论

1. **订单服务中台化**：`biz-aggregate`聚合多个下游服务
2. **支付多样化**：支持微信/支付宝/QQ三种支付
3. **反爬体系完善**：价格接口等重点保护
4. **Webview混合**：订单确认/详情使用webview渲染（安全考虑）

---
*分析人：知微*
*时间：2026-04-03*
