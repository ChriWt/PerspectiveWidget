#if !defined(__VECTOR3_H__)
#define __VECTOR3_H__
#include "Vector3.h"
#endif

#if !defined(__SHAPE3D_H__)
#define __SHAPE3D_H__
#include "Shape3D.h"
#endif


class Piramid: public Shape3D {

    public:

        Piramid() : Shape3D(Vector3(0, 0, 0), Vector3(0, 0, 0), Vector3(0, 0, 0), 0, 0, 0, 0) {}

        Piramid(Vector3 origin, Vector3 rotation, Vector3 translation, int verticeCount, int width, int height, int depth): 
            Shape3D(origin, rotation, translation, verticeCount, width, height, depth) {}

        std::vector<Vector3> getVertices() {
            return {};
        }

        std::vector<std::tuple<int, int>> getEdges() {
            return {};
        }

};