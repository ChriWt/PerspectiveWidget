
#ifndef __RENDERING_PROPERTIES_H__
#define __RENDERING_PROPERTIES_H__

class RenderingProperties {

    private:
        int fov, offsetX, offsetY;
        float scale, aspetRatio, near, far;

    public:

        RenderingProperties() : 
            fov(60), offsetX(400), offsetY(400), scale(150.0f), aspetRatio(1.0f), near(0.1f), far(100.0f) {}

        RenderingProperties(int fov, int offsetX, int offsetY, float scale, float aspetRatio, float near, float far) : 
            fov(fov), offsetX(offsetX), offsetY(offsetY), scale(scale), aspetRatio(aspetRatio), near(near), far(far) {}

        int getFov() {
            return this->fov;
        }

        int getOffsetX() {
            return this->offsetX;
        }

        int getOffsetY() {
            return this->offsetY;
        }

        float getScale() {
            return this->scale;
        }

        float getAspectRatio() {
            return this->aspetRatio;
        }

        float getNear() {
            return this->near;
        }

        float getFar() {
            return this->far;
        }

        void setFov(int fov) {
            this->fov = fov;
        }

        void setOffsetX(int offsetX) {
            this->offsetX = offsetX;
        }

        void setOffsetY(int offsetY) {
            this->offsetY = offsetY;
        }

        void setScale(float scale) {
            this->scale = scale;
        }

        void setAspectRatio(float aspetRatio) {
            this->aspetRatio = aspetRatio;
        }

        void setNear(float near) {
            this->near = near;
        }

        void setFar(float far) {
            this->far = far;
        }

        void setRenderingProperties(int fov, int offsetX, int offsetY, float scale, float aspetRatio, float near, float far) {
            this->fov = fov;
            this->offsetX = offsetX;
            this->offsetY = offsetY;
            this->scale = scale;
            this->aspetRatio = aspetRatio;
            this->near = near;
            this->far = far;
        }

        void setRenderingPropertiesFromExisting(RenderingProperties renderingProperties) {
            this->fov = renderingProperties.getFov();
            this->offsetX = renderingProperties.getOffsetX();
            this->offsetY = renderingProperties.getOffsetY();
            this->scale = renderingProperties.getScale();
            this->aspetRatio = renderingProperties.getAspectRatio();
            this->near = renderingProperties.getNear();
            this->far = renderingProperties.getFar();
        }

        bool operator==(const RenderingProperties& other) {
            if (this == &other) return true;
            return fov == other.fov && offsetX == other.offsetX && offsetY == other.offsetY && scale == other.scale && aspetRatio == other.aspetRatio && near == other.near && far == other.far;
        }
};
#endif