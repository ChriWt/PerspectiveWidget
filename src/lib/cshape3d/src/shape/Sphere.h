#include <cmath>
#include <numeric>

#ifndef M_PI
#define M_PI 3.14159265359
#endif

#include "../vector/Vector3.h"
#include "../shape/Object3D.h"

class Sphere: public Object3D {

    private:

        int getDefaultIfEmpty(int defaultValue, int value) {
            return value == 0 ? defaultValue : value;
        }

    public:
        Sphere() : Object3D(Vector3(0, 0, 0), Vector3(0, 0, 0), Vector3(0, 0, 0), 0, 0, 0, 0) {}

        Sphere(Vector3 origin, Vector3 rotation, Vector3 translation, int verticeCount, int width, int height, int depth): 
            Object3D(origin, rotation, translation, verticeCount, width, this->getDefaultIfEmpty(width, height), this->getDefaultIfEmpty(width, depth)) {}

        Sphere(Vector3 origin, int verticeCount, int width, int height, int depth):
            Object3D(origin, Vector3(0, 0, 0), Vector3(0, 0, 0), verticeCount, width, this->getDefaultIfEmpty(width, height), this->getDefaultIfEmpty(width, depth)) {}

        Sphere(Vector3 origin, int verticeCount, int width):
            Object3D(origin, Vector3(0, 0, 0), Vector3(0, 0, 0), verticeCount, width, width, width) {}

        std::vector<Vector3> getVertices() {
            std::vector<Vector3> vertices;
            int verticeCount = getVerticeCount();
            Vector3 origin = getOrigin();
            int width = getWidth();
            int height = getHeight();
            int depth = getDepth();
            double phiStep = M_PI / verticeCount; // Adjusting the step based on vertices count
            double thetaStep = 2 * M_PI / verticeCount;
            
            for (int phiIndex = 0; phiIndex < verticeCount; ++phiIndex) {
                for (int thetaIndex = 0; thetaIndex < verticeCount; ++thetaIndex) {
                    double phi = phiIndex * phiStep;
                    double theta = thetaIndex * thetaStep;
                    float x = origin.x + width * sin(phi) * cos(theta);
                    float y = origin.y + height * sin(phi) * sin(theta);
                    float z = origin.z + depth * cos(phi);
                    vertices.push_back(Vector3(x, y, z));
                }
            }

            // Adding the south pole vertex, assuming depth represents the radius in this context
            vertices.push_back(Vector3(origin.x, origin.y, origin.z - depth));
            return vertices;
        }

        // std::vector<Vector3> getVertices() {
        //     int verticesCount = getVerticeCount();
        //     Vector3 origin = getOrigin();
        //     int width = getWidth();
        //     int height = getHeight();
        //     int depth = getDepth();
        //     std::vector<Vector3> vertices;
        //     for (int phi = 0; phi < verticesCount; ++phi) {
        //         for (int theta = 0; theta < verticesCount; ++theta) {
        //             float x = origin.x + width * std::sin(phi * M_PI / verticesCount) * std::cos(theta * 2 * M_PI / verticesCount);
        //             float y = origin.y + height * std::sin(phi * M_PI / verticesCount) * std::sin(theta * 2 * M_PI / verticesCount);
        //             float z = origin.z + depth * std::cos(phi * M_PI / verticesCount);
        //             vertices.push_back(Vector3(x, y, z));
        //         }
        //     }
            
        //     vertices.push_back(Vector3(origin.x, origin.y, origin.z - depth));
        //     return vertices;
        // }

        std::vector<std::tuple<int, int>> getEdges() {
            std::vector<std::tuple<int, int>> edges;
            int verticeCount = getVerticeCount();
            edges.reserve(2 * verticeCount * (verticeCount - 1) + verticeCount); // Reserve space to avoid reallocations

            // Horizontal and vertical edges in one loop to reduce overhead
            for (int phi = 0; phi < verticeCount; ++phi) {
                for (int theta = 0; theta < verticeCount; ++theta) {
                    int currentIndex = phi * verticeCount + theta;
                    // Horizontal edge
                    if (theta < verticeCount - 1) {
                        edges.push_back(std::make_tuple(currentIndex, currentIndex + 1));
                    } else {
                        // Connecting end and start of the loop
                        edges.push_back(std::make_tuple(currentIndex, phi * verticeCount));
                    }
                    // Vertical edge, avoiding the last row
                    if (phi < verticeCount - 1) {
                        int nextPhiIndex = currentIndex + verticeCount;
                        edges.push_back(std::make_tuple(currentIndex, nextPhiIndex));
                    }
                }
            }

            // Connecting the last row to the south pole, optimized by avoiding separate loop
            int southPoleIndex = verticeCount * verticeCount;
            for (int theta = 0; theta < verticeCount; ++theta) {
                int lastRowVertexIndex = (verticeCount - 1) * verticeCount + theta;
                edges.push_back(std::make_tuple(lastRowVertexIndex, southPoleIndex));
            }

            return edges;
        }



        // std::vector<std::tuple<int, int>> getEdges() {
        //     std::vector<std::tuple<int, int>> edges;
        //     int verticesCount = getVerticeCount();
            
        //     int totalVertices = verticesCount * verticesCount;
        //     std::vector<int> phiIndices(totalVertices);
        //     std::iota(phiIndices.begin(), phiIndices.end(), 0);

        //     for (int i = 0; i < verticesCount; ++i) {
        //         for (int j = 0; j < verticesCount - 1; ++j) {
        //             int index = i * verticesCount + j;
        //             edges.push_back(std::make_tuple(phiIndices[index], phiIndices[index + 1]));
        //         }
        //     }

        //     for (int i = 0; i < verticesCount - 1; ++i) {
        //         for (int j = 0; j < verticesCount; ++j) {
        //             int index = i * verticesCount + j;
        //             edges.push_back(std::make_tuple(phiIndices[index], phiIndices[index + verticesCount]));
        //         }
        //     }

        //     for (int i = 0; i < verticesCount; ++i) {
        //         int startIndex = i * verticesCount;
        //         int endIndex = (i + 1) * verticesCount - 1;
        //         edges.push_back(std::make_tuple(phiIndices[endIndex], phiIndices[startIndex]));
        //     }

        //     int southPoleIndex = totalVertices - 1;
        //     for (int i = 0; i < verticesCount; ++i) {
        //         int index = (verticesCount - 1) * verticesCount + i;
        //         edges.push_back(std::make_tuple(phiIndices[index], southPoleIndex));
        //     }

        //     return edges;
        // }


        Object3D* clone() {
            return new Sphere(getOrigin(), getRotation(), getTranslation(), getVerticeCount(), getWidth(), getHeight(), getDepth());
        }
};