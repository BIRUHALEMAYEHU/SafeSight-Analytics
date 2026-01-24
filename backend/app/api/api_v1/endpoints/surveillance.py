class SegmentTree:
    def __init__(self, arr):
        self.n = len(arr)
        self.arr = arr[:]

        # Segment tree arrays
        self.sum_tree = [0] * (4 * self.n)
        self.min_tree = [0] * (4 * self.n)

        # Lazy propagation array
        self.lazy = [0] * (4 * self.n)

        self._build(1, 0, self.n - 1)

    # ---------------- BUILD ----------------
    def _build(self, node, start, end):
        if start == end:
            self.sum_tree[node] = self.arr[start]
            self.min_tree[node] = self.arr[start]
            return

        mid = (start + end) // 2
        left = node * 2
        right = node * 2 + 1

        self._build(left, start, mid)
        self._build(right, mid + 1, end)

        self.sum_tree[node] = self.sum_tree[left] + self.sum_tree[right]
        self.min_tree[node] = min(self.min_tree[left], self.min_tree[right])

    # ---------------- LAZY PROPAGATION ----------------
    def _push(self, node, start, end):
        if self.lazy[node] != 0:
            val = self.lazy[node]

            # Update current node
            self.sum_tree[node] += (end - start + 1) * val
            self.min_tree[node] += val

            # Propagate to children if not leaf
            if start != end:
                self.lazy[node * 2] += val
                self.lazy[node * 2 + 1] += val

            self.lazy[node] = 0

    # ---------------- RANGE UPDATE ----------------
    def range_update(self, l, r, val):
        self._range_update(1, 0, self.n - 1, l, r, val)

    def _range_update(self, node, start, end, l, r, val):
        self._push(node, start, end)

        if r < start or end < l:
            return

        if l <= start and end <= r:
            self.lazy[node] += val
            self._push(node, start, end)
            return

        mid = (start + end) // 2
        self._range_update(node * 2, start, mid, l, r, val)
        self._range_update(node * 2 + 1, mid + 1, end, l, r, val)

        self.sum_tree[node] = (
            self.sum_tree[node * 2] + self.sum_tree[node * 2 + 1]
        )
        self.min_tree[node] = min(
            self.min_tree[node * 2], self.min_tree[node * 2 + 1]
        )

    # ---------------- RANGE SUM QUERY ----------------
    def range_sum(self, l, r):
        return self._range_sum(1, 0, self.n - 1, l, r)

    def _range_sum(self, node, start, end, l, r):
        self._push(node, start, end)

        if r < start or end < l:
            return 0

        if l <= start and end <= r:
            return self.sum_tree[node]

        mid = (start + end) // 2
        return (
            self._range_sum(node * 2, start, mid, l, r) +
            self._range_sum(node * 2 + 1, mid + 1, end, l, r)
        )

    # ---------------- RANGE MIN QUERY ----------------
    def range_min(self, l, r):
        return self._range_min(1, 0, self.n - 1, l, r)

    def _range_min(self, node, start, end, l, r):
        self._push(node, start, end)

        if r < start or end < l:
            return float('inf')

        if l <= start and end <= r:
            return self.min_tree[node]

        mid = (start + end) // 2
        return min(
            self._range_min(node * 2, start, mid, l, r),
            self._range_min(node * 2 + 1, mid + 1, end, l, r)
        )

    # ---------------- POINT UPDATE ----------------
    def point_update(self, idx, val):
        self._point_update(1, 0, self.n - 1, idx, val)

    def _point_update(self, node, start, end, idx, val):
        self._push(node, start, end)

        if start == end:
            self.sum_tree[node] = val
            self.min_tree[node] = val
            return

        mid = (start + end) // 2

        if idx <= mid:
            self._point_update(node * 2, start, mid, idx, val)
        else:
            self._point_update(node * 2 + 1, mid + 1, end, idx, val)

        self.sum_tree[node] = (
            self.sum_tree[node * 2] + self.sum_tree[node * 2 + 1]
        )
        self.min_tree[node] = min(
            self.min_tree[node * 2], self.min_tree[node * 2 + 1]
        )

    # ---------------- DEBUG HELPERS ----------------
    def print_trees(self):
        print("Sum Tree:", self.sum_tree[:2*self.n])
        print("Min Tree:", self.min_tree[:2*self.n])
        print("Lazy:", self.lazy[:2*self.n])
