#if !defined(__VECTOR3_H__)
#define __VECTOR3_H__
#include "Vector3.h"
#endif

#if !defined(__SHAPE3D_H__)
#define __SHAPE3D_H__
#include "Shape3D.h"
#endif

#if !defined(M_PI)
#define M_2PI 6.283185307179586
#endif

#include <cmath>


class Cilinder: public Shape3D {

    public:

        Cilinder() : Shape3D(Vector3(0, 0, 0), Vector3(0, 0, 0), Vector3(0, 0, 0), 0, 0, 0, 0) {}

        Cilinder(Vector3 origin, Vector3 rotation, Vector3 translation, int verticeCount, int width, int height, int depth): 
            Shape3D(origin, rotation, translation, verticeCount, width, height, depth) {}

        // std::vector<Vector3> getVertices() {
        //     float alpha = M_2PI / getVerticeCount();
        //     std::vector<Vector3> topVertices;
        //     std::vector<Vector3> bottomVertices;

        //     Vector3 origin = getOrigin();
        //     int width = getWidth();
        //     int height = getHeight();
        //     int depth = getDepth();

        //     for (int i = 0; i < getVerticeCount(); i++) {
        //         float x = origin.x + width * cos(alpha * i);
        //         float z = origin.z + depth * sin(alpha * i);
        //         topVertices.push_back(Vector3(x, origin.y - height, z));
        //         bottomVertices.push_back(Vector3(x, origin.y + height, z));
        //     }
        //     topVertices.insert(topVertices.end(), bottomVertices.begin(), bottomVertices.end());
        //     return topVertices;
        // }

        std::vector<Vector3> getVertices() {
            std::vector<Vector3> vertices;
            float alpha = M_2PI / getVerticeCount();
            Vector3 origin = getOrigin();
            int width = getWidth();
            int height = getHeight();
            int depth = getDepth();

            for (int i = 0; i < getVerticeCount(); i++) {
                float x = origin.x + width * cos(alpha * i);
                float z = origin.z + depth * sin(alpha * i);
                vertices.push_back(Vector3(x, origin.y + height / 2, z));
                vertices.push_back(Vector3(x, origin.y - height / 2, z));
            }

            return vertices;
        }

        std::vector<std::tuple<int, int>> getEdges() {
            std::vector<std::tuple<int, int>> edges;
            int verticeCount = getVerticeCount();
            for (int i = 0; i < verticeCount; i++) {
                edges.push_back(std::make_tuple(2 * i, (2 * i + 2) % (2 * verticeCount)));
                edges.push_back(std::make_tuple(2 * i + 1, (2 * i + 3) % (2 * verticeCount)));
                edges.push_back(std::make_tuple(2 * i, 2 * i + 1));
            }
            return edges;
        }


        // std::vector<std::tuple<int, int>> getEdges() {
        //     std::vector<std::tuple<int, int>> edges = std::vector<std::tuple<int, int>>();
        //     int verticeCount = getVerticeCount();
        //     for (int i = 0; i < verticeCount; i++) {
        //         edges.push_back(std::make_tuple(i, (i + 1) % verticeCount));
        //         edges.push_back(std::make_tuple(i + verticeCount, ((i + 1) % verticeCount) + verticeCount));
        //         edges.push_back(std::make_tuple(i, i + verticeCount));
        //     }
        //     return edges;
        // }
};