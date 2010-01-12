#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include "matrix.h"


/* identity matrix */
Matrix* matrix_init_identity(Matrix *matrix)
{
	memset(matrix, 0, sizeof(Matrix));
	matrix->m[0][0] = matrix->m[1][1] = matrix->m[2][2] = matrix->m[3][3] = 1.0f;
}

//void matrix_free(Matrix* matrix)
//{
//	free(matrix);
//}

/* orthographic transform matrix */
void matrix_init_ortho(Matrix *ortho, float left, float right, float bottom, float top, float near, float far)
{
	memset(ortho, 0, sizeof(float)*16);
	ortho->m[0][0] =  2.0f / (right - left);
	ortho->m[1][1] =  2.0f / (top - bottom);
	ortho->m[2][2] = -2.0f / (far - near);
	ortho->m[3][0] = -(right + left) / (right - left);
	ortho->m[3][1] = -(top + bottom) / (top - bottom);
	ortho->m[3][2] = -(far + near) / (far - near);
	ortho->m[3][3] =  1.0f;
}

void matrix_op_mul(Matrix *result, const Matrix *matrix_a, const Matrix *matrix_b)
{
	float tmp[4][4];
	int i;

	for (i = 0; i < 4; i++)
	{
		tmp[i][0] =	(matrix_a->m[i][0] * matrix_b->m[0][0]) +
					(matrix_a->m[i][1] * matrix_b->m[1][0]) +
					(matrix_a->m[i][2] * matrix_b->m[2][0]) +
					(matrix_a->m[i][3] * matrix_b->m[3][0]);
		tmp[i][1] =	(matrix_a->m[i][0] * matrix_b->m[0][1]) + 
					(matrix_a->m[i][1] * matrix_b->m[1][1]) +
					(matrix_a->m[i][2] * matrix_b->m[2][1]) +
					(matrix_a->m[i][3] * matrix_b->m[3][1]);
		tmp[i][2] =	(matrix_a->m[i][0] * matrix_b->m[0][2]) + 
					(matrix_a->m[i][1] * matrix_b->m[1][2]) +
					(matrix_a->m[i][2] * matrix_b->m[2][2]) +
					(matrix_a->m[i][3] * matrix_b->m[3][2]);
		tmp[i][3] =	(matrix_a->m[i][0] * matrix_b->m[0][3]) + 
					(matrix_a->m[i][1] * matrix_b->m[1][3]) +
					(matrix_a->m[i][2] * matrix_b->m[2][3]) +
					(matrix_a->m[i][3] * matrix_b->m[3][3]);
	}

	memcpy(&result->m, &tmp, sizeof(Matrix));
}

void matrix_mul_f(Matrix *result, const Matrix *matrix_a, float b)
{
	result->m[0][0] = matrix_a->m[0][0] * b;
	result->m[0][1] = matrix_a->m[0][1] * b;
	result->m[0][2] = matrix_a->m[0][2] * b;
	result->m[0][3] = matrix_a->m[0][3] * b;

	result->m[1][0] = matrix_a->m[1][0] * b;
	result->m[1][1] = matrix_a->m[1][1] * b;
	result->m[1][2] = matrix_a->m[1][2] * b;
	result->m[1][3] = matrix_a->m[1][3] * b;

	result->m[2][0] = matrix_a->m[2][0] * b;
	result->m[2][1] = matrix_a->m[2][1] * b;
	result->m[2][2] = matrix_a->m[2][2] * b;
	result->m[2][3] = matrix_a->m[2][3] * b;
/*
	result->m[3][0] = matrix_a->m[3][0] * b;
	result->m[3][1] = matrix_a->m[3][1] * b;
	result->m[3][2] = matrix_a->m[3][2] * b;
	result->m[3][3] = matrix_a->m[3][3] * b;
*/
}
