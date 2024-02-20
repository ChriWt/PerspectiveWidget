#include <vector>

#include "../vector/Vector3.h"
#include "../shape/Object3D.h"

#ifndef __CUSTOM_OBJECT_H__
#define __CUSTOM_OBJECT_H__

class CustomObject3D : public Object3D {
    private:
        std::vector<Vector3> vertices;
        std::vector<std::vector<int>> faces;

    public:
        CustomObject3D(std::vector<Vector3> vertices, std::vector<std::vector<int>> faces) : 
            vertices(vertices), 
            faces(faces) {}

        std::vector<Vector3> getVertices() {
            return vertices;
        }

        std::vector<std::vector<int>> getFaces() {
            return faces;
        }

        std::vector<std::tuple<int, int>> getEdges() {
            std::cerr << "Use getFaces for CustomObject3D instead of getEdges" << std::endl;
            std::runtime_error("Use getFaces for CustomObject3D instead of getEdges");
            return std::vector<std::tuple<int, int>>();
        }

        Object3D* clone() {
            Object3D *object = new CustomObject3D(vertices, faces);
            object->setOrigin(getOrigin());
            object->setRotation(getRotation());
            object->setTranslation(getTranslation());
            object->setVerticeCount(getVerticeCount());
            object->setWidth(getWidth());
            object->setHeight(getHeight());
            object->setDepth(getDepth());
            return object;
        }
};

#endif