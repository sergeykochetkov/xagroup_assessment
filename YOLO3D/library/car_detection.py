import math


class CarDetection:
    def __init__(self, edge_centers_projection, speed_projection):
        self.edge_centers_projection, self.speed_projection = edge_centers_projection, speed_projection

    def get_talignating_point(self, other):
        min_dist = None
        talignating_pt = None
        for p in self.edge_centers_projection:
            for p1 in other.edge_centers_projection:
                d = sum([(p[i] - p1[i]) ** 2 for i in range(2)])
                d = math.sqrt(d)
                if min_dist is None or d < min_dist:
                    min_dist = d
                    talignating_pt = [int((p[i] + p1[i]) / 2) for i in range(2)]

        avg_speed = [(self.speed_projection[i] + other.speed_projection[i]) / 2 for i in range(2)]
        avg_speed = math.sqrt(avg_speed[0] ** 2 + avg_speed[1] ** 2)
        if avg_speed > 0 and min_dist / avg_speed < 1:
            return talignating_pt
        else:
            return None
