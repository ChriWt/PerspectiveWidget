#include <iostream>
#include <cassert>

#include "../shape/Sphere.h"
#include "../shape/Cube.h"
#include "../shape/Piramid.h"
#include "../shape/Cilinder.h"

#include "../renderer/Renderer.h"
#include "../renderer/RenderingProperties.h"


void assertVector3Equals() {
    std::cout << "Running assertVector3Equals" << std::endl;
    Vector3 a(1, 2, 3);
    Vector3 b(1, 2, 3);
    assert(a == b);
}

void assertVector3Addition() {
    std::cout << "Running assertVector3Addition" << std::endl;
    Vector3 a(1, 2, 3);
    Vector3 b(1, 1, 3);
    Vector3 result = a + b;
    assert(result.x == 2);
    assert(result.y == 3);
    assert(result.z == 6);
}

void assertVector3Subtraction() {
    std::cout << "Running assertVector3Subtraction" << std::endl;
    Vector3 a(1, 2, 3);
    Vector3 b(1, 1, 3);
    Vector3 result = a - b;
    assert(result.x == 0);
    assert(result.y == 1);
    assert(result.z == 0);
}

void assertVector3Multiplication() {
    std::cout << "Running assertVector3Multiplication" << std::endl;
    Vector3 a(1, 2, 3);
    Vector3 result = a * 2;
    assert(result.x == 2);
    assert(result.y == 4);
    assert(result.z == 6);
}

void assertVector3Division() {
    std::cout << "Running assertVector3Division" << std::endl;
    Vector3 a(1, 2, 3);
    Vector3 result = a / 2;
    assert(result.x == 0.5);
    assert(result.y == 1);
    assert(result.z == 1.5);
}

void assertVector3() {
    std::cout << "Running assertVector3:" << std::endl;
    std::string tests = "5";

    std::cout << "  1/" + tests + "\t";
    assertVector3Equals();
    
    std::cout << "  2/" + tests + "\t";
    assertVector3Addition();
    
    std::cout << "  3/" + tests + "\t";
    assertVector3Subtraction();

    std::cout << "  4/" + tests + "\t";
    assertVector3Multiplication();

    std::cout << "  5/" + tests + "\t";
    assertVector3Division();
}

void assertShape3DProperConstruction(std::string className, Shape3D shape) {
    std::cout << "Running assertShape3DProperConstruction (" << className << ")" << std::endl;
    assert(shape.getOrigin() == Vector3(100, 100, 100));
    assert(shape.getRotation() == Vector3(45, 45, 45));
    assert(shape.getTranslation() == Vector3(200, 150, 300));
    assert(shape.getVerticeCount() == 8);
    assert(shape.getWidth() == 340);
    assert(shape.getHeight() == 500);
    assert(shape.getDepth() == 240);
}

void assertShape3DSetters(std::string className, Shape3D shape) {
    std::cout << "Running assertShape3DSetters (" << className << ")" << std::endl;
    shape.setOrigin(Vector3(200, 200, 200));
    shape.setRotation(Vector3(90, 90, 90));
    shape.setTranslation(Vector3(300, 250, 400));
    shape.setVerticeCount(20);
    shape.setWidth(680);
    shape.setHeight(1000);
    shape.setDepth(480);
    assert(shape.getOrigin() == Vector3(200, 200, 200));
    assert(shape.getRotation() == Vector3(90, 90, 90));
    assert(shape.getTranslation() == Vector3(300, 250, 400));
    assert(shape.getVerticeCount() == 20);
    assert(shape.getWidth() == 680);
    assert(shape.getHeight() == 1000);
    assert(shape.getDepth() == 480);
}

void assertShape3D() {
    std::cout << "Running assertShape3D:" << std::endl;
    std::string tests = "10";

    std::cout << "  1/" + tests + "\t";
    assertShape3DProperConstruction("Shape3d", Shape3D(Vector3(100, 100, 100), Vector3(45, 45, 45), Vector3(200, 150, 300), 8, 340, 500, 240));
    std::cout << "  2/" + tests + "\t";
    assertShape3DSetters("Shape3d", Shape3D());

    std::cout << "  3/" + tests + "\t";
    assertShape3DProperConstruction("Sphere", Sphere(Vector3(100, 100, 100), Vector3(45, 45, 45), Vector3(200, 150, 300), 8, 340, 500, 240));
    std::cout << "  4/" + tests + "\t";
    assertShape3DSetters("Sphere", Sphere());

    std::cout << "  5/" + tests + "\t";
    assertShape3DProperConstruction("Cube", Cube(Vector3(100, 100, 100), Vector3(45, 45, 45), Vector3(200, 150, 300), 340, 500, 240));
    std::cout << "  6/" + tests + "\t";
    assertShape3DSetters("Cube", Cube());

    std::cout << "  7/" + tests + "\t";
    assertShape3DProperConstruction("Piramid", Piramid(Vector3(100, 100, 100), Vector3(45, 45, 45), Vector3(200, 150, 300), 8, 340, 500, 240));
    std::cout << "  8/" + tests + "\t";
    assertShape3DSetters("Piramid", Piramid());

    std::cout << "  9/" + tests + "\t";
    assertShape3DProperConstruction("Cilinder", Cilinder(Vector3(100, 100, 100), Vector3(45, 45, 45), Vector3(200, 150, 300), 8, 340, 500, 240));
    std::cout << " 10/" + tests + "\t";
    assertShape3DSetters("Cilinder", Cilinder());
}

void assertSphereVerticesCount() {
    std::cout << "Running assertSphereVerticesCount" << std::endl;
    Sphere sphere(Vector3(0, 0, 0), 8, 340);
    std::vector<Vector3> vertices = sphere.getVertices();
    assert(vertices.size() == 65);
}

void assertSphereEdgesCount() {
    std::cout << "Running assertSphereEdgesCount" << std::endl;
    Sphere sphere(Vector3(0, 0, 0), 8, 340);
    std::vector<Vector3> vertices = sphere.getVertices();
    std::vector<std::tuple<int, int>> edges = sphere.getEdges();
    assert(edges.size() == 128);
}

void assertSphere() {
    std::cout << "Running assertSphere" << std::endl;
    std::string tests = "2";

    std::cout << "  1/" + tests + "\t";
    assertSphereVerticesCount();

    std::cout << "  2/" + tests + "\t";
    assertSphereEdgesCount();
}

void assertCubeVerticesCount() {
    std::cout << "Running assertCubeVerticesCount" << std::endl;
    Cube cube(Vector3(0, 0, 0), 340, 500, 240);
    std::vector<Vector3> vertices = cube.getVertices();
    assert(vertices.size() == 8);
}

void assertCubeEdgesCount() {
    std::cout << "Running assertCubeEdgesCount" << std::endl;
    Cube cube(Vector3(0, 0, 0), 340, 500, 240);
    std::vector<Vector3> vertices = cube.getVertices();
    std::vector<std::tuple<int, int>> edges = cube.getEdges();
    assert(edges.size() == 18);
}

void assertCube() {
    std::cout << "Running assertCube" << std::endl;
    std::string tests = "2";

    std::cout << "  1/" + tests + "\t";
    assertCubeVerticesCount();

    std::cout << "  2/" + tests + "\t";
    assertCubeEdgesCount();
}

void assertPiramidVerticesCount() {
    std::cout << "Running assertPiramidVerticesCount" << std::endl;
    Piramid piramid(Vector3(0, 0, 0), 8, 340, 500, 240);
    std::vector<Vector3> vertices = piramid.getVertices();
    assert(vertices.size() == 9);
}

void assertPiramidEdgesCount() {
    std::cout << "Running assertPiramidEdgesCount" << std::endl;
    Piramid piramid(Vector3(0, 0, 0), 8, 340, 500, 240);
    std::vector<Vector3> vertices = piramid.getVertices();
    std::vector<std::tuple<int, int>> edges = piramid.getEdges();
    assert(edges.size() == 16);
}

void assertPiramid() {
    std::cout << "Running assertPiramid" << std::endl;
    std::string tests = "2";

    std::cout << "  1/" + tests + "\t";
    assertPiramidVerticesCount();

    std::cout << "  2/" + tests + "\t";
    assertPiramidEdgesCount();
}

void assertCiliinderVerticesCount() {
    std::cout << "Running assertCiliinderVerticesCount" << std::endl;
    Cilinder cilinder(Vector3(0, 0, 0), 8, 340, 500, 240);
    std::vector<Vector3> vertices = cilinder.getVertices();
    assert(vertices.size() == 16);
}

void assertCiliinderEdgesCount() {
    std::cout << "Running assertCiliinderEdgesCount" << std::endl;
    Cilinder cilinder(Vector3(0, 0, 0), 8, 340, 500, 240);
    std::vector<Vector3> vertices = cilinder.getVertices();
    std::vector<std::tuple<int, int>> edges = cilinder.getEdges();
    assert(edges.size() == 24);
}

void assertCilinder() {
    std::cout << "Running assertCilinder" << std::endl;
    std::string tests = "2";

    std::cout << "  1/" + tests + "\t";
    assertCiliinderVerticesCount();

    std::cout << "  2/" + tests + "\t";
    assertCiliinderEdgesCount();
}

void assertRenderer() {
    std::cout << "Running assertRenderer" << std::endl;
    Cube cube(Vector3(200, 300, 400), Vector3(10, 10, 10), Vector3(20, 20, 20), 300, 300, 300);
    RenderingProperties renderingProperties;
    Renderer renderer(renderingProperties);
    std::vector<std::tuple<int, int>> edges = renderer.render(cube);
    assert(edges.size() == 54);
}

int main() {
    assertVector3();
    assertShape3D();

    assertSphere();
    assertCube();
    assertPiramid();
    assertCilinder();

    assertRenderer();
    std::cout << "All tests passed!" << std::endl;
    return 0;
}