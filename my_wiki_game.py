#!/usr/bin/python
# -*- coding: utf-8 -*-
# ==============================================================================
# description     : 
# author          : David Qi
# date            : 07/03/2021
# usage           :
# ==============================================================================

import time
import asyncio
import aiohttp
from itertools import islice
from bs4 import BeautifulSoup
from collections import deque


def find_shortest_path_bfs(graph, start, end):
    print('Starting BFS ...')
    if start == end:
        return [start]
    visited = {start}
    queue = deque([(start, [])])

    while queue:
        current, path = queue.popleft()
        visited.add(current)
        for node in graph.get(current, []):
            if node == end:
                print(f'The processing took {time.time() - s} seconds.')
                return path + [current, node]
            if node in visited:
                continue
            queue.append((node, path + [current]))
            visited.add(node)
    print(f'The processing took {time.time() - s} seconds.')
    return None


def find_all_paths_bfs(graph, start, end):
    queue = deque([[start]])
    all_possible_paths = []

    while queue:
        current = queue.popleft()
        last_node = current[-1]
        if last_node == end:
            all_possible_paths.append(current)
        for node in graph.get(last_node, []):
            if node not in current:
                new_path = current + [node]
                queue.append(new_path)
    return all_possible_paths


class MingWikiGame(object):
    def __init__(self, s_url: str, e_url: str, s_type: str = 'all', max_depth: int = 3, workers: int = 16):
        self.base_url = 'https://en.wikipedia.org/wiki/'
        self.graph = {s_url: []}
        self.path, self.total_urls, self.total_pages = [], 0, 0
        self.s_url, self.e_url, self.s_type, self.max_depth, self.workers = s_url, e_url, s_type, max_depth, workers
        self.loop = asyncio.get_event_loop()

    async def extract_urls(self, session: aiohttp.client.ClientSession, url: str) -> list:
        async with session.get(url) as response:
            html = await response.text()
            urls = BeautifulSoup(html, features="lxml").find('div', {'id': 'bodyContent'}).find_all('a', href=True)
            links = [a['href'][6:] for a in set(urls)
                     if a['href'].startswith('/wiki/') and a['href'][6:] not in self.graph.keys()]
            self.total_pages += 1
            return links

    async def send_request(self, path: str) -> None:
        url = self.base_url + path
        async with aiohttp.ClientSession() as session:
            urls = await self.extract_urls(session, url)
            t = len(urls)
            self.total_urls += t
            print(f'Got {t} urls in {url}')
            if t > 0:
                self.graph[path] = urls

    def task_generator(self) -> bool:
        dct = self.graph.copy()
        for k, v in dct.items():
            links = set(v) or {k}
            while len(links) > 0:
                if len(links) > self.workers:
                    chunk = set(islice(links, self.workers))
                else:
                    chunk = links.copy()

                tasks = [asyncio.ensure_future(self.send_request(i)) for i in chunk]
                self.loop.run_until_complete(asyncio.gather(*tasks))
                time.sleep(0.5)
                links.difference_update(chunk)

        if self.s_type != 'all':
            self.path = find_shortest_path_bfs(self.graph, self.s_url, self.e_url)
            if self.path:
                print(f'Great!, The path has been found from {self.total_urls} urls in {self.total_pages} pages!')
                print(self.path)
                return True
        return False

    def run(self, depth: int = 1):
        if depth <= self.max_depth:
            print(f'Working on level {depth}')
            if not self.task_generator():
                self.run(depth + 1)
        elif self.s_type == 'all':
            self.path = find_all_paths_bfs(self.graph, self.s_url, self.e_url)
            if self.path:
                print('Great!, The path has been found!', self.path)
        else:
            print(f'Down to the deepest level with {self.total_urls} urls in {self.total_pages} but not find')


def test_bfs():
    graph = {
        '1': ['2', '3', '4'],
        '2': ['5', '6'],
        '5': ['9', '10'],
        '4': ['7', '8'],
        '7': ['11', '12']
    }

    print(find_shortest_path_bfs(graph, '1', '11'))
    print(find_all_paths_bfs(graph, '1', '11'))


if __name__ == '__main__':
    s = time.time()
    # o = MingWikiGame('Web_Bot', 'Tax_credit', 'short', 3)
    o = MingWikiGame('Web_Bot', 'Tax_holiday', 'short', 3)
    o.run()
    print(time.time() - s)


# Below is the result of shortest:
# Great!, The path has been found in 7925931 urls!
# ['Web_Bot', 'Pacific_Northwest', 'Taxation_in_Canada', 'Tax_holiday']
# 4446.613477468491

# Great!, The path has been found!
# Web Bot -> Barack Obama -> Tax incentive -> Tax holiday
# The processing took 4662.793370962143 seconds.


