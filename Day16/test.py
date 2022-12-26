"""
Day 16: Proboscidea Volcanium
"""

import heapq
import math
import re
from collections import defaultdict
from dataclasses import dataclass

PATTERN = re.compile(
    r"Valve (\w+) has flow rate=(\d+); "
    r"(?:tunnel leads to valve|tunnels lead to valves) (\w+(?:, \w+)*)"
)

SAMPLE_INPUT = [
"Valve EG has flow rate=21; tunnels lead to valves WZ, OF, ZP, QD",
"Valve OR has flow rate=0; tunnels lead to valves QD, CR",
"Valve VO has flow rate=0; tunnels lead to valves FL, OY",
"Valve BV has flow rate=0; tunnels lead to valves AA, KK",
"Valve OF has flow rate=0; tunnels lead to valves EJ, EG",
"Valve YZ has flow rate=0; tunnels lead to valves EL, AW",
"Valve EL has flow rate=16; tunnels lead to valves YZ, RD",
"Valve EJ has flow rate=0; tunnels lead to valves YI, OF",
"Valve FM has flow rate=0; tunnels lead to valves VX, FX",
"Valve FL has flow rate=22; tunnels lead to valves VO, FH",
"Valve QD has flow rate=0; tunnels lead to valves OR, EG",
"Valve XC has flow rate=0; tunnels lead to valves UA, GV",
"Valve WZ has flow rate=0; tunnels lead to valves FH, EG",
"Valve AT has flow rate=0; tunnels lead to valves FX, OZ",
"Valve MZ has flow rate=0; tunnels lead to valves UA, YI",
"Valve WI has flow rate=0; tunnels lead to valves OH, WW",
"Valve YD has flow rate=0; tunnels lead to valves OZ, WW",
"Valve QX has flow rate=0; tunnels lead to valves OY, YI",
"Valve AA has flow rate=0; tunnels lead to valves BV, ZE, PE, XL",
"Valve VX has flow rate=0; tunnels lead to valves FM, GQ",
"Valve VN has flow rate=0; tunnels lead to valves TU, OQ",
"Valve RD has flow rate=0; tunnels lead to valves OY, EL",
"Valve QR has flow rate=0; tunnels lead to valves QQ, OZ",
"Valve CD has flow rate=0; tunnels lead to valves WW, RJ",
"Valve VA has flow rate=20; tunnel leads to valve DE",
"Valve RJ has flow rate=0; tunnels lead to valves CR, CD",
"Valve UA has flow rate=19; tunnels lead to valves XC, MZ, KY",
"Valve WW has flow rate=4; tunnels lead to valves YD, PE, WI, DY, CD",
"Valve MC has flow rate=0; tunnels lead to valves ZP, XY",
"Valve XY has flow rate=24; tunnel leads to valve MC",
"Valve FH has flow rate=0; tunnels lead to valves FL, WZ",
"Valve DE has flow rate=0; tunnels lead to valves VA, FX",
"Valve DY has flow rate=0; tunnels lead to valves WW, YI",
"Valve FX has flow rate=14; tunnels lead to valves DE, FM, AT, OQ",
"Valve UU has flow rate=0; tunnels lead to valves AR, AW",
"Valve OY has flow rate=13; tunnels lead to valves RD, VO, AR, GV, QX",
"Valve CS has flow rate=0; tunnels lead to valves MG, OZ",
"Valve KY has flow rate=0; tunnels lead to valves UA, AW",
"Valve KK has flow rate=0; tunnels lead to valves BV, TU",
"Valve GQ has flow rate=18; tunnel leads to valve VX",
"Valve ZV has flow rate=0; tunnels lead to valves YI, LS",
"Valve QQ has flow rate=0; tunnels lead to valves CR, QR",
"Valve AW has flow rate=25; tunnels lead to valves YZ, KY, UU",
"Valve OH has flow rate=0; tunnels lead to valves WI, TU",
"Valve CR has flow rate=8; tunnels lead to valves OR, ZE, RJ, LS, QQ",
"Valve TU has flow rate=7; tunnels lead to valves MG, VN, OH, KK",
"Valve ZP has flow rate=0; tunnels lead to valves EG, MC",
"Valve AR has flow rate=0; tunnels lead to valves UU, OY",
"Valve OZ has flow rate=10; tunnels lead to valves YD, XL, CS, AT, QR",
"Valve GV has flow rate=0; tunnels lead to valves XC, OY",
"Valve PE has flow rate=0; tunnels lead to valves WW, AA",
"Valve ZE has flow rate=0; tunnels lead to valves AA, CR",
"Valve XL has flow rate=0; tunnels lead to valves OZ, AA",
"Valve YI has flow rate=15; tunnels lead to valves QX, MZ, EJ, DY, ZV",
"Valve OQ has flow rate=0; tunnels lead to valves FX, VN",
"Valve MG has flow rate=0; tunnels lead to valves TU, CS",
"Valve LS has flow rate=0; tunnels lead to valves CR, ZV",
]


def _parse(lines):
    return {
        (match := re.match(PATTERN, line)).group(1): (
            int(match.group(2)),
            match.group(3).split(", "),
        )
        for line in lines
    }


def _distances(adj):
    keys, distances = set(), defaultdict(lambda: math.inf)
    for src, dsts in adj:
        keys.add(src)
        distances[src, src] = 0
        for dst, weight in dsts:
            keys.add(dst)
            distances[dst, dst] = 0
            distances[src, dst] = weight
    for mid in keys:
        for src in keys:
            for dst in keys:
                distance = distances[src, mid] + distances[mid, dst]
                if distance < distances[src, dst]:
                    distances[src, dst] = distance
    return distances


@dataclass(order=True, frozen=True)
class _State:
    rooms: tuple[tuple[str, int]]
    valves: frozenset[str]
    flow: int
    total: int
    time: int


def _solve(lines, num_agents, total_time):
    # pylint: disable=too-many-branches,too-many-nested-blocks,too-many-locals
    graph = _parse(lines)
    distances = _distances(
        (src, ((dst, 1) for dst in dsts)) for src, (_, dsts) in graph.items()
    )
    seen, max_seen = set(), 0
    heap = [
        (
            0,
            _State(
                rooms=(("AA", 0),) * num_agents,
                valves=frozenset(src for src, (flow, _) in graph.items() if flow > 0),
                flow=0,
                total=0,
                time=total_time,
            ),
        )
    ]

    while heap:
        estimate, state = heapq.heappop(heap)
        estimate = -estimate
        if state in seen:
            continue
        seen.add(state)
        potential = estimate + sum(
            max(
                (
                    graph[valve][0] * (state.time - delta - 1)
                    for room, age in state.rooms
                    if (delta := distances[room, valve] - age) in range(state.time)
                ),
                default=0,
            )
            for valve in state.valves
        )
        if estimate > max_seen:
            max_seen = estimate
        if potential < max_seen:
            continue

        moves_by_time = defaultdict(lambda: defaultdict(list))
        for valve in state.valves:
            for i, (room, age) in enumerate(state.rooms):
                delta = distances[room, valve] - age
                if delta in range(state.time):
                    moves_by_time[delta][i].append(valve)
        if not moves_by_time:
            continue

        for delta, moves_by_agent in moves_by_time.items():
            indices = [None] * num_agents
            while True:
                for i, index in enumerate(indices):
                    index = 0 if index is None else index + 1
                    if index < len(moves_by_agent[i]):
                        indices[i] = index
                        break
                    indices[i] = None
                else:
                    break
                valves = [
                    (i, moves_by_agent[i][index])
                    for i, index in enumerate(indices)
                    if index is not None
                ]
                if len(valves) != len(set(valve for _, valve in valves)):
                    continue
                new_rooms = [(room, age + delta + 1) for room, age in state.rooms]
                for i, valve in valves:
                    new_rooms[i] = valve, 0
                rate = sum(graph[valve][0] for _, valve in valves)
                new_state = _State(
                    rooms=tuple(sorted(new_rooms)),
                    valves=state.valves - set(valve for _, valve in valves),
                    flow=state.flow + rate,
                    total=state.total + state.flow * (delta + 1),
                    time=state.time - delta - 1,
                )
                heapq.heappush(heap, (-estimate - rate * new_state.time, new_state))

    return max_seen


def part1(lines):
    """
    >>> part1(SAMPLE_INPUT)
    1651
    """
    return _solve(lines, num_agents=1, total_time=30)


def part2(lines):
    """
    >>> part2(SAMPLE_INPUT)
    1707
    """
    return _solve(lines, num_agents=2, total_time=26)


parts = (part1, part2)
print(parts[1](SAMP))