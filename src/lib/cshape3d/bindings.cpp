#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "src/shape/Sphere.h"
#include "src/shape/Cube.h"
#include "src/shape/Piramid.h"
#include "src/shape/Cilinder.h"

#include "src/renderer/Renderer.h"
#include "src/renderer/RenderingProperties.h"

#include "src/object/OBJParser.h"


namespace py = pybind11;

PYBIND11_MODULE(CShape3D, m){
    m.doc() = "3D shape manipulation module";

    py::class_<Vector3>(m, "Vector3")
        .def(py::init<>())
        .def(py::init<float, float, float>())
        .def("__add__", &Vector3::operator+)
        .def("__sub__", &Vector3::operator-)
        .def("__mul__", &Vector3::operator*, py::is_operator())
        .def("__truediv__", &Vector3::operator/, py::is_operator())
        .def("__repr__", &Vector3::toString)
        .def("__eq__", &Vector3::operator==)
        .def_readwrite("x", &Vector3::x)
        .def_readwrite("y", &Vector3::y)
        .def_readwrite("z", &Vector3::z);

    py::class_<Vector4>(m, "Vector4")
        .def(py::init<>())
        .def(py::init<float, float, float, float>())
        .def("__add__", &Vector4::operator+)
        .def("__sub__", &Vector4::operator-)
        .def("__mul__", &Vector4::operator*, py::is_operator())
        .def("__truediv__", &Vector4::operator/, py::is_operator())
        .def("__repr__", &Vector4::toString)
        .def("__eq__", &Vector4::operator==)
        .def_readwrite("x", &Vector4::x)
        .def_readwrite("y", &Vector4::y)
        .def_readwrite("z", &Vector4::z)
        .def_readwrite("w", &Vector4::w);

    py::class_<Object3D>(m, "Object3D")
        .def(py::init<>())
        .def(py::init<Vector3, Vector3, Vector3, int, int, int, int>())
        .def("get_origin", &Object3D::getOrigin)
        .def("get_rotation", &Object3D::getRotation)
        .def("get_translation", &Object3D::getTranslation)
        .def("get_vertice_count", &Object3D::getVerticeCount)
        .def("get_width", &Object3D::getWidth)
        .def("get_height", &Object3D::getHeight)
        .def("get_depth", &Object3D::getDepth)
        .def("set_origin", &Object3D::setOrigin)
        .def("set_rotation", &Object3D::setRotation)
        .def("set_translation", &Object3D::setTranslation)
        .def("set_vertice_count", &Object3D::setVerticeCount)
        .def("set_width", &Object3D::setWidth)
        .def("set_height", &Object3D::setHeight)
        .def("set_depth", &Object3D::setDepth)
        .def("to_string", &Object3D::toString)
        .def("get_vertices", &Object3D::getVertices)
        .def("get_edges", &Object3D::getEdges);

    py::class_<Cilinder, Object3D>(m, "Cilinder")
        .def(py::init<>())
        .def(py::init<Vector3, Vector3, Vector3, int, int, int, int>())
        .def(py::init<Vector3, int, int, int, int>())
        .def(py::init<Vector3, int, int>())
        .def("get_vertices", &Cilinder::getVertices)
        .def("get_edges", &Cilinder::getEdges);

    py::class_<Sphere, Object3D>(m, "Sphere")
        .def(py::init<>())
        .def(py::init<Vector3, Vector3, Vector3, int, int, int, int>())
        .def(py::init<Vector3, int, int, int, int>())
        .def(py::init<Vector3, int, int>())
        .def("get_vertices", &Sphere::getVertices)
        .def("get_edges", &Sphere::getEdges);

    py::class_<Cube, Object3D>(m, "Cube")
        .def(py::init<>())
        .def(py::init<Vector3, Vector3, Vector3, int, int, int>())
        .def(py::init<Vector3, int, int, int>())
        .def(py::init<Vector3, int>())
        .def("get_vertices", &Cube::getVertices)
        .def("get_edges", &Cube::getEdges);

    py::class_<Piramid, Object3D>(m, "Piramid")
        .def(py::init<>())
        .def(py::init<Vector3, Vector3, Vector3, int, int, int, int>())
        .def(py::init<Vector3, int, int, int, int>())
        .def(py::init<Vector3, int, int>())
        .def("get_vertices", &Piramid::getVertices)
        .def("get_edges", &Piramid::getEdges);

    py::class_<RenderingProperties>(m, "RenderingProperties")
        .def(py::init<>())
        .def(py::init<int, int, int, float, float, float, float>())
        .def("get_fov", &RenderingProperties::getFov)
        .def("get_offset_x", &RenderingProperties::getOffsetX)
        .def("get_offset_y", &RenderingProperties::getOffsetY)
        .def("get_scale", &RenderingProperties::getScale)
        .def("get_aspect_ratio", &RenderingProperties::getAspectRatio)
        .def("get_near", &RenderingProperties::getNear)
        .def("get_far", &RenderingProperties::getFar)
        .def("set_fov", &RenderingProperties::setFov)
        .def("set_offset_x", &RenderingProperties::setOffsetX)
        .def("set_offset_y", &RenderingProperties::setOffsetY)
        .def("set_scale", &RenderingProperties::setScale)
        .def("set_aspect_ratio", &RenderingProperties::setAspectRatio)
        .def("set_near", &RenderingProperties::setNear)
        .def("set_far", &RenderingProperties::setFar)
        .def("set_rendering_properties", &RenderingProperties::setRenderingProperties)
        .def("set_rendering_properties_from_existing", &RenderingProperties::setRenderingPropertiesFromExisting)
        .def("__eq__", &RenderingProperties::operator==);

    py::class_<Renderer>(m, "Renderer")
        .def(py::init<>())
        .def(py::init<RenderingProperties>())
        .def("render", &Renderer::render)
        .def("set_rendering_properties", &Renderer::setRenderingProperties)
        .def("set_rendering_properties_and_render", &Renderer::setRenderingPropertiesAndRender);

    py::class_<CustomObject3D, Object3D>(m, "CustomObject3D")
        .def(py::init<std::vector<Vector3>, std::vector<std::vector<int>>>())
        .def("get_vertices", &CustomObject3D::getVertices)
        .def("get_faces", &CustomObject3D::getFaces);

    py::class_<OBJParser>(m, "OBJParser")
        .def(py::init<>())
        .def_static("parse", &OBJParser::parse);

}