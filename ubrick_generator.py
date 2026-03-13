bl_info = {
    "name": "uBrick Generator",
    "author": "maox (ufolab.it)",
    "version": (0, 9),
    "blender": (3, 0, 0),
    "location": "View3D > Add > Mesh > uBrick",
    "description": "Genera mattoncini procedurali compatibili LEGO con stud, fondo cavo e nervature interne",
    "category": "Add Mesh",
}

import bpy
import bmesh
import math
from bpy.props import IntProperty, FloatProperty

UNIT         = 8.0
STUD_R       = 2.4
STUD_H       = 1.6
BRICK_H      = 9.6
GAP          = 0.2
WALL_T       = 1.2
RIB_T        = 0.8
TUBE_OUTER_R = 3.25
TUBE_INNER_R = 2.5
SEG          = 32

OUTER_EXPAND = 0.2
TUBE_EXPAND  = 0.3
STUD_EXPAND  = 0.1


def crea_mattone(stud_x, stud_y, altezza_mattoni, context,
                 outer_expand=OUTER_EXPAND,
                 tube_expand=TUBE_EXPAND,
                 stud_expand=STUD_EXPAND):

    bm  = bmesh.new()
    sr  = STUD_R + stud_expand
    W   = stud_x * UNIT - GAP + outer_expand * 2
    L   = stud_y * UNIT - GAP + outer_expand * 2
    H   = altezza_mattoni * BRICK_H
    t   = WALL_T
    ox  = -outer_expand;  oy = -outer_expand
    zp  = H - t

    def v(*a): return bm.verts.new(a)

    # ── Vertici ──────────────────────────────────────────────────
    e0=v(ox,   oy,   0); e1=v(ox+W, oy,   0)
    e2=v(ox+W, oy+L, 0); e3=v(ox,   oy+L, 0)
    e4=v(ox,   oy,   H); e5=v(ox+W, oy,   H)
    e6=v(ox+W, oy+L, H); e7=v(ox,   oy+L, H)
    ib0=v(t,      t,      0); ib1=v(ox+W-t, t,      0)
    ib2=v(ox+W-t, oy+L-t, 0); ib3=v(t,      oy+L-t, 0)
    im0=v(t,      t,      zp); im1=v(ox+W-t, t,      zp)
    im2=v(ox+W-t, oy+L-t, zp); im3=v(t,      oy+L-t, zp)
    it0=v(t,      t,      H); it1=v(ox+W-t, t,      H)
    it2=v(ox+W-t, oy+L-t, H); it3=v(t,      oy+L-t, H)

    # ── Pareti esterne — normale outward ─────────────────────────
    bm.faces.new([e0,e1,e5,e4])  # front -Y
    bm.faces.new([e1,e2,e6,e5])  # right +X
    bm.faces.new([e2,e3,e7,e6])  # back  +Y
    bm.faces.new([e3,e0,e4,e7])  # left  -X

    # ── Pareti interne — normale verso la cavità ──────────────────
    bm.faces.new([ib0,ib1,im1,im0])  # front inner +Y
    bm.faces.new([ib1,ib2,im2,im1])  # right inner -X
    bm.faces.new([ib2,ib3,im3,im2])  # back  inner -Y
    bm.faces.new([ib3,ib0,im0,im3])  # left  inner +X

    # ── Anello fondo — normale DOWN ───────────────────────────────
    bm.faces.new([e1,e0,ib0,ib1])
    bm.faces.new([e2,e1,ib1,ib2])
    bm.faces.new([e3,e2,ib2,ib3])
    bm.faces.new([e0,e3,ib3,ib0])

    # ── Soffitto cavità z=zp — normale DOWN ──────────────────────
    bm.faces.new([im1,im0,im3,im2])

    # ── Ring top z=H — normale UP (+Z) ───────────────────────────
    bm.faces.new([e4,e5,it1,it0])  # front ring
    bm.faces.new([e5,e6,it2,it1])  # right ring
    bm.faces.new([e6,e7,it3,it2])  # back  ring
    bm.faces.new([e7,e4,it0,it3])  # left  ring

    # ── Piano top centrale z=H — normale UP (+Z) ─────────────────
    bm.faces.new([it0,it1,it2,it3])

    # ── Stud: cilindri chiusi, base a H+0.01 ─────────────────────
    zb = H + 0.01;  zt = zb + STUD_H
    for xi in range(stud_x):
        for yi in range(stud_y):
            cx = UNIT*0.5 + xi*UNIT - GAP/2
            cy = UNIT*0.5 + yi*UNIT - GAP/2
            rb=[]; rt=[]
            for i in range(SEG):
                a = 2*math.pi*i/SEG
                rb.append(v(cx+sr*math.cos(a), cy+sr*math.sin(a), zb))
                rt.append(v(cx+sr*math.cos(a), cy+sr*math.sin(a), zt))
            bm.faces.new(list(reversed(rb)))  # base DOWN
            bm.faces.new(rt)                  # top  UP
            for i in range(SEG):
                n=(i+1)%SEG; bm.faces.new([rb[i],rb[n],rt[n],rt[i]])

    # ── Tubi anti-stud ───────────────────────────────────────────
    for xi in range(1, stud_x):
        for yi in range(1, stud_y):
            cx=xi*UNIT-GAP/2; cy=yi*UNIT-GAP/2
            ro=TUBE_OUTER_R+tube_expand; ri=TUBE_INNER_R
            aeb=[]; aib=[]; aet=[]; ait=[]
            for i in range(SEG):
                a=2*math.pi*i/SEG; c=math.cos(a); s=math.sin(a)
                aeb.append(v(cx+ro*c, cy+ro*s, 0))
                aib.append(v(cx+ri*c, cy+ri*s, 0))
                aet.append(v(cx+ro*c, cy+ro*s, zp))
                ait.append(v(cx+ri*c, cy+ri*s, zp))
            for i in range(SEG):
                n=(i+1)%SEG
                bm.faces.new([aet[i],aet[n],ait[n],ait[i]])
                bm.faces.new([aib[i],aib[n],aeb[n],aeb[i]])
                bm.faces.new([aeb[i],aeb[n],aet[n],aet[i]])
                bm.faces.new([ait[i],ait[n],aib[n],aib[i]])

    # ── Nervature interne ─────────────────────────────────────────
    y_start=t; y_end=oy+L-t
    for xi in range(1, stud_x):
        cx=xi*UNIT-GAP/2; x0=cx-RIB_T/2; x1=cx+RIB_T/2
        if stud_y==1:
            segs=[(y_start,y_end)]
        else:
            tys=[yi*UNIT-GAP/2 for yi in range(1,stud_y)]
            tr2=TUBE_OUTER_R+tube_expand
            segs=[(y_start,tys[0]-tr2)]
            for k in range(len(tys)-1): segs.append((tys[k]+tr2,tys[k+1]-tr2))
            segs.append((tys[-1]+tr2,y_end))
        for (ya,yb) in segs:
            if yb-ya<0.01: continue
            b0=v(x0,ya,0);  b1=v(x1,ya,0);  b2=v(x1,yb,0);  b3=v(x0,yb,0)
            t0=v(x0,ya,zp); t1=v(x1,ya,zp); t2=v(x1,yb,zp); t3=v(x0,yb,zp)
            bm.faces.new([b3,b2,b1,b0]); bm.faces.new([t0,t1,t2,t3])
            bm.faces.new([b0,b1,t1,t0]); bm.faces.new([b1,b2,t2,t1])
            bm.faces.new([b2,b3,t3,t2]); bm.faces.new([b3,b0,t0,t3])

    return bm


def bmesh_to_obj(bm, name, context):
    mesh = bpy.data.meshes.new(name)
    bm.to_mesh(mesh); bm.free()
    obj = bpy.data.objects.new(name, mesh)
    context.collection.objects.link(obj)
    return obj


class MESH_OT_aggiungi_mattone_lego(bpy.types.Operator):
    bl_idname      = "mesh.aggiungi_mattone_lego"
    bl_label       = "uBrick"
    bl_description = "Aggiunge un mattoncino uBrick manifold, pronto per la stampa 3D"
    bl_options     = {'REGISTER', 'UNDO'}

    stud_x: IntProperty(name="Larghezza (stud)", default=4, min=1, max=32)
    stud_y: IntProperty(name="Lunghezza (stud)",  default=2, min=1, max=32)
    altezza_mattoni: IntProperty(name="Altezza (mattoni)", default=1, min=1, max=16)
    outer_expand: FloatProperty(name="Espansione pareti (mm)",
        default=OUTER_EXPAND, min=0.0, max=1.0, step=1, precision=2)
    tube_expand: FloatProperty(name="Espansione tubi (mm)",
        default=TUBE_EXPAND,  min=0.0, max=1.0, step=1, precision=2)
    stud_expand: FloatProperty(name="Espansione stud (mm)",
        default=STUD_EXPAND,  min=0.0, max=1.0, step=1, precision=2)

    def execute(self, context):
        bm  = crea_mattone(self.stud_x, self.stud_y, self.altezza_mattoni,
                           context, self.outer_expand,
                           self.tube_expand, self.stud_expand)
        obj = bmesh_to_obj(bm, "uBrick", context)
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        context.view_layer.objects.active = obj
        self.report({'INFO'}, f"uBrick {self.stud_x}x{self.stud_y} creato!")
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(MESH_OT_aggiungi_mattone_lego.bl_idname,
                         text="uBrick", icon='MESH_CUBE')

def register():
    bpy.utils.register_class(MESH_OT_aggiungi_mattone_lego)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(MESH_OT_aggiungi_mattone_lego)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()
