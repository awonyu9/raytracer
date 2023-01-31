def make_BVH(surfaces,axis=0):
    """Build BVH from list of surfaces"""
    assert len(surfaces) > 0
    if len(surfaces) == 1:
        return surfaces[0]
    else:
        return BVH(surfaces,axis)

class BVH:
    def __init__(self,surfaces,axis):
        n = len(surfaces)
        assert n >1

        #sort objects by midpoint along axis
        def keyfn(s): return s.bbox.midpoint[axis]
        surfaces.sort(key=keyfn)
        self.surfaces = surfaces
        #split into two halves
        m = n//2
        next_axis = (axis+1)%3
        #put left objs into left bvh
        self.left = make_BVH(surfaces[:m],next_axis)
        #put right objs into right bvh
        self.right = make_BVH(surfaces[m:],next_axis)
        
        #build combined bbox
        self.bbox = self.left.bbox.combine(self.right.bbox)

    def intersect(self,ray,interval,info):
        if not self.bbox.hit(ray,interval):
            return False
        hit =False
        if self.left.intersect(ray,interval,info):
            hit= True
            interval.high = info.t
        if self.right.intersect(ray,interval,info):
            hit = True
            interval.high = info.t
        return hit

    def iter_polygons(self):
        for surface in self.surfaces:
            for poly in surface.iter_polygons():
                yield poly
        
