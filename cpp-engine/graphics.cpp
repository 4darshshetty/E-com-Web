#include <GL/glut.h>

void display() {
    glClear(GL_COLOR_BUFFER_BIT);
    glColor3f(0.1f, 0.5f, 1.0f);
    glutSolidCube(0.6);
    glFlush();
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutCreateWindow("Product Preview");
    glutDisplayFunc(display);
    glutMainLoop();
    return 0;
}
