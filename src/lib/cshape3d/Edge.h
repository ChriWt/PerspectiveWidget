
#ifndef __EDGE__
#define __EDGE__

#include "Vector2.h"

class Edge {
    
    public:

        Vector2 start, end;

        Edge(Vector2 start, Vector2 end) : start(start), end(end) {}

        Edge() : start(Vector2()), end(Vector2()) {}

        bool operator==(const Edge& other) {
            if (this == &other) return true;
            return start == other.start && end == other.end;
        }

};

#endif