"""
Управление:
    - ESC — выход
    - SPACE — пауза / продолжение
    - R — перезапустить с новым случайным массивом
"""

import pygame
import random

import math
from typing import List

def bubble_sort(a: List[int]):
    arr = a
    n = len(arr)
    for i in range(n):
        for j in range(0, n - 1 - i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
            yield arr

def selection_sort(a: List[int]):
    arr = a
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
            yield arr
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield arr

def insertion_sort(a: List[int]):
    arr = a
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            j -= 1
            yield arr
        arr[j+1] = key
        yield arr

def merge_sort(a: List[int]):
    arr = a
    aux = [0]*len(arr)

    def _merge_sort(l, r):
        if r - l <= 1:
            return
        m = (l + r)//2
        yield from _merge_sort(l, m)
        yield from _merge_sort(m, r)
        i, j, k = l, m, l
        while i < m and j < r:
            if arr[i] < arr[j]:
                aux[k] = arr[i]; i += 1
            else:
                aux[k] = arr[j]; j += 1
            k += 1
            yield arr
        while i < m:
            aux[k] = arr[i]; i += 1; k += 1; yield arr
        while j < r:
            aux[k] = arr[j]; j += 1; k += 1; yield arr
        for i in range(l, r):
            arr[i] = aux[i]
            yield arr

    yield from _merge_sort(0, len(arr))


def quick_sort(a: List[int]):
    arr = a

    def _q(l, r):
        if l >= r:
            return
        pivot = arr[r]
        i = l
        for j in range(l, r):
            if arr[j] < pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
            yield arr
        arr[i], arr[r] = arr[r], arr[i]
        yield arr
        yield from _q(l, i-1)
        yield from _q(i+1, r)

    yield from _q(0, len(arr)-1)


def heap_sort(a: List[int]):
    arr = a
    n = len(arr)

    def heapify(n, i):
        largest = i
        l, r = 2*i+1, 2*i+2
        if l < n and arr[l] > arr[largest]:
            largest = l
        if r < n and arr[r] > arr[largest]:
            largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            yield arr
            yield from heapify(n, largest)

    for i in range(n//2-1, -1, -1):
        yield from heapify(n, i)
    for i in range(n-1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        yield arr
        yield from heapify(i, 0)


def shell_sort(a: List[int]):
    arr = a
    n = len(arr)
    gap = n//2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j-gap] > temp:
                arr[j] = arr[j-gap]
                j -= gap
                yield arr
            arr[j] = temp
            yield arr
        gap //= 2


def comb_sort(a: List[int]):
    arr = a
    n = len(arr)
    gap = n
    shrink = 1.3
    swapped = True
    while gap > 1 or swapped:
        gap = max(1, int(gap / shrink))
        swapped = False
        for i in range(n - gap):
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swapped = True
            yield arr


def gnome_sort(a: List[int]):
    arr = a
    i = 0
    while i < len(arr):
        if i == 0 or arr[i-1] <= arr[i]:
            i += 1
        else:
            arr[i], arr[i-1] = arr[i-1], arr[i]
            i -= 1
        yield arr


def tim_sort(a):
    arr = a
    min_run = 32
    n = len(arr)


    for start in range(0, n, min_run):
        end = min(start + min_run, n)
        for i in range(start + 1, end):
            key = arr[i]
            j = i - 1
            while j >= start and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
                yield arr
            arr[j + 1] = key
            yield arr


    size = min_run
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n, left + size)
            right = min(n, left + 2 * size)
            merged = []
            i, j = left, mid
            while i < mid and j < right:
                if arr[i] < arr[j]:
                    merged.append(arr[i])
                    i += 1
                else:
                    merged.append(arr[j])
                    j += 1
                yield arr
            merged.extend(arr[i:mid])
            merged.extend(arr[j:right])
            for i in range(len(merged)):
                arr[left + i] = merged[i]
                yield arr
        size *= 2

# ------------------------------ Visualization ------------------------------

ALGORITHMS = {
    'Bubble': bubble_sort,
    'Selection': selection_sort,
    'Insertion': insertion_sort,
    'Merge': merge_sort,
    'Quick': quick_sort,
    'Heap': heap_sort,
    'Shell': shell_sort,
    'Comb': comb_sort,
    'Gnome': gnome_sort,
    'TimSort': tim_sort
}

COLORS = [(200, 80, 80), (80, 200, 120), (80, 150, 250), (230, 180, 70), (180, 120, 220), (90, 220, 180), (255, 130, 90), (100, 100, 255), (200, 200, 100), (255, 180, 180)]


def draw_array(surface, arr, color, x, y, w, h):
    n = len(arr)
    if n == 0:
        return
    bar_width = w / n
    max_val = max(arr) if max(arr) != 0 else 1
    for i, val in enumerate(arr):
        bar_height = (val / max_val) * (h - 30)
        rect = pygame.Rect(int(x + i * bar_width), int(y + h - bar_height), max(1, int(bar_width) - 1), int(bar_height))
        pygame.draw.rect(surface, color, rect)


def main():
    pygame.init()
    WIDTH, HEIGHT = 2000, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Сравнение алгоритмов сортировки")
    clock = pygame.time.Clock()

    n = 60
    arr = [random.randint(1, 100) for _ in range(n)]

    generators = {}
    arrays = {}
    done = {name: False for name in ALGORITHMS.keys()}
    for i, (name, func) in enumerate(ALGORITHMS.items()):
        arrays[name] = list(arr)
        generators[name] = func(arrays[name])

    paused = False
    running = True

    cols = 5
    rows = math.ceil(len(ALGORITHMS) / cols)
    panel_w = WIDTH // cols
    panel_h = HEIGHT // rows

    font = pygame.font.SysFont('Arial', 18)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    arr = [random.randint(1, 100) for _ in range(n)]
                    for name, func in ALGORITHMS.items():
                        arrays[name] = list(arr)
                        generators[name] = func(arrays[name])
                        done[name] = False

        screen.fill((30, 30, 40))

        if not paused:
            for name, gen in generators.items():
                if done.get(name):
                    continue
                try:
                    state = next(gen)
                    arrays[name] = state
                except StopIteration:
                    done[name] = True

        # Панельки
        for i, (name, arr_data) in enumerate(arrays.items()):
            x = (i % cols) * panel_w
            y = (i // cols) * panel_h

            panel_rect = pygame.Rect(x+2, y+2, panel_w-4, panel_h-4)
            pygame.draw.rect(screen, (40, 40, 50), panel_rect)

            draw_array(screen, arr_data, COLORS[i % len(COLORS)], x+8, y+30, panel_w-16, panel_h-40)

            label = font.render(name, True, (230, 230, 230))
            screen.blit(label, (x+10, y+6))
            if done.get(name):
                done_label = font.render('done', True, (180, 255, 180))
                screen.blit(done_label, (x+panel_w-60, y+6))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
