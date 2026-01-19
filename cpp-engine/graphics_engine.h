#ifndef GRAPHICS_ENGINE_H
#define GRAPHICS_ENGINE_H

extern "C" {
    // 3D Product Rendering
    void renderProduct3D(double width, double height, double depth, double* vertices, int* vertexCount);
    
    // Lighting calculations
    void calculateLighting(double* normal, double* lightDir, double* result);
    
    // Color gradient generation
    void generateGradient(double t, double* color);
    
    // Matrix operations for 3D transformations
    void multiplyMatrix(double* a, double* b, double* result);
    
    // Optimized discount calculation
    double applyDiscountOptimized(double price, int percent);
}

#endif

