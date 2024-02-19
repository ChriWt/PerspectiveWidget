#include <memory>
#include <vector>
#include <cmath>
#include <iostream>

#include "Shape3D.h"
#include "Vector3.h"
#include "Vector4.h"
#include "Edge.h"
#include "RenderingProperties.h"

#ifndef M_PI
#define M_PI 3.14159265359
#endif


using Matrix4x4 = std::array<std::array<float, 4>, 4>;

class Renderer {

    private:

        std::shared_ptr<Shape3D> shape;
        RenderingProperties renderingProperties;

        Matrix4x4 rotationMatrixX;
        Matrix4x4 rotationMatrixY;
        Matrix4x4 rotationMatrixZ;
        Matrix4x4 projectionMatrix;

        bool rotationMatrixXInitialized = false;
        bool rotationMatrixYInitialized = false;
        bool rotationMatrixZInitialized = false;

        std::vector<Edge> startRendering() {
            std::vector<Edge> edges;
            std::vector<Vector3> vertices = this->projectedVertices();

            std::vector<std::tuple<int, int>> connectinVertices = this->shape->getEdges();

            for (std::tuple<int, int> connection : connectinVertices) {
                Vector2 start = Vector2(vertices[std::get<0>(connection)].x, vertices[std::get<0>(connection)].y);
                Vector2 end = Vector2(vertices[std::get<1>(connection)].x, vertices[std::get<1>(connection)].y);
                edges.emplace_back(Edge(start, end));
            }

            return edges;
        }

        std::vector<Vector3> projectedVertices() {
            std::vector<Vector3> vertices = this->shape->getVertices();
            std::vector<Vector3> projectedVertices;

            for (Vector3 vertex : vertices) {
                projectedVertices.push_back(this->projectVertex(vertex));
            }

            return projectedVertices;
        }

        Vector3 projectVertex(Vector3 vertex) {
            Vector3 centeredVetex = vertex - this->shape->getOrigin();

            Vector4 vertex4d = Vector4(centeredVetex.x, centeredVetex.y, centeredVetex.z, 1);

            vertex4d = applyRotation(vertex4d);
            vertex4d = applyTranslation(vertex4d, this->shape->getTranslation());
            vertex4d = multiplyMatrixVector(this->projectionMatrix, vertex4d);
            Vector3 projectedVertex = normalizeProjection(vertex4d);

            float scale = this->renderingProperties.getScale();
            float offsetX = this->renderingProperties.getOffsetX();
            float offsetY = this->renderingProperties.getOffsetY();

            return Vector3(projectedVertex.x * scale + offsetX, projectedVertex.y * scale + offsetY, projectedVertex.z);
        }

        Vector4 applyRotation(Vector4 vertex) {
            vertex = multiplyMatrixVector(getRotationMatrixY(), vertex);
            vertex = multiplyMatrixVector(getRotationMatrixX(), vertex);
            vertex = multiplyMatrixVector(getRotationMatrixZ(), vertex);

            Vector3 origin = this->shape->getOrigin();
            vertex.x += origin.x;
            vertex.y += origin.y;
            vertex.z += origin.z;

            return vertex;
        }

        Matrix4x4 getRotationMatrixX() {
            if (!rotationMatrixXInitialized) {
                int degree = this->shape->getRotation().x;
                float radian = radians(degree);

                this->rotationMatrixX = {{
                    {cos(radian), 0, sin(radian), 0},
                    {0, 1, 0, 0},
                    {-sin(radian), 0, cos(radian), 0},
                    {0, 0, 0, 1}
                }};
                rotationMatrixXInitialized = true;
            }
            
            return this->rotationMatrixX;
        }

        Matrix4x4 getRotationMatrixY() {
            if (!rotationMatrixYInitialized) {
                int degree = this->shape->getRotation().y;
                float radian = radians(degree);

                this->rotationMatrixY = {{
                    {1, 0, 0, 0},
                    {0, cos(radian), -sin(radian), 0},
                    {0, sin(radian), cos(radian), 0},
                    {0, 0, 0, 1}
                }};
                rotationMatrixYInitialized = true;
            }

            return this->rotationMatrixY;
        }

        Matrix4x4 getRotationMatrixZ() {
            if (!rotationMatrixZInitialized) {
                int degree = this->shape->getRotation().z;
                float radian = radians(degree);

                this->rotationMatrixZ = {{
                    {cos(radian), -sin(radian), 0, 0},
                    {sin(radian), cos(radian), 0, 0},
                    {0, 0, 1, 0},
                    {0, 0, 0, 1}
                }};
                rotationMatrixZInitialized = true;
            }

            return this->rotationMatrixZ;
        }

        Vector4 multiplyMatrixVector(const Matrix4x4& mat, const Vector4 vec) {
            Vector4 result;
            result.x = mat[0][0] * vec.x + mat[0][1] * vec.y + mat[0][2] * vec.z + mat[0][3] * vec.w;
            result.y = mat[1][0] * vec.x + mat[1][1] * vec.y + mat[1][2] * vec.z + mat[1][3] * vec.w;
            result.z = mat[2][0] * vec.x + mat[2][1] * vec.y + mat[2][2] * vec.z + mat[2][3] * vec.w;
            result.w = mat[3][0] * vec.x + mat[3][1] * vec.y + mat[3][2] * vec.z + mat[3][3] * vec.w;
            return result;
        }

        Vector4 applyTranslation(Vector4 vertex, Vector3 translation) {
            vertex.x += translation.x;
            vertex.y += translation.y;
            vertex.z += translation.z;

            return vertex;
        }

        Vector3 normalizeProjection(Vector4 vertex) {
            if (vertex.w != 0.0f) {
                float invW = 1.0f / vertex.w;
                return Vector3(vertex.x * invW, vertex.y * invW, vertex.z * invW);
            } else {
                std::cerr << "Warning: Vertex has a w-component of 0. Returning unmodified vertex." << std::endl;
                return Vector3(vertex.x, vertex.y, vertex.z);
            }
        }

        void buildProjectionMatrix() {
            float scaleX = (1.0f / tan(radians(this->renderingProperties.getFov() / 2.0f))) * this->renderingProperties.getAspectRatio();
            float scaleY = 1.0f / tan(radians(this->renderingProperties.getFov() / 2.0f));
            float scaleZ = ((this->renderingProperties.getFar() + this->renderingProperties.getNear()) * -1.0f) / (this->renderingProperties.getFar() - this->renderingProperties.getNear());
            float translate_z = (-2 * this->renderingProperties.getFar() * this->renderingProperties.getNear()) / (this->renderingProperties.getFar() - this->renderingProperties.getNear());

            this->projectionMatrix = {{
                {scaleX, 0, 0, 0},
                {0, scaleY, 0, 0},
                {0, 0, scaleZ, translate_z},
                {0, 0, -1, 0}
            }};
        }

        float radians(int degree) {
            return degree * (M_PI / 180);
        }

    public:

        Renderer() : renderingProperties(RenderingProperties()) {
            this->buildProjectionMatrix();
        }

        Renderer(RenderingProperties renderingProperties) : renderingProperties(renderingProperties) {
            this->buildProjectionMatrix();
        }

        std::vector<Edge> render(std::shared_ptr<Shape3D> shape) {
            this->shape = shape;
            return this->startRendering();
        }

        void setRenderingProperties(RenderingProperties renderingProperties) {
            this->renderingProperties = renderingProperties;
            this->buildProjectionMatrix();
        }

        void setRenderingPropertiesAndRender(RenderingProperties renderingProperties) {
            this->setRenderingProperties(renderingProperties);
            this->startRendering();
        }
};