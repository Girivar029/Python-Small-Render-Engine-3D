class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"

def load_obj(filename):
    vertices = []
    faces = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('v '):
                parts = line.strip().split()
                x, y, z = map(float, parts[1:4])
                vertices.append(Vector3(x, y, z))
            elif line.startswith('f '):
                parts = line.strip().split()
                face = []
                for part in parts[1:]:
                    idx = part.split('/')[0]
                    face.append(int(idx) - 1)  # OBJ indices start at 1
                faces.append(tuple(face))
    return vertices, faces

if __name__ == "__main__":
    filename = 'Learning process\model.obj'
    verts, faces = load_obj(filename)
    print("Vertices:")
    for v in verts:
        print(v)
    print("\nFaces:")
    for f in faces:
        print(f)
