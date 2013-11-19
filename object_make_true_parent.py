# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    'name': 'Make True Parent',
    'description': 'Make True Parent',
    'location': 'View3D > Ctrl+Shift+Alt+P',
    'author': 'Bartek Skorupa',
    'version': (1, 0),
    'blender': (2, 6, 4),
    'category': 'Object',
    "warning": "",
    }

import bpy

def make_true_parent(option):
    selected = bpy.context.selected_objects
    active = bpy.context.active_object
    
    for ob in selected:
        if ob != active:
            m = ob.matrix_world
            ob.parent = active
            if option == 0:  # Make parent - leave visible transforms of children, recalculate transform values
                ob.matrix_world = m
            elif option == 1:  # Make parent and reset transforms (move children to parent's loc/rot/scale)
                ob.matrix_local.identity()
            # elif option 2 - do nothing - this will keep transforms values untouched, but move children accordingly.
    return {'FINISHED'}

class MakeTrueParent(bpy.types.Operator):
    bl_idname = "object.make_true_parent"
    bl_label = "Make True Parent"
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None and len(context.selected_objects) > 1)
    
    def execute(self, context):
        return make_true_parent(0)

class MakeTrueParentReset(bpy.types.Operator):
    bl_idname = "object.make_true_parent_reset"
    bl_label = "Make True Parent Reset"
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None and len(context.selected_objects) > 1)
    
    def execute(self, context):
        return make_true_parent(1)

class MakeTrueParentKeepTransforms(bpy.types.Operator):
    bl_idname = "object.make_true_parent_keep_transforms"
    bl_label = "Make True Parent and Keep Transforms"
    
    @classmethod
    def poll(cls, context):
        return (context.active_object != None and len(context.selected_objects) > 1)
    
    def execute(self, context):
        return make_true_parent(2)

class MakeTrueParentMenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_make_true_parent"
    bl_label = "Make True Parent"
    
    def draw(self, context):
        layout = self.layout
        layout.operator("object.make_true_parent", text = "Make True Parent (Keep Visual Transforms)")
        layout.operator("object.make_true_parent_keep_transforms", text = "Make True Parent (Keep Transform Values)")
        layout.operator("object.make_true_parent_reset", text = "Make True Parent (Reset Transforms)")

    
addon_keymaps = []

def register():
    bpy.utils.register_module(__name__)
    km = bpy.context.window_manager.keyconfigs.addon.keymaps.new(name="Object Mode")
    kmi = km.keymap_items.new('wm.call_menu', 'P', 'PRESS', shift = True, ctrl = True, alt = True)
    kmi.properties.name = 'OBJECT_MT_make_true_parent'
    addon_keymaps.append((km, kmi))

def unregister():
    bpy.utils.unregister_module(__name__)
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
	