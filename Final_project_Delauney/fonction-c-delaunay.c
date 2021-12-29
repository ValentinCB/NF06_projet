#include <stdio.h>
#include <stdlib.h>
#include <math.h>

float min(int n, float points[n][2], int recherche)
{ // recherche = 0 pour trouver le min des x et = 1 pour trouver le min des y
    float min = points[0][recherche];
    for (int i = 1; i < n; i++)
    {
        if (points[i][recherche] < min)
        {
            min = points[i][recherche];
        }
    }
    return min;
}

float max(int n, float points[n][2], int recherche)
{ // recherche = 0 pour trouver le max des x et = 1 pour trouver le min des y
    float max = points[0][recherche];
    for (int i = 1; i < n; i++)
    {
        if (points[i][recherche] > max)
        {
            max = points[i][recherche];
        }
    }
    return max;
}

void Super_Triangle(int n, float pts_supertriangle[3][2], float points[n][2])
{
    float xmax = max(n, points, 0), xmin = min(n, points, 0), ymax = max(n, points, 1), ymin = min(n, points, 1); // tableau avec les points du super triangle
    float eps = 1;                                                                                                // marge avec le triangle 0=le triangle est collé sur un point
    pts_supertriangle[0][0] = xmin - eps;
    pts_supertriangle[0][1] = ymin - eps;
    pts_supertriangle[1][0] = xmin + 2 * (xmax - xmin) + 3 * eps;
    pts_supertriangle[1][1] = ymin - eps;
    pts_supertriangle[2][0] = xmin - eps;
    pts_supertriangle[2][1] = ymin + 2 * (ymax - ymin) + 3 * eps;
}

void anti_horaire(float pts[3][2])
{
    int max = 0; // position dans la liste du point avec la valeur max pour le x
    int min = 0; // position dans la liste du point avec la valeur min pour le x
    int milieu;  // position dans la liste du point au milieu
    float a;     // coef directeur de la droite entre le min et max
    float tmp_pts[3][2];
    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 2; j++)
        {
            tmp_pts[i][j] = pts[i][j];
        }
    }
    for (int i = 1; i < 3; i++)
    {
        if (pts[i][0] > pts[max][0])
        {
            max = i;
        }
        if (pts[i][0] < pts[min][0])
        {
            min = i;
        }
    }

    for (int i = 0; i < 3; i++)
    { // on trouve la position du point du milieu
        if (i != min && i != max)
        {
            milieu = i;
            break;
        }
    }
    a = (pts[max][1] - pts[min][1]) / (pts[max][0] - pts[min][0]);
    if (pts[milieu][1] > a * pts[milieu][0] + pts[min][1] - a * pts[min][0])
    {
        pts[0][0] = tmp_pts[min][0];
        pts[0][1] = tmp_pts[min][1];
        pts[1][0] = tmp_pts[max][0];
        pts[1][1] = tmp_pts[max][1];
        pts[2][0] = tmp_pts[milieu][0];
        pts[2][1] = tmp_pts[milieu][1];
    }
    else
    {
        pts[0][0] = tmp_pts[min][0];
        pts[0][1] = tmp_pts[min][1];
        pts[1][0] = tmp_pts[milieu][0];
        pts[1][1] = tmp_pts[milieu][1];
        pts[2][0] = tmp_pts[max][0];
        pts[2][1] = tmp_pts[max][1];
    }
}

int is_in_cercle(float matrice[3][2], float pt[2])
{
    anti_horaire(matrice);
    float a = matrice[0][0] - pt[0], b = matrice[0][1] - pt[1], c = pow(matrice[0][0], 2) - pow(pt[0], 2) + pow(matrice[0][1], 2) - pow(pt[1], 2),
          d = matrice[1][0] - pt[0], e = matrice[1][1] - pt[1], f = pow(matrice[1][0], 2) - pow(pt[0], 2) + pow(matrice[1][1], 2) - pow(pt[1], 2),
          g = matrice[2][0] - pt[0], h = matrice[2][1] - pt[1], i = pow(matrice[2][0], 2) - pow(pt[0], 2) + pow(matrice[2][1], 2) - pow(pt[1], 2);
    if (a * (e * i - h * f) - d * (b * i - c * h) + g * (b * f - e * c) > 0)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}

int main()
{

    return 0;
}