
class Piramid: public Shape3D {

    public:

        Piramid() : Shape3D(Vector3(0, 0, 0), Vector3(0, 0, 0), Vector3(0, 0, 0), 0, 0, 0, 0) {}

        Piramid(Vector3 origin, Vector3 rotation, Vector3 translation, int verticeCount, int width, int height, int depth): 
            Shape3D(origin, rotation, translation, verticeCount, width, height, depth) {}

        Piramid(Vector3 origin, int verticeCount, int width, int height, int depth):
            Shape3D(origin, Vector3(0, 0, 0), Vector3(0, 0, 0), verticeCount, width, height, depth) {}

        Piramid(Vector3 origin, int verticeCount, int width):
            Shape3D(origin, Vector3(0, 0, 0), Vector3(0, 0, 0), verticeCount, width, width, width) {}

        std::vector<Vector3> getVertices() {
            std::vector<Vector3> vertices;
            Vector3 origin = getOrigin();
            int width = getWidth();
            int height = getHeight();
            int depth = getDepth();
            int verticeCount = getVerticeCount();
            vertices.push_back(Vector3(origin.x, origin.y + height, origin.z));

            float alpha = 2 * M_PI / getVerticeCount();

            for (int i = 0; i < verticeCount; i++) {
                float x = origin.x + width * cos(alpha * i);
                float z = origin.z + depth * sin(alpha * i);
                vertices.push_back(Vector3(x, origin.y, z));
            }

            return vertices;
        }

        std::vector<std::tuple<int, int>> getEdges() {
            std::vector<std::tuple<int, int>> edges;
            int verticeCount = getVerticeCount();

            for (int i = 1; i < verticeCount; i++) {
                edges.push_back(std::make_tuple(0, i));
                edges.push_back(std::make_tuple(i, i + 1));
            }
            
            edges.push_back(std::make_tuple(0, verticeCount));
            edges.push_back(std::make_tuple(1, verticeCount));

            return edges;
        }

};