#include "graphics_engine.h"
#include <cmath>
#include <algorithm>

// 3D Product Visualization Engine
void renderProduct3D(double width, double height, double depth, double* vertices, int* vertexCount) {
    // Generate 3D cube vertices for product visualization
    const int numVertices = 24; // 6 faces * 4 vertices
    *vertexCount = numVertices;
    
    double w = width / 2.0;
    double h = height / 2.0;
    double d = depth / 2.0;
    
    // Front face
    vertices[0] = -w; vertices[1] = -h; vertices[2] = d;
    vertices[3] = w; vertices[4] = -h; vertices[5] = d;
    vertices[6] = w; vertices[7] = h; vertices[8] = d;
    vertices[9] = -w; vertices[10] = h; vertices[11] = d;
    
    // Back face
    vertices[12] = -w; vertices[13] = -h; vertices[14] = -d;
    vertices[15] = -w; vertices[16] = h; vertices[17] = -d;
    vertices[18] = w; vertices[19] = h; vertices[20] = -d;
    vertices[21] = w; vertices[22] = -h; vertices[23] = -d;
    
    // Top face
    vertices[24] = -w; vertices[25] = h; vertices[26] = -d;
    vertices[27] = -w; vertices[28] = h; vertices[29] = d;
    vertices[30] = w; vertices[31] = h; vertices[32] = d;
    vertices[33] = w; vertices[34] = h; vertices[35] = -d;
    
    // Bottom face
    vertices[36] = -w; vertices[37] = -h; vertices[38] = -d;
    vertices[39] = w; vertices[40] = -h; vertices[41] = -d;
    vertices[42] = w; vertices[43] = -h; vertices[44] = d;
    vertices[45] = -w; vertices[46] = -h; vertices[47] = d;
    
    // Right face
    vertices[48] = w; vertices[49] = -h; vertices[50] = -d;
    vertices[51] = w; vertices[52] = h; vertices[53] = -d;
    vertices[54] = w; vertices[55] = h; vertices[56] = d;
    vertices[57] = w; vertices[58] = -h; vertices[59] = d;
    
    // Left face
    vertices[60] = -w; vertices[61] = -h; vertices[62] = -d;
    vertices[63] = -w; vertices[64] = -h; vertices[65] = d;
    vertices[66] = -w; vertices[67] = h; vertices[68] = d;
    vertices[69] = -w; vertices[70] = h; vertices[71] = -d;
}

// Calculate lighting for 3D rendering
void calculateLighting(double* normal, double* lightDir, double* result) {
    double dotProduct = normal[0] * lightDir[0] + normal[1] * lightDir[1] + normal[2] * lightDir[2];
    double intensity = std::max(0.0, dotProduct);
    result[0] = intensity;
    result[1] = intensity * 0.8; // Ambient
    result[2] = intensity * 0.5; // Specular
}

// Generate smooth color gradient
void generateGradient(double t, double* color) {
    // Smooth color transition
    color[0] = 0.2 + 0.6 * (1.0 - t); // Red component
    color[1] = 0.3 + 0.5 * t;         // Green component
    color[2] = 0.8 + 0.2 * (1.0 - t); // Blue component
    color[3] = 1.0;                    // Alpha
}

// Performance optimization: Fast matrix multiplication
void multiplyMatrix(double* a, double* b, double* result) {
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 4; j++) {
            result[i * 4 + j] = 0;
            for (int k = 0; k < 4; k++) {
                result[i * 4 + j] += a[i * 4 + k] * b[k * 4 + j];
            }
        }
    }
}

// High-performance discount calculation with caching
static double cachedPrice = 0.0;
static int cachedPercent = -1;
static double cachedResult = 0.0;

double applyDiscountOptimized(double price, int percent) {
    if (price == cachedPrice && percent == cachedPercent) {
        return cachedResult;
    }
    
    cachedPrice = price;
    cachedPercent = percent;
    
    if (percent < 0 || percent > 70) {
        cachedResult = price;
        return price;
    }
    
    cachedResult = price - (price * percent / 100.0);
    return cachedResult;
}

