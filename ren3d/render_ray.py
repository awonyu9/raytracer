# render_ray.py
#    Ray tracing rendering algorithms

from ren3d.ray3d import Interval, Point,Ray
from ren3d.models import Record


def raytrace(scene, img, updatefn=None):
    """basic raytracing algorithm to render scene into img
    """


    w,h = img.size
    cam = scene.camera
    cam.set_resolution(w,h)
    for j in range(h):
        for i in range(w):
            ray = cam.ij_ray(i,j)
            color = raycolorBP(scene,ray,Interval(),scene.reflections)
            img[(i,j)]= color.quantize(255)
        if updatefn:
            updatefn()
            
"""
def raycolorLambert(scene, ray, interval):
    #returns the color of ray in the scene
    
    #do scene intersection and return color that the ray intersects

    objects = scene.objects
    info = Record(color = None,t= None, normal=None, point=None)

    intrsct = objects.intersect(ray,interval,info)
    if intrsct:
        return lambert_shading(scene,info,ray)
    
    return scene.background
    """

def raycolorBP(scene, ray, interval,nreflections):
    """returns the color of ray in the scene
    """
    #do scene intersection and return color that the ray intersects

    surface = scene.surface
    info = Record(color = None,t= None, normal=None, point=None)

    #intrsct = objects.intersect(ray,interval,info)
    intrsct = surface.intersect(ray,interval,info)
    if intrsct:
        return blinn_phong(scene,info,ray,nreflections)
    
    return scene.background
    
def blinn_phong(scene,info,ray,nreflections):
    K = info.color
    
    if scene.textures and info.texture:
        uvn = info.uvn
        Kd = Ka = info.texture(uvn)
    else:
        Kd = K.diffuse
        Ka = K.ambient

    Ks = K.specular
    S = K.shininess
    Kr = K.reflect
 
    n = info.normal
    color = Ka*scene.ambient #add ambient
    
    for lightpos,lightcolor in scene.lights:
           
        lvec = (lightpos-info.point).normalized()
        lambert = max(0,lvec.dot(n))

        shadowray = Ray(info.point, (lightpos-info.point))
        #Check if light hits surface directly
        if not scene.surface.intersect(shadowray,Interval(0.001,1),Record()):
            #SURFACE INSTEAD AGAIN
            color += lambert*Kd*lightcolor#add diffuse
        
            h = ((-ray.dir).normalized()+ lvec)
            h.normalize()
            color += (Ks*lightcolor*max(0,(h.dot(n)))**S)#Add specular

    if Kr is not None and nreflections >0:
        reflected_dir = ray.dir.reflect(n)
        reflected_ray = Ray(info.point,reflected_dir)
        rcolor = raycolorBP(scene,reflected_ray,Interval(0.001,2),nreflections-1)
        color+= Kr*rcolor
    return color
        


#color of object modified by lambert coeff.

"""def lambert_shading(scene,info,ray):
    eye = scene.camera.eye
    normal = info.normal
    
    lvec = (scene.light - info.point).normalized()
    lambert = max(0,lvec.dot(normal))
    color = lambert*info.color+ scene.ambient*info.color

    return color"""

#REFLECTION
#def reflect(self,n):
#   return self- 2*(self.dot(n))*n

#SPECULAR FACTOR:
#r = reflection
#v = vector hit to eye
#spec factor = (max(0,(r.dot(v))**2))

#QUICKER WAY-half angle hack
# h= (lvec+viewvec).normalized()
# h.dot(normal).clamp => our specular factor
#if h on normal, eye

#blinn-phong shading
#c = Ka Ia + Kd I max(0,n.dot(lvec))+ Ks I max(0,n.dot(h))
#K stuf => surface properties
#I stuff => light(illumination) properties(from scene?)
#a => ambient, d=> diffuse, s=> specular
#(Ia = scene.ambient, I = color of light source)
#Color of object tweaked with (Kd, Ka, Ks, S)- collect them together and call it
    #material


#INCORPORATING
#SCENE must have ambient property
#@property
#def ambient(self):  #getter
    #return self._ambient

#@ambient.setter
#def ambient(self,color):  #setter
    #if type(color) == float:
        #color = [color]*3
    #self.ambient= RGB(color)

#MODELS=>self.color = make_material(color)

#Add to scene set_light
#def set_light(self,pos,color):
    #set self.light to pair(point,RGB) #make sure to set reasonable default in
                                        #init

#RGB.py => modify __mul__ => if type ofother is RGB then component wise
                            #else do what we did before


#RENDER RAY(blinn-phong):
#if scene.objects.intersect(ray,interval,info):
        #compute ambient
    #K = info.color     
    #hitpoint = info.point
    #n = hit.normal
    #color = K.ambient*scene.ambient
        #compute diffuse(lambert)
    
        #compute specular
    #lightpos,lightcolor=scene.light
    #lvec=...
    #vvec = eye position
    #compute h
    #k.specular* lightcolor*max(0,(h.dot(n))**k.shininess #calc and add to color
    


#TO GET MULTIPLE LIGHT SOURCES:
#loop over previous for every light
#set_light,add_light, by making self.lights a list of lights
#for lpos,lcol in scene.lights:

#TO ADD SHADOWS
#only add in the diffuse and specular components if the light source is "visible"
    #from the hit point

#shadow test: shoot a ray from hitpoint to light position
    #Ray(hitpoint, (lpos-hitpoint))
    # scene.objects.intersect(shadowray,Interval(0.001,1),newRecord())







