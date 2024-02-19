#include <array>
#include <list>
#include <vector>

#include "../vector/Vector3.h"

#ifndef __SHAPE3D_H__
#define __SHAPE3D_H__

class Shape3D {

    private:
        Vector3 origin;
        Vector3 rotation;
        Vector3 translation;
        int verticeCount;
        int width;
        int height;
        int depth;

    public: 
        Shape3D() : Shape3D(Vector3(0, 0, 0), Vector3(0, 0, 0), Vector3(0, 0, 0), 0, 0, 0, 0) {}

        Shape3D(Vector3 origin, Vector3 rotation, Vector3 translation, int verticeCount, int width, int height, int depth): 
            origin(origin), 
            rotation(rotation), 
            translation(translation),
            verticeCount(verticeCount),
            width(width), 
            height(height), 
            depth(depth) {}

        Vector3 getOrigin() {
            return origin;
        }

        Vector3 getRotation() {
            return rotation;
        }

        Vector3 getTranslation() {
            return translation;
        }

        int getVerticeCount() {
            return verticeCount;
        }

        int getWidth() {
            return width;
        }

        int getHeight() {
            return height;
        }

        int getDepth() {
            return depth;
        }

        void setOrigin(Vector3 origin) {
            this->origin = origin;
        }

        void setRotation(Vector3 rotation) {
            this->rotation = rotation;
        }

        void setTranslation(Vector3 translation) {
            this->translation = translation;
        }

        void setVerticeCount(int verticeCount) {
            this->verticeCount = verticeCount;
        }

        void setWidth(int width) {
            this->width = width;
        }

        void setHeight(int height) {
            this->height = height;
        }

        void setDepth(int depth) {
            this->depth = depth;
        }

        std::string toString() {
            return "Shape3D(" + origin.toString() + ", " + rotation.toString() + ", " + translation.toString() + ", " + std::to_string(verticeCount) + ", " + std::to_string(width) + ", " + std::to_string(height) + ", " + std::to_string(depth) + ")";
        }

        virtual std::vector<Vector3> getVertices() {
            return std::vector<Vector3>();
        }

        virtual std::vector<std::tuple<int, int>> getEdges() {
            return std::vector<std::tuple<int, int>>();
        }

        virtual Shape3D* clone() {
            return new Shape3D(origin, rotation, translation, verticeCount, width, height, depth);
        }
};

#endif