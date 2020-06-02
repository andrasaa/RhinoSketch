import Rhino
import scriptcontext
import rhinoscriptsyntax as rs
import scriptcontext as sc

def SolidSlabSQ():
    rs.WorldXYPlane()
    thk = rs.GetReal ( "Wall thickness", number=None, minimum=None, maximum=None )
    rs.Command("_Plane " ,False)
    rs.EnableRedraw(False)
    surface = rs.LastCreatedObjects (select=False)
    # Create slab:
    if thk != 0:
        surfaceOffset = rs.OffsetSurface (surface, thk, None, False, False)
        connect = rs.DuplicateSurfaceBorder (surface, type=0)
        connectOffset = rs.DuplicateSurfaceBorder (surfaceOffset, type=0)
        loft = rs.AddLoftSrf ( (connect[0],connectOffset[0]), None, None, 0, 0, 0, False )  
        expl = rs.ExplodePolysurfaces (loft, True)
        # Notes: rs.Command() requires object to be added to the objectTable.
        surfaceCO = rs.coercebrep(surface)
        obj = sc.doc.Objects.AddBrep(surfaceCO)
        sc.doc.Views.Redraw()
        rs.DeleteObject(surface)
        rs.Command("_Dir SelID " + str(obj) +  " _Enter Flip _Enter ")
        rs.SetUserText(obj, "Surface", "Base", attach_to_geometry=False)
        rs.SetUserText(obj, "SurfaceType", "Planar", attach_to_geometry=False)
        # Add items to group;
        group = rs.AddGroup()
        rs.AddObjectsToGroup([surface,surfaceOffset], group)
        for i in expl:
            rs.AddObjectToGroup(i,group)
        rs.DeleteObjects([connect,connectOffset])
    return
if __name__ == "__main__":
    ExtrudeStraigt()
