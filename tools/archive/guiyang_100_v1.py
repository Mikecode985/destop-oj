#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""贵阳生活 100 题：题面、数据、参考解、C++ 答案都在这里生成。

每题都按标准 OJ 格式给出：任务、输入格式、输出格式、数据范围、样例、测试数据。
参考解同时提供 Python（用于生成期望输出）和 C++（写入 data/solutions）。
"""
import random

PROBLEMS = []
SOL = {}

INSTANCES = {
    "sum": [
        ("青云路夜市的摊位账本", "青云路夜市收摊后，摊主老周把每个摊位的营业额依次记在账本上。他想知道今晚整条街一共卖了多少，以及卖得最好的第一个摊位是几号。"),
        ("贵阳北站网约车接单量", "贵阳北站夜间接驳高峰，调度员按小时记录了网约车的接单量。请算出当晚总接单量，并找出接单量最高的第一个小时。"),
        ("黔灵山猕猴桃果园产量", "修文县谷堡镇的果农把每棵猕猴桃树的产量记成一串数字。请算出果园总产量，并指出产量最高的第一棵树。"),
        ("花果园快递柜取件量", "花果园半山小镇的快递柜按格口记录了当天取件量。物业想知道总取件量，以及取件最多的第一个格口号。"),
        ("地铁 1 号线各站客流", "早高峰结束后，贵阳地铁 1 号线从窦官到小孟工业园的每个站都报来了上车人数。请统计全线总客流，并找出客流最大的第一个站。"),
    ],
    "count": [
        ("贵阳的雨到底下了几天", "贵阳人说“天无三日晴”。气象站记录了连续 n 天的降雨量，降雨量达到 k 毫米才算一个有效雨天。请数一数有效雨天有几天。"),
        ("黔灵山猴子的体重普查", "黔灵山公园给一群猕猴称体重。饲养员想统计体重不低于 k 千克的猴子有多少只，好准备加餐。"),
        ("数博会单日客流预警", "数博会期间，入口闸机按天统计参观人数。安保组关心参观人数达到 k 人的日子有多少天，需要提前加派人手。"),
        ("观山湖公园的晨跑人数", "观山湖公园北门记录了连续 n 个清晨的跑者人数。体育局想统计人数不少于 k 的清晨有多少个。"),
        ("青岩古镇客栈的入住率", "青岩古镇一家客栈记录了连续 n 天的入住房间数。老板想统计入住数达到 k 间的天数，判断旺季是否真的来了。"),
    ],
    "sort": [
        ("青云路小吃价格榜", "青云路夜市的管理员要把各家小吃的价格整理成榜单：先按价格从低到高，价格相同的再按拼音名字从 A 到 Z。"),
        ("花溪大学城食堂窗口评分", "花溪大学城食堂要公示各窗口的评分。请按评分从低到高排序；评分相同的窗口按窗口拼音名排序。"),
        ("青岩古镇伴手礼价目表", "青岩古镇的伴手礼店把商品名和价格交给店员。请按价格升序打印价目表，同价的商品按名称升序。"),
        ("贵阳地铁沿线的二手房", "房产中介整理了一批地铁沿线小区，每个小区有一个拼音名和挂牌总价。请按总价从低到高列出，同价按名称排序。"),
        ("数博会参展商的展位面积", "数博会展馆要核对参展商面积。请按面积从小到大输出参展商名称和面积，面积相同的按名称排序。"),
    ],
    "range": [
        ("南明河分段水质采样", "南明河被分成 n 段，每段记录了一个水质指标。监测员会询问若干次“第 l 段到第 r 段的总指标是多少”。"),
        ("地铁 1 号线区间客流", "贵阳地铁 1 号线把相邻站点之间的客流记成 n 个数。调度中心想知道任意一段连续区间的客流总和。"),
        ("观山湖跑道分段计时", "观山湖公园的跑道被分成 n 段，每段有一个计时值。教练会问很多次“从第 l 段到第 r 段一共用了多少”。"),
        ("黔灵山台阶分段高度", "黔灵山的一条登山步道被分成 n 段，每段有固定爬升高度。游客想知道连续若干段的总爬升。"),
        ("花果园楼栋公摊电费", "花果园一栋楼的 n 层各自记录了公摊电费。物业要回答多次“第 l 层到第 r 层一共多少钱”。"),
    ],
    "rangeadd": [
        ("灯会临时摊位的人流增量", "观山湖灯会期间，沿湖 n 个点位的人流会因临时摊位增加。每次活动给 [l, r] 区间每个点位增加 x 人。所有活动结束后，求最大人流和总人流。"),
        ("南明河清淤施工影响", "南明河沿线 n 段同时施工，每次施工让 [l, r] 段的浑浊度增加 x。全部施工结束后，求最大浑浊度和总浑浊度。"),
        ("地铁站出入口客流叠加", "某地铁站有 n 个出入口，活动期间会有一批批乘客从 [l, r] 连续出入口进入，每个出入口增加 x 人。求最终最大客流和总客流。"),
        ("老旧小区加装电梯补贴", "某街道 n 个单元申请加装电梯，每批批复给 [l, r] 单元每户补贴 x 元。全部批复后求单户最高补贴和总补贴。"),
        ("青云路夜市的油烟监测", "青云路夜市 n 个摊位，每次集中烹饪会让 [l, r] 摊位的油烟值增加 x。夜市结束后求最高油烟值和油烟总和。"),
    ],
    "interval": [
        ("夜市摊位的时间段排班", "青云路夜市有 n 个摊位申请使用同一条过道，每个申请给出开始和结束时间。过道同一时刻只能给一个摊位用，求最多能安排多少个申请。"),
        ("地铁志愿者的服务时段", "贵阳地铁招募志愿者，每人报了一个 [开始, 结束) 服务时段。同一时段只能安排一人，求最多能安排多少名志愿者。"),
        ("青岩古镇讲解员的预约", "青岩古镇的讲解员收到了 n 个预约，每个预约有开始和结束时刻。同一时刻只能接一个团，求最多能接多少个团。"),
        ("观山湖公园充电桩的占用", "观山湖公园的充电桩收到 n 个占用申请，每个申请有起止时间。同一时刻只能服务一辆车，求最多能服务多少辆。"),
        ("花果园电梯的维修窗口", "花果园一栋楼的电梯收到 n 个维修申请，每个申请占用一个时间区间。同一时刻只能做一项维修，求最多能完成多少项。"),
    ],
    "knap01": [
        ("回贵阳要带的特产", "在外地上学的小黔要回贵阳，行李箱最多装 W 千克。每样特产有重量和价值，每样最多带一件，求能带走的最高总价值。"),
        ("龙洞堡机场的托运行李", "龙洞堡机场的托运额度是 W 千克。小黔有 n 件行李，每件有重量和价值，每件只能带一件，求不超重时能带的最大价值。"),
        ("花果园搬家的纸箱", "花果园搬家时只有一辆能装 W 千克的小车。n 个纸箱各有重量和价值，每个纸箱只能装一次，求能搬走的最大价值。"),
        ("青岩古镇的伴手礼预算", "在青岩古镇买伴手礼，背包最多承受 W 的重量。每件商品有重量和喜欢程度，每件只能买一件，求最大喜欢程度之和。"),
        ("露营装备的背包装载", "去高坡云顶露营，背包承重 W。n 件装备各有重量和保暖价值，每件只能带一件，求最大总价值。"),
    ],
    "knapfull": [
        ("丝娃娃的配菜不限量", "吃丝娃娃时，一张皮最多卷 W 克的配菜。每种配菜有重量和美味值，同一种可以重复拿，求一张皮的最大美味值。"),
        ("烙锅点菜可以重复", "在贵阳吃烙锅，锅最多放 W 克的菜。每种菜有重量和香辣值，同一种可以重复点，求一锅的最大香辣值。"),
        ("肠旺面的加料", "一碗肠旺面最多加 W 克的料。每种加料有重量和满足感，同一种可以重复加，求最大满足感。"),
        ("酸汤鱼的配菜", "一锅酸汤鱼最多放 W 克配菜。每种配菜有重量和鲜味值，可以重复放，求最大鲜味值。"),
        ("豆米火锅的自助配菜", "豆米火锅自助台最多装 W 克。每种配菜有重量和喜爱值，可以重复取，求最大喜爱值。"),
    ],
    "lis": [
        ("观山湖的水位上涨记录", "观山湖泵站按天记录了水位。小黔想知道，按时间顺序挑出若干天，让水位严格递增，最多能挑出多少天。"),
        ("黔灵山猕猴的排队身高", "黔灵山的猕猴按到达顺序排成一列，饲养员记录每只的身高。他想按原顺序挑出一组身高严格递增的猴子，最多挑多少只。"),
        ("花果园电梯的楼层记录", "花果园电梯一天里按顺序停靠了很多楼层。小黔想从中挑出若干次停靠，使楼层严格递增，最多能挑多少次。"),
        ("数博会的入场编号", "数博会入口按顺序发放参观编号。工作人员想从这些编号里挑出一组严格递增的编号做抽奖样本，最多能挑多少个。"),
        ("贵阳的逐日气温", "气象站记录了连续 n 天的最高气温。小黔想找一段按时间严格升温的日子，最多能有多少天。"),
    ],
    "bfs": [
        ("花果园地下车库找车位", "花果园地下车库是一个 n×m 的格子，1 表示墙，0 表示能走。小黔从左上角出发，每次上下左右走一格，求到右下角的最少步数；走不到输出 -1。"),
        ("青岩古镇石板巷找出口", "青岩古镇的石板巷被抽象成 n×m 的格子，1 是封闭院落，0 是巷道。游客从左上角走到右下角，求最少转弯前的步数。"),
        ("黔灵山公园的迷宫步道", "黔灵山公园有一段迷宫步道，n×m 的格子中 1 表示不可通行。小黔从左上角出发，求到右下角的最少移动次数。"),
        ("贵阳地铁站厅的换乘通道", "地铁站厅被看成 n×m 的网格，1 表示封闭区域。乘客从左上角走到右下角，求最少走多少格；到不了输出 -1。"),
        ("数博会展馆寻展位", "数博会展馆的展位排成 n×m 网格，1 表示被占用。参观者从左上角走到右下角，求最短步行格数。"),
    ],
    "graph": [
        ("贵阳地铁换乘最少站数", "贵阳地铁有 n 个站、m 条直接相连的线路。小黔从 1 号站出发，求到 n 号站最少经过多少条边；到不了输出 -1。"),
        ("花果园楼栋间的步行网络", "花果园小区有 n 栋楼，m 对楼栋之间有直达小路。快递员从 1 号楼到 n 号楼，求最少经过多少条小路。"),
        ("青岩古镇的公交线路", "青岩古镇周边有 n 个站点、m 条双向公交线。游客从 1 号站到 n 号站，求最少换乘段数。"),
        ("观山湖绿道的连接", "观山湖绿道有 n 个入口、m 条相连的步道。小黔从 1 号入口到 n 号入口，求最少走几条步道。"),
        ("北站到机场的大巴换乘", "贵阳北站到龙洞堡机场之间有 n 个接驳点和 m 条双向接驳线。求从 1 号点到 n 号点最少坐几段。"),
    ],
    "dsu": [
        ("小区团购群的合并", "花果园有 n 个团购群，m 次合并操作把两个群合成一个。求最后还剩多少个群。"),
        ("老小区院落的连通", "贵阳某老小区有 n 个院落，m 条小路连接其中两个院落。求这些院落一共分成多少个互不相通的片区。"),
        ("花溪大学城的社团联盟", "花溪大学城有 n 个社团，m 对社团结成了联盟。求最后有多少个独立的联盟。"),
        ("数博会参展商的合作群", "数博会有 n 家参展商，m 对参展商建立了合作关系。求最后有多少个互不合作的群体。"),
        ("观山湖公园的健身小组", "观山湖公园有 n 个健身小组，m 次合并把两个小组合并。求最后剩下多少个小组。"),
    ],
    "gcd": [
        ("分丝娃娃的薄饼", "小黔有 a 张丝娃娃薄饼和 b 份配菜，想平均分给尽可能多的人且不浪费。求最多能分给多少人。"),
        ("分烙锅的土豆", "一锅烙锅有 a 片土豆和 b 片藕片，要平均分到若干盘且不浪费。求最多能分多少盘。"),
        ("青岩古镇分玫瑰糖", "青岩古镇有 a 颗玫瑰糖和 b 块核桃糖，要装成若干份完全相同的礼盒。求最多能装多少盒。"),
        ("花果园分停车位", "花果园有 a 个地面车位和 b 个地下车位，要平均分配给若干栋楼。求最多能分给多少栋楼。"),
        ("肠旺面分面条", "面馆有 a 团面和 b 份血旺，要分成若干碗分量相同的肠旺面。求最多能分多少碗。"),
    ],
    "prime": [
        ("数博会的质数门票号", "数博会门票按 1 到 n 编号。工作人员想知道编号是质数的门票一共有多少张。"),
        ("甲秀楼的石栏编号", "甲秀楼修缮时给 n 块石栏编号。小黔想知道编号为质数的石栏有多少块。"),
        ("贵阳公交的线路编号", "贵阳公交把 n 条线路从 1 到 n 编号。调度员想统计编号为质数的线路有多少条。"),
        ("猕猴桃装箱的编号", "修文猕猴桃装箱后从 1 到 n 编号。质检员想统计质数编号的箱子有多少个。"),
        ("南明河桥墩的编号", "南明河沿线有 n 个桥墩，从 1 到 n 编号。巡检员想统计质数编号的桥墩有多少个。"),
    ],
    "vowel": [
        ("“肠旺面”的拼音招牌", "青云路一家肠旺面馆把拼音 changwangmian 印在招牌上。老板想知道招牌里有多少个元音字母。"),
        ("“丝娃娃”的拼音菜单", "一家丝娃娃店的菜单上写着 siwawa。店员想统计其中元音字母的个数。"),
        ("“甲秀楼”的拼音导览", "甲秀楼导览牌上印着 jiaxiulou。讲解员想统计元音字母的个数。"),
        ("“观山湖”的拼音路牌", "观山湖公园的路牌上写着 guanshanhu。小黔想统计元音字母的个数。"),
        ("“青岩古镇”的拼音门票", "青岩古镇门票上印着 qingyanguzhen。售票员想统计元音字母的个数。"),
    ],
    "robot": [
        ("黔灵山猕猴的散步路线", "黔灵山的一只猕猴从原点出发，按 U/D/L/R 指令散步。U 向上、D 向下、L 向左、R 向右，求最后的位置。"),
        ("花果园的送快递机器人", "花果园的快递机器人从原点出发，按上下左右指令移动。求它送完这一趟后的坐标。"),
        ("数博会展馆的巡检机器人", "数博会展馆里有一台巡检机器人，从原点开始按指令移动。求巡检结束时的坐标。"),
        ("南明河的保洁船", "南明河保洁船从码头出发，按上下左右指令移动。求它最后停在哪里。"),
        ("青岩古镇的导览车", "青岩古镇的导览车从原点出发，按 U/D/L/R 指令行驶。求它最后的坐标。"),
    ],
    "kth": [
        ("花果园二手房总价第 k 高", "花果园一批二手房各有总价。小黔想知道总价从高到低排第 k 的房子是多少钱。"),
        ("贵阳中考录取分第 k 高", "某校记录了 n 名考生的录取分。老师想知道从高到低第 k 高的分数。"),
        ("青云路摊位营业额第 k 高", "青云路夜市各摊位的营业额已经统计好。管理员想知道营业额从高到低第 k 名是多少。"),
        ("观山湖马拉松第 k 名成绩", "观山湖马拉松记录了 n 名选手的完赛成绩（秒）。求从高到低第 k 名的时间。"),
        ("数博会预约人数第 k 高", "数博会各展馆的预约人数不同。主办方想知道从高到低第 k 名的预约人数。"),
    ],
    "nextgreater": [
        ("观山湖天际线的下一栋高楼", "观山湖沿线有 n 栋楼，给出每栋的高度。对每栋楼，求它右边第一栋比它高的楼的编号；没有就输出 0。"),
        ("黔灵山步道的下一段陡坡", "黔灵山步道有 n 段，每段有一个坡度值。求每一段右边第一段比它更陡的段的编号；没有输出 0。"),
        ("南明河的下一处深水段", "南明河被分成 n 段，每段有一个深度。求每一段右边第一段更深的段的编号；没有输出 0。"),
        ("花果园楼栋的下一栋高楼", "花果园一排楼栋各有高度。求每栋楼右边第一栋更高的楼的编号；没有输出 0。"),
        ("贵阳气温的下一个高温日", "贵阳连续 n 天记录了最高气温。求每一天右边第一个气温更高的日子的编号；没有输出 0。"),
    ],
    "minpath": [
        ("花果园送货的最短路径", "花果园的送货地图是 n×m 的网格，每格有一个通行代价。快递员从左上角走到右下角，只能向右或向下，求最小总代价。"),
        ("黔灵山爬山的体力消耗", "黔灵山爬山路线是 n×m 的网格，每格有体力消耗。小黔从左上角走到右下角，只能向右或向下，求最少消耗。"),
        ("青岩古镇石板路的游览", "青岩古镇的游览图是 n×m 的网格，每格有步行代价。游客从左上角到右下角，只能向右或向下，求最小总代价。"),
        ("数博会展馆的参观路线", "数博会展馆排成 n×m 网格，每格有一个参观耗时。参观者从左上角到右下角，只能向右或向下，求最短耗时。"),
        ("南明河滨河步道的跑步", "南明河滨河步道是 n×m 的网格，每格有一个疲劳值。跑者从左上角到右下角，只能向右或向下，求最小疲劳值。"),
    ],
    "bracket": [
        ("甲秀楼长联的标点检查", "甲秀楼长联整理时，需要检查一段由 ()[]{} 组成的括号串是否合法：每个左括号都要有同类型右括号按正确顺序闭合。"),
        ("贵阳地铁导向牌的括号", "地铁导向牌的文案里有 ()[]{} 组成的括号串。检查它们是否配对正确。"),
        ("数博会展位编号的括号", "数博会展位编号里混入了一串括号。检查这段括号串是否合法。"),
        ("青云路摊位招牌的括号", "青云路摊位的招牌文案里有括号串。检查左右括号是否一一对应。"),
        ("花果园电梯告示的括号", "花果园电梯告示里有一串括号，检查它们是否正确闭合。"),
    ],
}

# ------------------------------------------------------------------ 引擎
def _lines(t):
    return [ln.strip() for ln in t.replace("\r", "").split("\n") if ln.strip() != ""]


def solve_sum(t):
    d = list(map(int, t.split()))
    n = d[0]
    a = d[1:1 + n]
    best = max(a)
    return "%d %d" % (sum(a), a.index(best) + 1)


def rand_sum(rng):
    n = rng.randint(2, 10)
    a = [rng.randint(0, 1000) for _ in range(n)]
    return "%d\n%s" % (n, " ".join(map(str, a)))


def solve_count(t):
    d = list(map(int, t.split()))
    n, k = d[0], d[1]
    a = d[2:2 + n]
    return str(sum(1 for x in a if x >= k))


def rand_count(rng):
    n = rng.randint(4, 20)
    k = rng.randint(-20, 60)
    a = [rng.randint(-20, 80) for _ in range(n)]
    return "%d %d\n%s" % (n, k, " ".join(map(str, a)))


def solve_sort(t):
    lines = _lines(t)
    n = int(lines[0])
    rows = []
    for i in range(n):
        name, v = lines[1 + i].split()
        rows.append((name, int(v)))
    rows.sort(key=lambda x: (x[1], x[0]))
    return "\n".join("%s %d" % (n, v) for n, v in rows)


def rand_sort(rng):
    names = ["changwang", "siwawa", "lusi", "doumi", "kaoluo", "yangyuba", "bingjiang", "suanfen"]
    n = rng.randint(3, 8)
    pick = rng.sample(names, n)
    return "%d\n%s" % (n, "\n".join("%s %d" % (x, rng.randint(1, 99)) for x in pick))


def solve_range(t):
    d = list(map(int, t.split()))
    n, q = d[0], d[1]
    a = d[2:2 + n]
    p = d[2 + n:]
    pre = [0]
    for x in a:
        pre.append(pre[-1] + x)
    out = []
    for i in range(q):
        l, r = p[2 * i], p[2 * i + 1]
        out.append(str(pre[r] - pre[l - 1]))
    return "\n".join(out)


def rand_range(rng):
    n = rng.randint(5, 15)
    q = rng.randint(3, 8)
    a = [rng.randint(0, 200) for _ in range(n)]
    qs = []
    for _ in range(q):
        l = rng.randint(1, n)
        r = rng.randint(l, n)
        qs.append((l, r))
    return "%d %d\n%s\n%s" % (n, q, " ".join(map(str, a)),
                              "\n".join("%d %d" % x for x in qs))


def solve_rangeadd(t):
    d = list(map(int, t.split()))
    n, m = d[0], d[1]
    a = d[2:2 + n]
    ops = d[2 + n:]
    diff = [0] * (n + 2)
    for i in range(m):
        l, r, x = ops[3 * i], ops[3 * i + 1], ops[3 * i + 2]
        diff[l] += x
        diff[r + 1] -= x
    cur = 0
    vals = []
    for i in range(1, n + 1):
        cur += diff[i]
        vals.append(a[i - 1] + cur)
    return "%d %d" % (max(vals), sum(vals))


def rand_rangeadd(rng):
    n = rng.randint(5, 15)
    m = rng.randint(3, 8)
    a = [rng.randint(0, 50) for _ in range(n)]
    ops = []
    for _ in range(m):
        l = rng.randint(1, n)
        r = rng.randint(l, n)
        ops.append((l, r, rng.randint(1, 20)))
    return "%d %d\n%s\n%s" % (n, m, " ".join(map(str, a)),
                              "\n".join("%d %d %d" % x for x in ops))


def solve_interval(t):
    lines = _lines(t)
    n = int(lines[0])
    seg = []
    for i in range(n):
        l, r = map(int, lines[1 + i].split())
        seg.append((l, r))
    seg.sort(key=lambda x: x[1])
    cnt = 0
    last = -10**18
    for l, r in seg:
        if l >= last:
            cnt += 1
            last = r
    return str(cnt)


def rand_interval(rng):
    n = rng.randint(3, 9)
    seg = []
    for _ in range(n):
        l = rng.randint(0, 20)
        r = l + rng.randint(1, 8)
        seg.append((l, r))
    return "%d\n%s" % (n, "\n".join("%d %d" % x for x in seg))


def solve_knap01(t):
    d = list(map(int, t.split()))
    n, W = d[0], d[1]
    dp = [0] * (W + 1)
    for i in range(n):
        w, v = d[2 + 2 * i], d[3 + 2 * i]
        for j in range(W, w - 1, -1):
            dp[j] = max(dp[j], dp[j - w] + v)
    return str(max(dp))


def rand_knap01(rng):
    n = rng.randint(2, 7)
    W = rng.randint(8, 25)
    rows = []
    for _ in range(n):
        w = rng.randint(1, W)
        rows.append((w, rng.randint(1, 80)))
    return "%d %d\n%s" % (n, W, "\n".join("%d %d" % x for x in rows))


def solve_knapfull(t):
    d = list(map(int, t.split()))
    n, W = d[0], d[1]
    dp = [0] * (W + 1)
    for i in range(n):
        w, v = d[2 + 2 * i], d[3 + 2 * i]
        for j in range(w, W + 1):
            dp[j] = max(dp[j], dp[j - w] + v)
    return str(max(dp))


def rand_knapfull(rng):
    n = rng.randint(2, 6)
    W = rng.randint(8, 25)
    rows = []
    for _ in range(n):
        w = rng.randint(1, W)
        rows.append((w, rng.randint(1, 80)))
    return "%d %d\n%s" % (n, W, "\n".join("%d %d" % x for x in rows))


def solve_lis(t):
    d = list(map(int, t.split()))
    n = d[0]
    a = d[1:1 + n]
    tails = []
    for x in a:
        lo, hi = 0, len(tails)
        while lo < hi:
            mid = (lo + hi) // 2
            if tails[mid] < x:
                lo = mid + 1
            else:
                hi = mid
        if lo == len(tails):
            tails.append(x)
        else:
            tails[lo] = x
    return str(len(tails))


def rand_lis(rng):
    n = rng.randint(6, 20)
    a = [rng.randint(0, 50) for _ in range(n)]
    return "%d\n%s" % (n, " ".join(map(str, a)))


def solve_bfs(t):
    lines = _lines(t)
    n, m = map(int, lines[0].split())
    g = lines[1:1 + n]
    if g[0][0] == "1" or g[n - 1][m - 1] == "1":
        return "-1"
    dist = [[-1] * m for _ in range(n)]
    dist[0][0] = 0
    q = [(0, 0)]
    h = 0
    while h < len(q):
        x, y = q[h]
        h += 1
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and g[nx][ny] == "0" and dist[nx][ny] < 0:
                dist[nx][ny] = dist[x][y] + 1
                q.append((nx, ny))
    return str(dist[n - 1][m - 1])


def rand_bfs(rng):
    n = rng.randint(3, 7)
    m = rng.randint(3, 7)
    g = []
    for i in range(n):
        row = "".join("1" if rng.random() < 0.22 else "0" for _ in range(m))
        g.append(row)
    g[0] = "0" + g[0][1:]
    g[n - 1] = g[n - 1][:m - 1] + "0"
    return "%d %d\n%s" % (n, m, "\n".join(g))


def solve_graph(t):
    d = list(map(int, t.split()))
    n, m = d[0], d[1]
    adj = [[] for _ in range(n + 1)]
    for i in range(m):
        u, v = d[2 + 2 * i], d[3 + 2 * i]
        adj[u].append(v)
        adj[v].append(u)
    dist = [-1] * (n + 1)
    dist[1] = 0
    q = [1]
    h = 0
    while h < len(q):
        u = q[h]
        h += 1
        for v in adj[u]:
            if dist[v] < 0:
                dist[v] = dist[u] + 1
                q.append(v)
    return str(dist[n])


def rand_graph(rng):
    n = rng.randint(3, 8)
    m = rng.randint(2, 10)
    edges = []
    for _ in range(m):
        u = rng.randint(1, n)
        v = rng.randint(1, n)
        if u == v:
            v = v % n + 1
        edges.append((min(u, v), max(u, v)))
    return "%d %d\n%s" % (n, len(edges), "\n".join("%d %d" % x for x in edges))


def solve_components(t):
    d = list(map(int, t.split()))
    n, m = d[0], d[1]
    par = list(range(n + 1))

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    cnt = n
    for i in range(m):
        u, v = d[2 + 2 * i], d[3 + 2 * i]
        ru, rv = find(u), find(v)
        if ru != rv:
            par[ru] = rv
            cnt -= 1
    return str(cnt)


def rand_components(rng):
    n = rng.randint(3, 8)
    m = rng.randint(2, 10)
    edges = []
    for _ in range(m):
        u = rng.randint(1, n)
        v = rng.randint(1, n)
        if u == v:
            v = v % n + 1
        edges.append((u, v))
    return "%d %d\n%s" % (n, len(edges), "\n".join("%d %d" % x for x in edges))


def solve_gcd(t):
    d = list(map(int, t.split()))
    n = d[0]
    out = []
    for i in range(n):
        a, b = d[1 + 2 * i], d[2 + 2 * i]
        while b:
            a, b = b, a % b
        out.append(str(a))
    return "\n".join(out)


def rand_gcd(rng):
    n = rng.randint(2, 6)
    rows = [(rng.randint(1, 500), rng.randint(1, 500)) for _ in range(n)]
    return "%d\n%s" % (n, "\n".join("%d %d" % x for x in rows))


def solve_prime(t):
    n = int(t.strip())
    if n < 2:
        return "0"
    sieve = bytearray(b"\x01") * (n + 1)
    sieve[0] = sieve[1] = 0
    i = 2
    while i * i <= n:
        if sieve[i]:
            sieve[i * i:n + 1:i] = b"\x00" * (((n - i * i) // i) + 1)
        i += 1
    return str(sum(sieve))


def rand_prime(rng):
    return str(rng.randint(10, 3000))


def solve_vowel(t):
    s = t.strip()
    return str(sum(1 for c in s if c in "aeiou"))


def rand_vowel(rng):
    letters = "changwamiansi"
    return "".join(rng.choice(letters) for _ in range(rng.randint(5, 18)))


def solve_robot(t):
    lines = _lines(t)
    n = int(lines[0])
    x = y = 0
    for c in lines[1:1 + n]:
        c = c.upper()
        if c == "U":
            y += 1
        elif c == "D":
            y -= 1
        elif c == "L":
            x -= 1
        elif c == "R":
            x += 1
    return "%d %d" % (x, y)


def rand_robot(rng):
    n = rng.randint(3, 10)
    return "%d\n%s" % (n, "\n".join(rng.choice("UDLR") for _ in range(n)))


def solve_kth(t):
    d = list(map(int, t.split()))
    n, k = d[0], d[1]
    a = sorted(d[2:2 + n], reverse=True)
    return str(a[k - 1])


def rand_kth(rng):
    n = rng.randint(3, 10)
    k = rng.randint(1, n)
    a = [rng.randint(0, 500) for _ in range(n)]
    return "%d %d\n%s" % (n, k, " ".join(map(str, a)))


def solve_nextgreater(t):
    d = list(map(int, t.split()))
    n = d[0]
    a = d[1:1 + n]
    st = []
    ans = [0] * n
    for i in range(n - 1, -1, -1):
        while st and a[st[-1]] <= a[i]:
            st.pop()
        ans[i] = st[-1] + 1 if st else 0
        st.append(i)
    return "\n".join(map(str, ans))


def rand_nextgreater(rng):
    n = rng.randint(3, 10)
    a = [rng.randint(1, 30) for _ in range(n)]
    return "%d\n%s" % (n, " ".join(map(str, a)))


def solve_minpath(t):
    d = list(map(int, t.split()))
    n, m = d[0], d[1]
    g = []
    p = 2
    for i in range(n):
        g.append(d[p:p + m])
        p += m
    dp = [[0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            best = 10**18
            if i:
                best = min(best, dp[i - 1][j])
            if j:
                best = min(best, dp[i][j - 1])
            dp[i][j] = g[i][j] + (0 if (i == 0 and j == 0) else best)
    return str(dp[n - 1][m - 1])


def rand_minpath(rng):
    n = rng.randint(2, 6)
    m = rng.randint(2, 6)
    g = [[rng.randint(1, 9) for _ in range(m)] for _ in range(n)]
    return "%d %d\n%s" % (n, m, "\n".join(" ".join(map(str, row)) for row in g))


def solve_bracket(t):
    s = t.strip()
    st = []
    pairs = {")": "(", "]": "[", "}": "{"}
    for c in s:
        if c in "([{":
            st.append(c)
        elif c in ")]}":
            if not st or st[-1] != pairs[c]:
                return "NO"
            st.pop()
    return "YES" if not st else "NO"


def rand_bracket(rng):
    n = rng.randint(2, 12)
    return "".join(rng.choice("()[]{}") for _ in range(n))


ENGINES = {
    "sum": dict(solve=solve_sum, rand=rand_sum, difficulty=1,
                tags=["模拟", "求和"],
                task="统计这 n 个数的总和，并输出总和与第一个最大值的位置（位置从 1 开始）。",
                input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n第二行 n 个整数 a[i]（0 ≤ a[i] ≤ 10^9）。",
                output_md="一行两个整数：总和、第一个最大值的下标（从 1 开始），用一个空格隔开。",
                constraints_md="1 ≤ n ≤ 10^5，0 ≤ a[i] ≤ 10^9；总和可能超过 int，请用 64 位整数。",
                hints=["先读入 n 和整个数组，边累加边记录当前最大值。",
                       "最大值相等时不要更新下标，才能得到“第一个”最大值的编号。",
                       "总和最大约 10^14，C++ 用 long long。"],
                cpp=r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; cin >> n;
    long long sum = 0, mx = LLONG_MIN;
    int pos = 1;
    for (int i = 1; i <= n; i++) {
        long long x; cin >> x;
        sum += x;
        if (x > mx) { mx = x; pos = i; }
    }
    cout << sum << " " << pos << "\n";
    return 0;
}
'''),
    "count": dict(solve=solve_count, rand=rand_count, difficulty=1,
                  tags=["循环", "计数"],
                  task="统计 n 个数中不小于 k 的数有多少个。",
                  input_md="第一行两个整数 n、k（1 ≤ n ≤ 10^5，-10^9 ≤ k ≤ 10^9）。\n第二行 n 个整数 a[i]（-10^9 ≤ a[i] ≤ 10^9）。",
                  output_md="一个整数，表示满足 a[i] ≥ k 的个数。",
                  constraints_md="1 ≤ n ≤ 10^5，-10^9 ≤ a[i], k ≤ 10^9。",
                  hints=["循环每个数，用一个计数器统计 ≥ k 的个数。",
                         "注意 k 可能为负数，不要只考虑正数。",
                         "数据量 10^5，O(n) 足够。"],
                  cpp=r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; long long k; cin >> n >> k;
    int cnt = 0;
    for (int i = 0; i < n; i++) {
        long long x; cin >> x;
        if (x >= k) cnt++;
    }
    cout << cnt << "\n";
    return 0;
}
'''),
    "sort": dict(solve=solve_sort, rand=rand_sort, difficulty=2,
                 tags=["排序", "结构体"],
                 task="把 n 个“名称 + 数值”按数值从小到大排序；数值相同的按名称字典序从小到大。输出排序后的名称和数值。",
                 input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n接下来 n 行，每行一个不含空格的字符串 name 和一个整数 value。",
                 output_md="n 行，每行一个名称和一个整数，表示排序后的结果。",
                 constraints_md="1 ≤ n ≤ 10^5，名称只含小写字母，1 ≤ value ≤ 10^9。",
                 hints=["用结构体或 pair 存下名称和数值。",
                        "排序规则是：先比数值，数值相同再比名称。",
                        "直接调用 sort 并写自定义比较函数即可。"],
                 cpp=r'''#include <bits/stdc++.h>
using namespace std;
struct Item { string name; long long value; };
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; cin >> n;
    vector<Item> v(n);
    for (auto &x : v) cin >> x.name >> x.value;
    sort(v.begin(), v.end(), [](const Item &a, const Item &b) {
        if (a.value != b.value) return a.value < b.value;
        return a.name < b.name;
    });
    for (auto &x : v) cout << x.name << " " << x.value << "\n";
    return 0;
}
'''),
    "range": dict(solve=solve_range, rand=rand_range, difficulty=2,
                  tags=["前缀和", "区间查询"],
                  task="给定长度为 n 的数组，回答 q 次询问：第 l 个数到第 r 个数的和是多少（下标从 1 开始）。",
                  input_md="第一行两个整数 n、q（1 ≤ n, q ≤ 10^5）。\n第二行 n 个整数 a[i]（0 ≤ a[i] ≤ 10^9）。\n接下来 q 行，每行两个整数 l、r（1 ≤ l ≤ r ≤ n）。",
                  output_md="q 行，每行一个整数，表示区间和。",
                  constraints_md="1 ≤ n, q ≤ 10^5，0 ≤ a[i] ≤ 10^9；区间和可能超过 int。",
                  hints=["多次区间求和，不要每次 for 一遍，会超时。",
                         "预处理前缀和 pre[i] = a[1] + … + a[i]。",
                         "答案就是 pre[r] - pre[l-1]。"],
                  cpp=r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q; cin >> n >> q;
    vector<long long> pre(n + 1, 0);
    for (int i = 1; i <= n; i++) {
        long long x; cin >> x;
        pre[i] = pre[i - 1] + x;
    }
    while (q--) {
        int l, r; cin >> l >> r;
        cout << pre[r] - pre[l - 1] << "\n";
    }
    return 0;
}
'''),
    "rangeadd": dict(solve=solve_rangeadd, rand=rand_rangeadd, difficulty=3,
                     tags=["差分", "区间修改"],
                     task="给定初始数组，做 m 次操作：把区间 [l, r] 的每个数都增加 x。所有操作结束后，输出数组最大值与总和。",
                     input_md="第一行两个整数 n、m（1 ≤ n, m ≤ 10^5）。\n第二行 n 个整数 a[i]（0 ≤ a[i] ≤ 10^9）。\n接下来 m 行，每行三个整数 l、r、x（1 ≤ l ≤ r ≤ n，1 ≤ x ≤ 10^9）。",
                     output_md="一行两个整数：最终数组最大值、最终数组总和。",
                     constraints_md="1 ≤ n, m ≤ 10^5，0 ≤ a[i], x ≤ 10^9。",
                     hints=["每次给一整段加同一个数，用差分数组。",
                            "对 [l, r] 加 x：d[l] += x，d[r+1] -= x。",
                            "最后从前往后累加 d，还原每个位置，再统计最大值和总和。"],
                     cpp=r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m; cin >> n >> m;
    vector<long long> a(n + 1), d(n + 2, 0);
    for (int i = 1; i <= n; i++) cin >> a[i];
    while (m--) {
        int l, r; long long x; cin >> l >> r >> x;
        d[l] += x; d[r + 1] -= x;
    }
    long long cur = 0, sum = 0, mx = LLONG_MIN;
    for (int i = 1; i <= n; i++) {
        cur += d[i];
        long long v = a[i] + cur;
        sum += v;
        mx = max(mx, v);
    }
    cout << mx << " " << sum << "\n";
    return 0;
}
'''),
    "interval": dict(solve=solve_interval, rand=rand_interval, difficulty=3,
                     tags=["贪心", "区间调度"],
                     task="有 n 个时间区间 [l, r)。同一时刻只能安排一个区间，求最多能安排多少个互不重叠的区间。",
                     input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n接下来 n 行，每行两个整数 l、r（0 ≤ l < r ≤ 10^9）。",
                     output_md="一个整数，表示最多能安排的区间数。",
                     constraints_md="1 ≤ n ≤ 10^5，0 ≤ l < r ≤ 10^9。",
                     hints=["按结束时间从早到晚考虑。",
                            "每次选结束最早的区间，能给后面留出最多时间。",
                            "下一个区间的开始时间必须 ≥ 上一个的结束时间。"],
                     cpp=r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; cin >> n;
    vector<pair<long long, long long>> seg(n);
    for (auto &x : seg) cin >> x.second >> x.first; // 先存结束，再存开始
    sort(seg.begin(), seg.end());
    int cnt = 0;
    long long last = LLONG_MIN / 2;
    for (auto &x : seg) {
        long long r = x.first, l = x.second;
        if (l >= last) { cnt++; last = r; }
    }
    cout << cnt << "\n";
    return 0;
}
'''),
    "knap01": dict(solve=solve_knap01, rand=rand_knap01, difficulty=3,
                    tags=["动态规划", "01 背包"],
                    task="有 n 件物品，每件有重量 w[i] 和价值 v[i]，每件最多选一次。背包容量为 W，求不超过容量时能获得的最大总价值。",
                    input_md="第一行两个整数 n、W（1 ≤ n ≤ 1000，1 ≤ W ≤ 10^5）。\n接下来 n 行，每行两个整数 w[i]、v[i]（1 ≤ w[i] ≤ W，1 ≤ v[i] ≤ 10^9）。",
                    output_md="一个整数，表示最大总价值。",
                    constraints_md="1 ≤ n ≤ 1000，1 ≤ W ≤ 10^5，1 ≤ v[i] ≤ 10^9。",
                    hints=["每件物品只有选或不选两种状态。",
                           "dp[j] 表示容量 j 时的最大价值，倒着枚举容量避免重复选同一件。",
                           "答案是 dp[W]。"],
                    cpp=r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, W; cin >> n >> W;
    vector<long long> dp(W + 1, 0);
    for (int i = 0; i < n; i++) {
        int w; long long v; cin >> w >> v;
        for (int j = W; j >= w; j--) dp[j] = max(dp[j], dp[j - w] + v);
    }
    cout << dp[W] << "\n";
    return 0;
}
'''),
    "knapfull": dict(solve=solve_knapfull, rand=rand_knapfull, difficulty=3,
                     tags=["动态规划", "完全背包"],
                     task="有 n 种物品，每种有重量 w[i] 和价值 v[i]，每种可以选任意多次。背包容量为 W，求不超过容量时的最大总价值。",
                     input_md="第一行两个整数 n、W（1 ≤ n ≤ 1000，1 ≤ W ≤ 10^5）。\n接下来 n 行，每行两个整数 w[i]、v[i]（1 ≤ w[i] ≤ W，1 ≤ v[i] ≤ 10^9）。",
                     output_md="一个整数，表示最大总价值。",
                     constraints_md="1 ≤ n ≤ 1000，1 ≤ W ≤ 10^5，1 ≤ v[i] ≤ 10^9。",
                     hints=["和 01 背包只差一个枚举方向。",
                            "容量从小到大枚举，dp[j] 就可以在同一件物品上继续加。",
                            "答案是 dp[W]。"],
                     cpp=r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, W; cin >> n >> W;
    vector<long long> dp(W + 1, 0);
    for (int i = 0; i < n; i++) {
        int w; long long v; cin >> w >> v;
        for (int j = w; j <= W; j++) dp[j] = max(dp[j], dp[j - w] + v);
    }
    cout << dp[W] << "\n";
    return 0;
}
'''),
    "lis": dict(solve=solve_lis, rand=rand_lis, difficulty=4,
                tags=["动态规划", "二分", "LIS"],
                task="给定长度为 n 的序列，求最长严格上升子序列的长度（不要求连续）。",
                input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n第二行 n 个整数 a[i]（0 ≤ a[i] ≤ 10^9）。",
                output_md="一个整数，表示最长严格上升子序列的长度。",
                constraints_md="1 ≤ n ≤ 10^5，0 ≤ a[i] ≤ 10^9。",
                hints=["最朴素的做法是 dp[i] 表示以 i 结尾的 LIS，O(n²) 会超时。",
                       "维护一个 tails 数组：长度为 len 的上升子序列，结尾最小能是多少。",
                       "对每个数二分找到第一个 ≥ 它的位置替换；严格上升用 lower_bound。"],
                cpp=r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; cin >> n;
    vector<long long> tails;
    for (int i = 0; i < n; i++) {
        long long x; cin >> x;
        auto it = lower_bound(tails.begin(), tails.end(), x);
        if (it == tails.end()) tails.push_back(x);
        else *it = x;
    }
    cout << tails.size() << "\n";
    return 0;
}
'''),
    "bfs": dict(solve=solve_bfs, rand=rand_bfs, difficulty=4,
                tags=["BFS", "网格", "最短路"],
                task="在 n×m 的 0/1 网格中，0 表示可走，1 表示墙。从左上角 (1,1) 走到右下角 (n,m)，每步上下左右移动一格，求最少步数；走不到输出 -1。",
                input_md="第一行两个整数 n、m（1 ≤ n, m ≤ 1000）。\n接下来 n 行，每行一个长度为 m 的 01 串。",
                output_md="一个整数，表示最少步数；无法到达输出 -1。",
                constraints_md="1 ≤ n, m ≤ 1000，保证字符只有 0 和 1。",
                hints=["边权都是 1，用 BFS 一层层扩展。",
                       "起点或终点是墙时直接输出 -1。",
                       "用 dist 数组记录步数，首次到达就是最短。"],
                cpp=r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m; cin >> n >> m;
    vector<string> g(n);
    for (auto &s : g) cin >> s;
    if (g[0][0] == '1' || g[n - 1][m - 1] == '1') {
        cout << -1 << "\n";
        return 0;
    }
    vector<vector<int>> dist(n, vector<int>(m, -1));
    queue<pair<int,int>> q;
    dist[0][0] = 0;
    q.push({0, 0});
    int dx[4] = {1, -1, 0, 0}, dy[4] = {0, 0, 1, -1};
    while (!q.empty()) {
        auto [x, y] = q.front(); q.pop();
        for (int k = 0; k < 4; k++) {
            int nx = x + dx[k], ny = y + dy[k];
            if (nx < 0 || nx >= n || ny < 0 || ny >= m) continue;
            if (g[nx][ny] == '1' || dist[nx][ny] != -1) continue;
            dist[nx][ny] = dist[x][y] + 1;
            q.push({nx, ny});
        }
    }
    cout << dist[n - 1][m - 1] << "\n";
    return 0;
}
'''),
    "graph": dict(solve=solve_graph, rand=rand_graph, difficulty=4,
                  tags=["图", "BFS", "最短路"],
                  task="给定 n 个点和 m 条双向边，求从 1 号点到 n 号点最少经过多少条边；走不到输出 -1。",
                  input_md="第一行两个整数 n、m（1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5）。\n接下来 m 行，每行两个整数 u、v，表示一条双向边。",
                  output_md="一个整数，表示最少边数；无法到达输出 -1。",
                  constraints_md="1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5，1 ≤ u, v ≤ n。",
                  hints=["无权图的最短路径就是 BFS 的层数。",
                         "从 1 号点入队，dist[1]=0。",
                         "第一次访问到 n 号点时的 dist 就是答案。"],
                  cpp=r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m; cin >> n >> m;
    vector<vector<int>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int u, v; cin >> u >> v;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    vector<int> dist(n + 1, -1);
    queue<int> q;
    dist[1] = 0; q.push(1);
    while (!q.empty()) {
        int u = q.front(); q.pop();
        for (int v : adj[u]) {
            if (dist[v] == -1) {
                dist[v] = dist[u] + 1;
                q.push(v);
            }
        }
    }
    cout << dist[n] << "\n";
    return 0;
}
'''),
    "dsu": dict(solve=solve_components, rand=rand_components, difficulty=3,
                tags=["并查集", "连通块"],
                task="给定 n 个点和 m 条边，求这个图一共有多少个连通块。",
                input_md="第一行两个整数 n、m（1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5）。\n接下来 m 行，每行两个整数 u、v，表示一条边。",
                output_md="一个整数，表示连通块数量。",
                constraints_md="1 ≤ n ≤ 10^5，0 ≤ m ≤ 2×10^5。",
                hints=["初始时有 n 个连通块。",
                       "每成功合并两个不同集合，连通块数减一。",
                       "用并查集判断两个点是否已经在同一集合。"],
                cpp=r'''#include <bits/stdc++.h>
using namespace std;
int par[100005];
int find(int x) { return par[x] == x ? x : par[x] = find(par[x]); }
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m; cin >> n >> m;
    for (int i = 1; i <= n; i++) par[i] = i;
    int cnt = n;
    while (m--) {
        int u, v; cin >> u >> v;
        int a = find(u), b = find(v);
        if (a != b) { par[a] = b; cnt--; }
    }
    cout << cnt << "\n";
    return 0;
}
'''),
    "gcd": dict(solve=solve_gcd, rand=rand_gcd, difficulty=2,
                tags=["数论", "最大公约数"],
                task="给定 n 对数，分别输出每一对数的最大公约数。",
                input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n接下来 n 行，每行两个正整数 a、b（1 ≤ a, b ≤ 10^9）。",
                output_md="n 行，每行一个整数，表示对应两数的最大公约数。",
                constraints_md="1 ≤ n ≤ 10^5，1 ≤ a, b ≤ 10^9。",
                hints=["用辗转相除法：gcd(a,b) = gcd(b, a%b)。",
                       "C++17 可以直接调用 std::gcd。",
                       "注意 a、b 都很大，用 long long。"],
                cpp=r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; cin >> n;
    while (n--) {
        long long a, b; cin >> a >> b;
        cout << std::gcd(a, b) << "\n";
    }
    return 0;
}
'''),
    "prime": dict(solve=solve_prime, rand=rand_prime, difficulty=3,
                  tags=["数论", "筛法", "质数"],
                  task="统计 1 到 n 之间（含 n）有多少个质数。",
                  input_md="一个整数 n（1 ≤ n ≤ 2×10^6）。",
                  output_md="一个整数，表示 1 到 n 的质数个数。",
                  constraints_md="1 ≤ n ≤ 2×10^6。",
                  hints=["逐个试除到 sqrt(n) 的总复杂度太高。",
                         "用埃氏筛：先假设全是质数，再把每个质数的倍数标记为合数。",
                         "筛完后统计仍然为 true 的个数。"],
                  cpp=r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; cin >> n;
    vector<bool> isp(max(2, n + 1), true);
    isp[0] = isp[1] = false;
    for (int i = 2; (long long)i * i <= n; i++)
        if (isp[i])
            for (long long j = (long long)i * i; j <= n; j += i) isp[j] = false;
    int cnt = 0;
    for (int i = 2; i <= n; i++) cnt += isp[i];
    cout << cnt << "\n";
    return 0;
}
'''),
    "vowel": dict(solve=solve_vowel, rand=rand_vowel, difficulty=2,
                  tags=["字符串", "计数"],
                  task="给定一个只含小写字母的字符串，统计其中元音字母 a、e、i、o、u 的个数。",
                  input_md="一行一个只含小写字母的字符串 s（1 ≤ |s| ≤ 10^5）。",
                  output_md="一个整数，表示元音字母个数。",
                  constraints_md="1 ≤ |s| ≤ 10^5，字符只含小写字母。",
                  hints=["用 getline 读入整行，避免空格截断（虽然本题没有空格）。",
                         "遍历每个字符，判断是否属于 aeiou。",
                         "O(|s|) 一遍扫描即可。"],
                  cpp=r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s; getline(cin, s);
    int cnt = 0;
    for (char c : s) if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') cnt++;
    cout << cnt << "\n";
    return 0;
}
'''),
    "robot": dict(solve=solve_robot, rand=rand_robot, difficulty=2,
                  tags=["模拟", "坐标"],
                  task="机器人从原点 (0,0) 出发，按 n 条指令移动：U 向上、D 向下、L 向左、R 向右。输出最终坐标 x y。",
                  input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n接下来 n 行，每行一个大写字母 U/D/L/R。",
                  output_md="一行两个整数 x、y，表示最终坐标。",
                  constraints_md="1 ≤ n ≤ 10^5，指令只会是 U/D/L/R。",
                  hints=["维护 x、y 两个变量，初始为 0。",
                         "U 让 y 加 1，D 让 y 减 1，L 让 x 减 1，R 让 x 加 1。",
                         "最后按 x y 输出。"],
                  cpp=r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; cin >> n;
    long long x = 0, y = 0;
    while (n--) {
        char c; cin >> c;
        if (c == 'U') y++;
        else if (c == 'D') y--;
        else if (c == 'L') x--;
        else if (c == 'R') x++;
    }
    cout << x << " " << y << "\n";
    return 0;
}
'''),
    "kth": dict(solve=solve_kth, rand=rand_kth, difficulty=4,
                tags=["排序", "第 k 大", "堆"],
                task="给定 n 个整数，输出从大到小排第 k 的数（1 ≤ k ≤ n）。",
                input_md="第一行两个整数 n、k（1 ≤ n ≤ 10^5，1 ≤ k ≤ n）。\n第二行 n 个整数 a[i]（0 ≤ a[i] ≤ 10^9）。",
                output_md="一个整数，表示第 k 大的数。",
                constraints_md="1 ≤ n ≤ 10^5，1 ≤ k ≤ n。",
                hints=["直接排序后取第 k 个最省事，O(n log n)。",
                       "也可以维护一个大小为 k 的小根堆，O(n log k)。",
                       "注意“第 k 大”是从 1 开始数，不是下标 k。"],
                cpp=r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k; cin >> n >> k;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    nth_element(a.begin(), a.begin() + (n - k), a.end());
    cout << a[n - k] << "\n";
    return 0;
}
'''),
    "nextgreater": dict(solve=solve_nextgreater, rand=rand_nextgreater, difficulty=5,
                        tags=["单调栈", "数据结构"],
                        task="给定 n 个数，对每个位置 i，求它右边第一个严格大于 a[i] 的位置编号；不存在则输出 0。",
                        input_md="第一行一个整数 n（1 ≤ n ≤ 10^5）。\n第二行 n 个整数 a[i]（1 ≤ a[i] ≤ 10^9）。",
                        output_md="n 行，第 i 行表示位置 i 的答案（1-based 编号，找不到输出 0）。",
                        constraints_md="1 ≤ n ≤ 10^5，1 ≤ a[i] ≤ 10^9。",
                        hints=["暴力向右找是 O(n²)，需要换个方向。",
                               "从右往左扫，维护一个“还没找到更大值”的单调栈。",
                               "栈里存下标，遇到 ≤ 当前值的就弹出，栈顶就是答案。"],
                        cpp=r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n; cin >> n;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    vector<int> ans(n, 0);
    stack<int> st;
    for (int i = n - 1; i >= 0; i--) {
        while (!st.empty() && a[st.top()] <= a[i]) st.pop();
        ans[i] = st.empty() ? 0 : st.top() + 1;
        st.push(i);
    }
    for (int i = 0; i < n; i++) cout << ans[i] << "\n";
    return 0;
}
'''),
    "minpath": dict(solve=solve_minpath, rand=rand_minpath, difficulty=4,
                    tags=["动态规划", "网格 DP"],
                    task="给定 n×m 的代价网格，从左上角走到右下角，每次只能向右或向下，求路径上的最小总代价（包含起点和终点）。",
                    input_md="第一行两个整数 n、m（1 ≤ n, m ≤ 1000）。\n接下来 n 行，每行 m 个整数，表示每格的代价。",
                    output_md="一个整数，表示最小总代价。",
                    constraints_md="1 ≤ n, m ≤ 1000，0 ≤ 格子代价 ≤ 10^9。",
                    hints=["dp[i][j] 表示从左上角走到 (i,j) 的最小代价。",
                           "只能从上面或左边过来：dp[i][j] = a[i][j] + min(dp[i-1][j], dp[i][j-1])。",
                           "第一行和第一列只能单向转移，要单独处理。"],
                    cpp=r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m; cin >> n >> m;
    vector<vector<long long>> dp(n, vector<long long>(m, 0));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            long long x; cin >> x;
            if (i == 0 && j == 0) dp[i][j] = x;
            else if (i == 0) dp[i][j] = dp[i][j - 1] + x;
            else if (j == 0) dp[i][j] = dp[i - 1][j] + x;
            else dp[i][j] = min(dp[i - 1][j], dp[i][j - 1]) + x;
        }
    }
    cout << dp[n - 1][m - 1] << "\n";
    return 0;
}
'''),
    "bracket": dict(solve=solve_bracket, rand=rand_bracket, difficulty=2,
                    tags=["栈", "字符串"],
                    task="给定一个由 ()[]{} 组成的括号串，判断是否合法：每个左括号都要有同类型右括号按正确顺序闭合，且不能有多余括号。",
                    input_md="一行一个长度不超过 10^5 的括号串。",
                    output_md="合法输出 YES，否则输出 NO。",
                    constraints_md="1 ≤ |s| ≤ 10^5，字符只含 ()[]{}。",
                    hints=["用栈保存还没配对的左括号。",
                           "遇到右括号时，栈顶必须是同类型左括号。",
                           "扫描结束后栈必须为空。"],
                    cpp=r'''#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s; getline(cin, s);
    stack<char> st;
    bool ok = true;
    for (char c : s) {
        if (c == '(' || c == '[' || c == '{') st.push(c);
        else if (c == ')' || c == ']' || c == '}') {
            char need = c == ')' ? '(' : (c == ']' ? '[' : '{');
            if (st.empty() || st.top() != need) { ok = false; break; }
            st.pop();
        }
    }
    if (!st.empty()) ok = false;
    cout << (ok ? "YES" : "NO") << "\n";
    return 0;
}
'''),
}

ORDER = ["sum", "count", "sort", "range", "rangeadd", "interval", "knap01", "knapfull",
         "lis", "bfs", "graph", "dsu", "gcd", "prime", "vowel", "robot", "kth",
         "nextgreater", "minpath", "bracket"]


def add_problem(engine, num):
    spec = ENGINES[engine]
    story = INSTANCES[engine][(num - 1) % 5]
    title, text = story
    pid = "gy-%03d" % num
    rng = random.Random("guiyang-" + pid)
    cases = [spec["rand"](rng) for _ in range(6)]
    outs = [spec["solve"](c).strip("\n") for c in cases]
    PROBLEMS.append({
        "id": pid, "kind": "local", "chapter": 0,
        "chapter_title": "贵阳生活 100 题",
        "label": "GY-%03d" % num, "title": title,
        "difficulty": spec["difficulty"],
        "difficulty_label": {1: "入门", 2: "基础", 3: "提高", 4: "进阶", 5: "挑战"}[spec["difficulty"]],
        "time_limit": 2.0,
        "statement_md": text + "\n\n**任务**：" + spec["task"],
        "input_md": spec["input_md"], "output_md": spec["output_md"],
        "constraints_md": spec["constraints_md"],
        "hint_md": "\n".join(spec["hints"]), "hints": list(spec["hints"]),
        "note_md": "", "tags": list(spec["tags"]),
        "sample_n": 1,
        "cases": cases, "solve": spec["solve"],
        "source": "本地 OJ 原创 · 贵阳生活 100 题",
        "samples": [{"in": cases[0], "out": outs[0]}],
        "tests": [{"in": cases[i], "out": outs[i]} for i in range(len(cases))],
    })
    SOL[pid] = spec["cpp"]


def build():
    PROBLEMS.clear()
    SOL.clear()
    num = 1
    for engine in ORDER:
        for _ in range(5):
            add_problem(engine, num)
            num += 1


build()
