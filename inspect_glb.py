import sys
import struct
import json
from pathlib import Path


def inspect_glb(path):
    p = Path(path)
    if not p.exists():
        print(f"File not found: {path}")
        return 1

    with p.open('rb') as f:
        header = f.read(12)
        if len(header) < 12:
            print('Not a valid GLB (header too short)')
            return 2
        magic, version, length = struct.unpack('<4sII', header)
        if magic != b'glTF':
            print('Not a GLB file (magic mismatch)')
            return 3

        json_chunk = None
        # Read chunks
        bytes_read = 12
        while bytes_read < length:
            chunk_header = f.read(8)
            if len(chunk_header) < 8:
                break
            chunk_len, chunk_type = struct.unpack('<I4s', chunk_header)
            chunk_data = f.read(chunk_len)
            bytes_read += 8 + chunk_len
            if chunk_type == b'JSON':
                try:
                    json_chunk = json.loads(chunk_data.decode('utf-8'))
                except Exception as e:
                    print('Failed to decode JSON chunk:', e)
                    return 4
                break

    if json_chunk is None:
        print('No JSON chunk found in GLB')
        return 5

    # Inspect JSON for skins/animations
    skins = json_chunk.get('skins', [])
    animations = json_chunk.get('animations', [])
    nodes = json_chunk.get('nodes', [])

    rigged = False
    joints_info = []
    if skins:
        rigged = True
        for i, skin in enumerate(skins):
            joints = skin.get('joints', [])
            skeleton_root = skin.get('skeleton')
            joints_info.append({
                'skin_index': i,
                'joints_count': len(joints),
                'skeleton_root': skeleton_root
            })

    # Also check if any node has a skin property
    nodes_with_skin = [i for i, n in enumerate(nodes) if isinstance(n, dict) and 'skin' in n]
    if nodes_with_skin:
        rigged = True

    print('GLB inspection result for:', path)
    print(' - Animations found:', len(animations))
    if len(animations):
        names = [anim.get('name') for anim in animations]
        print(' - Animation names:', names)
    print(' - Skins present:', len(skins))
    if joints_info:
        for info in joints_info:
            print(f"   - Skin {info['skin_index']}: joints={info['joints_count']}, skeleton_root={info['skeleton_root']}")
    if nodes_with_skin:
        print(' - Nodes with skin property (indices):', nodes_with_skin)

    if rigged:
        print('\nConclusion: The model appears to be rigged (has skins/joints).')
    else:
        print('\nConclusion: No skin data found; model is likely not rigged.')

    return 0


if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'dq.glb'
    sys.exit(inspect_glb(target))
