#include <iostream>
#include <random>
#include <float.h>
#include <fstream>
#include <sys/time.h>

#include "predicates/predicates.h"
#include "gogui.hpp"


using namespace std;

static double gtod_ref_time_sec = 0.0;

/* Adapted from the bl2_clock() routine in the BLIS library */

double dclock()
{
    double the_time, norm_sec;
    struct timeval tv;
    gettimeofday( &tv, NULL );
    if ( gtod_ref_time_sec == 0.0 )
        gtod_ref_time_sec = ( double ) tv.tv_sec;
    norm_sec = ( double ) tv.tv_sec - gtod_ref_time_sec;
    the_time = norm_sec + tv.tv_usec * 1.0e-6;
    return the_time;
}

gogui::vector<gogui::Point> generateIntervalPoints(double lowerBound, double upperBound, int n, string outputFile){

    gogui::vector<gogui::Point> points;

    std::uniform_real_distribution<double> unif(lowerBound,upperBound);
    std::default_random_engine re;

    double minx = DBL_MAX;
    double maxx = DBL_MIN;

    for (int i = 0; i < n; i++){
        double x = unif(re);
        double y = unif(re);

        if (x < minx) minx = x;
        if (x > maxx) maxx = x;

        gogui::Point p(x, y);
        points.push_back(p);
    }

    double miny = 0.05*minx + 0.05;
    double maxy = 0.05*maxx + 0.05;

    gogui::Point a(minx,miny);
    gogui::Point b(maxx,maxy);

    gogui::vector<gogui::Line> lines;

    gogui::Line line1(a, b);
    lines.push_back(line1);

    {
        gogui::ActiveLine active(line1);
        gogui::snapshot();
    }

    gogui::snapshot();

    return points;
}

gogui::vector<gogui::Point> generateCircle(double x0, double y0, double R, int n, string outputFile){

    gogui::vector<gogui::Point> points;

    std::uniform_real_distribution<double> unif(0,2*PI);
    std::default_random_engine re;

    double minx = DBL_MAX;
    double maxx = DBL_MIN;

    for (int i = 0; i < n; i++){
        double alpha = unif(re);

        double x = x0 + cos(alpha) * R;
        double y = x0 + sin(alpha) * R;

        if (x < minx) minx = x;
        if (x > maxx) maxx = x;

        gogui::Point p(x, y);
        points.push_back(p);
    }

    double miny = 0.05*minx + 0.05;
    double maxy = 0.05*maxx + 0.05;

    gogui::Point a(minx,miny);
    gogui::Point b(maxx,maxy);

    gogui::vector<gogui::Line> lines;

    gogui::Line line1(a, b);
    lines.push_back(line1);

    {
        gogui::ActiveLine active(line1);
        gogui::snapshot();
    }

    gogui::snapshot();

    return points;
}

gogui::vector<gogui::Point> generateLinePoints(double lowerBound, double upperBound, int n, string outputFile){

    gogui::vector<gogui::Point> points;

    std::uniform_real_distribution<double> unif(lowerBound,upperBound);
    std::default_random_engine re;

    double minx = DBL_MAX;
    double maxx = DBL_MIN;

    for (int i = 0; i < n; i++){
        double x = unif(re);
        double y = 0.05*x + 0.05;

        if (x < minx) minx = x;
        if (x > maxx) maxx = x;

        gogui::Point p(x, y);
        points.push_back(p);
    }

    double miny = 0.05*minx + 0.05;
    double maxy = 0.05*maxx + 0.05;

    gogui::Point a(minx,miny);
    gogui::Point b(maxx,maxy);

    gogui::vector<gogui::Line> lines;

    gogui::Line line1(a, b);
    lines.push_back(line1);

    {
        gogui::ActiveLine active(line1);
        gogui::snapshot();
    }

    gogui::snapshot();

    return points;
}

gogui::vector<gogui::Point> generatePointsA(){

    int n = 100000;

    double lowerBound = -100;
    double upperBound = 100;

    return generateIntervalPoints(lowerBound, upperBound, n, "a.txt");

}

gogui::vector<gogui::Point> generatePointsB(){

    int n = 100000;

    double upperBound = 10.0E14;
    double lowerBound = -10.0E14;

    return generateIntervalPoints(lowerBound, upperBound, n, "b.txt");
}

gogui::vector<gogui::Point> generatePointsC(){

    int n = 1000;

    double x = 0;
    double y = 0;
    double R = 100;

    return generateCircle(x, y, R, n, "c.txt");
}

gogui::vector<gogui::Point> generatePointsD(){

    int n = 1000;

    double upperBound = 1000;
    double lowerBound = -1000;

    return generateLinePoints(lowerBound, upperBound, n, "d.txt");
}

double det3(double *a, double *b, double *c){
      return a[0]*b[1] + a[1]*c[0] + b[0]*c[1] - (b[1]*c[0] + a[0]*c[1] + a[1]*b[0]);
}

double det2(double *a, double *b, double *c){
    return (a[0]-c[0])*(b[1]-c[1]) - ((a[1]-c[1])*(b[0]-c[0]));
}

void compareToDet3(gogui::vector<gogui::Point> points, double *a, double *b, string testName){
    int leftSidePoints = 0;
    int rightSidePoints = 0;
    int inlinePoints = 0;
    double dtime;

    for (auto i = points.begin(); i != points.end(); ++i){
        double *c = new double[2] {(*i).x, (*i).y};

        dtime = dclock();
        double det = det3(a,b,c);
        dtime = dclock()-dtime;

        if (det >0) leftSidePoints++;
        else if (det < 0) rightSidePoints++;
        else inlinePoints++;
    }

    cout << testName << " while using det 3x3: " << endl;
    cout << "On the left side: " << leftSidePoints << endl;
    cout << "On the right side: " << rightSidePoints << endl;
    cout << "On the line: " << inlinePoints << endl;
    printf("Execution time: %le \n\n", dtime);
}

void compareToDet2(gogui::vector<gogui::Point> points, double *a, double *b, string testName){
    int leftSidePoints = 0;
    int rightSidePoints = 0;
    int inlinePoints = 0;
    double dtime;

    for (auto i = points.begin(); i != points.end(); ++i){
        double *c = new double[2] {(*i).x, (*i).y};

        dtime = dclock();
        double det = det2(a,b,c);
        dtime = dclock()-dtime;

        if (det >0) leftSidePoints++;
        else if (det < 0) rightSidePoints++;
        else inlinePoints++;
    }

    cout << testName << " while using det 2x2: " << endl;
    cout << "On the left side: " << leftSidePoints << endl;
    cout << "On the right side: " << rightSidePoints << endl;
    cout << "On the line: " << inlinePoints << endl;
    printf("Execution time: %le \n\n", dtime);
}

void compareToOrient2dFast(gogui::vector<gogui::Point> points, double *a, double *b, string testName){
    int leftSidePoints = 0;
    int rightSidePoints = 0;
    int inlinePoints = 0;
    double dtime;

    for (auto i = points.begin(); i != points.end(); ++i){
        double *c = new double[2] {(*i).x, (*i).y};

        dtime = dclock();
        double det = orient2dfast(a,b,c);
        dtime = dclock()-dtime;

        if (det >0) leftSidePoints++;
        else if (det < 0) rightSidePoints++;
        else inlinePoints++;
    }

    cout << testName << " while using orient2dFast: " << endl;
    cout << "On the left side: " << leftSidePoints << endl;
    cout << "On the right side: " << rightSidePoints << endl;
    cout << "On the line: " << inlinePoints << endl;
    printf("Execution time: %le \n\n", dtime);
}

void compareToOrient2dExact(gogui::vector<gogui::Point> points, double *a, double *b, string testName){
    int leftSidePoints = 0;
    int rightSidePoints = 0;
    int inlinePoints = 0;
    double dtime;

    for (auto i = points.begin(); i != points.end(); ++i){
        double *c = new double[2] {(*i).x, (*i).y};

        dtime = dclock();
        double det = orient2dexact(a,b,c);
        dtime = dclock()-dtime;

        if (det >0) leftSidePoints++;
        else if (det < 0) rightSidePoints++;
        else inlinePoints++;
    }

    cout << testName << " while using orient2dExact: " << endl;
    cout << "On the left side: " << leftSidePoints << endl;
    cout << "On the right side: " << rightSidePoints << endl;
    cout << "On the line: " << inlinePoints << endl;
    printf("Execution time: %le \n\n", dtime);
}

void compareToOrient2dSlow(gogui::vector<gogui::Point> points, double *a, double *b, string testName){
    int leftSidePoints = 0;
    int rightSidePoints = 0;
    int inlinePoints = 0;
    double dtime;

    for (auto i = points.begin(); i != points.end(); ++i){

        double *c = new double[2] {(*i).x, (*i).y};

        dtime = dclock();
        double det = orient2dslow(a,b,c);
        dtime = dclock()-dtime;

        if (det >0) leftSidePoints++;
        else if (det < 0) rightSidePoints++;
        else inlinePoints++;
    }

    cout << testName << " while using orient2dSlow: " << endl;
    cout << "On the left side: " << leftSidePoints << endl;
    cout << "On the right side: " << rightSidePoints << endl;
    cout << "On the line: " << inlinePoints << endl;
    printf("Execution time: %le \n\n", dtime);

}

void serializePoints(gogui::vector<gogui::Point> points, string fileName){

    ofstream myfile(fileName);

    for (auto i = points.begin(); i != points.end(); ++i){
        myfile << i->x << ";" << i->y << endl;
    }

    myfile.close();
}

int main() {

    double* a = new double[2] {-1.0, 0.0};
    double* b = new double[2] {1.0, 0.1};

    gogui::vector<gogui::Point> pointsA = generatePointsA();
    gogui::vector<gogui::Point> pointsB = generatePointsB();
    gogui::vector<gogui::Point> pointsC = generatePointsC();
    gogui::vector<gogui::Point> pointsD = generatePointsD();

    serializePoints(pointsA, "pointsA.txt");
    serializePoints(pointsB, "pointsB.txt");
    serializePoints(pointsC, "pointsC.txt");
    serializePoints(pointsD, "pointsD.txt");

    exactinit();

    compareToDet3(pointsA, a, b, "a) ");
    compareToDet2(pointsA, a, b, "a) ");
    compareToOrient2dFast(pointsA, a, b, "a) ");
    compareToOrient2dExact(pointsA, a, b, "a) ");
    compareToOrient2dSlow(pointsA, a, b, "a) ");

    compareToDet3(pointsB, a, b, "b) ");
    compareToDet2(pointsB, a, b, "b) ");
    compareToOrient2dFast(pointsB, a, b, "b) ");
    compareToOrient2dExact(pointsB, a, b, "b) ");
    compareToOrient2dSlow(pointsB, a, b, "b) ");

    compareToDet3(pointsC, a, b, "c) ");
    compareToDet2(pointsC, a, b, "c) ");
    compareToOrient2dFast(pointsC, a, b, "c) ");
    compareToOrient2dExact(pointsC, a, b, "c) ");
    compareToOrient2dSlow(pointsC, a, b, "c) ");

    compareToDet3(pointsD, a, b, "d) ");
    compareToDet2(pointsD, a, b, "d) ");
    compareToOrient2dFast(pointsD, a, b, "d) ");
    compareToOrient2dExact(pointsD, a, b, "d) ");
    compareToOrient2dSlow(pointsD, a, b, "d) ");

    return 0;
}