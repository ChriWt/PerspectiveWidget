#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "shape/Sphere.h"
#include "shape/Cube.h"
#include "shape/Piramid.h"
#include "shape/Cilinder.h"
#include "renderer/Renderer.h"
#include "renderer/RenderingProperties.h"
#include "vector/Vector3.h"
#include "vector/Vector4.h"



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

    py::class_<Shape3D>(m, "Shape3D")
        .def(py::init<>())
        .def(py::init<Vector3, Vector3, Vector3, int, int, int, int>())
        .def("get_origin", &Shape3D::getOrigin)
        .def("get_rotation", &Shape3D::getRotation)
        .def("get_translation", &Shape3D::getTranslation)
        .def("get_vertice_count", &Shape3D::getVerticeCount)
        .def("get_width", &Shape3D::getWidth)
        .def("get_height", &Shape3D::getHeight)
        .def("get_depth", &Shape3D::getDepth)
        .def("set_origin", &Shape3D::setOrigin)
        .def("set_rotation", &Shape3D::setRotation)
        .def("set_translation", &Shape3D::setTranslation)
        .def("set_vertice_count", &Shape3D::setVerticeCount)
        .def("set_width", &Shape3D::setWidth)
        .def("set_height", &Shape3D::setHeight)
        .def("set_depth", &Shape3D::setDepth)
        .def("to_string", &Shape3D::toString)
        .def("get_vertices", &Shape3D::getVertices)
        .def("get_edges", &Shape3D::getEdges);

    py::class_<Cilinder, Shape3D>(m, "Cilinder")
        .def(py::init<>())
        .def(py::init<Vector3, Vector3, Vector3, int, int, int, int>())
        .def(py::init<Vector3, int, int, int, int>())
        .def(py::init<Vector3, int, int>())
        .def("get_vertices", &Cilinder::getVertices)
        .def("get_edges", &Cilinder::getEdges);

    py::class_<Sphere, Shape3D>(m, "Sphere")
        .def(py::init<>())
        .def(py::init<Vector3, Vector3, Vector3, int, int, int, int>())
        .def(py::init<Vector3, int, int, int, int>())
        .def(py::init<Vector3, int, int>())
        .def("get_vertices", &Sphere::getVertices)
        .def("get_edges", &Sphere::getEdges);

    py::class_<Cube, Shape3D>(m, "Cube")
        .def(py::init<>())
        .def(py::init<Vector3, Vector3, Vector3, int, int, int>())
        .def(py::init<Vector3, int, int, int>())
        .def(py::init<Vector3, int>())
        .def("get_vertices", &Cube::getVertices)
        .def("get_edges", &Cube::getEdges);

    py::class_<Piramid, Shape3D>(m, "Piramid")
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

}
