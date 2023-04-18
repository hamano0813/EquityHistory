#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cn2an

CIRCLE_NUMBER = [chr(i) for i in list(range(9312, 9332)) + list(range(12881, 12896)) + list(range(12977, 12992))]


def grouping_history(history):
    history_group = dict()
    history.sort(key=lambda x: x[0])
    for date, event, *detail in history:
        if (date, event) not in history_group:
            history_group[(date, event)] = [detail]
        else:
            history_group[(date, event)].append(detail)
    return history_group


def classify_detail(details):
    investors = [i[0] for i in details]
    divesters = [i[1] for i in details]
    regists = [i[2] for i in details]
    paidins = [i[3] for i in details]
    ways = [i[4] for i in details]
    remark = '，' + temp[0] if (temp := [i[5] for i in details if i[5]]) else ''
    return investors, divesters, regists, paidins, ways, remark


def adjust_structure(structure, event, details):
    for d in details:
        if event in ('成立', '增资'):
            structure[d[0]] = structure.get(d[0], 0) + d[2]
        elif event == '减资':
            structure[d[1]] = structure.get(d[1], 0) - d[2]
        elif event == '转让':
            if d[0] and d[1]:
                structure[d[0]] = structure.get(d[0], 0) + d[2]
                structure[d[1]] = structure.get(d[1], 0) - d[2]
            elif d[0]:
                structure[d[0]] = structure.get(d[0], 0) + d[2]
            elif d[1]:
                structure[d[1]] = structure.get(d[1], 0) - d[2]


def build_shareholding(structure, captial):
    shareholding = list()
    idx = 0
    for shareholder, registered in structure.items():
        if registered:
            idx += 1
            shareholding.append([f'{idx}', shareholder,
                                 f'{registered / 10000:,.4f}',
                                 f'{registered / captial * 100:.4f}'])
    shareholding.append(['', '合计', f'{captial / 10000:,.4f}', '100.0000'])
    return shareholding


def generate_group(history, company):
    history_group = grouping_history(history)
    event_group = dict()

    count = {'增资': 0, '减资': 0, '转让': 0, '变更': 0}
    structure = dict()
    captial = 0

    for idx, ((date, event), details) in enumerate(history_group.items()):
        investors, divesters, regists, paidins, ways, remark = classify_detail(details)

        overview = f'{CIRCLE_NUMBER[idx]} '

        if event == '成立':
            overview += f'公司成立\n{company}成立于{date.strftime("%Y年%m月%d日")}，' \
                        f'成立时注册资本{sum(regists) / 10000:,}万元，由'
            if len(investors) == 1:
                overview += f'{investors[0]}单独出资成立，出资方式为{ways[0]}'
            else:
                if len(investors) == 2:
                    overview += '及'.join(investors) + f'共同出资组建，其中'
                else:
                    overview += '、'.join(investors[:-1]) + f'及{investors[-1]}共同出资组建，其中'
                for i, investor in enumerate(investors):
                    overview += f'{investor}认缴出资{regists[i] / 10000:,}万元，出资方式为{ways[i]}；'
            overview = overview.rstrip('；')
            overview += f'{remark}。成立时，公司股权结构如下：'

        elif event == '增资':
            count['增资'] += 1
            overview += f'第{cn2an.an2cn(count["增资"])}次增资\n' \
                        f'{date.strftime("%Y年%m月")}，根据公司股东会决议，' \
                        f'公司注册资本由{captial / 10000:,}万元增至{(captial + sum(regists)) / 10000:,}万元，'
            if len(investors) == 1:
                overview += f'全部由{investors[0]}认缴出资，' \
                            f'投资金额{paidins[0] / 10000:,}万元，出资方式为{ways[0]}'
                if paidins[0] > regists[0]:
                    overview += f'，其中{regists[0] / 10000:,}万元计入注册资本，剩余部分计入资本公积'
            else:
                if len(investors) == 2:
                    overview += '由' + '及'.join(investors) + f'认缴出资，其中'
                else:
                    overview += '由' + '、'.join(investors[:-1]) + f'及{investors[-1]}认缴出资，其中'
                for i, investor in enumerate(investors):
                    overview += f'{investor}以{ways[i]}方式出资{paidins[i] / 10000:,}万元；'
                    if paidins[i] > regists[i]:
                        overview = overview.rstrip('；')
                        overview += f'，其中{regists[i] / 10000:,}万元计入注册资本，剩余部分计入资本公积；'
            overview = overview.rstrip('；')
            overview += f'{remark}。本次增资后，公司股权结构如下：'

        elif event == '减资':
            count['减资'] += 1
            overview += f'第{cn2an.an2cn(count["减资"])}次减资\n' \
                        f'{date.strftime("%Y年%m月")}，根据公司股东会决议，' \
                        f'公司注册资本由{captial / 10000:,}万元减至{(captial - sum(regists)) / 10000:,}万元，由'
            if len(divesters) == 1:
                overview += f'{divesters[0]}减少{regists[0] / 10000:,}万元注册资本'
            elif len(divesters) == 2:
                overview += '及'.join(divesters) + '分别减资' + '和'.join([f'{r / 10000:,}万元' for r in regists])
            else:
                overview += '、'.join(investors[:-1]) + f'及{investors[-1]}分别减资，共减资{sum(regists) / 10000:,}万元'
            overview += f'{remark}。本次减资后，公司股权结构如下：'

        elif event == '转让':
            count['转让'] += 1
            overview += f'第{cn2an.an2cn(count["转让"])}次股权转让\n' \
                        f'{date.strftime("%Y年%m月")}，根据公司股东会决议，'
            for i, investor in enumerate(investors):
                if investor and (divester := divesters[i]):
                    overview += f'同意{divester}将其持有的{regists[i] / captial:.2%}股权'
                    if paidins[i] > regists[i]:
                        overview += f'以{paidins[i] / 10000:,}万元'
                    overview += f'转让给{investor}；'
            overview = overview.rstrip('；')
            overview += '，其他股东放弃优先受让权'
            for i, investor in enumerate(investors):
                if investor and not divesters[i]:
                    overview += f'同意{investor}以{ways[i]}方式增资{paidins[i] / 10000:,}万元；'
                    if paidins[i] > regists[i]:
                        overview = overview.rstrip('；')
                        overview += f'，其中{regists[0] / 10000:,}万元计入注册资本，剩余部分计入资本公积；'
            for i, divester in enumerate(divesters):
                if divester and not investors[i]:
                    overview += f'同意{divester}减资{regists[i] / 10000:,}万元；'
            overview = overview.rstrip('；')
            overview += f'{remark}。本次股权转让后，公司股权结构如下：'

        adjust_structure(structure, event, details)
        captial = sum(structure.values())
        shareholding = build_shareholding(structure, captial)
        event_group[(date, event)] = {'overview': overview, 'shareholding': shareholding}

    return event_group
