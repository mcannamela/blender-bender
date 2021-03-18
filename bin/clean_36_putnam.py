from collections import defaultdict

import bpy


def get_materials_map():
    return {
        '__11_Colonial_White': 'white-porcelain-material',
        'Aquatica_Aquatica_True_Ofuro_Regular_True_Ofuro_Regular_Aquatic': 'tub-material',
        'Color_C01': 'ceiling-material',
        'Color_C02': 'ceiling-material',
        'Color_C06': 'teak-material',
        'Color_F01': 'guest-bath-floor-material',
        'Color_G06': 'dormer-interior-material',
        'Color_K01': 'Roofing_Shingles_GAF_Estates',
        'Color_M07': 'master-sink-material',
        'dormer-interior-material': 'dormer-interior-material',
        'guest-bath-floor-material': 'guest-bath-floor-material',
        'guest-bath-half-wall-material': 'guest-bath-half-wall-material',
        'guest-surround-tile': 'guest-surround-tile',
        'Helen_BraceletGlasses': 'Helen_BraceletGlasses',
        'interior-shell-angled-wall-material': 'interior-shell-angled-wall-material',
        'interior-shell-kneewall-material': 'interior-shell-kneewall-material',
        'interior-wall-angled-shell-back-material': 'interior-wall-angled-shell-back-material',
        'light-material': 'light-material',
        'master-bath-countertop-material': 'master-bath-countertop-material',
        'master-bath-material': 'master-bath-material',
        'master-vanity-material': 'master-vanity-material',
        'Material': 'material',
        'material': 'material',
        'metal-fixture-material': 'metal-fixture-material',
        'metal-fixture-material_0': 'metal-fixture-material',
        'Mirror_01': 'Mirror_01',
        'off-white-porcelain-material': 'material',
        'Roofing_Shingles_GAF_Estates': 'Roofing_Shingles_GAF_Estates',
        'shiny-grey-metal-seamless-texture-light-steel-chrome-material-h': 'metal-fixture-material',
        'Steel_Brushed_Stainless': 'metal-fixture-material',
        'Steel_Brushed_Stainless_1': 'metal-fixture-material',
        'Translucent_Glass_Gray': 'Translucent_Glass_Gray',
        'tub-material': 'tub-material',
        'Wallpaper_Thin_Brown_Stripes': 'Wallpaper_Thin_Brown_Stripes',
        'wet-bar-cabinet-material': 'wet-bar-cabinet-material',
        'wetbar-countertop-material': 'wetbar-countertop-material',
        'white-porcelain-material': 'white-porcelain-material',
        'White_Subway_Tile': 'guest-surround-tile',
        'wife-hair-material': 'wife-hair-material',
        'wife-skin-material': 'wife-skin-material',
        'window-trim-material': 'window-trim-material',
        'wood-floor-material': 'wood-floor-material',
    }


def get_materials_renames():
    return {
        'Helen_BraceletGlasses': 'wife-eye-material',  # erin eye
        'Mirror_01': 'mirror-material',
        'Roofing_Shingles_GAF_Estates': 'roof-shingles-material',
        'Translucent_Glass_Gray': 'glass-material',
        'tub-material': 'tub-material',
        'Wallpaper_Thin_Brown_Stripes': 'bed-material',
        'wet-bar-cabinet-material': 'wet-bar-cabinet-material',
        'wetbar-countertop-material': 'wet-bar-countertop-material',
    }


def get_renamed_materials_map():
    nm = get_materials_renames()
    return {nm.get(k, k): nm.get(v, v) for k, v in get_materials_map().items()}


def log(msg='', indent=0):
    print('' * 2 * indent, msg)


def remove_non_default_cameras():
    log('remove non-default cameras')
    for cam in bpy.data.cameras:
        if cam.name != "Camera":
            log(f'remove {cam}', 1)
            bpy.data.cameras.remove(cam)


def hide_roof_and_ceilings():
    log('hide roof and ceilings')
    keys = ['roof', 'ceiling', 'guest-bath-ceiling']
    for k in keys:
        hide_set_recursive(bpy.data.objects[k], state=True)


def hide_set_recursive(node, state=True):
    node.hide_set(state)
    for c in node.children:
        hide_set_recursive(c)


def clean_up():
    log('\nclean up')
    remove_non_default_cameras()
    hide_roof_and_ceilings()


def clean_unused_and_edge_materials():
    log('\nclean materials')

    usages = defaultdict(int)

    remove_all_unused_material_slots()

    for obj in bpy.data.objects:
        for slot in obj.material_slots:
            if slot.material is not None:
                usages[slot.material.name] += 1

    materials = bpy.data.materials

    for m in materials:
        log(f'{m.name} - {usages[m.name]}', 1)
        if usages[m.name] == 0:
            log('deleting (no usages)', 2)
            bpy.data.materials.remove(m)
        if m.name.startswith('edge_color'):
            log('deleting (edge)', 2)
            bpy.data.materials.remove(m)

    remove_all_unused_material_slots()


def remove_all_unused_material_slots():
    context = bpy.context
    scene = context.scene

    bpy.ops.object.material_slot_remove_unused(
        {"object": scene.objects[0],
         "selected_objects": scene.objects
         }
    )


def rename_materials():
    nm = get_materials_renames()
    for m in bpy.data.materials:
        if m.name in nm:
            m.name = nm[m.name]


def reassign_materials():
    mat_map = get_renamed_materials_map()
    for obj in bpy.data.objects:
        for slot_idx, slot in enumerate(obj.material_slots):
            if slot.material is not None:
                new_mat_nm = mat_map.get(slot.material.name, slot.material)
                if new_mat_nm != slot.material.name:
                    new_mat = bpy.data.materials[new_mat_nm]
                    obj.material_slots[slot_idx] = new_mat


def list_material_names():
    log('\n list materials:')
    materials = bpy.data.materials

    for m in materials:
        log(m.name, 1)


if __name__ == "__main__":
    #    clean_up()
    clean_unused_and_edge_materials()
    list_material_names()

    rename_materials()
    list_material_names()
