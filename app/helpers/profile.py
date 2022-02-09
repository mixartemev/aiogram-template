import decimal

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload, raiseload, subqueryload, immediateload, noload, lazyload
from sqlalchemy.sql import Select

from app.models import Forex, Order, Tsaction, User, IpoOrder, IpoTrade, Stock


class Profile:
    """User portfolio representation"""
    tsactions: list[Tsaction]
    forexes: list[Forex]
    orders: dict[set[Order]] = {}
    trades: dict[set[Order]] = {}
    ipo_orders: list[IpoOrder]
    ipo_trades: list[IpoTrade]

    def __init__(self, uid: int):
        """Dependencies inject"""
        self.uid = uid

    async def load(self, db: AsyncSession, only: int = None):  # only: {0: tscts, 1: frxs, 2: ordrs, 3: ios, 4: its}
        """Load data from db"""
        # user: User = await db.get(User, self.uid) todo set user relations in async mode
        if only:
            await (self._tsacts, self._forexes, self._orders, self._ipo_orders, self._ipo_trades)[only](db)
        else:
            await self._tsacts(db)
            await self._forexes(db)
            await self._orders(db)
            await self._ipo_orders(db)
            await self._ipo_trades(db)
        return self

    async def _tsacts(self, db):
        stmt: Select = select(Tsaction).where(Tsaction.user_id == self.uid)
        self.tsactions = (await db.execute(stmt)).scalars().all()  # Money transfers

    async def _forexes(self, db):
        stmt: Select = select(Forex).where(Forex.user_id == self.uid)
        self.forexes = (await db.execute(stmt)).scalars().all()  # Currency changes (now only 1)

    async def _orders(self, db):
        deals = {}
        for cur in [0, 1, 2]:  # ₽, $, €
            stmt: Select = select(Order, Stock.cur).join(Stock).where(Order.user_id == self.uid, Stock.cur == cur)
            deals[cur]: dict[Order] = (await db.execute(stmt)).scalars().all()   # All orders (executed and not)
            if deals[cur]:
                self.trades[cur] = set(filter(lambda o: o.executed_at, deals[cur]))
                self.orders[cur] = set(deals[cur]) - self.trades[cur]

    async def _ipo_orders(self, db):
        stmt: Select = select(IpoOrder).options(selectinload(IpoOrder.ipo)) \
            .where(IpoOrder.user_id == self.uid).where(IpoOrder.status == 0)
        self.ipo_orders: list[IpoOrder] = (await db.execute(stmt)).scalars().all()  # Ipo orders

    async def _ipo_trades(self, db):
        stmt: Select = select(IpoTrade).options(selectinload(IpoTrade.ipo)).where(IpoTrade.user_id == self.uid)
        self.ipo_trades: list[IpoTrade] = (await db.execute(stmt)).scalars().all()  # Ipo trades

    def tsact_dif(self) -> decimal:
        """Money transfers sum (inputs + outputs)"""
        return sum(t.amount for t in self.tsactions)

    def forex_diffs(self, cur: int = 0) -> (decimal, decimal):
        """Money transfers sum (inputs + outputs)"""
        return sum(-f.rate * f.qty if cur == 1 else f.qty if cur == f.cur else 0 for f in self.forexes)

    # - ORDERS RESERVE - #
    def reserved(self, cur: int = 0) -> decimal:
        """Reserved money for not executed buy all orders"""
        return self._stock_reserved(cur) + self._ipo_reserved(cur)

    def _stock_reserved(self, cur: int = 0) -> decimal:
        """Reserved money for not executed buy stock orders"""
        if orders := self.orders.get(cur):
            orders = list(filter(lambda o: o.qty > 0, orders))
            return sum(o.qty * o.price for o in orders)
        return 0

    def _ipo_reserved(self, cur: int = 1) -> decimal:
        """Reserved money for not executed ipo orders"""
        ipo_orders = list(filter(lambda o: o.ipo.cur == cur, self.ipo_orders))
        return sum(io.amount for io in ipo_orders)
    # - ORDERS RESERVE - #

    # - DEALS PROFIT - #
    def profit(self, cur: int = 0) -> decimal:
        """Profit from all trades"""
        return self._stock_profit(cur) + self._ipo_profit(cur)

    def _stock_profit(self, cur: int = 0) -> decimal:
        """Profit from stock trades(=executed orders)"""
        return sum(-t.qty * t.price for t in tr) if (tr := self.trades.get(cur)) else 0

    def _ipo_profit(self, cur: int = 0) -> decimal:
        """Profit from ipo_trades"""
        ipo_trades = filter(lambda it: it.ipo.cur == cur, self.ipo_trades)
        return sum(-it.qty * it.price for it in ipo_trades)
    # - DEALS PROFIT - #

    def balance(self, cur: int = 0, with_reserve: bool = True) -> decimal:
        """Current spendable balance"""
        bal = self.forex_diffs(cur) + self.profit(cur)
        if cur == 0:
            bal += self.tsact_dif()
        if not with_reserve:
            bal -= self.reserved(cur)
        return bal

    def qty_can_sell(self, stock: Stock) -> int:
        """How much has this stocks"""
        return sum(-o.qty if o.qty > 0 and o.stock_id == stock.id else 0 for o in self.trades.get(stock.cur))
