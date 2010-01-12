#ifndef MATRIX_H
#define MATRIX_H


typedef struct Matrix_tag Matrix;
struct Matrix_tag
{
	float m[4][4];
};

/* identity matrix */
Matrix* matrix_init_identity();
//void matrix_free(Matrix*);

/* orthographic transform matrix */
void matrix_init_ortho(Matrix *ortho, float left, float right, float bottom, float top, float near, float far);

void matrix_op_mul(Matrix *, const Matrix *, const Matrix *);
void matrix_mul_f(Matrix *, const Matrix *, float);


#endif
