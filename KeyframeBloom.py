bl_info = {
    "name": "Keyframeable Bloom",
    "description": "Allows keyframing of bloom effect parameters in Blender (Toolbar -> Bloom). Part of the Blender Essential Addon (BEA)",
    "author": "Shadow",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "3D View > Bloom",
    "category": "Animation"
}

import bpy

def update_bloom_settings(self, context):
    scene = context.scene
    bloom_settings = scene.bloom_settings
    render_settings = context.scene.eevee

    render_settings.use_bloom = True
    render_settings.bloom_intensity = bloom_settings.intensity
    render_settings.bloom_threshold = bloom_settings.threshold
    render_settings.bloom_radius = bloom_settings.radius

def frame_change_handler(scene):
    context = bpy.context
    bloom_settings = context.scene.bloom_settings
    render_settings = context.scene.eevee

    render_settings.use_bloom = True
    render_settings.bloom_intensity = bloom_settings.intensity
    render_settings.bloom_threshold = bloom_settings.threshold
    render_settings.bloom_radius = bloom_settings.radius

class BloomKeyframePanel(bpy.types.Panel):
    bl_label = "Bloom Keyframe"
    bl_idname = "PT_BloomKeyframe"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Bloom'

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        scene = context.scene
        bloom_settings = scene.bloom_settings
        render_settings = context.scene.eevee

        layout.prop(bloom_settings, "intensity")
        layout.prop(bloom_settings, "threshold")
        layout.prop(bloom_settings, "radius")
        layout.operator("bloom.keyframe", text="Add Keyframe")
        layout.operator("bloom.reset", text="Reset to Default")

class BloomSettings(bpy.types.PropertyGroup):
    intensity: bpy.props.FloatProperty(name="Intensity", default=0.05, min=0.0, update=update_bloom_settings)
    threshold: bpy.props.FloatProperty(name="Threshold", default=0.8, min=0.0, update=update_bloom_settings)
    radius: bpy.props.FloatProperty(name="Radius", default=6.5, min=0.0, update=update_bloom_settings)

class KeyframeBloomOperator(bpy.types.Operator):
    bl_idname = "bloom.keyframe"
    bl_label = "Keyframe Bloom"

    def execute(self, context):
        # Keyframe the bloom settings
        context.scene.bloom_settings.keyframe_insert(data_path="intensity")
        context.scene.bloom_settings.keyframe_insert(data_path="threshold")
        context.scene.bloom_settings.keyframe_insert(data_path="radius")
        return {'FINISHED'}

class ResetBloomOperator(bpy.types.Operator):
    bl_idname = "bloom.reset"
    bl_label = "Reset Bloom Settings to Default"

    def execute(self, context):
        # Reset bloom settings to default values
        context.scene.bloom_settings.intensity = 0.05
        context.scene.bloom_settings.threshold = 0.8
        context.scene.bloom_settings.radius = 6.5

        return {'FINISHED'}

classes = (
    BloomKeyframePanel,
    BloomSettings,
    KeyframeBloomOperator,
    ResetBloomOperator,
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    bpy.types.Scene.bloom_settings = bpy.props.PointerProperty(type=BloomSettings)
    bpy.app.handlers.frame_change_post.append(frame_change_handler)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.bloom_settings
    bpy.app.handlers.frame_change_post.remove(frame_change_handler)

if __name__ == "__main__":
    register()
