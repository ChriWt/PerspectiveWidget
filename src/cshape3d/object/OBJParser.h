#ifndef __OBJPARSER_H__
#define __OBJPARSER_H__

#include <vector>
#include <fstream>
#include <string>
#include <sstream>
#include <algorithm>

#include "CustomObject3D.h"
#include "../vector/Vector3.h"


class OBJParser {

    public:
        static CustomObject3D parse(std::string filename) {
            std::vector<Vector3> vertices;
            std::vector<std::vector<int>> faces;

            std::ifstream infile(filename);

            std::string line;
            while (std::getline(infile, line)) {
                std::istringstream iss(line);
                std::string type;

                iss >> type;
                if (type == "v") {
                    float x, y, z;
                    iss >> x >> y >> z;
                    vertices.push_back(Vector3(x, y, z));
                } else if (type == "f") {
                    std::vector<int> face;
                    std::string vertexIndex;

                    while (iss >> vertexIndex) {
                        size_t pos = vertexIndex.find("/");
                        if (pos != std::string::npos) {
                            vertexIndex = vertexIndex.substr(0, pos);
                        }
                        face.push_back(std::stoi(vertexIndex) - 1);
                    }
                    faces.push_back(face);
                }
            }

            std::sort(faces.begin(), faces.end(), [](const std::vector<int>& a, const std::vector<int>& b) {
                if (a.front() == b.front()) {
                    return a.back() < b.back();
                }
                return a.front() < b.front();
            });

            return CustomObject3D(vertices, faces);
        }

};

#endif