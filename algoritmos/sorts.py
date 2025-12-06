# algoritmos/sorts.py
import time
from typing import List, Tuple

def _time_it(func):
    def wrapper(arr: List[int], *args, **kwargs) -> Tuple[List[int], float]:
        start = time.perf_counter()
        result = func(arr, *args, **kwargs)
        end = time.perf_counter()
        elapsed_ms = (end - start) * 1000.0
        return result, elapsed_ms
    return wrapper


def _ensure_copy(arr: List[int]) -> List[int]:
    return list(arr)

@_time_it
def bubble_improved(arr: List[int]) -> List[int]:
    v = _ensure_copy(arr)
    n = len(v)
    for i in range(n):
        swapped = False
        # limitar el recorrido a n-i-1
        for j in range(0, n - i - 1):
            if v[j] > v[j + 1]:
                v[j], v[j + 1] = v[j + 1], v[j]
                swapped = True
        if not swapped:
            break
    return v

@_time_it
def insertion_sort(arr: List[int]) -> List[int]:
    v = _ensure_copy(arr)
    for i in range(1, len(v)):
        key = v[i]
        j = i - 1
        while j >= 0 and v[j] > key:
            v[j + 1] = v[j]
            j -= 1
        v[j + 1] = key
    return v

@_time_it
def selection_sort(arr: List[int]) -> List[int]:
    v = _ensure_copy(arr)
    n = len(v)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if v[j] < v[min_idx]:
                min_idx = j
        if min_idx != i:
            v[i], v[min_idx] = v[min_idx], v[i]
    return v

@_time_it
def shell_sort(arr: List[int]) -> List[int]:
    v = _ensure_copy(arr)
    n = len(v)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = v[i]
            j = i
            while j >= gap and v[j - gap] > temp:
                v[j] = v[j - gap]
                j -= gap
            v[j] = temp
        gap //= 2
    return v

# Quicksort recursivo (cuidado con recursionlimit en tamaños muy grandes)
def _quick_rec(v, low, high):
    if low < high:
        pivot = v[high]
        i = low - 1
        for j in range(low, high):
            if v[j] <= pivot:
                i += 1
                v[i], v[j] = v[j], v[i]
        v[i + 1], v[high] = v[high], v[i + 1]
        p = i + 1
        _quick_rec(v, low, p - 1)
        _quick_rec(v, p + 1, high)

@_time_it
def quicksort_recursive(arr: List[int]) -> List[int]:
    v = _ensure_copy(arr)
    if len(v) <= 1:
        return v
    _quick_rec(v, 0, len(v) - 1)
    return v

# Merge sort recursivo
def _merge(left, right):
    i = j = 0
    out = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out

def _merge_rec(v):
    if len(v) <= 1:
        return v
    mid = len(v) // 2
    left = _merge_rec(v[:mid])
    right = _merge_rec(v[mid:])
    return _merge(left, right)

@_time_it
def mergesort_recursive(arr: List[int]) -> List[int]:
    v = _ensure_copy(arr)
    return _merge_rec(v)
